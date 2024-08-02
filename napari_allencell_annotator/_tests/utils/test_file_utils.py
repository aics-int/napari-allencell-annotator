from pathlib import Path
from typing import List

from napari_allencell_annotator.util.file_utils import FileUtils
import napari_allencell_annotator


def test_select_valid_images() -> None:
    # ARRANGE
    all_files: List[Path] = [
        Path("test.tiff"),
        Path("test.png"),
        Path("test.jpeg"),
        Path("test.czi"),
        Path("test/raw.ome.zarr"),
        Path("test.csv"),
        Path("test.json"),
        Path("valid_img_dir"),
        Path(napari_allencell_annotator.__file__).parent / "_tests" / "assets" / "zarr_dir",
    ]

    # ACT
    valid_files: List[Path] = FileUtils.select_valid_images(all_files)

    # ASSERT
    assert valid_files == [
        Path("test.tiff"),
        Path("test.png"),
        Path("test.jpeg"),
        Path("test.czi"),
        Path("test/raw.ome.zarr"),
        Path(napari_allencell_annotator.__file__).parent / "_tests" / "assets" / "zarr_dir" / "raw.ome.zarr",
    ]


def test_get_file_name() -> None:
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
