from pathlib import Path
import numpy as np
import pytest

from napari_allencell_annotator.util.image_utils import ImageUtils


def test_get_dask_data_tiff() -> None:
    # ACT
    test_image = ImageUtils(Path("napari_allencell_annotator/_tests/assets/image_types/test_img.ome.tiff")).get_dask_data()

    # ASSERT
    assert (test_image == np.array([[[0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0]]])).all()


def test_get_dask_data_tif() -> None:
    # ACT
    test_image = ImageUtils(Path("napari_allencell_annotator/_tests/assets/image_types/test_img.ome.tif")).get_dask_data()

    # ASSERT
    assert (test_image == np.array([[[0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0]]])).all()

