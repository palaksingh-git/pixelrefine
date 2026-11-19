"""Basic shape and argument checks for the processing stages."""

import numpy as np
import pytest

from image_enhancement.processing import detect_edges, equalize, remove_noise, to_grayscale


def test_to_grayscale_returns_single_channel() -> None:
    image = np.zeros((12, 16, 3), dtype=np.uint8)
    grayscale = to_grayscale(image)
    assert grayscale.shape == (12, 16)
    assert grayscale.ndim == 2


def test_remove_noise_preserves_shape_and_rejects_even_kernel() -> None:
    image = np.zeros((12, 16), dtype=np.uint8)
    image[6, 8] = 255
    blurred = remove_noise(image)
    assert blurred.shape == image.shape
    assert blurred[6, 8] < image[6, 8]
    with pytest.raises(ValueError):
        remove_noise(image, kernel_size=4)


def test_equalize_preserves_single_channel_shape() -> None:
    image = np.tile(np.arange(16, dtype=np.uint8), (12, 1))
    equalized = equalize(image)
    assert equalized.shape == image.shape
    assert equalized.ndim == 2


@pytest.mark.parametrize("low, high", [(100, 100), (200, 100), (-1, 200), (100, 256)])
def test_detect_edges_shape_and_threshold_validation(low: int, high: int) -> None:
    image = np.zeros((12, 16), dtype=np.uint8)
    assert detect_edges(image).shape == image.shape
    with pytest.raises(ValueError):
        detect_edges(image, low, high)
