# Swift macOS Build Resilience Guideline

## Purpose

This guideline describes how Swift macOS applications should structure their source tree and build scripts so they can still build and test when Swift Package Manager, Xcode Command Line Tools, or the local sandbox environment is partially broken.

The target audience is small native macOS apps that intentionally avoid an Xcode project and use SwiftPM as their manifest format.

## Design Goals

- Keep `Package.swift` as the canonical manifest for healthy toolchains.
- Do not make day-to-day local builds depend exclusively on SwiftPM manifest evaluation.
- Keep generated build products inside the project workspace, not under the user's home directory.
- Keep the build path explicit enough that a maintainer can debug compiler, SDK, and modulemap problems quickly.
- Provide a minimal smoke-test path when XCTest or SwiftPM is unavailable.
- Prefer Apple platform frameworks over external packages for features they already provide.

## Required Project Shape

Use a source layout that can be built by both SwiftPM and direct `swiftc` commands:

```text
Package.swift
Makefile
Sources/
  AppNameCore/
    *.swift
  AppNameApp/
    *.swift
  appname-cli/
    main.swift
Tests/
  AppNameCoreTests/
    *.swift
scripts/
  build.sh
  bundle.sh
  run.sh
  test.sh
  toolchain-workaround.sh
```

`Package.swift` remains the source of truth for products and targets on healthy toolchains. Whenever targets are added, removed, or renamed, update both `Package.swift` and the direct build script in the same change.

Do not name the `@main` struct file `main.swift`. The Swift compiler treats any file named `main.swift` as the module's top-level entry point, which conflicts with `@main` and causes a "expressions are not allowed at the top level" or "file cannot contain top-level code" error. Name the file after the struct instead (for example `AppNameApp.swift`).

## External Dependency Rule

Before adding any external package dependency to `Package.swift`:

1. **Validate the URL resolves to a real Swift package.** Run `swift package resolve` in isolation and confirm it succeeds. A URL that returns 404, hosts a non-Swift project, or exports a product with a different name than referenced will cause `swift build` to fail for every developer on every toolchain — the direct `swiftc` path is immune because it never parses `Package.swift`, but any healthy-toolchain user hitting `swift build` will be broken.

2. **Check whether a platform framework covers the use case.** Apple's frameworks expose many capabilities that are commonly pulled in as third-party packages: rich text and markdown via `Foundation.AttributedString`, attributed rendering via `AppKit.NSTextView`, image handling via `AppKit.NSImage`, HTTP via `Foundation.URLSession`. Prefer the built-in over an external dependency whenever the feature overlap is substantial.

3. **Record the rationale.** If an external dependency is genuinely needed, add a comment in `Package.swift` stating what the package provides and why no platform framework substitutes.

4. **If SwiftPM is broken and an external package is genuinely required, use a vendor build.** Clone the package source at a pinned revision, build any C/C++ layers with cmake or make into static archives, and compile Swift source files with direct `swiftc`. Extend the build script (or a companion vendor script) to produce and cache the static library and `.swiftmodule`, then link them in the normal direct build step. See the Vendor Build Rule below for the full pipeline.

If a dependency turns out to be unresolvable (wrong URL, renamed product, deleted repository), remove it from `Package.swift` and substitute the platform equivalent. The direct `swiftc` build path (`make build`) will continue to work throughout; only `swift build` is gated on `Package.swift` resolution.

## Build Rule

The `make build` target must run a direct `swiftc` script, not `swift build`.

Reason: some Command Line Tools installs fail before compiling project source files because SwiftPM cannot compile or link the package manifest. A direct `swiftc` path bypasses `Package.swift` manifest evaluation and can still compile the same source targets.

The direct build script must:

- Build library modules first with `-parse-as-library`, `-emit-module-path`, and a static archive output.
- Build app and CLI executables against the emitted local modules.
- Pass `-parse-as-library` when compiling any module whose entry point is a `@main` struct. Without this flag, `swiftc` expects a `main.swift` top-level expression and will reject `@main`. This applies to both library modules and `@main`-based app targets.
- Use an explicit deployment target, for example `arm64-apple-macosx14.0`.
- Support `CONFIG=debug` and `CONFIG=release`.
- Write all outputs to `.build-scripts/<config>/`.
- Set `CLANG_MODULE_CACHE_PATH` to `.build-scripts/<config>/module-cache`.

Example policy:

```sh
CONFIG="${CONFIG:-debug}"
BUILD_DIR="$ROOT_DIR/.build-scripts/$CONFIG"
TARGET="$(uname -m)-apple-macosx14.0"
export CLANG_MODULE_CACHE_PATH="$BUILD_DIR/module-cache"
```

Build scripts that construct Swift source file lists must account for macOS's system shell being bash 3.2, which lacks `readarray` and `mapfile`. When source paths may contain spaces (common in vendored packages with multi-word directory names), collect file lists using `python3`, a null-delimited `find -print0 | xargs -0` loop, or write a temporary path file from Python. Do not rely on word-splitting or `IFS` substitution when subdirectory names contain spaces.

## Vendor Build Rule

When an external Swift package is genuinely required and SwiftPM cannot resolve or build it, build the package from source directly rather than abandoning the dependency.

General pipeline:

1. **Clone at a pinned revision.** Use `git clone --depth 1 --branch <tag>` into a gitignored local directory (`.vendor/`).

2. **Build C/C++ layers with cmake or make.** For packages that wrap a C library, configure and build static archives in the clone. Prefer static (`-DBUILD_SHARED_LIBS=OFF`) so the final binary is self-contained:
   ```sh
   cmake -S "$VENDOR_DIR/c-lib" -B "$BUILD_DIR/c-build" \
     -DCMAKE_BUILD_TYPE=Release -DBUILD_SHARED_LIBS=OFF
   cmake --build "$BUILD_DIR/c-build" --target <archive-target>
   ```

3. **Compile Swift sources with direct swiftc.** Collect the file list with a bash-3.2-compatible method (see above), then invoke `swiftc`:
   ```sh
   swiftc -parse-as-library -module-name <Module> \
     -emit-library -o "$BUILD_DIR/lib<Module>.a" \
     -emit-module-path "$BUILD_DIR/<Module>.swiftmodule" \
     @"$BUILD_DIR/swift-sources.txt" \
     -I <c-include-path> \
     -L "$BUILD_DIR/c-build/src" -l<clib>
   ```

4. **Link in the app build.** Pass `-L "$BUILD_DIR"`, `-l<Module>`, and any C archive flags to the `swiftc` invocation that produces the app executable.

5. **Apply the VFS overlay to every swiftc invocation.** If the project uses a SwiftBridging VFS overlay, pass it to each `swiftc` call in the vendor pipeline — not only the final app compile. A missing overlay in any intermediate step triggers the same `redefinition of module 'SwiftBridging'` failure that it fixes in the main build.

6. **Make the vendor step idempotent.** Check for existing `.a` and `.swiftmodule` artifacts before invoking cmake or swiftc. Skip any step whose outputs are already present.

On a healthy toolchain, `swift build` via `Package.swift` handles the same dependency through normal package resolution; the vendor pipeline is only the broken-SwiftPM fallback.

Vendor sources (`.vendor/`) and compiled artifacts (`.build-scripts/vendor/`) must be gitignored. Do not commit cloned sources or pre-built libraries.

## SwiftUI App Initialization Rule

Minimal SwiftUI app scaffolds that need a Dock icon and menu bar in direct-run mode should set
the activation policy through `NSApplication.shared`, not `NSApp`, during `App.init()`:

```swift
import AppKit
import SwiftUI

@main
struct AppNameApplication: App {
    init() {
        NSApplication.shared.setActivationPolicy(.regular)
    }

    var body: some Scene {
        WindowGroup("AppName") {
            ContentView()
        }
    }
}
```

Do not call `NSApp.setActivationPolicy(.regular)` in `App.init()`. In direct `swiftc` builds and
fresh `.app` launches, `NSApp` can still be uninitialized at that point and the app may trap before
rendering its first window. Using `NSApplication.shared` forces AppKit initialization through the
supported accessor.

## Module Namespace Rule

When an imported Swift module exports types with the same names as platform framework types (for example, `Text`, `Link`, `Image`, or `Table`), every unqualified reference to those names becomes ambiguous and the compiler rejects the file.

Resolve collisions with module-qualified type aliases declared at file scope:

```swift
typealias PKGText  = PackageName.Text   // resolves conflict with SwiftUI.Text
typealias PKGLink  = PackageName.Link   // resolves conflict with SwiftUI.Link
typealias PKGImage = PackageName.Image  // resolves conflict with SwiftUI.Image
```

Use the alias name everywhere the package type is needed: local variables, return types, and protocol conformance method parameters.

Access control: aliases referenced in protocol conformance method signatures must be `internal` (the Swift default). Marking them `private` causes a secondary compiler error: "method must be declared private/fileprivate because its parameter uses a private type."

This pattern applies to any pair of imported modules, not only external packages vs. platform frameworks. Add aliases immediately after the import block in any file where the collision occurs.

## Toolchain Workaround Rule

Every direct Swift build script must source a shared `scripts/toolchain-workaround.sh`.

That file must detect known local Command Line Tools defects and apply narrowly scoped compiler flags. The known issue for this environment is duplicate `SwiftBridging` modulemaps:

- `/Library/Developer/CommandLineTools/usr/include/swift/module.modulemap`
- `/Library/Developer/CommandLineTools/usr/include/swift/bridging.modulemap`

When both define `SwiftBridging`, the build should create a VFS overlay that masks the stale modulemap with an empty file, then pass it through `swiftc -vfsoverlay`.

This workaround must be conditional. Healthy toolchains should receive no extra flags.

The VFS overlay must be passed to every `swiftc` invocation in the full build pipeline. When the pipeline includes multiple `swiftc` stages — for example, a vendor compilation step followed by the app compilation step — each stage independently needs `-vfsoverlay`. Omitting the overlay from any intermediate stage produces the same `redefinition of module 'SwiftBridging'` failure in that stage.

Suppressing the `SwiftBridging` redefinition also resolves a secondary `this SDK is not supported by the compiler` error. When `SwiftBridging` cannot load, the standard library import chain breaks and downstream modules report an SDK mismatch. The overlay removes both errors together.

## Test Rule

The `make test` target must try the real test suite first:

```sh
swift test --package-path "$ROOT_DIR"
```

If SwiftPM fails with known toolchain-level errors before project tests run, the script may fall back to a smoke test. Acceptable fallback triggers include:

- `Invalid manifest`
- `Operation not permitted` while writing a compiler module cache outside the workspace
- `SwiftShims`
- `SwiftBridging`
- `not supported by the compiler` SDK/compiler mismatch errors

For any other failure, print the SwiftPM log and exit non-zero. Do not hide real test failures behind the smoke test.

The smoke test must exercise a public app or CLI invariant, for example:

```sh
appname-cli --version
```

The smoke test is not a replacement for XCTest on a healthy toolchain. It is a resilience check for broken local toolchains.

## Bundle Rule

The app bundling script must use the direct release build:

```sh
CONFIG=release "$ROOT_DIR/scripts/build.sh"
```

Then assemble:

```text
dist/AppName.app/
  Contents/
    Info.plist
    MacOS/AppName
    MacOS/appname-cli
    Resources/
```

The bundle script must write `Info.plist`, copy the built executables from `.build-scripts/release/`, and ad-hoc sign local development bundles with:

```sh
codesign --force -s - "$APP_DIR"
```

Developer ID signing, hardened runtime, entitlements, and notarization can be layered onto the same script later, but the unsigned local build path should remain simple and deterministic.

After bundling, verify both the signature and Launch Services path:

```sh
codesign --verify --deep --strict --verbose=2 dist/AppName.app
open dist/AppName.app
```

If `open` returns success but the app does not appear, check for a fresh crash report before changing
the bundle script:

```sh
ls -lt ~/Library/Logs/DiagnosticReports | head
```

For scaffolds, a launch crash is usually an app initialization problem, not proof that bundling or
codesigning failed.

## Makefile Contract

Expose the resilient path through the normal developer commands:

```make
build:
	./scripts/build.sh

run:
	./scripts/run.sh

test:
	./scripts/test.sh

app:
	./scripts/bundle.sh

clean:
	rm -rf .build .build-scripts dist
```

Developers must be able to start from a fresh checkout and run:

```sh
make build
make test
make app
```

without depending on SwiftPM cache directories under `~/Library` or `~/.cache`.

## Git Ignore Rule

Generated build outputs must not be tracked:

```gitignore
.build/
.build-scripts/
dist/
.DS_Store
```

Reference projects and checked-in source examples should not include their generated `.app` bundles unless the repository intentionally stores binary examples.

## Troubleshooting Checklist

When a Swift macOS project fails before compiling project files, check the toolchain before changing app source:

```sh
swift --version
xcrun --sdk macosx --show-sdk-version
xcode-select -p
make build
```

If `swift build` or `swift test` fails with `Invalid manifest` but `make build` succeeds, treat it as a local SwiftPM, SDK, Command Line Tools, or sandbox issue.

If `swift build` fails with a package resolution error (`error: no such module`, `could not find a package`, `product 'X' not found`), confirm that the URL in `Package.swift` hosts a real Swift package and exports the referenced product name:

```sh
swift package resolve
# On failure, inspect the URL in Package.swift and verify it with:
# curl -I <url>
```

A resolution failure is a `Package.swift` authoring error, not a toolchain error. `make build` is unaffected since it never resolves packages, but any healthy-toolchain developer will be blocked until the dependency is corrected or removed.

If `swiftc` fails with `expressions are not allowed at the top level` or `'@main' attribute cannot be used in a module that contains top-level code`, a file named `main.swift` exists in the same module as the `@main` struct. Rename the file (for example `AppNameApp.swift`) and ensure `-parse-as-library` is passed when compiling the module.

Always separate "this repository is wrong" from "this toolchain is wrong" by reproducing against a minimal manifest outside the repo before editing `Package.swift`:

```sh
mkdir /tmp/spmcheck && cd /tmp/spmcheck
printf '// swift-tools-version: 6.0\nimport PackageDescription\nlet package = Package(name: "spmcheck")\n' > Package.swift
swift build
```

If the minimal manifest fails the same way, no change to the project can fix `swift build`; the failure is environmental and the direct `swiftc` path is the supported local build.

If direct `swiftc` fails with `redefinition of module 'SwiftBridging'`, confirm whether both Command Line Tools modulemaps define `SwiftBridging` and whether the VFS overlay masks the stale one.

If direct `swiftc` fails with `this SDK is not supported by the compiler`, first check whether the `SwiftBridging` duplicate-modulemap error is also present. The `SwiftBridging` redefinition breaks the standard library import chain and produces downstream `this SDK is not supported` messages even when the compiler and SDK are genuinely compatible. Suppressing the redefinition with the VFS overlay typically removes the secondary mismatch error as well. If the overlay is already active and the SDK error persists in isolation, then the compiler and SDK are actually mismatched; the durable fix is reinstalling or switching Xcode Command Line Tools.

If the project requires an external Swift package and SwiftPM is broken, check whether a vendor build script exists (for example `scripts/vendor.sh`). If present, run it in isolation (`bash scripts/vendor.sh`) before re-running `make build`. Confirm that C static archives and the `.swiftmodule` file are present under the vendor artifact directory. The first run can take several minutes due to cmake configuration and swiftc compilation; subsequent runs skip completed steps and are fast.

If `swiftc` fails with `'memberName' is inaccessible due to 'private' protection level` and the accessing code is in a different type in the same file (e.g. an outer `struct` method accessing a `private` member of a nested `class`), change the member's access modifier from `private` to `fileprivate`. Swift's `private` scopes to the enclosing declaration, not the file; `fileprivate` grants same-file access without widening to the whole module. Note that closures defined inside the nested type's own methods retain `private` access without any change.

If `swiftc` fails with `error: 'TypeName' is ambiguous for type lookup in this context`, an imported module exports a type with the same name as a platform framework type. Add module-qualified type aliases at file scope (see the Module Namespace Rule) to resolve the ambiguity at each affected file.

If `swiftc` fails with `value of type 'any SomeProtocol' has no member 'propertyName'`, the property is defined in a protocol extension rather than the protocol requirement itself. Existential values (`any Protocol`) do not dispatch protocol extension members. Cast to the known concrete type before accessing the property.

If `make app` succeeds and `codesign --verify` passes but `open dist/AppName.app` exits immediately,
inspect the newest `~/Library/Logs/DiagnosticReports/AppName-*.ips` file. A SIGTRAP in the SwiftUI
`App.init()` frame usually points to unsafe startup code such as `NSApp` access before AppKit has
created the shared application instance.

## Confirmed Failure Modes

### Duplicate SwiftBridging modulemaps

`/Library/Developer/CommandLineTools/usr/include/swift/` contains both `module.modulemap` and `bridging.modulemap` defining `SwiftBridging`, so direct `swiftc` fails with `redefinition of module 'SwiftBridging'`. Worked around conditionally in `scripts/toolchain-workaround.sh` with a VFS overlay (see Toolchain Workaround Rule).

### SwiftUI direct-build launch trap from early `NSApp` access

Symptom: `make build` and `make app` succeed, `codesign --verify` passes,
and `open dist/AppName.app` returns zero, but the app never shows a window. A fresh crash report
appears under `~/Library/Logs/DiagnosticReports/` with `EXC_BREAKPOINT` / `SIGTRAP`; the crashing
frame is in `protocol witness for App.init()` or the concrete SwiftUI `App.init()`.

Root cause: the scaffold called `NSApp.setActivationPolicy(.regular)` inside `App.init()`. In a
direct `swiftc` executable or newly launched bundle, the global `NSApp` can be nil/uninitialized
at that point. Swift traps before the app body renders.

Remediation: call `NSApplication.shared.setActivationPolicy(.regular)` instead. Keep this as the
default pattern in no-Xcode SwiftUI scaffolds that need a regular app activation policy.

### Mismatched SwiftPM ManifestAPI (stale private swiftinterface)

Symptom: every `swift build` / `swift test` / `swift run` — including a trivial `Package(name:)` manifest in an empty directory — fails with `Invalid manifest` followed by a linker error such as:

```text
Undefined symbols for architecture arm64:
  "PackageDescription.Package.__allocating_init(... swiftLanguageVersions: [PackageDescription.SwiftVersion]? ...)"
```

Root cause: a partially updated Command Line Tools install left stale files inside `usr/lib/swift/pm/ManifestAPI/PackageDescription.swiftmodule/`. On the affected machine the `*.private.swiftinterface` files dated from an older CLT generation (where `SwiftVersion` is a standalone `enum`), while `libPackageDescription.dylib` and the regular `*.swiftinterface` came from CLT 16.2 (where `SwiftVersion` is a deprecated `typealias` of `SwiftLanguageMode`). The compiler prefers the private interface when present, so the manifest is compiled against the old API signature and then fails to link against the new dylib, which only exports the `SwiftLanguageMode` symbols.

Diagnosis:

```sh
# Interface files and dylib should come from the same CLT release.
stat -f "%Sm %N" /Library/Developer/CommandLineTools/usr/lib/swift/pm/ManifestAPI/PackageDescription.swiftmodule/*
stat -f "%Sm %N" /Library/Developer/CommandLineTools/usr/lib/swift/pm/ManifestAPI/libPackageDescription.dylib

# Compare what the dylib actually exports against the undefined symbol.
nm -gU /Library/Developer/CommandLineTools/usr/lib/swift/pm/ManifestAPI/libPackageDescription.dylib \
  | swift demangle | grep "Package.__allocating_init"
```

Remediation: this cannot be patched from inside a project — the broken files are root-owned toolchain files and SwiftPM controls the manifest compile invocation. The durable fix is a clean Command Line Tools reinstall (`sudo rm -rf /Library/Developer/CommandLineTools && xcode-select --install`) or switching to a full Xcode toolchain with `xcode-select`. Until then, the direct `swiftc` path (`make build` / `make test` / `make app`) is the supported local build, and `scripts/test.sh` already falls back to smoke tests when `swift test` dies on `Invalid manifest`.

Prevention: documents and acceptance checklists must never list `swift build` / `swift test` / `swift run` as the only verification path; always list the `make` equivalent alongside, and verify doc cross-references still resolve after consolidating or deleting findings files.

### `@main` entry-point conflict with `main.swift`

Symptom: `swiftc` (or `swift build`) fails with either `expressions are not allowed at the top level` or `'@main' attribute cannot be used in a module that contains top-level code`, even though no top-level expressions appear in the `@main` struct file.

Root cause: a file named `main.swift` was present in the same compilation unit as the `@main` struct. Swift gives `main.swift` special treatment — it is implicitly the top-level entry point. Having both `main.swift` (implicit entry) and `@main` (explicit entry) in the same module is an error.

Remediation: rename the file containing the `@main` struct to match the struct name (for example `AppNameApp.swift`). Pass `-parse-as-library` when compiling the module so `swiftc` does not expect a `main.swift` top-level expression.

Prevention: the source layout rule above prohibits naming `@main` struct files `main.swift`. The only file legitimately named `main.swift` should be a CLI target whose entry point is a free top-level expression (not `@main`).

### Unresolvable external package dependency in `Package.swift`

Symptom: `swift build` fails during package resolution with an error such as `could not find a package`, `product 'X' not found`, or a 404/timeout fetching the dependency URL. `make build` is unaffected.

Root cause: `Package.swift` referenced an external package at a URL that does not host a Swift package, does not export a product under the expected name, or has since been deleted or renamed.

Remediation: remove the dependency from `Package.swift`. Replace the functionality with the platform equivalent — check whether `Foundation`, `AppKit`, or `SwiftUI` covers the use case before seeking another external package.

Prevention: run `swift package resolve` and confirm success before committing any new external dependency. Prefer platform frameworks; document the rationale for any external package that genuinely cannot be replaced. See the External Dependency Rule above.

### Type namespace collision between imported module and platform framework

Symptom: `swiftc` fails with `error: 'TypeName' is ambiguous for type lookup in this context` at every usage site for any type exported by both an imported package and a platform framework under the same unqualified name (for example, `Text`, `Link`, `Image`, or `Table` when importing a third-party package alongside SwiftUI).

Root cause: Swift does not automatically prefer one module's definition over another when two imported modules export the same unqualified type name. Every reference is ambiguous at the call site.

Remediation: add `internal` type aliases at file scope — one per conflicting name — using the fully-qualified `ModuleName.TypeName` form. Use those aliases in all method signatures, variable declarations, and protocol conformance method parameters in files that import both modules. Do not use `private` for aliases that appear in conformance method signatures; `private` causes a secondary "method must be declared private/fileprivate because its parameter uses a private type" error. See the Module Namespace Rule above.

Prevention: before importing a new package, identify its exported type names. Add aliases proactively for any that collide with framework types.

### Protocol extension methods not accessible through `any Protocol` existentials

Symptom: `swiftc` (Swift 5.7+ / Swift 6) reports `value of type 'any SomeProtocol' has no member 'propertyOrMethod'` even though the property or method works correctly when called on a concrete conforming type.

Root cause: in Swift's existential model, members defined only in a protocol extension (present in `extension SomeProtocol { ... }` but not listed in the protocol declaration itself) cannot be dynamically dispatched through an `any SomeProtocol` existential. Libraries that model tree or node hierarchies commonly return `any NodeProtocol` from child-iteration APIs; computed convenience properties in extensions are not available on those existential values.

Remediation: downcast the existential to the concrete type that owns the extension before accessing the member:

```swift
for child in parent.children {
    if let cell = child as? ConcreteCell {
        let text = cell.extensionProperty   // accessible on the concrete type
    }
}
```

Prevention: when working with a library's node-iteration API, check whether the needed property is a protocol requirement (listed in the `protocol` declaration) or extension-only. If extension-only, plan for a concrete-type downcast at the call site.

### Implicit `self` unavailable inside nested closures after `guard let self`

Symptom: `swiftc` reports errors such as `call to method 'foo' in closure requires explicit use of 'self' to make capture semantics explicit` and `reference to property 'bar' in closure requires explicit use of 'self'` inside a nested closure, even though `guard let self else { return }` appears just above. A companion warning — `value 'self' was defined but never used; consider replacing with boolean test` — is emitted for the `guard let self` binding itself.

Root cause: the shorthand `guard let self else { return }` (Swift 5.3+) rebinds `self` as a non-optional strong reference within the `guard`'s scope, but the compiler does not extend implicit-`self` capture into closures nested inside that scope. A nested closure (such as a trailing closure passed to a method call) requires every member reference to be qualified explicitly with `self.`, even when the enclosing `guard let self` has already confirmed `self` is alive.

Remediation: replace the shorthand form with the explicit rebind:

```swift
// Before — compiles but silently fails to enable implicit self in nested closures:
guard let self else { return }

// After — rebinds self as a named non-optional; explicit self. in nested closures satisfies the compiler:
guard let self = self else { return }
self.performUpdate {
    self.property = newValue
    self.counter = count
}
```

Prevention: whenever a `[weak self]` closure calls a method that itself accepts a closure argument, use `guard let self = self` and qualify every member reference with `self.` inside the nested closure. Do not rely on `guard let self` (shorthand) enabling implicit capture in nested closure bodies.

### `private` member of a nested type inaccessible from the enclosing type's methods

Symptom: `swiftc` fails with `'memberName' is inaccessible due to 'private' protection level` when a method on an outer type (e.g. a `struct`) tries to read or write a `private` member of a nested type (e.g. a nested `class`) through an instance of that nested type — even when both declarations are in the same file.

```
SomeView.swift:56: error: 'memberName' is inaccessible due to 'private' protection level
    context.coordinator.memberName = value
    private var memberName: String = ""   ← declared in Coordinator, a nested class
```

Root cause: Swift's `private` access modifier scopes to the **enclosing declaration** (the innermost `{ }` block that contains the declaration), not to the file. A `private` member declared inside a nested type (e.g. `Coordinator`) is inaccessible from a method on the outer type (e.g. `makeNSView` on the enclosing `struct`) — even though both types live in the same `.swift` file.

This is distinct from the case where a closure is defined inside the nested type's own methods: closures defined within a declaration scope inherit that scope and **can** access `private` members of the same type without issue.

Summary of Swift access levels relevant to this pattern:

| Modifier | Accessible from |
|---|---|
| `private` | The enclosing declaration only (same `{ }` block, including extensions in the same file) |
| `fileprivate` | Anywhere within the same `.swift` file |
| `internal` | Anywhere within the same module |

Remediation: change the access modifier from `private` to `fileprivate` on any member that must be set or read by a method on an outer/enclosing type in the same file. Prefer the narrowest modifier that compiles: use `fileprivate` rather than loosening all the way to `internal`.

```swift
// Before — private: inaccessible from the enclosing struct's methods
private var memberName: String = ""

// After — fileprivate: accessible from the enclosing struct's methods (same file), hidden from other files
fileprivate var memberName: String = ""
```

Prevention: when specifying that a nested-type member should be assigned from an enclosing type's method (e.g. `makeNSView`, `updateNSView` for `NSViewRepresentable`), explicitly check the member's access modifier before the change is committed. If it is `private`, the compiler will reject the cross-scope access; `fileprivate` is the correct minimum fix.

## Maintenance Requirements

- Keep `Package.swift` and `scripts/build.sh` target lists in sync.
- Keep smoke tests minimal and public API based.
- Do not special-case test assertions to pass smoke tests.
- Keep compiler workarounds conditional and documented.
- Keep all generated files inside `.build-scripts/`, `.build/`, or `dist/`.
- Update this guideline when a new toolchain failure mode is confirmed and worked around.
- When a vendor build script is added, keep it synchronized with `scripts/build.sh`: every C archive or Swift module added to the vendor pipeline must be reflected in both the vendor script (build step) and the build script (link step).
- When module namespace aliases are added to resolve type name conflicts, comment the conflicting module names at the alias declaration so the reason remains clear after the surrounding import context is forgotten.
