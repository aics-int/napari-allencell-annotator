from pathlib import Path
import numpy as np

import napari_allencell_annotator
from napari_allencell_annotator.util.image_utils import ImageUtils


def test_get_dask_data_tiff() -> None:
    # ARRANGE
    test_path: Path = (
        Path(napari_allencell_annotator.__file__).parent / "_tests" / "assets" / "image_types" / "img.ome.tiff"
    )

    # ACT
    test_image = ImageUtils(test_path).get_dask_data()

    # ASSERT
    np.testing.assert_array_equal(test_image[0, 0, :, :, :, :], np.zeros((2, 2, 2, 2)))
