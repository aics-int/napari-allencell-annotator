from pathlib import Path
import napari_allencell_annotator
import pytest

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


@pytest.fixture()
def files_widget() -> FilesWidget:
    return FilesWidget()


def test_update_shuff_text_checked(images_view: ImagesView) -> None:
    # ACT
    images_view._update_shuff_text(True)

    # ASSERT
    assert images_view.shuffle.text() == "Unhide"


def test_update_shuff_text_unchecked(images_view) -> None:
    # ACT
    images_view._update_shuff_text(False)

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


def test_enable_delete_buttons(images_view: ImagesView) -> None:
    # ACT
    images_view._enable_delete_button()

    # ASSERT
    assert images_view.delete.toolTip() == "Check box on the right \n to select files for deletion"
    assert images_view.delete.text() == "Delete All"
    assert images_view.delete.isEnabled()


def test_disable_delete_buttons(images_view: ImagesView) -> None:
    # ACT
    images_view._disable_delete_button()

    # ASSERT
    assert images_view.delete.toolTip() == ""
    assert not images_view.delete.isEnabled()


def test_enable_shuffle_buttons(images_view: ImagesView) -> None:
    # ACT
    images_view._enable_shuffle_button()

    # ASSERT
    assert images_view.shuffle.isEnabled()


def test_disable_shuffle_buttons(images_view: ImagesView) -> None:
    # ACT
    images_view._disable_shuffle_button()

    # ASSERT
    assert not images_view.shuffle.isEnabled()


def test_handle_files_added_when_file_added(images_view: ImagesView) -> None:
    # ACT
    images_view._handle_files_added(True)

    # ASSERT
    assert images_view.delete.toolTip() == "Check box on the right \n to select files for deletion"
    assert images_view.delete.text() == "Delete All"
    assert images_view.delete.isEnabled()
    assert images_view.shuffle.isEnabled()


def test_handle_files_added_when_no_file_added(images_view: ImagesView) -> None:
    # ACT
    images_view._handle_files_added(False)

    # ASSERT
    assert images_view.delete.toolTip() == ""
    assert not images_view.delete.isEnabled()
    assert not images_view.shuffle.isEnabled()


def test_display_img_stop_display(images_view: ImagesView, files_widget: FilesWidget) -> None:
    # ARRANGE
    test_previous_file: Path = Path(napari_allencell_annotator.__file__).parent / "_tests" / "assets" / "test_img1.tiff"
    test_previous_file_item: FileItem = FileItem(test_previous_file, files_widget, False)

    # ACT
    images_view._display_img(current=None, previous=test_previous_file_item)

    # ASSERT
    assert len(images_view.viewer.get_layers()) == 0
    assert test_previous_file_item.label.styleSheet() == """QLabel{}"""


# TODO: Implement after merging bioio, FakeImageUtils
def test_display_img_start_display(images_view: ImagesView, files_widget: FilesWidget) -> None:
    # ARRANGE
    test_current_file: Path = Path(napari_allencell_annotator.__file__).parent / "_tests" / "assets" / "test_img1.tiff"
    test_current_file_item: FileItem = FileItem(test_current_file, files_widget, False)
    pass


# TODO: Implement after merging bioio, FakeImageUtils
def test_display_img_change_image(images_view: ImagesView, files_widget: FilesWidget) -> None:
    # ARRANGE
    test_previous_file: Path = Path(napari_allencell_annotator.__file__).parent / "_tests" / "assets" / "test_img1.tiff"
    test_previous_file_item: FileItem = FileItem(test_previous_file, files_widget, False)

    test_current_file: Path = Path(napari_allencell_annotator.__file__).parent / "_tests" / "assets" / "test_img1.tiff"
    test_current_file_item: FileItem = FileItem(test_current_file, files_widget, False)
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
    images_view._add_selected_dir_to_ui(empty_dir)

    # ASSERT
    assert len(images_view.viewer.alerts) == 1
    assert images_view.viewer.alerts[-1] == "Folder is empty"
    assert annotator_model.get_num_images() == 0


def test_add_selected_dir_to_ui_non_empty_dir(images_view: ImagesView, annotator_model: AnnotatorModel):
    # ARRANGE
    img_dir: Path = Path(napari_allencell_annotator.__file__).parent / "_tests" / "assets" / "valid_img_dir"

    # ACT
    images_view._add_selected_dir_to_ui(img_dir)

    # ASSERT
    assert len(images_view.viewer.alerts) == 0
    assert annotator_model.get_num_images() == 2
    assert annotator_model.get_all_images()[0] == img_dir / "test_img1.tiff"
    assert annotator_model.get_all_images()[1] == img_dir / "test_img2.tiff"


def test_add_new_item(images_view: ImagesView, annotator_model: AnnotatorModel) -> None:
    # ARRANGE
    test_file: Path = Path(napari_allencell_annotator.__file__).parent / "_tests" / "assets" / "test_img1.tiff"
    assert annotator_model.get_num_images() == 0

    # ACT
    images_view.add_new_item(test_file)

    # ASSERT
    assert annotator_model.get_num_images() == 1
    assert annotator_model.get_all_images()[annotator_model.get_num_images() - 1] == test_file
    assert images_view.shuffle.isEnabled()
    assert images_view.delete.isEnabled()
    assert images_view.num_files_label.text() == "Image files: 1"


def test_add_selected_files_invalid_files(images_view: ImagesView, annotator_model: AnnotatorModel) -> None:
    # ACT
    images_view._add_selected_files(
        [
            Path(napari_allencell_annotator.__file__).parent / "_tests" / "assets" / "invalid_img_dir" / "test_dir",
            Path(napari_allencell_annotator.__file__).parent / "_tests" / "assets" / "invalid_img_dir" / ".test.csv",
        ]
    )

    # ASSERT
    assert len(images_view.viewer.alerts) == 0
    assert annotator_model.get_num_images() == 0


def test_add_selected_files_unsupported_files(images_view: ImagesView, annotator_model: AnnotatorModel) -> None:
    # ACT
    images_view._add_selected_files(
        [Path(napari_allencell_annotator.__file__).parent / "_tests" / "assets" / "invalid_img_dir" / "test.csv"]
    )

    # ASSERT
    assert len(images_view.viewer.alerts) == 1
    assert images_view.viewer.alerts[-1] == "Unsupported file type(s)"
    assert annotator_model.get_num_images() == 0


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


# TODO: Implement after shuffle refactoring
def test_handle_shuffle_clicked_checked(images_view: ImagesView):
    pass


def test_handle_shuffle_clicked_unchecked(images_view: ImagesView) -> None:
    # ARRANGE
    test_previous_file: Path = Path(napari_allencell_annotator.__file__).parent / "_tests" / "assets" / "test_img1.tiff"
    test_previous_file_item: FileItem = FileItem(test_previous_file, images_view.file_widget, False)

    # ACT
    images_view._handle_shuffle_clicked(False)

    # ASSERT
    assert not images_view.file_widget._shuffled
    for i in range(images_view.file_widget.count()):
        assert images_view.file_widget.item(i).label.text() == images_view.file_widget.item(i)._make_display_name()
        assert not images_view.file_widget.item(i).check.isHidden()


def test_delete_checked(images_view: ImagesView, annotator_model: AnnotatorModel) -> None:
    # ARRANGE
    test_file_1: Path = Path(napari_allencell_annotator.__file__).parent / "_tests" / "assets" / "test_img1.tiff"
    test_file_item_1: FileItem = FileItem(test_file_1, images_view.file_widget, False)

    test_file_2: Path = Path(napari_allencell_annotator.__file__).parent / "_tests" / "assets" / "test_img2.tiff"
    test_file_item_2: FileItem = FileItem(test_file_2, images_view.file_widget, False)

    images_view.file_widget.checked = {test_file_item_1, test_file_item_2}
    annotator_model.set_all_images([test_file_1, test_file_2])

    # ACT
    images_view.delete_checked()

    # ASSERT
    assert images_view.file_widget.count() == 0
    assert len(images_view.file_widget.checked) == 0
    assert annotator_model.get_num_images() == 0


def test_remove_image(images_view: ImagesView, annotator_model: AnnotatorModel) -> None:
    # ARRANGE
    test_file: Path = Path(napari_allencell_annotator.__file__).parent / "_tests" / "assets" / "test_img1.tiff"
    test_file_item: FileItem = FileItem(test_file, images_view.file_widget, False)
    annotator_model.set_all_images([test_file])

    # ACT
    images_view.remove_image(test_file_item)

    # ASSERT
    assert annotator_model.get_num_images() == 0
    assert images_view.file_widget.count() == 0


def test_clear_all(images_view: ImagesView, annotator_model: AnnotatorModel) -> None:
    # ARRANGE
    test_file: Path = Path(napari_allencell_annotator.__file__).parent / "_tests" / "assets" / "test_img1.tiff"
    test_file_item: FileItem = FileItem(test_file, images_view.file_widget, False)
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


def test_start_annotating_with_files(images_view: ImagesView) -> None:
    # ARRANGE
    test_file_1: Path = Path(napari_allencell_annotator.__file__).parent / "_tests" / "assets" / "test_img1.tiff"
    test_file_item_1: FileItem = FileItem(test_file_1, images_view.file_widget, False)

    test_file_2: Path = Path(napari_allencell_annotator.__file__).parent / "_tests" / "assets" / "test_img2.tiff"
    test_file_item_2: FileItem = FileItem(test_file_2, images_view.file_widget, False)

    # ACT
    images_view.start_annotating()

    # ASSERT
    for i in range(images_view.file_widget.count()):
        assert images_view.file_widget.item(i).check.isHidden()

    assert images_view.file_widget.currentItem() == test_file_item_1


def test_next_img(images_view: ImagesView) -> None:
    # ARRANGE
    test_file_1: Path = Path(napari_allencell_annotator.__file__).parent / "_tests" / "assets" / "test_img1.tiff"
    test_file_item_1: FileItem = FileItem(test_file_1, images_view.file_widget, False)

    test_file_2: Path = Path(napari_allencell_annotator.__file__).parent / "_tests" / "assets" / "test_img2.tiff"
    test_file_item_2: FileItem = FileItem(test_file_2, images_view.file_widget, False)

    images_view.file_widget.setCurrentItem(test_file_item_1)

    # ACT
    images_view.next_img()

    # ASSERT
    assert images_view.file_widget.currentItem() == test_file_item_2


def test_next_img_last_img(images_view: ImagesView) -> None:
    # ARRANGE
    test_file: Path = Path(napari_allencell_annotator.__file__).parent / "_tests" / "assets" / "test_img1.tiff"
    test_file_item: FileItem = FileItem(test_file, images_view.file_widget, False)
    images_view.file_widget.setCurrentItem(test_file_item)

    # ACT
    images_view.next_img()

    # ASSERT
    assert images_view.file_widget.currentItem() == test_file_item


def test_prev_img(images_view: ImagesView) -> None:
    # ARRANGE
    test_file_1: Path = Path(napari_allencell_annotator.__file__).parent / "_tests" / "assets" / "test_img1.tiff"
    test_file_item_1: FileItem = FileItem(test_file_1, images_view.file_widget, False)

    test_file_2: Path = Path(napari_allencell_annotator.__file__).parent / "_tests" / "assets" / "test_img2.tiff"
    test_file_item_2: FileItem = FileItem(test_file_2, images_view.file_widget, False)

    images_view.file_widget.setCurrentItem(test_file_item_2)

    # ACT
    images_view.prev_img()

    # ASSERT
    assert images_view.file_widget.currentItem() == test_file_item_1


def test_prev_img_first_img(images_view: ImagesView) -> None:
    # ARRANGE
    test_file: Path = Path(napari_allencell_annotator.__file__).parent / "_tests" / "assets" / "test_img1.tiff"
    test_file_item: FileItem = FileItem(test_file, images_view.file_widget, False)
    images_view.file_widget.setCurrentItem(test_file_item)

    # ACT
    images_view.prev_img()

    # ASSERT
    assert images_view.file_widget.currentItem() == test_file_item


def test_hide_image_paths(images_view: ImagesView, annotator_model: AnnotatorModel) -> None:
    # ACT
    images_view.hide_image_paths()

    # ASSERT
    assert images_view.input_dir.isHidden()
    assert images_view.input_file.isHidden()
    assert images_view.shuffle.isHidden()
    assert images_view.delete.isHidden()
