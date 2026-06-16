# First-Class macOS Development Guideline

Rules for building macOS applications with Swift, SwiftUI, and AppKit. Each rule addresses
a real failure mode: a build error, a thread-safety bug, a performance regression, or a
silent behavioral break. Apply the rules that match your current change.

---

## 1. Build System

**Build gate:** Every change must end with your build command exiting 0. If Xcode.app is
absent (only CommandLineTools), state this explicitly. Do not claim the build passes without
running it.

**Entry points when building directly with `swiftc`:**
- App targets using `@main` must pass `-parse-as-library`.
- CLI targets using a `main.swift` top-level entry point must NOT pass `-parse-as-library`.
  Mixing these produces a misleading "expressions not allowed at the top level" error.

**Deployment target for vendored C libraries:** Set `CMAKE_OSX_DEPLOYMENT_TARGET` in your
vendor build script to match the app's minimum deployment target. Without this, vendored C
libraries build for the host OS version and emit linker warnings on every build.

**Shell scripts:** Use ASCII `...` not the UTF-8 ellipsis `…`. Bash 3.2 (macOS default)
treats the multi-byte character as three separate bytes and silently misbehaves.

**Vendor builds:** Run the vendor build once per toolchain version. Do not re-run it on every
build. The vendor output is gitignored; rebuilding takes minutes.

---

## 2. Swift Access Modifiers

`private` scopes to the enclosing **declaration**, not the file. A `private` member of an
inner class or struct is inaccessible from any method on an outer or sibling type, even when
both are in the same file.

**Common failure:** A `Coordinator` property marked `private` is inaccessible from
`makeNSView` on the enclosing `NSViewRepresentable` struct, even though they share a file.
The compiler error is `'memberName' is inaccessible due to 'private' protection level`.

- Use `fileprivate` when a member must be accessible across types within the same file but
  hidden from other files. This is the correct scope for coordinator properties assigned
  from `makeNSView` or `updateNSView`.
- Use `private` only for members accessed exclusively within the declaring type's own `{ }`
  block, including its closures.
- Do NOT promote to `internal` or `public` to resolve an access error. Determine the
  required scope first.

Before marking any coordinator property `private`, verify that `makeNSView` and
`updateNSView` do not assign or read it.

---

## 3. AppKit / SwiftUI Bridge (`NSViewRepresentable`)

### Keep the coordinator current

Set `context.coordinator.parent = self` in `updateNSView`. Without this, closures captured
in the coordinator reference stale copies of the view struct after SwiftUI re-renders.

### Suppress spurious updates

In `textViewDidChangeText` (or equivalent text-change callback), guard against publishing
when the text did not actually change:

```swift
guard textView.string != parent.text else { return }
```

Every programmatic change — formatting, reload, initial assignment — fires the delegate.
Without this guard, each one triggers a redundant SwiftUI re-render.

### Initial string assignment

Wrap `textView.string = initialValue` in `makeNSView` with an `isInitialLoad` flag:

```swift
coordinator.isInitialLoad = true
textView.string = initialValue
coordinator.isInitialLoad = false
```

The `NSTextStorageDelegate` fires on every string mutation, including this assignment.
Without the flag, expensive post-processing (e.g., syntax highlighting) runs synchronously
during `makeNSView` before layout is ready.

### Deferred processing after initial assignment

After `isInitialLoad = false`, trigger any full-document processing via
`DispatchQueue.main.async`. This ensures the text view's layout manager has committed the
new string before attributes or measurements are applied.

### Deinit thread safety

Never read `NSTextView.string` (or `NSTextStorage.string`) in `deinit`. By the time `deinit`
fires, the coordinator may be released from a non-main context; reading text storage off the
main thread is unsafe and may capture a mid-mutation string.

Instead, maintain a property updated on the main thread inside your text-change callback:

```swift
fileprivate var lastText: String = ""  // updated in textViewDidChangeText on main thread

deinit {
    parent.onViewDisappear(lastText)   // safe: reads a plain String, not live NSTextStorage
}
```

Cancel Combine subscriptions as the **first** line of `deinit`, before any other cleanup. A
live subscription firing during teardown can access deallocated coordinator state.

### Settings window (macOS 13 / 14 split)

- macOS 14+: use `@Environment(\.openSettings)` inside a view marked `@available(macOS 14.0, *)`.
- macOS 13: use `NSApp.sendAction(Selector(("showSettingsWindow:")), to: nil, from: nil)`.
- Do NOT call both. Use an `if #available(macOS 14, *)` dispatch with separate view types.

### Proxy icon (clickable title chevron)

- macOS 13+: apply `.navigationDocument(url)` in your root content view inside
  `#available(macOS 13.0, *)`. SwiftUI `WindowGroup` windows require this modifier for the
  standard proxy-icon popup (Name / Tags / Where / Locked) to appear reliably.
- macOS 12 fallback: `NSApp.mainWindow?.representedURL = url` set whenever the document URL
  changes.
- Keep both: `.navigationDocument` is macOS 13+ only; the AppKit call is the macOS 12 path.

### Window deduplication when using an `AppDelegate` for file events

Add `.handlesExternalEvents(preferring: Set<String>(), allowing: Set<String>())` to the
`WindowGroup` scene. Without this, `open -a App.app file` while the app is already running
creates a second window: `WindowGroup` responds to the activation event and `AppDelegate`
handles the file open event — both fire.

---

## 4. `NSTextStorage` and Syntax Highlighting

### Use the storage delegate, not async dispatch

Use `NSTextStorageDelegate.textStorage(_:didProcessEditing:range:changeInLength:)` for
syntax highlighting. Do not use `DispatchQueue.main.async` inside a text-change callback.
The delegate fires synchronously after the storage processes each edit, eliminating the
one-frame flicker that async dispatch causes.

Set `textView.textStorage?.delegate = context.coordinator` in `makeNSView`.

Guard against re-entrant calls: check `editedMask.contains(.editedCharacters)` before
applying attributes. Without this, attribute changes inside the delegate re-fire the
delegate and recurse.

### Choosing inline vs. full highlighting

- **Per keystroke:** apply highlighting only to the affected paragraph range (inline
  patterns: bold, italic, inline code, links). This keeps the main thread clear.
- **Periodically (every ~300 ms, background thread):** collect all tokens from a full-
  document string snapshot on a background queue, then apply them on the main thread inside
  `textStorage.beginEditing() / endEditing()`.
- **Large documents (> 200 000 characters):** always use per-keystroke inline highlighting.
  Never call a full-document highlight pass on the main thread during editing.

### Stale background highlight guard

Use a monotonically increasing generation counter:

```swift
highlightGeneration += 1
let generation = highlightGeneration
DispatchQueue.global(qos: .userInitiated).async {
    let tokens = collectTokens(from: snapshot)
    DispatchQueue.main.async {
        guard generation == self.highlightGeneration else { return }
        self.applyTokens(tokens)
    }
}
```

Without this guard, rapid typing applies stale highlight results from earlier keystrokes.

### Multi-line syntax scope detection

Before choosing inline vs. full highlighting, determine whether the edit position is inside
an unclosed multi-line construct (e.g., a code fence). Count scope-opening markers before
the edit position; an odd count means the cursor is inside an unclosed span. Force a full
pass in that case to restore correct multi-line attributes.

Expand the paragraph range by a small lookahead (e.g., ±250 characters) when the current
paragraph contains a scope-opening character. This brings the opening/closing delimiters
within the inline scan window and eliminates flicker from attributes temporarily reverting
on every keystroke inside a multi-line span.

### Block pattern ordering

When multiple block-level patterns can match the same text, apply the most specific
(override) pattern **last**. A later-applied pattern overwrites earlier attributes. For
example: a horizontal-rule pattern may match the closing delimiter of a front-matter block;
applying the front-matter pattern after all others ensures it wins over false positives.

### Cache `NSRegularExpression` patterns

Declare patterns as `private static let` constants at the type level, not inside methods:

```swift
private static let reHeading = try? NSRegularExpression(
    pattern: #"^#{1,6} .*$"#,
    options: .anchorsMatchLines
)
```

`NSRegularExpression` compilation is CPU-intensive. Constructing patterns inside a method
body compiles them on every call — measurably slow at one invocation per keypress.

---

## 5. Undo and Selection Preservation

### Saving the selected range

In `textViewDidChangeSelection`, save the current range to a coordinator property — except
when undo or redo is active:

```swift
guard !(tv.undoManager?.isUndoing == true || tv.undoManager?.isRedoing == true) else { return }
savedSelectedRange = tv.selectedRange()
```

During undo/redo, `NSTextView` restores the pre-action selection automatically. Overwriting
`savedSelectedRange` at that point causes the cursor to jump on the next programmatic
format action.

### Undo cursor placement

When `undoManager.isUndoing || undoManager.isRedoing`, return immediately from any custom
cursor-placement logic in the text-change callback. Let AppKit's native undo cursor placement
take effect. Custom offset math layered on top of AppKit's undo stack produces incorrect
cursor positions after format-then-undo sequences.

### Preventing selection loss during programmatic formatting

Before a programmatic format action:

1. Set an `isApplyingFormat` flag to `true`.
2. Call `makeFirstResponder(textView)` to ensure the text view holds focus.
3. Call `textView.setSelectedRange(savedSelectedRange)` to restore the pre-click selection.
4. Apply the format.
5. Set `isApplyingFormat = false`.

In `textViewDidChangeSelection`, skip saving the range while `isApplyingFormat` is `true`.
Without step 2, formatting inserts at the correct location but the cursor does not return
to the editor after the user clicks a toolbar button.

---

## 6. Inline Format Toggle (Text Editors)

When implementing bold / italic / code wrapping actions, detect and unwrap before wrapping:

**Case A — selection includes markers:** if the selection starts with the opening marker and
ends with the closing marker and contains more content between them, strip the markers.

```swift
if sel.hasPrefix(pre) && sel.hasSuffix(suf) && sel.count > pre.count + suf.count {
    let inner = String(sel.dropFirst(pre.count).dropLast(suf.count))
    // replace selection with inner
}
```

**Case B — selection is surrounded by markers in the document:** read the characters
immediately before and after the selection range in the full string. If they match the
opening and closing markers, expand the replacement range to include them and replace with
the bare selection.

Guard `sel.count > pre.count + suf.count` before Case A to avoid a false match when the
selection consists solely of the markers (e.g., `"****"`).

---

## 7. Performance — SwiftUI List Views

### `LazyVStack` inside `HSplitView`

Do not use `LazyVStack` for a content list that shares a layout pass with an `NSScrollView`
pane in an `HSplitView`. `LazyVStack` reports estimated sizes for off-screen items; SwiftUI
uses the list's content size to compute the split layout, and wrong estimates cause
`NSScrollView` to receive incorrect bounds, producing blank regions at the bottom of the
adjacent AppKit pane.

Use `VStack` in split-view layouts where both panes participate in a shared layout pass.
Use `LazyVStack` only in single-pane scrolling contexts where no sibling pane depends on
the content size.

### `ForEach` item identity

Use integer offset IDs when item content contains `AttributedString` or other O(n)-to-hash
values:

```swift
ForEach(Array(items.enumerated()), id: \.offset) { _, item in ... }
```

`AttributedString` hashing is O(n) per item. With frequent updates in a live-preview pane,
`id: \.self` adds measurable diffing overhead per frame. Integer offset hashing is O(1).

### Skip unchanged item re-renders

Conform list item views to `Equatable` (comparing only data fields, not closures) and apply
`.equatable()` in the `ForEach`. SwiftUI then skips re-rendering items whose data has not
changed:

```swift
struct ItemView: View, Equatable {
    let item: Item
    let onTap: () -> Void
    static func == (lhs: ItemView, rhs: ItemView) -> Bool { lhs.item == rhs.item }
}
// in ForEach:
ItemView(item: item, onTap: { … }).equatable()
```

### Combine pipeline

Apply `.removeDuplicates()` before `.debounce` in any publisher that drives expensive
downstream work:

```swift
$editedText
    .removeDuplicates()
    .debounce(for: .milliseconds(200), scheduler: DispatchQueue.main)
    .sink { [weak self] text in self?.reparse(text) }
```

Use 200 ms debounce for live preview. 150 ms is sub-perceptible in latency but triggers
~25% more parses during fast typing.

### Redundant-parse guard

Before starting an expensive background parse, compare the new content to the last-parsed
content:

```swift
guard newContent != lastParsedContent else { return }
lastParsedContent = newContent
```

Without this guard, debounce fires trigger full parses even when the content is unchanged
(e.g., undo back to a previously parsed state).

### Dirty detection fast path

Before comparing full strings for unsaved-change detection, compare byte counts first:

```swift
let dirty = text.utf8.count != sourceByteCount || text != source
```

Cache `sourceByteCount` as an `Int` updated whenever `source` is set. This short-circuits
the O(n) string comparison for the common case where lengths differ.

---

## 8. Appearance and Theming

### Inject theme colors via environment keys

Do not apply `Color.primary` or `Color.secondary` directly to text in themed views.
`Color.primary` follows system appearance, which conflicts with explicit dark or light
paper themes. Instead, inject foreground and secondary colors through custom SwiftUI
environment keys:

```swift
struct ThemeForegroundKey: EnvironmentKey {
    static let defaultValue: Color = .primary
}

// In a parent view:
.environment(\.themeForeground, theme.foregroundColor)

// In leaf views:
@Environment(\.themeForeground) var foreground
Text(content).foregroundStyle(foreground)
```

For system-adaptive themes: use `NSColor.labelColor` / `NSColor.secondaryLabelColor`
wrapped in `Color(nsColor:)`. For explicit named themes: use forced static colors
independent of system appearance.

### Scale all text sizes from a single base size

Do not hardcode point sizes or SwiftUI semantic text sizes (`.caption`, `.callout`) in
views that participate in a user-adjustable font-size setting. Derive all sizes from a
single base:

```swift
@Environment(\.bodyFontSize) var bodyFontSize

Text(label).font(.system(size: bodyFontSize * 0.85))  // e.g., for secondary text
```

Monospaced elements (code blocks) should use `.monospacedDigit()` or `.monospaced()` design
directly and remain unaffected by the proportional font family setting.

### `NSFont` family nil-guard

`NSFont(name:size:)` returns `nil` for unknown or misspelled family names. Always provide
a fallback:

```swift
let font = NSFont(name: family, size: size)
    ?? NSFont.systemFont(ofSize: size)
```

When `family` is empty (user has not set a preference), skip the `NSFont(name:size:)` call
entirely and use the system font directly to avoid a nil-then-fallback path on every call.

### Picker style for more than three options

Use `.pickerStyle(.menu)` with `ForEach` over a `CaseIterable` enum for pickers with four
or more options. `.pickerStyle(.segmented)` truncates labels at four items and becomes
unusable at five or more.

### Floating panel visibility

Set `hidesOnDeactivate = true` in any `NSPanel` subclass `init()`. The default is `false`,
which keeps floating panels visible over other applications after the user switches focus
away from your app.

---

## 9. File Watching and Document State

### Thread safety

Dispatch all UI-state updates — setting `isModified`, triggering reloads, showing banners —
to the main thread from file watcher callbacks. `DispatchSource` and `kqueue` callbacks fire
on a private queue.

### Auto-reload vs. unsaved changes

In the file watcher callback:
- If the document has no unsaved changes, reload silently.
- If the document has unsaved changes, set a `fileChangedExternally` flag and show a
  non-destructive banner. Do not discard unsaved edits without explicit user confirmation.

### `isDirty` tracking

Track `isDirty` as a boolean flag updated in the editor's content `didSet` observer:

```swift
var editorContent: String = "" {
    didSet { isDirty = editorContent != savedContent }
}
```

Do not compare full strings on every keypress to determine dirty state. Reset `isDirty`
to `false` after a successful save or user-initiated reload.

---

## 10. Tab Stops

When recalculating tab stops for an `NSTextView`, measure the advance width from the actual
font being applied, not a fallback. If the displayed font family differs from the font used
to calculate tab stops, the visual tab alignment is wrong.

Capture font parameters on the main thread before dispatching to a background queue:

```swift
let family = currentFontFamily   // capture on main thread
let size = currentFontSize
DispatchQueue.main.async {
    self.applyTabStops(family: family, size: size)
}
```

Closures that capture `self.currentFontFamily` from inside a dispatch block may race with a
settings change on the main thread.

---

## 11. Documentation Hygiene

Update documentation in the same commit that changes user-visible behavior. Drift between
code and docs compounds across changes and causes incorrect assumptions in future work.

| Document | Rule |
|---|---|
| `CHANGELOG.md` | Add a versioned entry for every release or milestone. Do not leave version gaps. |
| Roadmap or release plan | Mark a milestone complete in the same commit that implements its last required change. |
| Architecture / spec doc | Keep directory maps and module lists current. Mark planned-but-not-yet-built items explicitly with a target version. |
| `README.md` | "What works now" and directory listings must reflect the current codebase. Remove references to deleted modules. |

When behavior changes — API surface, UI layout, undo semantics, file handling — update the
relevant spec or architecture section in the same commit. Do not accumulate documentation
debt across changes.

---

## 12. macOS API Availability

| Feature | macOS 12 | macOS 13 | macOS 14+ |
|---|---|---|---|
| `\.openSettings` environment key | — | — | ✓ |
| `showSettingsWindow:` selector | ✓ | ✓ | Deprecated, functional |
| `.navigationDocument(url)` modifier | — | ✓ | ✓ |
| `NSApp.mainWindow?.representedURL` | ✓ | ✓ (fallback) | ✓ (fallback) |
| `.textSelection(.enabled)` | — | ✓ | ✓ |
| `Font.custom(_:size:).weight(_:)` | ✓ | ✓ | ✓ |

Use `if #available(macOS N, *)` for runtime dispatch between code paths. Use
`@available(macOS N, *)` on types whose stored properties or protocol conformances require
SDK types available only from version N — the compiler requires this when
`@Environment(\.openSettings)` appears in a stored property.

Do not use a deprecated API path without documenting the fallback and the macOS version at
which it becomes available or superseded.

State the project's minimum deployment target in one place (the Xcode project, Package.swift,
or a build script constant) and enforce it consistently across all vendor and CI builds.
