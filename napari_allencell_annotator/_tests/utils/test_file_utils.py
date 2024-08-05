from pathlib import Path
from typing import List

from napari_allencell_annotator.util.file_utils import FileUtils
import napari_allencell_annotator


def test_sorted_dirs_and_files_in_dir():
    # ACT
    sorted_file_list: List[Path] = FileUtils.get_sorted_dirs_and_files_in_dir(
        Path(napari_allencell_annotator.__file__).parent / "_tests" / "assets" / "sort_img_dir"
    )

    # ASSERT
    assert sorted_file_list == [
        Path(napari_allencell_annotator.__file__).parent / "_tests" / "assets" / "sort_img_dir" / "a",
        Path(napari_allencell_annotator.__file__).parent / "_tests" / "assets" / "sort_img_dir" / "b.ome.tiff",
        Path(napari_allencell_annotator.__file__).parent / "_tests" / "assets" / "sort_img_dir" / "c.ome.tiff",
    ]


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
    zarr_file_name: str = FileUtils.get_file_name(Path("parent/test.ome.zarr"))

    # ASSERT
    assert tiff_file_name == "test.tiff"
    assert zarr_file_name == "parent"
