from unittest import mock
from unittest.mock import MagicMock, create_autospec

from napari_allencell_annotator.controller.images_controller import (
    ImagesController,
    ImagesView,
)
from napari_allencell_annotator.controller.images_controller import (
    SUPPORTED_FILE_TYPES,
)
import napari
import os


class TestImagesController:
    def setup_method(self):
        self._mock_viewer: MagicMock = create_autospec(napari.Viewer)
        with mock.patch(
                "napari_allencell_annotator.controller.images_controller.ImagesView"
        ):
            self._controller = ImagesController(self._mock_viewer)

    def test_shuffle_clicked_none(self):
        # test when list widget has no items
        self._controller.view.file_widget.clear_for_shuff = MagicMock(return_value=[])
        self._controller._shuffle_clicked(True)
        self._controller.view.file_widget.clear_for_shuff.assert_called_once_with()
        self._controller.view.file_widget.set_shuff_order.assert_not_called()
        self._controller.view.toggle_add.assert_not_called()
        self._controller.view.file_widget.add_item.assert_not_called()

    def test_shuffle_clicked_one(self):
        # test when list widget has one item
        self._controller.view.file_widget = MagicMock()
        self._controller.view.file_widget.clear_for_shuff.return_value = {
            "file_1.png": {"File Name": 'name', "FMS": ""}
        }

        self._controller._shuffle_clicked(True)
        self._controller.view.file_widget.add_item.assert_called_once_with(
            "file_1.png", hidden=True
        )
        self._controller.view.file_widget.set_shuff_order.assert_called_once()

    def test_shuffle_clicked_one_false(self):
        self._controller.view.file_widget = MagicMock()
        self._controller.view.file_widget.clear_for_shuff.return_value = {
            "file_1.png": {"File Name": 'name', "FMS": ""}
        }
        self._controller._shuffle_clicked(False)
        self._controller.view.file_widget.add_item.assert_called_once_with(
            "file_1.png", hidden=False
        )
        self._controller.view.file_widget.set_shuff_order.assert_called_once_with()

    def test_shuffle_clicked_mult(self):
        # test when list widget has multiple items
        self._controller.view.file_widget = MagicMock()
        self._controller.view.file_widget.file_dict = {"file_1.png": {"File Name": 'name', "FMS": ""},
                                                       "file_2.png": {"File Name": 'name', "FMS": ""},
                                                       "file_3.png": {"File Name": 'name', "FMS": ""},
                                                       "file_4.png": {"File Name": 'name', "FMS": ""}}

        self._controller.view.file_widget.clear_for_shuff.return_value = self._controller.view.file_widget.file_dict
        self._controller._shuffle_clicked(True)
        assert len(
            self._controller.view.file_widget.add_item.mock_calls
        ) == len(
            self._controller.view.file_widget.clear_for_shuff.return_value
        )
        self._controller.view.file_widget.set_shuff_order.assert_called_once()

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
        self._controller.view.alert.assert_called_once_with(
            "No selection provided"
        )

    def test_dir_selected_evt_none(self):
        # test None dir list
        self._controller.view.alert = MagicMock()
        self._controller._dir_selected_evt(None)
        self._controller.view.alert.assert_called_once_with(
            "No selection provided"
        )

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
        d = ["/some/path"]
        self._controller.is_supported = MagicMock(return_value=True)
        self._controller.view.file_widget.add_new_item = MagicMock()
        os.listdir = MagicMock(return_value=["file_1.jpg"])
        self._controller._dir_selected_evt(d)
        self._controller.view.alert.assert_not_called()
        self._controller.is_supported.assert_called_once_with(
            "/some/path/file_1.jpg"
        )
        self._controller.view.file_widget.add_new_item.assert_called_once_with(
            "/some/path/file_1.jpg"
        )

    def test_dir_selected_evt_one_not_supp(self):
        # test for one file, is not supported
        self._controller.view.alert = MagicMock()
        self._controller.is_supported = MagicMock(return_value=False)
        self._controller.view.file_widget.add_new_item = MagicMock()
        os.listdir = MagicMock(return_value=["file_1.jpg"])
        d = ["/some/path"]
        self._controller._dir_selected_evt(d)
        self._controller.view.alert.assert_called_once_with(
            "Unsupported file type:/some/path/file_1.jpg"
        )
        self._controller.is_supported.assert_called_once_with(
            "/some/path/file_1.jpg"
        )
        self._controller.view.file_widget.add_new_item.assert_not_called()

    def test_dir_selected_evt_mult(self):
        # test for one multiple files
        self._controller.view.alert = MagicMock()
        self._controller.is_supported = MagicMock(return_value=True)
        self._controller.view.file_widget.add_new_item = MagicMock()
        d = ["/some/path"]
        os.listdir = MagicMock(
            return_value=["file_1.jpg", "file_2.png", "file_3.jpg"]
        )
        self._controller._dir_selected_evt(d)
        self._controller.view.alert.assert_not_called()
        self._controller.is_supported.assert_has_calls(
            [
                mock.call("/some/path/file_1.jpg"),
                mock.call("/some/path" "/file_2.png"),
                mock.call("/some/path/file_3.jpg"),
            ]
        )
        self._controller.view.file_widget.add_new_item.assert_has_calls(
            [
                mock.call("/some/path/file_1.jpg"),
                mock.call("/some/path/file_2.png"),
                mock.call("/some/path/file_3.jpg"),
            ]
        )

    def test_file_selected_evt_none(self):
        file_list = None
        self._controller.view.alert = MagicMock()
        self._controller._file_selected_evt(file_list)
        self._controller.view.alert.assert_called_once_with(
            "No selection provided"
        )

        file_list = []
        self._controller.view.alert = MagicMock()
        self._controller._file_selected_evt(file_list)
        self._controller.view.alert.assert_called_once_with(
            "No selection provided"
        )

    def test_file_selected_evt_supported(self):
        file_list = ["file_1.png", "file_2.png", "file_3.png"]
        self._controller.view.alert = MagicMock()
        self._controller.is_supported = MagicMock(return_value=True)
        self._controller.view.file_widget.add_new_item = MagicMock()
        self._controller._file_selected_evt(file_list)
        self._controller.view.alert.assert_not_called()
        self._controller.is_supported.assert_has_calls(
            [
                mock.call("file_1.png"),
                mock.call("file_2.png"),
                mock.call("file_3.png"),
            ]
        )
        self._controller.view.file_widget.add_new_item.assert_has_calls(
            [
                mock.call("file_1.png"),
                mock.call("file_2.png"),
                mock.call("file_3.png"),
            ]
        )

    def test_file_selected_evt_not_supported(self):
        file_list = ["file_1.png", "file_2.png", "file_3.png"]
        self._controller.view.alert = MagicMock()
        self._controller.is_supported = MagicMock(return_value=False)
        self._controller.view.file_widget.add_new_item = MagicMock()
        self._controller._file_selected_evt(file_list)
        self._controller.view.alert.assert_has_calls(
            [
                mock.call("Unsupported file type:file_1.png"),
                mock.call("Unsupported file type:file_2.png"),
                mock.call("Unsupported file type:file_3.png"),
            ]
        )

        self._controller.is_supported.assert_has_calls(
            [
                mock.call("file_1.png"),
                mock.call("file_2.png"),
                mock.call("file_3.png"),
            ]
        )
        self._controller.view.file_widget.add_new_item.assert_not_called()

    def test_start_annotating_zero(self):
        self._controller.view.file_widget = MagicMock()
        self._controller.view.file_widget.count = MagicMock(return_value=0)
        self._controller.view.file_widget.setCurrentItem = MagicMock()
        self._controller.view.alert = MagicMock()
        self._controller.start_annotating()
        self._controller.view.file_widget.setCurrentItem.assert_not_called()
        self._controller.view.alert.assert_called_once_with(
            "No files to annotate"
        )

    def test_start_annotating_not_shuffled(self):
        self._controller.view.file_widget = MagicMock()
        self._controller.view.file_widget.count = MagicMock(return_value=3)
        self._controller.view.file_widget.setCurrentItem = MagicMock()
        self._controller.view.alert = MagicMock()

        self._controller.start_annotating()
        self._controller.view.file_widget.setCurrentItem.assert_called_once_with(
            self._controller.view.file_widget.item(0)
        )
        self._controller.view.alert.assert_not_called()

    def test_stop_annotating(self):
        self._controller.view.file_widget = MagicMock()
        self._controller.stop_annotating()
        self._controller.view.file_widget.clear_all.assert_called_once_with()
        self._controller.view.reset_buttons.assert_called_once_with()

    def test_curr_img_dict(self):
        self._controller.view.file_widget.currentItem = MagicMock()
        self._controller.view.file_widget.currentItem().get_name = MagicMock(
            return_value="name"
        )
        self._controller.view.file_widget.currentItem().file_path = "path"
        self._controller.view.file_widget.get_curr_row = MagicMock(
            return_value=0
        )
        d = {"File Name": "name", "File Path": "path", "FMS": "", "Row": "0"}
        d_act = self._controller.curr_img_dict()
        assert d == d_act
        self._controller.view.file_widget.currentItem().get_name.assert_called_once()
        self._controller.view.file_widget.get_curr_row.assert_called_once()

    def test_next_img(self):
        self._controller.view.file_widget.get_curr_row = MagicMock(
            return_value=0
        )
        self._controller.view.file_widget.count = MagicMock(return_value=2)
        self._controller.view.file_widget.setCurrentItem = MagicMock()
        self._controller.view.file_widget.item = MagicMock(return_value=None)

        self._controller.next_img()
        assert (
                len(self._controller.view.file_widget.get_curr_row.mock_calls) == 2
        )

        self._controller.view.file_widget.count.assert_called_once()
        self._controller.view.file_widget.setCurrentItem.assert_called_once_with(
            None
        )
        self._controller.view.file_widget.item.assert_called_once_with(1)

    def test_next_img_last_img(self):
        self._controller.view.file_widget.get_curr_row = MagicMock(
            return_value=0
        )
        self._controller.view.file_widget.count = MagicMock(return_value=1)
        self._controller.view.file_widget.setCurrentItem = MagicMock()
        self._controller.view.file_widget.item = MagicMock(return_value=None)

        self._controller.next_img()
        assert (
                len(self._controller.view.file_widget.get_curr_row.mock_calls) == 1
        )

        self._controller.view.file_widget.count.assert_called_once()
        self._controller.view.file_widget.setCurrentItem.assert_not_called()
        self._controller.view.file_widget.item.assert_not_called()

    def test_prev_img(self):
        self._controller.view.file_widget.get_curr_row = MagicMock(
            return_value=1
        )
        self._controller.view.file_widget.setCurrentItem = MagicMock()
        self._controller.view.file_widget.item = MagicMock(return_value=None)

        self._controller.prev_img()
        assert (
                len(self._controller.view.file_widget.get_curr_row.mock_calls) == 2
        )

        self._controller.view.file_widget.setCurrentItem.assert_called_once_with(
            None
        )
        self._controller.view.file_widget.item.assert_called_once_with(0)

    def test_prev_img_first_img(self):
        self._controller.view.file_widget.get_curr_row = MagicMock(
            return_value=0
        )
        self._controller.view.file_widget.setCurrentItem = MagicMock()
        self._controller.view.file_widget.item = MagicMock(return_value=None)

        self._controller.prev_img()
        assert (
                len(self._controller.view.file_widget.get_curr_row.mock_calls) == 1
        )

        self._controller.view.file_widget.setCurrentItem.assert_not_called()
        self._controller.view.file_widget.item.assert_not_called()

    def test_get_num_files(self):
        self._controller.view.file_widget.count = MagicMock(return_value=1)
        num = self._controller.get_num_files()
        assert num == 1
        self._controller.view.file_widget.count.assert_called_once()
