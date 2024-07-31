from pathlib import Path
import numpy as np
import pytest

from napari_allencell_annotator.util.image_utils import ImageUtils


def test_get_dask_data() -> None:
    # ARRANGE
    test_dir: Path = Path("napari_allencell_annotator/_tests/assets/image_types/")

    for test_img_path in test_dir.glob("test_img.*"):
        # ACT
        test_image = ImageUtils(test_img_path).get_dask_data()

        # ASSERT
        assert np.allclose(test_image, np.array([[[0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0]]]))
