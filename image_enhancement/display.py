"""Matplotlib display of the input image and each processing result."""

import cv2
import matplotlib.pyplot as plt
import numpy as np


def show_images(
    original: np.ndarray,
    grayscale: np.ndarray,
    blurred: np.ndarray,
    equalized: np.ndarray,
    edges: np.ndarray,
) -> None:
    """Show all five pipeline stages side by side in one window."""
    images = [cv2.cvtColor(original, cv2.COLOR_BGR2RGB), grayscale, blurred, equalized, edges]
    titles = ["Original", "Grayscale", "Gaussian Blur", "Histogram Equalized", "Canny Edges"]
    figure, axes = plt.subplots(1, 5, figsize=(20, 5))
    for index, (axis, image, title) in enumerate(zip(axes, images, titles)):
        if index == 0:
            axis.imshow(image)
        else:
            axis.imshow(image, cmap="gray", vmin=0, vmax=255)
        axis.set_title(title)
        axis.axis("off")
    figure.tight_layout()
    plt.show()
