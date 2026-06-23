from visual_diff import CompareConfig, compare_images

result = compare_images(
    "before.png",
    "after.png",
    CompareConfig(
        size_policy="pad",
        output_dir="visual_diff_report",
        diff_threshold=8,
        edge_threshold=40,
        edge_dilation_radius=1,
        object_min_area=20,
    ),
)

report = result.to_dict()
print("Decision:", result.decision)
print("Explanation:", result.explanation)
print("Changed ratio:", report["changed_pixel_ratio"])
print("Residual p95 abs:", report["residual"]["global"]["p95_abs"])
print("Edge F1:", report["edge_metrics"]["edge_f1"])
print("Input A SHA-256:", report["audit"]["inputs"]["image_a"]["sha256"])
print("Overlay artifact:", report["output_files"].get("overlay"))
