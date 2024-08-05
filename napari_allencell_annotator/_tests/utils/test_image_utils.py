from pathlib import Path
import numpy as np
from bioio import BioImage

import napari_allencell_annotator
from napari_allencell_annotator.util.image_utils import ImageUtils


def test_get_image_tiff() -> None:
    # ARRANGE
    test_path: Path = (
        Path(napari_allencell_annotator.__file__).parent / "_tests" / "assets" / "image_types" / "img.ome.tiff"
    )

    # ACT
    test_image: BioImage = ImageUtils(test_path).get_image()

    # ASSERT
    np.testing.assert_array_equal(test_image.get_dask_stack()[0, 0, :, :, :, :], np.zeros((2, 2, 2, 2)))
