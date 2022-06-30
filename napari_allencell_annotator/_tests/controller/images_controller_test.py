from unittest import mock
from unittest.mock import MagicMock, create_autospec

from napari_allencell_annotator.controller.images_controller import ImagesController
from constants.constants import SUPPORTED_FILE_TYPES
import napari
import os


class TestImagesController:
    def setup_method(self):
        self._mock_viewer: MagicMock = create_autospec(napari.Viewer)
        with mock.patch("napari_allencell_annotator.controller.images_controller.ImagesView"):
            self._controller = ImagesController(self._mock_viewer)

    def test_shuffle_clicked_none(self):
        # test when list widget has no items
        self._controller.view.file_widget.clear_for_shuff = MagicMock()
        self._controller.view.toggle_add = MagicMock()
        self._controller.view.file_widget.add_item = MagicMock()
        self._controller._shuffle_clicked(True)
        self._controller.view.file_widget.clear_for_shuff.assert_called_once_with()
        self._controller.view.toggle_add.assert_called_once_with(False)
        self._controller.view.file_widget.add_item.assert_not_called()

        self._controller.view.file_widget.clear_for_shuff = MagicMock()
        self._controller.view.toggle_add = MagicMock()
        self._controller.view.file_widget.add_item = MagicMock()
        self._controller._shuffle_clicked(False)
        self._controller.view.file_widget.clear_for_shuff.assert_called_once_with()
        self._controller.view.toggle_add.assert_called_once_with(True)
        self._controller.view.file_widget.add_item.assert_not_called()

    def test_shuffle_clicked_one(self):
        # test when list widget has one item
        self._controller.view.file_widget.add_item = MagicMock()
        self._controller.view.file_widget.clear_for_shuff.return_value = ["file_1.png"]
        self._controller._shuffle_clicked(True)
        self._controller.view.file_widget.add_item.assert_called_once_with("file_1.png", hidden=True)

        self._controller.view.file_widget.add_item = MagicMock()
        self._controller._shuffle_clicked(False)
        self._controller.view.file_widget.add_item.assert_called_once_with("file_1.png", hidden=False)

    def test_shuffle_clicked_mult(self):
        # test when list widget has multiple items
        self._controller.view.file_widget.add_item = MagicMock()
        self._controller.view.file_widget.clear_for_shuff.return_value = ["file_1.png", "file_2.png", "file_3.png"]
        self._controller._shuffle_clicked(True)
        assert len(self._controller.view.file_widget.add_item.mock_calls) == len(
            self._controller.view.file_widget.clear_for_shuff.return_value)

    def test_is_supported(self):
        for file_type in SUPPORTED_FILE_TYPES:
            assert ImagesController.is_supported("path" + file_type)
        assert ImagesController.is_supported("path.ome.tiff")
        assert not ImagesController.is_supported("path")
        assert not ImagesController.is_supported("")
        assert not ImagesController.is_supported(".jpg")
        assert not ImagesController.is_supported("path.txt")
        assert not ImagesController.is_supported(None)

    def test_dir_selected_evt_empty_list(self):
        # test empty dir list
        self._controller.view.alert = MagicMock()
        self._controller._dir_selected_evt([])
        self._controller.view.alert.assert_called_once_with("No selection provided")

    def test_dir_selected_evt_none(self):
        # test None dir list
        self._controller.view.alert = MagicMock()
        self._controller._dir_selected_evt(None)
        self._controller.view.alert.assert_called_once_with("No selection provided")

    def test_dir_selected_evt_empty_dir(self):
        # test empty dir
        self._controller.view.alert = MagicMock()
        d = ["/some/path"]
        os.listdir = MagicMock(return_value=[])
        self._controller._dir_selected_evt(d)
        self._controller.view.alert.assert_called_once_with("Folder is empty")

    def test_dir_selected_evt_one_supp(self):
        # test for one file, is supported
        self._controller.view.alert = MagicMock()
        self._controller.is_supported = MagicMock(return_value=True)
        self._controller.view.file_widget.add_new_item = MagicMock()
        os.listdir = MagicMock(return_value=["file_1.jpg"])
        self._controller._dir_selected_evt(d)
        self._controller.view.alert.assert_not_called()
        self._controller.is_supported.assert_called_once_with("/some/path/file_1.jpg")
        self._controller.view.file_widget.add_new_item.assert_called_once_with("/some/path/file_1.jpg")

    def test_dir_selected_evt_one_not_supp(self):
        # test for one file, is not supported
        self._controller.view.alert = MagicMock()
        self._controller.is_supported = MagicMock(return_value=False)
        self._controller.view.file_widget.add_new_item = MagicMock()
        os.listdir = MagicMock(return_value=["file_1.jpg"])
        self._controller._dir_selected_evt(d)
        self._controller.view.alert.assert_called_once_with("Unsupported file type:/some/path/file_1.jpg")
        self._controller.is_supported.assert_called_once_with("/some/path/file_1.jpg")
        self._controller.view.file_widget.add_new_item.assert_not_called()

    def test_dir_selected_evt_mult(self):
        # test for one multiple files
        self._controller.view.alert = MagicMock()
        self._controller.is_supported = MagicMock(return_value=True)
        self._controller.view.file_widget.add_new_item = MagicMock()
        os.listdir = MagicMock(return_value=["file_1.jpg", "file_2.png", "file_3.jpg"])
        self._controller._dir_selected_evt(d)
        self._controller.view.alert.assert_not_called()
        self._controller.is_supported.assert_has_calls([mock.call("/some/path/file_1.jpg"), mock.call("/some/path"
                                                                                                      "/file_2.png"),
                                                        mock.call("/some/path/file_3.jpg")])
        self._controller.view.file_widget.add_new_item.assert_has_calls(
            [mock.call("/some/path/file_1.jpg"), mock.call("/some/path/file_2.png"),
             mock.call("/some/path/file_3.jpg")])
