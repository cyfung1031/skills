#!/usr/bin/env python3
"""
visual_diff.py

A fully featured image visual-difference skill for agents.
Uses Pillow, NumPy, and SciPy only.

Features:
- Exact and perceptual comparison
- Robust loading with EXIF orientation
- Size handling: strict, pad, or resize
- Alpha handling by compositing RGBA over a chosen background
- Pixel metrics: MAE, MSE, RMSE, max channel delta, changed-pixel ratio
- Signed residual/value comparison, including per-channel residual statistics
- PSNR and SSIM-like structural similarity implemented with scipy.ndimage
- Difference masks, heatmaps, residual maps, overlay images, and bounding boxes
- Connected-component regions for changed areas
- Numerical object-like component coordinates derived from edge/component analysis
- Edge/shape/line comparison using Sobel edges, tolerance matching, and distance metrics
- Agent-friendly JSON report with same/different decision and evidence
- CLI interface
"""

from __future__ import annotations

import argparse
import dataclasses
import hashlib
import json
import math
import os
import platform
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional, Sequence, Tuple

import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageOps
from scipy import ndimage

SizePolicy = Literal["strict", "pad", "resize"]
Decision = Literal["same", "similar", "different"]

__version__ = "0.2.0"


@dataclasses.dataclass
class CompareConfig:
    """Configuration for image comparison.

    Thresholds are intentionally conservative. Tune them for your domain.
    For UI screenshots, use lower tolerances. For photos/renders, use higher tolerances.
    """

    size_policy: SizePolicy = "pad"
    alpha_background: Tuple[int, int, int] = (255, 255, 255)

    # Pixel/value comparison thresholds.
    diff_threshold: int = 8
    region_min_area: int = 12
    ssim_window_sigma: float = 1.5
    same_changed_ratio_max: float = 0.0005
    same_mae_max: float = 0.5
    same_ssim_min: float = 0.998
    similar_changed_ratio_max: float = 0.02
    similar_mae_max: float = 4.0
    similar_ssim_min: float = 0.96

    # Edge/shape comparison thresholds.
    edge_threshold: float = 40.0
    edge_dilation_radius: int = 1
    edge_region_min_area: int = 8
    same_edge_f1_min: float = 0.995
    same_edge_changed_ratio_max: float = 0.001
    similar_edge_f1_min: float = 0.94
    similar_edge_changed_ratio_max: float = 0.025

    # Object-like component coordinate extraction.
    object_min_area: int = 20
    object_edge_dilation_radius: int = 3
    max_objects: int = 50
    include_object_coordinates: bool = True

    # Output controls.
    residual_visual_gain: float = 1.0
    make_outputs: bool = True
    output_dir: Optional[str] = None
    output_prefix: str = "visual_diff"

    # Safety / production limits. Set to None only in controlled local runs.
    max_pixels: Optional[int] = 80_000_000


@dataclasses.dataclass
class DifferenceRegion:
    id: int
    bbox_xyxy: Tuple[int, int, int, int]
    area_pixels: int
    changed_pixel_ratio: float
    mean_delta: float
    max_delta: int


@dataclasses.dataclass
class ObjectRegion:
    """Object-like connected visual component coordinates.

    This is not semantic object detection. It identifies connected visual components
    from edge maps so an agent gets numerical coordinates for visible shapes/objects.
    """

    id: int
    bbox_xyxy: Tuple[int, int, int, int]
    bbox_cxcywh: Tuple[float, float, int, int]
    centroid_xy: Tuple[float, float]
    area_pixels: int
    edge_pixels: int
    edge_density: float
    mean_luma: float


@dataclasses.dataclass
class VisualDiffResult:
    decision: Decision
    is_exact_match: bool
    same_size: bool
    image_a_size: Tuple[int, int]
    image_b_size: Tuple[int, int]
    compared_size: Tuple[int, int]
    changed_pixels: int
    total_pixels: int
    changed_pixel_ratio: float
    mae: float
    mse: float
    rmse: float
    max_delta: int
    psnr_db: Optional[float]
    ssim: float
    residual: Dict[str, Any]
    edge_metrics: Dict[str, Any]
    regions: List[DifferenceRegion]
    edge_regions: List[DifferenceRegion]
    objects_a: List[ObjectRegion]
    objects_b: List[ObjectRegion]
    output_files: Dict[str, str]
    config: Dict[str, Any]
    audit: Dict[str, Any]
    explanation: str

    def to_dict(self) -> Dict[str, Any]:
        return _json_safe(dataclasses.asdict(self))


class VisualDiffError(RuntimeError):
    pass

def _sha256_file(path: str | Path, chunk_size: int = 1024 * 1024) -> str:
    """Return a SHA-256 digest for auditability without loading the whole file."""
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda: f.read(chunk_size), b""):
            h.update(chunk)
    return h.hexdigest()


def _file_info(path: str | Path) -> Dict[str, Any]:
    p = Path(path)
    try:
        stat = p.stat()
        return {
            "path": str(p),
            "name": p.name,
            "size_bytes": int(stat.st_size),
            "sha256": _sha256_file(p),
        }
    except OSError as exc:
        raise VisualDiffError(f"Could not stat input file {p!s}: {exc}") from exc


def _dependency_versions() -> Dict[str, str]:
    versions = {"python": sys.version.split()[0]}
    try:
        versions["pillow"] = Image.__version__
    except Exception:
        versions["pillow"] = "unknown"
    try:
        versions["numpy"] = np.__version__
    except Exception:
        versions["numpy"] = "unknown"
    try:
        import scipy  # type: ignore

        versions["scipy"] = scipy.__version__
    except Exception:
        versions["scipy"] = "unknown"
    return versions


def _validate_config(config: CompareConfig) -> None:
    """Fail early for nonsensical values so CI and agents get deterministic errors."""
    if config.size_policy not in ("strict", "pad", "resize"):
        raise VisualDiffError(f"Unsupported size_policy: {config.size_policy!r}")
    if len(config.alpha_background) != 3 or any(int(v) < 0 or int(v) > 255 for v in config.alpha_background):
        raise VisualDiffError("alpha_background must contain three integers in 0..255")
    nonnegative_ints = {
        "diff_threshold": config.diff_threshold,
        "region_min_area": config.region_min_area,
        "edge_dilation_radius": config.edge_dilation_radius,
        "edge_region_min_area": config.edge_region_min_area,
        "object_min_area": config.object_min_area,
        "object_edge_dilation_radius": config.object_edge_dilation_radius,
        "max_objects": config.max_objects,
    }
    for name, value in nonnegative_ints.items():
        if int(value) < 0:
            raise VisualDiffError(f"{name} must be non-negative")
    if not 0 <= int(config.diff_threshold) <= 255:
        raise VisualDiffError("diff_threshold must be in 0..255")
    for name in (
        "same_changed_ratio_max",
        "similar_changed_ratio_max",
        "same_edge_changed_ratio_max",
        "similar_edge_changed_ratio_max",
        "same_ssim_min",
        "similar_ssim_min",
        "same_edge_f1_min",
        "similar_edge_f1_min",
    ):
        value = float(getattr(config, name))
        if not 0.0 <= value <= 1.0:
            raise VisualDiffError(f"{name} must be in 0..1")
    if config.same_changed_ratio_max > config.similar_changed_ratio_max:
        raise VisualDiffError("same_changed_ratio_max cannot exceed similar_changed_ratio_max")
    if config.same_mae_max > config.similar_mae_max:
        raise VisualDiffError("same_mae_max cannot exceed similar_mae_max")
    if config.same_ssim_min < config.similar_ssim_min:
        raise VisualDiffError("same_ssim_min cannot be lower than similar_ssim_min")
    if config.same_edge_f1_min < config.similar_edge_f1_min:
        raise VisualDiffError("same_edge_f1_min cannot be lower than similar_edge_f1_min")
    if config.same_edge_changed_ratio_max > config.similar_edge_changed_ratio_max:
        raise VisualDiffError("same_edge_changed_ratio_max cannot exceed similar_edge_changed_ratio_max")
    if float(config.ssim_window_sigma) <= 0:
        raise VisualDiffError("ssim_window_sigma must be positive")
    if float(config.edge_threshold) < 0:
        raise VisualDiffError("edge_threshold must be non-negative")
    if float(config.residual_visual_gain) <= 0:
        raise VisualDiffError("residual_visual_gain must be positive")
    if config.max_pixels is not None and int(config.max_pixels) <= 0:
        raise VisualDiffError("max_pixels must be positive or None")


def _guard_image_size(label: str, img: Image.Image, config: CompareConfig) -> None:
    if config.max_pixels is None:
        return
    pixels = int(img.width * img.height)
    if pixels > int(config.max_pixels):
        raise VisualDiffError(
            f"{label} has {pixels} pixels, exceeding max_pixels={config.max_pixels}. "
            "Raise the limit only for trusted local inputs."
        )



def _json_safe(value: Any) -> Any:
    """Convert dataclass output containing tuples/NumPy scalars to JSON-safe values."""
    if isinstance(value, dict):
        return {str(k): _json_safe(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_safe(v) for v in value]
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, np.floating):
        return float(value)
    if isinstance(value, np.ndarray):
        return value.tolist()
    return value


def _load_image(path: str | Path) -> Image.Image:
    """Load image with EXIF transpose and convert to RGBA."""
    try:
        img = Image.open(path)
        img = ImageOps.exif_transpose(img)
        return img.convert("RGBA")
    except Exception as exc:
        raise VisualDiffError(f"Could not load image {path!s}: {exc}") from exc


def _composite_alpha(img: Image.Image, bg_rgb: Tuple[int, int, int]) -> Image.Image:
    """Composite an RGBA image over a solid RGB background."""
    if img.mode != "RGBA":
        img = img.convert("RGBA")
    bg = Image.new("RGBA", img.size, bg_rgb + (255,))
    return Image.alpha_composite(bg, img).convert("RGB")


def _prepare_images(
    a: Image.Image,
    b: Image.Image,
    config: CompareConfig,
) -> Tuple[Image.Image, Image.Image, Tuple[int, int], Tuple[int, int]]:
    """Normalize alpha and size according to config."""
    original_a_size = a.size
    original_b_size = b.size

    a = _composite_alpha(a, config.alpha_background)
    b = _composite_alpha(b, config.alpha_background)

    if a.size == b.size:
        return a, b, original_a_size, original_b_size

    if config.size_policy == "strict":
        raise VisualDiffError(
            f"Image sizes differ: {a.size} vs {b.size}. Use size_policy='pad' or 'resize'."
        )

    if config.size_policy == "resize":
        b = b.resize(a.size, Image.Resampling.LANCZOS)
        return a, b, original_a_size, original_b_size

    if config.size_policy == "pad":
        width = max(a.width, b.width)
        height = max(a.height, b.height)
        padded_a = Image.new("RGB", (width, height), config.alpha_background)
        padded_b = Image.new("RGB", (width, height), config.alpha_background)
        padded_a.paste(a, (0, 0))
        padded_b.paste(b, (0, 0))
        return padded_a, padded_b, original_a_size, original_b_size

    raise VisualDiffError(f"Unsupported size_policy: {config.size_policy}")


def _rgb_to_luma(arr: np.ndarray) -> np.ndarray:
    """Convert RGB uint8/float array to luminance float64."""
    arr = arr.astype(np.float64)
    return 0.2126 * arr[..., 0] + 0.7152 * arr[..., 1] + 0.0722 * arr[..., 2]


def _compute_ssim_luma(a: np.ndarray, b: np.ndarray, sigma: float = 1.5) -> float:
    """Compute a global SSIM-like score on luminance using scipy.ndimage.

    This follows the standard SSIM formula with Gaussian local statistics.
    Returns 1.0 for identical images and lower values for structural differences.
    """
    x = _rgb_to_luma(a)
    y = _rgb_to_luma(b)

    data_range = 255.0
    c1 = (0.01 * data_range) ** 2
    c2 = (0.03 * data_range) ** 2

    ux = ndimage.gaussian_filter(x, sigma=sigma)
    uy = ndimage.gaussian_filter(y, sigma=sigma)
    ux2 = ux * ux
    uy2 = uy * uy
    uxuy = ux * uy

    vx = ndimage.gaussian_filter(x * x, sigma=sigma) - ux2
    vy = ndimage.gaussian_filter(y * y, sigma=sigma) - uy2
    vxy = ndimage.gaussian_filter(x * y, sigma=sigma) - uxuy

    numerator = (2 * uxuy + c1) * (2 * vxy + c2)
    denominator = (ux2 + uy2 + c1) * (vx + vy + c2)
    ssim_map = numerator / np.maximum(denominator, np.finfo(np.float64).eps)
    return float(np.clip(np.mean(ssim_map), -1.0, 1.0))


def _psnr(mse: float) -> Optional[float]:
    if mse == 0:
        return None
    return float(20.0 * math.log10(255.0 / math.sqrt(mse)))


def _make_heatmap(delta_mag: np.ndarray) -> Image.Image:
    """Create a simple heatmap without requiring matplotlib.

    Black/transparent-ish low values become dark; stronger differences become yellow/red.
    Output is RGB.
    """
    norm = delta_mag.astype(np.float64)
    max_val = float(norm.max()) if norm.size else 0.0
    if max_val > 0:
        norm = norm / max_val
    else:
        norm = norm * 0

    # Piecewise heat: black -> blue -> cyan -> yellow -> red, generated numerically.
    r = np.clip(4 * norm - 1.5, 0, 1)
    g = np.clip(4 * norm - 0.5, 0, 1) - np.clip(4 * norm - 3.0, 0, 1)
    b = np.clip(2.5 - 4 * norm, 0, 1)
    heat = np.stack([r, g, b], axis=-1)
    return Image.fromarray(np.uint8(np.clip(heat * 255, 0, 255)), mode="RGB")


def _make_overlay(base: Image.Image, mask: np.ndarray, rgba: Tuple[int, int, int, int] = (255, 0, 0, 140)) -> Image.Image:
    """Overlay a mask over the first image."""
    overlay = base.convert("RGBA")
    color = Image.new("RGBA", base.size, (rgba[0], rgba[1], rgba[2], 0))
    alpha = np.where(mask, rgba[3], 0).astype(np.uint8)
    color.putalpha(Image.fromarray(alpha, mode="L"))
    return Image.alpha_composite(overlay, color).convert("RGB")


def _find_regions(
    delta_mag: np.ndarray,
    mask: np.ndarray,
    min_area: int,
) -> List[DifferenceRegion]:
    """Find connected components in a binary difference mask."""
    structure = np.ones((3, 3), dtype=np.uint8)
    labeled, count = ndimage.label(mask, structure=structure)
    if count == 0:
        return []

    slices = ndimage.find_objects(labeled)
    regions: List[DifferenceRegion] = []
    total_pixels = int(mask.size)

    for idx, slc in enumerate(slices, start=1):
        if slc is None:
            continue
        region_mask = labeled[slc] == idx
        area = int(region_mask.sum())
        if area < min_area:
            continue
        y_slice, x_slice = slc
        y1, y2 = int(y_slice.start), int(y_slice.stop)
        x1, x2 = int(x_slice.start), int(x_slice.stop)
        values = delta_mag[slc][region_mask]
        regions.append(
            DifferenceRegion(
                id=len(regions) + 1,
                bbox_xyxy=(x1, y1, x2, y2),
                area_pixels=area,
                changed_pixel_ratio=float(area / total_pixels) if total_pixels else 0.0,
                mean_delta=float(values.mean()) if values.size else 0.0,
                max_delta=int(values.max()) if values.size else 0,
            )
        )

    regions.sort(key=lambda r: r.area_pixels, reverse=True)
    # Reassign IDs after sorting.
    for i, region in enumerate(regions, start=1):
        region.id = i
    return regions


def _draw_region_boxes(img: Image.Image, regions: Sequence[DifferenceRegion]) -> Image.Image:
    out = img.convert("RGB").copy()
    draw = ImageDraw.Draw(out)
    for region in regions:
        x1, y1, x2, y2 = region.bbox_xyxy
        # Pillow rectangle is inclusive; x2/y2 from NumPy slicing are exclusive.
        draw.rectangle((x1, y1, max(x1, x2 - 1), max(y1, y2 - 1)), outline=(255, 0, 0), width=2)
        draw.text((x1 + 2, y1 + 2), str(region.id), fill=(255, 0, 0))
    return out


def _draw_object_boxes(img: Image.Image, objects: Sequence[ObjectRegion]) -> Image.Image:
    out = img.convert("RGB").copy()
    draw = ImageDraw.Draw(out)
    for obj in objects:
        x1, y1, x2, y2 = obj.bbox_xyxy
        draw.rectangle((x1, y1, max(x1, x2 - 1), max(y1, y2 - 1)), outline=(0, 128, 255), width=2)
        draw.text((x1 + 2, y1 + 2), f"obj {obj.id}", fill=(0, 128, 255))
    return out


def _residual_summary(delta_signed: np.ndarray, delta_abs: np.ndarray) -> Dict[str, Any]:
    """Summarize signed residuals and absolute residual values."""
    names = ["r", "g", "b"]
    per_channel: Dict[str, Any] = {}
    total_per_channel_pixels = int(delta_signed.shape[0] * delta_signed.shape[1]) if delta_signed.ndim == 3 else 0

    for channel_idx, name in enumerate(names):
        signed = delta_signed[..., channel_idx].astype(np.float64)
        absolute = np.abs(signed)
        positive = int((signed > 0).sum())
        negative = int((signed < 0).sum())
        zero = int((signed == 0).sum())
        per_channel[name] = {
            "min_signed": int(signed.min()) if signed.size else 0,
            "max_signed": int(signed.max()) if signed.size else 0,
            "mean_signed": float(signed.mean()) if signed.size else 0.0,
            "std_signed": float(signed.std()) if signed.size else 0.0,
            "mean_abs": float(absolute.mean()) if absolute.size else 0.0,
            "median_abs": float(np.percentile(absolute, 50)) if absolute.size else 0.0,
            "p95_abs": float(np.percentile(absolute, 95)) if absolute.size else 0.0,
            "mean_squared": float(np.mean(signed ** 2)) if signed.size else 0.0,
            "positive_pixels_a_brighter": positive,
            "negative_pixels_b_brighter": negative,
            "zero_pixels": zero,
            "positive_ratio_a_brighter": float(positive / total_per_channel_pixels) if total_per_channel_pixels else 0.0,
            "negative_ratio_b_brighter": float(negative / total_per_channel_pixels) if total_per_channel_pixels else 0.0,
            "zero_ratio": float(zero / total_per_channel_pixels) if total_per_channel_pixels else 0.0,
        }

    abs_channel_max = np.max(delta_abs, axis=2).astype(np.float64) if delta_abs.size else np.array([], dtype=np.float64)
    signed_all = delta_signed.astype(np.float64).ravel()
    abs_all = np.abs(signed_all)
    positive_all = int((signed_all > 0).sum()) if signed_all.size else 0
    negative_all = int((signed_all < 0).sum()) if signed_all.size else 0
    zero_all = int((signed_all == 0).sum()) if signed_all.size else 0
    total_values = int(signed_all.size)

    return {
        "definition": "signed residual is image_a - image_b per RGB channel; positive means image A is brighter in that channel",
        "global": {
            "min_signed": int(signed_all.min()) if signed_all.size else 0,
            "max_signed": int(signed_all.max()) if signed_all.size else 0,
            "mean_signed": float(signed_all.mean()) if signed_all.size else 0.0,
            "std_signed": float(signed_all.std()) if signed_all.size else 0.0,
            "mean_abs": float(abs_all.mean()) if abs_all.size else 0.0,
            "median_abs": float(np.percentile(abs_all, 50)) if abs_all.size else 0.0,
            "p90_abs": float(np.percentile(abs_all, 90)) if abs_all.size else 0.0,
            "p95_abs": float(np.percentile(abs_all, 95)) if abs_all.size else 0.0,
            "p99_abs": float(np.percentile(abs_all, 99)) if abs_all.size else 0.0,
            "positive_values_a_brighter": positive_all,
            "negative_values_b_brighter": negative_all,
            "zero_values": zero_all,
            "positive_ratio_a_brighter": float(positive_all / total_values) if total_values else 0.0,
            "negative_ratio_b_brighter": float(negative_all / total_values) if total_values else 0.0,
            "zero_ratio": float(zero_all / total_values) if total_values else 0.0,
        },
        "per_channel": per_channel,
        "per_pixel_channel_max_abs": {
            "mean": float(abs_channel_max.mean()) if abs_channel_max.size else 0.0,
            "median": float(np.percentile(abs_channel_max, 50)) if abs_channel_max.size else 0.0,
            "p90": float(np.percentile(abs_channel_max, 90)) if abs_channel_max.size else 0.0,
            "p95": float(np.percentile(abs_channel_max, 95)) if abs_channel_max.size else 0.0,
            "p99": float(np.percentile(abs_channel_max, 99)) if abs_channel_max.size else 0.0,
            "max": int(abs_channel_max.max()) if abs_channel_max.size else 0,
        },
    }


def _compute_edge_mask(arr: np.ndarray, threshold: float) -> Tuple[np.ndarray, np.ndarray]:
    """Compute Sobel luminance gradient magnitude and binary edge mask."""
    luma = _rgb_to_luma(arr)
    sx = ndimage.sobel(luma, axis=1, mode="reflect")
    sy = ndimage.sobel(luma, axis=0, mode="reflect")
    grad_mag = np.hypot(sx, sy)
    edge_mask = grad_mag > float(threshold)
    return grad_mag, edge_mask


def _dilate_bool(mask: np.ndarray, iterations: int) -> np.ndarray:
    if iterations <= 0:
        return mask.astype(bool)
    structure = np.ones((3, 3), dtype=bool)
    return ndimage.binary_dilation(mask.astype(bool), structure=structure, iterations=int(iterations))


def _distance_stats(source_edges: np.ndarray, target_edges: np.ndarray) -> Dict[str, Optional[float]]:
    """Distance in pixels from each source edge pixel to nearest target edge pixel."""
    source_count = int(source_edges.sum())
    target_count = int(target_edges.sum())
    if source_count == 0 and target_count == 0:
        return {"mean": 0.0, "p95": 0.0, "max": 0.0}
    if source_count == 0:
        return {"mean": 0.0, "p95": 0.0, "max": 0.0}
    if target_count == 0:
        return {"mean": None, "p95": None, "max": None}

    # distance_transform_edt computes distance to nearest False, so pass inverse target edges.
    distances_to_target = ndimage.distance_transform_edt(~target_edges.astype(bool))
    vals = distances_to_target[source_edges.astype(bool)]
    return {
        "mean": float(vals.mean()) if vals.size else 0.0,
        "p95": float(np.percentile(vals, 95)) if vals.size else 0.0,
        "max": float(vals.max()) if vals.size else 0.0,
    }


def _edge_metrics(
    edge_a: np.ndarray,
    edge_b: np.ndarray,
    grad_a: np.ndarray,
    grad_b: np.ndarray,
    config: CompareConfig,
) -> Tuple[Dict[str, Any], np.ndarray, List[DifferenceRegion]]:
    """Compare edge maps with configurable tolerance and distance metrics."""
    tolerance = int(config.edge_dilation_radius)
    a_tol = _dilate_bool(edge_a, tolerance)
    b_tol = _dilate_bool(edge_b, tolerance)

    matched_a = edge_a & b_tol
    matched_b = edge_b & a_tol
    unmatched_a = edge_a & ~b_tol
    unmatched_b = edge_b & ~a_tol
    edge_changed_mask = unmatched_a | unmatched_b

    edge_pixels_a = int(edge_a.sum())
    edge_pixels_b = int(edge_b.sum())
    total_pixels = int(edge_a.size)
    matched_edge_pixels_a = int(matched_a.sum())
    matched_edge_pixels_b = int(matched_b.sum())
    unmatched_edge_pixels_a = int(unmatched_a.sum())
    unmatched_edge_pixels_b = int(unmatched_b.sum())

    if edge_pixels_a == 0 and edge_pixels_b == 0:
        precision = recall = f1 = 1.0
    else:
        precision = float(matched_edge_pixels_b / edge_pixels_b) if edge_pixels_b else 0.0
        recall = float(matched_edge_pixels_a / edge_pixels_a) if edge_pixels_a else 0.0
        f1 = float(2 * precision * recall / (precision + recall)) if (precision + recall) else 0.0

    dist_a_to_b = _distance_stats(edge_a, edge_b)
    dist_b_to_a = _distance_stats(edge_b, edge_a)
    max_dist_candidates = [v for v in (dist_a_to_b["max"], dist_b_to_a["max"]) if v is not None]
    p95_candidates = [v for v in (dist_a_to_b["p95"], dist_b_to_a["p95"]) if v is not None]

    grad_delta = np.abs(grad_a - grad_b)
    edge_delta_for_regions = np.uint8(np.where(edge_changed_mask, np.clip(grad_delta, 0, 255), 0))
    edge_regions = _find_regions(edge_delta_for_regions, edge_changed_mask, config.edge_region_min_area)

    metrics = {
        "method": "Sobel luminance edges via scipy.ndimage.sobel; matching allows configurable dilation tolerance",
        "edge_threshold": float(config.edge_threshold),
        "edge_dilation_radius_px": int(config.edge_dilation_radius),
        "edge_pixels_a": edge_pixels_a,
        "edge_pixels_b": edge_pixels_b,
        "edge_pixel_ratio_a": float(edge_pixels_a / total_pixels) if total_pixels else 0.0,
        "edge_pixel_ratio_b": float(edge_pixels_b / total_pixels) if total_pixels else 0.0,
        "matched_edge_pixels_a": matched_edge_pixels_a,
        "matched_edge_pixels_b": matched_edge_pixels_b,
        "unmatched_edge_pixels_a": unmatched_edge_pixels_a,
        "unmatched_edge_pixels_b": unmatched_edge_pixels_b,
        "edge_changed_pixels": int(edge_changed_mask.sum()),
        "edge_changed_ratio": float(edge_changed_mask.sum() / total_pixels) if total_pixels else 0.0,
        "edge_precision_b_to_a": precision,
        "edge_recall_a_to_b": recall,
        "edge_f1": f1,
        "distance_a_edges_to_b_edges_px": dist_a_to_b,
        "distance_b_edges_to_a_edges_px": dist_b_to_a,
        "hausdorff_distance_px": float(max(max_dist_candidates)) if max_dist_candidates else None,
        "robust_hausdorff_p95_px": float(max(p95_candidates)) if p95_candidates else None,
        "edge_region_count": len(edge_regions),
    }
    return metrics, edge_changed_mask, edge_regions


def _detect_object_regions(
    arr: np.ndarray,
    edge_mask: np.ndarray,
    config: CompareConfig,
) -> List[ObjectRegion]:
    """Extract object-like connected components and return numerical coordinates.

    This is deliberately dependency-light. It uses edges, dilation, hole filling, and
    connected components. It gives coordinates for visible objects/shapes/lines, not
    semantic labels such as "cat" or "button".
    """
    if not config.include_object_coordinates:
        return []

    luma = _rgb_to_luma(arr)
    component_mask = _dilate_bool(edge_mask, int(config.object_edge_dilation_radius))
    component_mask = ndimage.binary_fill_holes(component_mask)
    labeled, count = ndimage.label(component_mask, structure=np.ones((3, 3), dtype=np.uint8))
    if count == 0:
        return []

    slices = ndimage.find_objects(labeled)
    objects: List[ObjectRegion] = []
    for idx, slc in enumerate(slices, start=1):
        if slc is None:
            continue
        region_mask = labeled[slc] == idx
        area = int(region_mask.sum())
        if area < int(config.object_min_area):
            continue

        y_slice, x_slice = slc
        y1, y2 = int(y_slice.start), int(y_slice.stop)
        x1, x2 = int(x_slice.start), int(x_slice.stop)
        width = int(x2 - x1)
        height = int(y2 - y1)
        cy_local, cx_local = ndimage.center_of_mass(region_mask.astype(np.float64))
        if math.isnan(cx_local) or math.isnan(cy_local):
            cx = float(x1 + width / 2.0)
            cy = float(y1 + height / 2.0)
        else:
            cx = float(x1 + cx_local)
            cy = float(y1 + cy_local)

        edge_pixels = int(edge_mask[slc][region_mask].sum())
        objects.append(
            ObjectRegion(
                id=len(objects) + 1,
                bbox_xyxy=(x1, y1, x2, y2),
                bbox_cxcywh=(float(x1 + width / 2.0), float(y1 + height / 2.0), width, height),
                centroid_xy=(cx, cy),
                area_pixels=area,
                edge_pixels=edge_pixels,
                edge_density=float(edge_pixels / area) if area else 0.0,
                mean_luma=float(luma[slc][region_mask].mean()) if area else 0.0,
            )
        )

    objects.sort(key=lambda obj: obj.area_pixels, reverse=True)
    objects = objects[: int(config.max_objects)]
    for i, obj in enumerate(objects, start=1):
        obj.id = i
    return objects


def _make_signed_residual_image(delta_signed: np.ndarray, gain: float) -> Image.Image:
    """Visualize signed residuals around neutral gray.

    128 means no residual. Values above 128 mean A is brighter than B in that
    channel; values below 128 mean B is brighter than A.
    """
    residual_vis = np.clip(128.0 + delta_signed.astype(np.float64) * float(gain), 0, 255)
    return Image.fromarray(residual_vis.astype(np.uint8), mode="RGB")


def _save_outputs(
    a_img: Image.Image,
    b_img: Image.Image,
    delta_signed: np.ndarray,
    delta_abs: np.ndarray,
    delta_mag: np.ndarray,
    mask: np.ndarray,
    regions: Sequence[DifferenceRegion],
    edge_a: np.ndarray,
    edge_b: np.ndarray,
    edge_changed_mask: np.ndarray,
    edge_regions: Sequence[DifferenceRegion],
    objects_a: Sequence[ObjectRegion],
    objects_b: Sequence[ObjectRegion],
    config: CompareConfig,
) -> Dict[str, str]:
    if not config.make_outputs:
        return {}

    output_dir = Path(config.output_dir or os.getcwd())
    output_dir.mkdir(parents=True, exist_ok=True)
    prefix = config.output_prefix

    diff_abs = np.uint8(np.clip(delta_abs, 0, 255))
    # Enhance subtle differences for easy human/agent inspection.
    diff_img = Image.fromarray(diff_abs, mode="RGB")
    diff_enhanced = ImageEnhance.Contrast(diff_img).enhance(2.5)
    heatmap = _make_heatmap(delta_mag)
    overlay = _make_overlay(a_img, mask, rgba=(255, 0, 0, 140))
    boxes = _draw_region_boxes(overlay, regions)
    mask_img = Image.fromarray(np.where(mask, 255, 0).astype(np.uint8), mode="L")

    signed_residual = _make_signed_residual_image(delta_signed, config.residual_visual_gain)
    positive_residual = np.max(np.maximum(delta_signed, 0), axis=2).astype(np.uint8)
    negative_residual = np.max(np.maximum(-delta_signed, 0), axis=2).astype(np.uint8)
    positive_heatmap = _make_heatmap(positive_residual)
    negative_heatmap = _make_heatmap(negative_residual)

    edge_a_img = Image.fromarray(np.where(edge_a, 255, 0).astype(np.uint8), mode="L")
    edge_b_img = Image.fromarray(np.where(edge_b, 255, 0).astype(np.uint8), mode="L")
    edge_diff_img = Image.fromarray(np.where(edge_changed_mask, 255, 0).astype(np.uint8), mode="L")
    edge_overlay = _make_overlay(a_img, edge_changed_mask, rgba=(255, 128, 0, 160))
    edge_boxes = _draw_region_boxes(edge_overlay, edge_regions)

    object_boxes_a = _draw_object_boxes(a_img, objects_a)
    object_boxes_b = _draw_object_boxes(b_img, objects_b)

    outputs = {
        "normalized_a": str(output_dir / f"{prefix}_a_normalized.png"),
        "normalized_b": str(output_dir / f"{prefix}_b_normalized.png"),
        "abs_diff": str(output_dir / f"{prefix}_abs_diff.png"),
        "heatmap": str(output_dir / f"{prefix}_heatmap.png"),
        "mask": str(output_dir / f"{prefix}_mask.png"),
        "overlay": str(output_dir / f"{prefix}_overlay.png"),
        "regions": str(output_dir / f"{prefix}_regions.png"),
        "signed_residual": str(output_dir / f"{prefix}_signed_residual.png"),
        "positive_residual_heatmap_a_brighter": str(output_dir / f"{prefix}_positive_residual_heatmap_a_brighter.png"),
        "negative_residual_heatmap_b_brighter": str(output_dir / f"{prefix}_negative_residual_heatmap_b_brighter.png"),
        "edge_a": str(output_dir / f"{prefix}_edge_a.png"),
        "edge_b": str(output_dir / f"{prefix}_edge_b.png"),
        "edge_diff": str(output_dir / f"{prefix}_edge_diff.png"),
        "edge_overlay": str(output_dir / f"{prefix}_edge_overlay.png"),
        "edge_regions": str(output_dir / f"{prefix}_edge_regions.png"),
        "object_boxes_a": str(output_dir / f"{prefix}_object_boxes_a.png"),
        "object_boxes_b": str(output_dir / f"{prefix}_object_boxes_b.png"),
    }

    a_img.save(outputs["normalized_a"])
    b_img.save(outputs["normalized_b"])
    diff_enhanced.save(outputs["abs_diff"])
    heatmap.save(outputs["heatmap"])
    mask_img.save(outputs["mask"])
    overlay.save(outputs["overlay"])
    boxes.save(outputs["regions"])
    signed_residual.save(outputs["signed_residual"])
    positive_heatmap.save(outputs["positive_residual_heatmap_a_brighter"])
    negative_heatmap.save(outputs["negative_residual_heatmap_b_brighter"])
    edge_a_img.save(outputs["edge_a"])
    edge_b_img.save(outputs["edge_b"])
    edge_diff_img.save(outputs["edge_diff"])
    edge_overlay.save(outputs["edge_overlay"])
    edge_boxes.save(outputs["edge_regions"])
    object_boxes_a.save(outputs["object_boxes_a"])
    object_boxes_b.save(outputs["object_boxes_b"])
    return outputs


def _decide(
    exact: bool,
    changed_ratio: float,
    mae: float,
    ssim: float,
    edge_f1: float,
    edge_changed_ratio: float,
    config: CompareConfig,
) -> Decision:
    if exact:
        return "same"
    pixel_same = (
        changed_ratio <= config.same_changed_ratio_max
        and mae <= config.same_mae_max
        and ssim >= config.same_ssim_min
    )
    edge_same = (
        edge_f1 >= config.same_edge_f1_min
        and edge_changed_ratio <= config.same_edge_changed_ratio_max
    )
    if pixel_same and edge_same:
        return "same"

    pixel_similar = (
        changed_ratio <= config.similar_changed_ratio_max
        and mae <= config.similar_mae_max
        and ssim >= config.similar_ssim_min
    )
    edge_similar = (
        edge_f1 >= config.similar_edge_f1_min
        and edge_changed_ratio <= config.similar_edge_changed_ratio_max
    )
    if pixel_similar and edge_similar:
        return "similar"
    return "different"


def _explain(result: VisualDiffResult) -> str:
    if result.is_exact_match:
        return "The normalized images are pixel-identical. Treat them as the same."

    size_note = (
        "Original image sizes are the same."
        if result.same_size
        else f"Original image sizes differ: {result.image_a_size} vs {result.image_b_size}."
    )
    region_note = (
        f"Detected {len(result.regions)} meaningful changed pixel region(s)."
        if result.regions
        else "No meaningful changed pixel regions survived the minimum-area filter."
    )
    edge_note = (
        f"Edge comparison: F1={result.edge_metrics.get('edge_f1', 0.0):.6f}, "
        f"changed_edge_ratio={result.edge_metrics.get('edge_changed_ratio', 0.0):.6%}, "
        f"edge_regions={len(result.edge_regions)}."
    )
    object_note = (
        f"Object-like component coordinates: A={len(result.objects_a)}, B={len(result.objects_b)}."
    )

    if result.decision == "same":
        verdict = "Pixel residuals and edge/shape differences are below the configured same-image thresholds."
    elif result.decision == "similar":
        verdict = "Images are not identical, but residuals and edge/shape differences are small enough to call them visually similar."
    else:
        verdict = "Pixel residuals or edge/shape differences exceed the configured similarity thresholds. Treat them as different."

    psnr_text = "infinite" if result.psnr_db is None else f"{result.psnr_db:.2f} dB"
    residual_p95 = result.residual.get("global", {}).get("p95_abs", 0.0)
    return (
        f"{verdict} {size_note} Changed pixels: {result.changed_pixels}/"
        f"{result.total_pixels} ({result.changed_pixel_ratio:.6%}); MAE={result.mae:.4f}; "
        f"RMSE={result.rmse:.4f}; max_delta={result.max_delta}; residual_p95_abs={residual_p95:.4f}; "
        f"PSNR={psnr_text}; SSIM={result.ssim:.6f}. {edge_note} {region_note} {object_note}"
    )


def compare_images(
    image_a_path: str | Path,
    image_b_path: str | Path,
    config: Optional[CompareConfig] = None,
) -> VisualDiffResult:
    """Compare two images and return an agent-friendly result.

    Parameters
    ----------
    image_a_path, image_b_path:
        Input image paths.
    config:
        CompareConfig controlling thresholds, size policy, edge comparison,
        object-coordinate extraction, and output images.

    Returns
    -------
    VisualDiffResult
        Structured metrics, residuals, edge metrics, decision, regions, object
        coordinates, and output file paths.
    """
    started_perf = time.perf_counter()
    started_at = datetime.now(timezone.utc).isoformat()
    config = config or CompareConfig()
    _validate_config(config)

    input_a_info = _file_info(image_a_path)
    input_b_info = _file_info(image_b_path)

    a_raw = _load_image(image_a_path)
    b_raw = _load_image(image_b_path)
    _guard_image_size("image_a", a_raw, config)
    _guard_image_size("image_b", b_raw, config)
    a_img, b_img, original_a_size, original_b_size = _prepare_images(a_raw, b_raw, config)
    _guard_image_size("compared canvas", a_img, config)

    a_arr = np.asarray(a_img, dtype=np.uint8)
    b_arr = np.asarray(b_img, dtype=np.uint8)

    exact = bool(np.array_equal(a_arr, b_arr))
    same_size = bool(original_a_size == original_b_size)

    delta_signed = a_arr.astype(np.int16) - b_arr.astype(np.int16)
    delta_abs = np.abs(delta_signed).astype(np.uint8)
    delta_mag = np.max(delta_abs, axis=2).astype(np.uint8)
    mask = delta_mag > int(config.diff_threshold)

    changed_pixels = int(mask.sum())
    total_pixels = int(mask.size)
    changed_ratio = float(changed_pixels / total_pixels) if total_pixels else 0.0

    mae = float(np.mean(delta_abs)) if delta_abs.size else 0.0
    mse = float(np.mean(delta_signed.astype(np.float64) ** 2)) if delta_signed.size else 0.0
    rmse = float(math.sqrt(mse))
    max_delta = int(delta_abs.max()) if delta_abs.size else 0
    psnr_db = _psnr(mse)
    ssim = _compute_ssim_luma(a_arr, b_arr, sigma=config.ssim_window_sigma)

    residual = _residual_summary(delta_signed, delta_abs)

    grad_a, edge_a = _compute_edge_mask(a_arr, config.edge_threshold)
    grad_b, edge_b = _compute_edge_mask(b_arr, config.edge_threshold)
    edge_metrics, edge_changed_mask, edge_regions = _edge_metrics(edge_a, edge_b, grad_a, grad_b, config)

    objects_a = _detect_object_regions(a_arr, edge_a, config)
    objects_b = _detect_object_regions(b_arr, edge_b, config)

    regions = _find_regions(delta_mag, mask, config.region_min_area)
    output_files = _save_outputs(
        a_img,
        b_img,
        delta_signed,
        delta_abs,
        delta_mag,
        mask,
        regions,
        edge_a,
        edge_b,
        edge_changed_mask,
        edge_regions,
        objects_a,
        objects_b,
        config,
    )

    decision = _decide(
        exact,
        changed_ratio,
        mae,
        ssim,
        float(edge_metrics["edge_f1"]),
        float(edge_metrics["edge_changed_ratio"]),
        config,
    )

    elapsed_ms = round((time.perf_counter() - started_perf) * 1000.0, 3)
    audit = {
        "skill_name": "visual-diff-skill",
        "skill_version": __version__,
        "generated_at_utc": started_at,
        "elapsed_ms": elapsed_ms,
        "platform": platform.platform(),
        "dependencies": _dependency_versions(),
        "inputs": {
            "image_a": {**input_a_info, "original_size": original_a_size},
            "image_b": {**input_b_info, "original_size": original_b_size},
        },
        "normalized": {
            "size_policy": config.size_policy,
            "alpha_background": config.alpha_background,
            "compared_size": a_img.size,
        },
    }

    result = VisualDiffResult(
        decision=decision,
        is_exact_match=exact,
        same_size=same_size,
        image_a_size=original_a_size,
        image_b_size=original_b_size,
        compared_size=a_img.size,
        changed_pixels=changed_pixels,
        total_pixels=total_pixels,
        changed_pixel_ratio=changed_ratio,
        mae=mae,
        mse=mse,
        rmse=rmse,
        max_delta=max_delta,
        psnr_db=psnr_db,
        ssim=ssim,
        residual=residual,
        edge_metrics=edge_metrics,
        regions=regions,
        edge_regions=edge_regions,
        objects_a=objects_a,
        objects_b=objects_b,
        output_files=output_files,
        config=_json_safe(dataclasses.asdict(config)),
        audit=_json_safe(audit),
        explanation="",
    )
    result.explanation = _explain(result)
    return result


def _parse_rgb(value: str) -> Tuple[int, int, int]:
    parts = value.split(",")
    if len(parts) != 3:
        raise argparse.ArgumentTypeError("RGB must be formatted as R,G,B")
    try:
        rgb = tuple(int(p.strip()) for p in parts)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("RGB values must be integers") from exc
    if any(v < 0 or v > 255 for v in rgb):
        raise argparse.ArgumentTypeError("RGB values must be in 0..255")
    return rgb  # type: ignore[return-value]


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Compare two images visually and emit an agent-friendly JSON report."
    )
    parser.add_argument("image_a", help="First image path")
    parser.add_argument("image_b", help="Second image path")
    parser.add_argument("--size-policy", choices=["strict", "pad", "resize"], default="pad")
    parser.add_argument("--alpha-background", type=_parse_rgb, default=(255, 255, 255), help="RGB background for alpha compositing, e.g. 255,255,255")
    parser.add_argument("--diff-threshold", type=int, default=8, help="Per-pixel channel delta threshold for changed-pixel mask")
    parser.add_argument("--region-min-area", type=int, default=12, help="Minimum connected changed-region area in pixels")
    parser.add_argument("--output-dir", default="visual_diff_output", help="Directory for generated artifacts")
    parser.add_argument("--output-prefix", default="visual_diff", help="Output filename prefix")
    parser.add_argument("--no-images", action="store_true", help="Do not write visual output images")
    parser.add_argument("--json-out", default=None, help="Optional path to write the JSON report")

    parser.add_argument("--same-changed-ratio-max", type=float, default=0.0005)
    parser.add_argument("--same-mae-max", type=float, default=0.5)
    parser.add_argument("--same-ssim-min", type=float, default=0.998)
    parser.add_argument("--similar-changed-ratio-max", type=float, default=0.02)
    parser.add_argument("--similar-mae-max", type=float, default=4.0)
    parser.add_argument("--similar-ssim-min", type=float, default=0.96)

    parser.add_argument("--edge-threshold", type=float, default=40.0, help="Sobel luminance gradient threshold for edge detection")
    parser.add_argument("--edge-dilation-radius", type=int, default=1, help="Pixel tolerance radius for matching edges")
    parser.add_argument("--edge-region-min-area", type=int, default=8, help="Minimum connected unmatched-edge region area")
    parser.add_argument("--same-edge-f1-min", type=float, default=0.995)
    parser.add_argument("--same-edge-changed-ratio-max", type=float, default=0.001)
    parser.add_argument("--similar-edge-f1-min", type=float, default=0.94)
    parser.add_argument("--similar-edge-changed-ratio-max", type=float, default=0.025)

    parser.add_argument("--object-min-area", type=int, default=20, help="Minimum object-like component area in pixels")
    parser.add_argument("--object-edge-dilation-radius", type=int, default=3, help="Dilation radius used before object-like component extraction")
    parser.add_argument("--max-objects", type=int, default=50, help="Maximum object-like components to return per image")
    parser.add_argument("--no-object-coordinates", action="store_true", help="Disable object-like coordinate extraction")

    parser.add_argument("--residual-visual-gain", type=float, default=1.0, help="Gain for signed residual visualization around neutral gray")
    parser.add_argument("--max-pixels", type=int, default=80_000_000, help="Maximum pixels allowed for each input and compared canvas")
    parser.add_argument("--fail-on", choices=["never", "different", "similar-or-different"], default="never", help="Return exit code 1 when the decision meets this condition; useful for CI")
    parser.add_argument("--quiet", action="store_true", help="Do not print JSON to stdout; still writes --json-out when provided")
    parser.add_argument("--version", action="version", version=f"visual-diff-skill {__version__}")
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_arg_parser()
    args = parser.parse_args(argv)

    config = CompareConfig(
        size_policy=args.size_policy,
        alpha_background=args.alpha_background,
        diff_threshold=args.diff_threshold,
        region_min_area=args.region_min_area,
        same_changed_ratio_max=args.same_changed_ratio_max,
        same_mae_max=args.same_mae_max,
        same_ssim_min=args.same_ssim_min,
        similar_changed_ratio_max=args.similar_changed_ratio_max,
        similar_mae_max=args.similar_mae_max,
        similar_ssim_min=args.similar_ssim_min,
        edge_threshold=args.edge_threshold,
        edge_dilation_radius=args.edge_dilation_radius,
        edge_region_min_area=args.edge_region_min_area,
        same_edge_f1_min=args.same_edge_f1_min,
        same_edge_changed_ratio_max=args.same_edge_changed_ratio_max,
        similar_edge_f1_min=args.similar_edge_f1_min,
        similar_edge_changed_ratio_max=args.similar_edge_changed_ratio_max,
        object_min_area=args.object_min_area,
        object_edge_dilation_radius=args.object_edge_dilation_radius,
        max_objects=args.max_objects,
        include_object_coordinates=not args.no_object_coordinates,
        residual_visual_gain=args.residual_visual_gain,
        make_outputs=not args.no_images,
        output_dir=args.output_dir,
        output_prefix=args.output_prefix,
        max_pixels=args.max_pixels,
    )

    try:
        result = compare_images(args.image_a, args.image_b, config)
    except VisualDiffError as exc:
        print(json.dumps({"error": str(exc)}, indent=2), flush=True)
        return 2

    data = result.to_dict()
    text = json.dumps(data, indent=2)
    if not args.quiet:
        print(text, flush=True)

    if args.json_out:
        out_path = Path(args.json_out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(text + "\n", encoding="utf-8")

    if args.fail_on == "different" and result.decision == "different":
        return 1
    if args.fail_on == "similar-or-different" and result.decision != "same":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
