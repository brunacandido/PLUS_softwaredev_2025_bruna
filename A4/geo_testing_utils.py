"""
geo_testing_utils.py

I created this file because I'm interested in testing, and I wanted to start building
a test file to help validate parts of the project. These are the first utility functions
I wrote to make it easier to test the code, especially with raster data.

The idea is to start organizing tests early so we can make sure everything keeps working
even when we need to change or update parts of the project later on.

Author: Bruna Candido
"""

import os
import numpy as np
import rasterio
import matplotlib.pyplot as plt
from rasterio.transform import from_origin


def create_dummy_raster(path='test_files/dummy.tif', width=100, height=100, bands=3, value=128):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    data = np.full((bands, height, width), value, dtype='uint8')
    transform = from_origin(0, 0, 10, 10)

    with rasterio.open(
        path, 'w',
        driver='GTiff',
        height=height,
        width=width,
        count=bands,
        dtype='uint8',
        transform=transform,
        crs='EPSG:4326'
    ) as dst:
        dst.write(data)

    return path


def load_raster_as_numpy(path):
    with rasterio.open(path) as src:
        return src.read()


def validate_image_shape(image, expected_shape):
    return image.shape == expected_shape


def assert_no_nan(image):
    return not np.isnan(image).any()


def validate_pixel_range(image, min_value=0, max_value=255):
    return np.all((image >= min_value) & (image <= max_value))


def visualize_raster(image):
    if image.shape[0] < 3:
        raise ValueError("Need at least 3 bands to visualize as RGB")
    rgb = image[:3].transpose(1, 2, 0)
    plt.imshow(rgb.astype(np.uint8))
    plt.title("Raster RGB Visualization")
    plt.axis("off")
    plt.show()
