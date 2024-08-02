from pathlib import Path

from napari_allencell_annotator.util.file_utils import FileUtils


def test_get_file_name():
    # ACT
    tiff_file_name: str = FileUtils.get_file_name(Path("parent/test.tiff"))
    png_file_name: str = FileUtils.get_file_name(Path("parent/test.png"))
    jpeg_file_name: str = FileUtils.get_file_name(Path("parent/test.jpeg"))
    czi_file_name: str = FileUtils.get_file_name(Path("parent/test.czi"))
    zarr_file_name: str = FileUtils.get_file_name(Path("parent/test.ome.zarr"))

    # ASSERT
    assert tiff_file_name == "test.tiff"
    assert png_file_name == "test.png"
    assert jpeg_file_name == "test.jpeg"
    assert czi_file_name == "test.czi"
    assert zarr_file_name == "parent"

