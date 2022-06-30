from unittest import mock
from unittest.mock import MagicMock, create_autospec, patch
from napari_allencell_annotator.controller.images_controller import ImagesController
from napari_allencell_annotator.view.images_view import ImagesView
from napari_allencell_annotator.widgets.list_widget import ListWidget
from napari_allencell_annotator.widgets.list_item import ListItem
from PyQt5.QtWidgets import QMessageBox
from aicsimageio import AICSImage, exceptions
import napari
import os


class TestImagesView:
    def setup_method(self):
        self._mock_controller: MagicMock = create_autospec(ImagesController)
        self._mock_viewer: MagicMock = create_autospec(napari.Viewer())
        self._view = ImagesView(self._mock_viewer, self._mock_controller)

    def test_update_shuff_text(self):
        # checked
        self._view.shuffle.setText = MagicMock()
        self._view._update_shuff_text(True)
        self._view.shuffle.setText.assert_called_once_with("Unshuffle and Unhide")
        # not checked
        self._view.shuffle.setText = MagicMock()
        self._view._update_shuff_text(False)
        self._view.shuffle.setText.assert_called_once_with("Shuffle and Hide")

    def test_delete_clicked(self):
        # test nothing checked
        self._view.file_widget: MagicMock = create_autospec(ListWidget)
        self._view.file_widget.checked = set()
        self._view.alert = MagicMock()
        self._view._delete_clicked()
        self._view.alert.assert_called_once_with("No Images Selected")
        # test lists all files for one/mult
        # check return value is ok, delete checked called once
        self._view.file_widget: MagicMock = create_autospec(ListWidget)
        item: MagicMock = create_autospec(ListItem)
        item.file_path = "path"
        self._view.file_widget.checked = {item}
        QMessageBox.exec = MagicMock(return_value=QMessageBox.Ok)
        self._view.alert = MagicMock()
        self._view.file_widget.delete_checked = MagicMock()
        self._view._delete_clicked()
        self._view.file_widget.delete_checked.assert_called_once()
        self._view.alert.assert_not_called()
        # check cancel value, delete checked not called
        self._view.file_widget: MagicMock = create_autospec(ListWidget)
        item: MagicMock = create_autospec(ListItem)
        item.file_path = "path"
        self._view.file_widget.checked = {item}
        QMessageBox.exec = MagicMock(return_value=QMessageBox.Cancel)
        self._view.alert = MagicMock()
        self._view.file_widget.delete_checked = MagicMock()
        self._view._delete_clicked()
        self._view.file_widget.delete_checked.assert_not_called()
        self._view.alert.assert_not_called()
        # check msg_box text

    def test_toggle_add(self):
        # check enabled and un-enabled
        self._view.input_dir.toggle = MagicMock()
        self._view.input_file.toggle = MagicMock()
        self._view.toggle_add(True)
        self._view.input_dir.toggle.assert_called_once_with(True)
        self._view.input_file.toggle.assert_called_once_with(True)

        self._view.input_dir.toggle = MagicMock()
        self._view.input_file.toggle = MagicMock()
        self._view.toggle_add(False)
        self._view.input_dir.toggle.assert_called_once_with(False)
        self._view.input_file.toggle.assert_called_once_with(False)

    def test_toggle_delete(self):
        self._view.delete.setEnabled = MagicMock()
        self._view._toggle_delete(True)
        self._view.delete.setEnabled.assert_called_once_with(True)

        self._view.delete.setEnabled = MagicMock()
        self._view._toggle_delete(False)
        self._view.delete.setEnabled.assert_called_once_with(False)

    def test_toggle_shuffle(self):
        self._view.shuffle.setEnabled = MagicMock()
        self._view._toggle_shuffle(True)
        self._view.shuffle.setEnabled.assert_called_once_with(True)

        self._view.shuffle.setEnabled = MagicMock()
        self._view._toggle_shuffle(False)
        self._view.shuffle.setEnabled.assert_called_once_with(False)

    def test_display_img_none(self):
        # current item none
        self._view.napari.layers.clear = MagicMock()
        self._view.file_widget.currentItem = MagicMock(return_value=None)
        self._view.napari.add_image = MagicMock()
        self._view._display_img()
        self._view.napari.layers.clear.assert_called_once_with()
        self._view.file_widget.currentItem.assert_called_once_with()
        self._view.napari.add_image.assert_not_called()

    @mock.patch("napari_allencell_annotator.view.images_view.AICSImage")
    def test_display_img_add(self, mock_aics_image):
        # self.napari add img called
        self._view.napari.layers.clear = MagicMock()
        item: MagicMock = create_autospec(ListItem)
        item.file_path = "/path/to/image.tiff"
        self._view.file_widget.currentItem = MagicMock(return_value=item)
        mock_image = create_autospec(AICSImage)
        mock_image.data = "data"
        mock_aics_image.return_value = mock_image

        self._view.napari.add_image = MagicMock()
        self._view._display_img()
        self._view.napari.layers.clear.assert_called_once_with()
        mock_aics_image.assert_called_with("/path/to/image.tiff")
        assert len(self._view.file_widget.currentItem.mock_calls) == 2
        self._view.napari.add_image.assert_called_once_with("data")

    def test_display_img_error(self):
        # unsupported file format
        self._view.napari.layers.clear = MagicMock()
        item: MagicMock = create_autospec(ListItem)
        item.file_path = "/path/to/image.tiff"
        self._view.file_widget.currentItem = MagicMock(return_value=item)
        self._view.alert = MagicMock()
        self._view.napari.add_image = MagicMock()
        error = create_autospec(exceptions.UnsupportedFileFormatError)
        #error.path = "path"
        #error.reader_name = "name"
        with patch('napari_allencell_annotator.view.images_view.AICSImage',
                   side_effect=error):
            #TODO: error here when error is made "TypeError: exceptions must derive from BaseException"
            self._view._display_img()
        self._view.napari.layers.clear.assert_called_once_with()
        # mock_aics_image.assert_called_with("/path/to/image.tiff")
        assert len(self._view.file_widget.currentItem.mock_calls) == 2
        self._view.napari.add_image.assert_not_called()
        self._view.alert.assert_called_once_with("AICS Unsupported File Type")
        # file not found
