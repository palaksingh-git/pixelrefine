"""Individual OpenCV image processing steps."""

import cv2
import numpy as np


def to_grayscale(image: np.ndarray) -> np.ndarray:
    """Convert a BGR image to a single-channel grayscale image."""
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def remove_noise(image: np.ndarray, kernel_size: int = 5) -> np.ndarray:
    """Smooth a grayscale image with a square Gaussian kernel."""
    if kernel_size < 1 or kernel_size % 2 == 0:
        raise ValueError("kernel_size must be a positive odd integer")
    return cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)


def equalize(image: np.ndarray) -> np.ndarray:
    """Improve grayscale contrast with histogram equalization."""
    return cv2.equalizeHist(image)


def detect_edges(image: np.ndarray, low: int = 100, high: int = 200) -> np.ndarray:
    """Detect edges in a grayscale image using Canny thresholds."""
    if not 0 <= low < high <= 255:
        raise ValueError("Canny thresholds must satisfy 0 <= low < high <= 255")
    return cv2.Canny(image, low, high)
