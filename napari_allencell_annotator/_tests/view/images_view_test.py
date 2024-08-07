from pathlib import Path
import napari_allencell_annotator
import pytest
from pytestqt import qtbot

from napari_allencell_annotator._tests.fakes.fake_viewer import FakeViewer
from napari_allencell_annotator.model.annotation_model import AnnotatorModel
from napari_allencell_annotator.view.images_view import ImagesView
from napari_allencell_annotator.widgets.files_widget import FilesWidget
from napari_allencell_annotator.widgets.file_item import FileItem


@pytest.fixture
def annotator_model() -> AnnotatorModel:
    return AnnotatorModel()


@pytest.fixture
def images_view(annotator_model, qtbot) -> ImagesView:
    return ImagesView(annotator_model, FakeViewer())


def test_update_shuff_text_checked(images_view: ImagesView) -> None:
    # ACT
    images_view._handle_shuffle_ui(True)

    # ASSERT
    assert images_view.shuffle.text() == "Unhide"


def test_update_shuff_text_unchecked(images_view) -> None:
    # ACT
    images_view._handle_shuffle_ui(False)

    # ASSERT
    assert images_view.shuffle.text() == "Shuffle and Hide"


def test_reset_buttons(images_view) -> None:
    # ACT
    images_view.reset_buttons()

    # ASSERT
    assert images_view.delete.text() == "Delete All"
    assert not images_view.shuffle.isChecked()
    assert images_view.delete.toolTip() == ""  # When tooltip is empty its an empty string
    assert not images_view.delete.isEnabled()
    assert not images_view.shuffle.isEnabled()
    assert images_view.input_dir.isEnabled()
    assert images_view.input_file.isEnabled()


def test_enable_add_buttons(images_view: ImagesView) -> None:
    # ACT
    images_view.enable_add_buttons()

    # ASSERT
    assert images_view.input_dir._input_btn.isEnabled()
    assert images_view.input_file._input_btn.isEnabled()


def test_disable_add_buttons(images_view: ImagesView) -> None:
    # ACT
    images_view.disable_add_buttons()

    # ASSERT
    assert not images_view.input_dir._input_btn.isEnabled()
    assert not images_view.input_file._input_btn.isEnabled()


def test_toggle_delete_button_text_checked(images_view: ImagesView) -> None:
    # ACT
    images_view._toggle_delete_button_text(True)

    # ASSERT
    assert images_view.delete.text() == "Delete Selected"


def test_toggle_delete_button_text_unchecked(images_view: ImagesView) -> None:
    # ACT
    images_view._toggle_delete_button_text(False)

    # ASSERT
    assert images_view.delete.text() == "Delete All"


# TODO: Implement after merging bioio, FakeImageUtils
def test_display_img_start_display(images_view: ImagesView) -> None:
    # ARRANGE
    test_current_file: Path = Path(napari_allencell_annotator.__file__).parent / "_tests" / "assets" / "test_img1.tiff"
    test_current_file_item: FileItem = FileItem(test_current_file, images_view.file_widget, False)
    pass


# TODO: Implement after merging bioio, FakeImageUtils
def test_display_img_change_image(images_view: ImagesView) -> None:
    # ARRANGE
    test_previous_file: Path = Path(napari_allencell_annotator.__file__).parent / "_tests" / "assets" / "test_img1.tiff"
    test_previous_file_item: FileItem = FileItem(test_previous_file, images_view.file_widget, False)

    test_current_file: Path = Path(napari_allencell_annotator.__file__).parent / "_tests" / "assets" / "test_img1.tiff"
    test_current_file_item: FileItem = FileItem(test_current_file, images_view.file_widget, False)
    pass


def test_update_num_files_label(images_view: ImagesView) -> None:
    # ACT
    images_view.update_num_files_label(1)

    # ASSERT
    assert images_view.num_files_label.text() == "Image files: 1"


def test_add_selected_dir_to_ui_empty_dir(images_view: ImagesView, annotator_model: AnnotatorModel) -> None:
    # ARRANGE
    empty_dir: Path = Path(napari_allencell_annotator.__file__).parent / "_tests" / "assets" / "empty_dir"

    # ACT
    images_view._add_sorted_valid_images_in_dir(empty_dir)

    # ASSERT
    assert len(images_view.viewer.alerts) == 1
    assert images_view.viewer.alerts[-1] == "Folder is empty"
    assert annotator_model.get_num_images() == 0


def test_add_selected_dir_to_ui_non_empty_dir(images_view: ImagesView, annotator_model: AnnotatorModel):
    # ARRANGE
    img_dir: Path = Path(napari_allencell_annotator.__file__).parent / "_tests" / "assets" / "valid_img_dir"

    # ACT
    images_view._add_sorted_valid_images_in_dir(img_dir)

    # ASSERT
    assert len(images_view.viewer.alerts) == 0
    assert annotator_model.get_num_images() == 2
    assert annotator_model.get_all_images()[0] == img_dir / "test_img1.tiff"
    assert annotator_model.get_all_images()[1] == img_dir / "test_img2.tiff"


def test_add_new_item(images_view: ImagesView, annotator_model: AnnotatorModel) -> None:
    # ARRANGE
    test_file: Path = Path(napari_allencell_annotator.__file__).parent / "_tests" / "assets" / "test_img1.tiff"

    # ACT
    images_view.add_new_item(test_file)

    # ASSERT
    assert annotator_model.get_num_images() == 1
    assert annotator_model.get_all_images()[annotator_model.get_num_images() - 1] == test_file
    assert images_view.file_widget.count() == 1
    assert images_view.file_widget.item(0).label.text() == "test_img1.tiff"


def test_add_selected_files_repeated_files(images_view: ImagesView, annotator_model: AnnotatorModel) -> None:
    # ARRANGE
    test_image_path: Path = Path(napari_allencell_annotator.__file__).parent / "_tests" / "assets" / "test_img1.tiff"

    # ACT
    images_view._add_selected_files([test_image_path])
    images_view._add_selected_files([test_image_path])

    # ASSERT
    assert annotator_model.get_num_images() == 1
    assert annotator_model.get_all_images()[0] == test_image_path


def test_add_selected_files_valid_files(images_view: ImagesView, annotator_model: AnnotatorModel) -> None:
    # ACT
    images_view._add_selected_files(
        [
            Path(napari_allencell_annotator.__file__).parent / "_tests" / "assets" / "valid_img_dir" / "test_img1.tiff",
            Path(napari_allencell_annotator.__file__).parent / "_tests" / "assets" / "valid_img_dir" / "test_img2.tiff",
        ]
    )

    # ASSERT
    assert len(images_view.viewer.alerts) == 0
    assert annotator_model.get_num_images() == 2
    assert (
        annotator_model.get_all_images()[0]
        == Path(napari_allencell_annotator.__file__).parent / "_tests" / "assets" / "valid_img_dir" / "test_img1.tiff"
    )
    assert (
        annotator_model.get_all_images()[1]
        == Path(napari_allencell_annotator.__file__).parent / "_tests" / "assets" / "valid_img_dir" / "test_img2.tiff"
    )


def test_handle_shuffle_clicked_toggled_on(images_view: ImagesView, annotator_model: AnnotatorModel):
    # ARRANGE
    test_previous_file: Path = Path(napari_allencell_annotator.__file__).parent / "_tests" / "assets" / "test_img1.tiff"

    # ACT
    annotator_model.set_shuffled_images([test_previous_file])

    # ASSERT
    assert len(annotator_model.get_shuffled_images()) == 1
    assert annotator_model.get_shuffled_images()[0] == test_previous_file


def test_handle_shuffle_clicked_toggled_off(images_view: ImagesView, annotator_model: AnnotatorModel) -> None:
    # ARRANGE
    test_previous_file: Path = Path(napari_allencell_annotator.__file__).parent / "_tests" / "assets" / "test_img1.tiff"
    annotator_model.set_shuffled_images([test_previous_file])

    # ACT
    images_view._handle_shuffle_clicked()

    # ASSERT
    assert annotator_model.get_shuffled_images() is None


def test_delete_checked(images_view: ImagesView, annotator_model: AnnotatorModel) -> None:
    # ARRANGE
    test_file_1: Path = Path(napari_allencell_annotator.__file__).parent / "_tests" / "assets" / "test_img1.tiff"
    test_file_2: Path = Path(napari_allencell_annotator.__file__).parent / "_tests" / "assets" / "test_img2.tiff"

    annotator_model.set_all_images([test_file_1, test_file_2])
    test_file_item_1: FileItem = images_view.file_widget.item(0)
    test_file_item_2: FileItem = images_view.file_widget.item(1)
    images_view.file_widget.checked = {test_file_item_1, test_file_item_2}
    assert annotator_model.get_num_images() == 2
    assert images_view.file_widget.count() == 2

    # ACT
    images_view.delete_checked()

    # ASSERT
    assert annotator_model.get_num_images() == 0
    assert images_view.file_widget.count() == 0


def test_remove_image(images_view: ImagesView, annotator_model: AnnotatorModel) -> None:
    # ARRANGE
    test_file: Path = Path(napari_allencell_annotator.__file__).parent / "_tests" / "assets" / "test_img1.tiff"

    annotator_model.set_all_images([test_file])
    test_file_item: FileItem = images_view.file_widget.item(0)

    # ACT
    images_view.remove_image(test_file_item)

    # ASSERT
    assert annotator_model.get_num_images() == 0
    assert images_view.file_widget.count() == 0


def test_clear_all(images_view: ImagesView, annotator_model: AnnotatorModel) -> None:
    # ARRANGE
    test_file: Path = Path(napari_allencell_annotator.__file__).parent / "_tests" / "assets" / "test_img1.tiff"
    annotator_model.set_all_images([test_file])

    # ACT
    images_view.clear_all()

    # ASSERT
    assert annotator_model.get_num_images() == 0
    assert images_view.file_widget.count() == 0


def test_start_annotating_no_files(images_view: ImagesView) -> None:
    # ACT
    images_view.start_annotating()

    # ASSERT
    assert len(images_view.viewer.alerts) == 1
    assert images_view.viewer.alerts[-1] == "No files to annotate"


def test_start_annotating_with_files(images_view: ImagesView, annotator_model: AnnotatorModel) -> None:
    # ARRANGE
    test_file_1: Path = Path(napari_allencell_annotator.__file__).parent / "_tests" / "assets" / "test_img1.tiff"
    test_file_2: Path = Path(napari_allencell_annotator.__file__).parent / "_tests" / "assets" / "test_img2.tiff"
    annotator_model.set_all_images([test_file_1, test_file_2])

    # ACT
    images_view.start_annotating()

    # ASSERT
    for i in range(images_view.file_widget.count()):
        assert images_view.file_widget.item(i).check.isHidden()


def test_hide_image_paths(images_view: ImagesView, annotator_model: AnnotatorModel) -> None:
    # ACT
    images_view.hide_image_paths()

    # ASSERT
    assert images_view.input_dir.isHidden()
    assert images_view.input_file.isHidden()
    assert images_view.shuffle.isHidden()
    assert images_view.delete.isHidden()


def test_handle_image_count_changed_some_images(images_view: ImagesView) -> None:
    # ACT
    images_view._handle_image_count_changed(1)

    # ASSERT
    assert images_view.shuffle.isEnabled()
    assert images_view.delete.toolTip() == "Check box on the right \n to select files for deletion"
    assert images_view.delete.text() == "Delete All"
    assert images_view.delete.isEnabled()


def test_handle_image_count_changed_no_images(images_view: ImagesView) -> None:
    # ACT
    images_view._handle_image_count_changed(0)

    # ASSERT
    assert images_view.delete.text() == "Delete All"
    assert not images_view.shuffle.isChecked()
    assert images_view.delete.toolTip() == ""
    assert not images_view.delete.isEnabled()
    assert not images_view.shuffle.isEnabled()
    assert images_view.input_dir.isEnabled()
    assert images_view.input_file.isEnabled()


# def test_stop_annotating(images_view):
#     # ARRANGE
#     test_file: Path = Path(napari_allencell_annotator.__file__).parent / "_tests" / "assets" / "test_img1.tiff"
#     test_file_item: FileItem = FileItem(test_file, images_view.file_widget, False)
#     assert images_view.file_widget.count() == 1
#
#     # ACT
#     images_view.stop_annotating()
#
#     # ASSERT
#     assert images_view.file_widget.count() == 0
