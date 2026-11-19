"""Select an image, run the enhancement pipeline, and display the results."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Sequence, TextIO

import cv2
import numpy as np

from display import show_images
from processing import detect_edges, equalize, remove_noise, to_grayscale


SUPPORTED_EXTENSIONS = {".bmp", ".jpeg", ".jpg", ".png", ".tif", ".tiff", ".webp"}
OUTPUT_DIR = Path(__file__).resolve().parent / "output"


def report(message: str, stream: TextIO = sys.stdout) -> None:
    """Print a message safely when a Windows console cannot encode a path."""
    encoding = stream.encoding or "utf-8"
    print(message.encode(encoding, errors="backslashreplace").decode(encoding), file=stream)


def select_image() -> Path | None:
    """Open a file dialog and return the selected path, or None on cancellation."""
    try:
        import tkinter as tk
        from tkinter import filedialog
    except ImportError as exc:
        raise RuntimeError("Tkinter is unavailable; pass an image with --image instead.") from exc

    try:
        root = tk.Tk()
    except tk.TclError as exc:
        raise RuntimeError("Could not open the file dialog; pass an image with --image instead.") from exc
    root.withdraw()
    try:
        selected = filedialog.askopenfilename(
            title="Select an image",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.bmp *.tif *.tiff *.webp"),
                ("All files", "*.*"),
            ],
        )
    except tk.TclError as exc:
        raise RuntimeError("The file dialog failed; pass an image with --image instead.") from exc
    finally:
        root.destroy()
    return Path(selected) if selected else None


def load_image(path: Path) -> np.ndarray:
    """Load a supported image as BGR, including paths with Unicode characters."""
    if not path.is_file():
        raise ValueError(f"Image path does not exist or is not a file: {path}")
    if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
        raise ValueError(f"Unsupported image file type: {path.suffix or '(none)'}")

    try:
        encoded = np.fromfile(str(path), dtype=np.uint8)
        image = cv2.imdecode(encoded, cv2.IMREAD_COLOR)
    except (OSError, cv2.error) as exc:
        raise ValueError(f"Could not read image: {path}") from exc
    if image is None:
        raise ValueError(f"Image failed to load (it may be corrupt or unsupported): {path}")
    return image


def save_results(image_path: Path, results: dict[str, np.ndarray]) -> None:
    """Write the four processed images as PNG files in the output folder."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for name, image in results.items():
        destination = OUTPUT_DIR / f"{image_path.stem}_{name}.png"
        success, encoded = cv2.imencode(".png", image)
        if not success:
            raise OSError(f"Could not encode image: {destination}")
        encoded.tofile(str(destination))
        report(f"Saved: {destination}")


def build_parser() -> argparse.ArgumentParser:
    """Create the command-line parser."""
    parser = argparse.ArgumentParser(description="Enhance and inspect an image with OpenCV.")
    parser.add_argument("--image", type=Path, help="Input image path; opens a file dialog if omitted")
    parser.add_argument("--kernel", type=int, default=5, help="Odd Gaussian kernel size (default: 5)")
    parser.add_argument("--low", type=int, default=100, help="Lower Canny threshold (default: 100)")
    parser.add_argument("--high", type=int, default=200, help="Upper Canny threshold (default: 200)")
    parser.add_argument("--no-save", action="store_true", help="Display results without saving them")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the image pipeline and return a process exit status."""
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.kernel < 1 or args.kernel % 2 == 0:
        parser.error("--kernel must be a positive odd integer")
    if not 0 <= args.low < args.high <= 255:
        parser.error("Canny thresholds must satisfy 0 <= --low < --high <= 255")

    try:
        image_path = args.image if args.image is not None else select_image()
        if image_path is None:
            report("No image selected; nothing to process.", sys.stderr)
            return 1

        original = load_image(image_path)
        grayscale = to_grayscale(original)
        blurred = remove_noise(grayscale, args.kernel)
        equalized = equalize(blurred)
        edges = detect_edges(equalized, args.low, args.high)
        results = {
            "grayscale": grayscale,
            "blurred": blurred,
            "equalized": equalized,
            "edges": edges,
        }
        if not args.no_save:
            save_results(image_path, results)
        show_images(original, grayscale, blurred, equalized, edges)
    except (OSError, RuntimeError, ValueError, cv2.error) as exc:
        report(f"Error: {exc}", sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
