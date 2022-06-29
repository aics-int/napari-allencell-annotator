from unittest.mock import MagicMock, create_autospec
from napari_allencell_annotator.controller.images_controller import ImagesController
from napari_allencell_annotator.view.images_view import ImagesView
from napari_allencell_annotator.widgets.list_widget import ListWidget
from napari_allencell_annotator.widgets.list_item import ListItem
from PyQt5.QtWidgets import QMessageBox
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
        self._view._ile_widget: MagicMock = create_autospec(ListWidget)
        self._view.file_widget.checked = set()
        self._view.alert = MagicMock()
        self._view._delete_clicked()
        self._view.alert.assert_called_once_with("No Images Selected")
        # test lists all files for one/mult
        # check return value is ok, delete checked called once
        self._view.file_widget: MagicMock = create_autospec(ListWidget)
        os.path.basename = MagicMock(return_value="file.jpg")
        item = ListItem("", None)
        self._view.file_widget.checked = {item}
        QMessageBox.exec = MagicMock(return_value=QMessageBox.Ok)
        self._view.alert = MagicMock()
        self._view.file_widget.delete_checked = MagicMock()
        self._view._delete_clicked()
        self._view.file_widget.delete_checked.assert_called_once()
        self._view.alert.assert_not_called()
        # check cancel value, delete checked not called
        self._view.file_widget: MagicMock = create_autospec(ListWidget)
        os.path.basename = MagicMock(return_value="file.jpg")
        item = ListItem("", None)
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
        self._view.toggle_add(True)
        assert self._view.input_dir.isEnabled()
        assert self._view.input_file.isEnabled()
        self._view.toggle_add(False)
        assert not self._view.input_dir.isEnabled()
        assert not self._view.input_file.isEnabled()
