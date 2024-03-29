from unittest import mock
from unittest.mock import MagicMock, create_autospec, patch
from napari_allencell_annotator.controller.images_controller import ImagesController
from napari_allencell_annotator.view.images_view import (
    ImagesView,
    FileItem,
    ScrollablePopup,
    Popup,
    QDialog,
    QPushButton,
    FilesWidget,
)

from napari_allencell_annotator.view.images_view import AICSImage
from napari_allencell_annotator.view.images_view import napari
from napari_allencell_annotator.view.images_view import exceptions


class TestImagesView:
    def setup_method(self):
        with mock.patch.object(ImagesView, "__init__", lambda x: None):
            self._view = ImagesView()
            self._view.controller: MagicMock = create_autospec(ImagesController)
            self._view.viewer: MagicMock = create_autospec(napari.Viewer)
            self._view.AICSImage = create_autospec(AICSImage)

    def test_connect_slots(self):
        self._view.file_widget = create_autospec(FilesWidget)
        self._view.file_widget.files_selected.connect = MagicMock()
        self._view._toggle_delete = MagicMock()

        self._view.file_widget.files_added.connect = MagicMock()
        self._view._toggle_shuffle = MagicMock()

        self._view.shuffle = create_autospec(QPushButton)
        self._view.shuffle.toggled.connect = MagicMock()
        self._view._update_shuff_text = MagicMock()

        self._view.delete = create_autospec(QPushButton)
        self._view.delete.clicked.connect = MagicMock()
        self._view._delete_clicked = MagicMock()

        self._view.file_widget.currentItemChanged.connect = MagicMock()
        self._view._display_img = MagicMock()

        self._view._connect_slots()

        self._view.file_widget.files_selected.connect.assert_called_once_with(self._view._toggle_delete)
        self._view.file_widget.files_added.connect.assert_called_once_with(self._view._toggle_shuffle)
        self._view.shuffle.toggled.connect.assert_called_once_with(self._view._update_shuff_text)
        self._view.delete.clicked.connect.assert_called_once_with(self._view._delete_clicked)
        self._view.file_widget.currentItemChanged.connect.assert_called_once_with(self._view._display_img)

    def test_update_shuff_text(self):
        # checked
        self._view.shuffle = MagicMock()
        self._view.shuffle.setText = MagicMock()
        self._view._update_shuff_text(True)
        self._view.shuffle.setText.assert_called_once_with("Unhide")
        # not checked
        self._view.shuffle.setText = MagicMock()
        self._view._update_shuff_text(False)
        self._view.shuffle.setText.assert_called_once_with("Shuffle and Hide")

    def test_reset_buttons(self):
        self._view._toggle_delete = MagicMock()
        self._view._toggle_shuffle = MagicMock()
        self._view.shuffle = MagicMock()
        self._view.toggle_add = MagicMock()

        self._view.reset_buttons()
        self._view._toggle_delete.assert_called_once_with(False)
        self._view.shuffle.setChecked.assert_called_once_with(False)
        self._view._toggle_shuffle.assert_called_once_with(False)

        self._view.toggle_add.assert_called_once_with(True)

    def test_delete_clicked_none_checked_true(self):
        # test nothing checked
        self._view.file_widget: MagicMock = MagicMock()
        Popup.make_popup = MagicMock(return_value=True)
        self._view.file_widget = create_autospec(FilesWidget)
        self._view.reset_buttons = MagicMock()

        self._view.file_widget.checked = set()
        self._view._delete_clicked()

        self._view.file_widget.clear_all.assert_called_once_with()
        self._view.reset_buttons.assert_called_once_with()

    def test_delete_clicked_none_checked_false(self):
        # test nothing checked
        self._view.file_widget: MagicMock = MagicMock()
        Popup.make_popup = MagicMock(return_value=False)
        self._view.file_widget = create_autospec(FilesWidget)
        self._view.reset_buttons = MagicMock()

        self._view.file_widget.checked = set()
        self._view._delete_clicked()

        self._view.file_widget.clear_all.assert_not_called()
        self._view.reset_buttons.assert_not_called()

    @patch("napari_allencell_annotator.view.images_view.ScrollablePopup.__init__")
    def test_delete_clicked_accept(self, mock_init):
        mock_init.return_value = None
        self._view.file_widget = create_autospec(FilesWidget)
        item = create_autospec(FileItem)
        item.file_path = "path"
        self._view.file_widget.checked = {item}
        self._view.alert = MagicMock()
        ScrollablePopup.exec = MagicMock(return_value=QDialog.Accepted)
        self._view.file_widget.delete_checked = MagicMock()
        self._view._delete_clicked()

        self._view.alert.assert_not_called()

        mock_init.assert_called_once_with("Delete these files from the list?", {"--- path"})
        ScrollablePopup.exec.assert_called_once_with()
        self._view.file_widget.delete_checked.assert_called_once_with()

    @patch("napari_allencell_annotator.view.images_view.ScrollablePopup.__init__")
    def test_delete_clicked_reject(self, mock_init):
        mock_init.return_value = None
        self._view.file_widget: MagicMock = MagicMock()
        item = create_autospec(FileItem)
        item.file_path = "path"
        item2 = create_autospec(FileItem)
        item2.file_path = "path2"
        self._view.file_widget.checked = {item, item2}
        self._view.alert = MagicMock()
        ScrollablePopup.exec = MagicMock(return_value=QDialog.Rejected)
        self._view.file_widget.delete_checked = MagicMock()
        self._view._delete_clicked()

        self._view.alert.assert_not_called()
        mock_init.assert_called_once_with("Delete these files from the list?", {"--- path", "--- path2"})
        ScrollablePopup.exec.assert_called_once_with()
        self._view.file_widget.delete_checked.assert_not_called()

    def test_alert(self):
        with mock.patch("napari_allencell_annotator.view.images_view.show_info") as mock_info:
            self._view.alert("hello")
            mock_info.assert_called_once_with("hello")

    def test_toggle_add(self):
        # check enabled and un-enabled
        self._view.input_dir = MagicMock()
        self._view.input_dir.toggle = MagicMock()
        self._view.input_file = MagicMock()
        self._view.input_file.toggle = MagicMock()
        self._view.toggle_add(True)
        self._view.input_dir.toggle.assert_called_once_with(True)
        self._view.input_file.toggle.assert_called_once_with(True)

        self._view.input_dir.toggle = MagicMock()
        self._view.input_file.toggle = MagicMock()
        self._view.toggle_add(False)
        self._view.input_dir.toggle.assert_called_once_with(False)
        self._view.input_file.toggle.assert_called_once_with(False)

    def test_toggle_delete_true(self):
        self._view.delete = create_autospec(QPushButton)
        self._view._toggle_delete(True)
        self._view.delete.setText("Delete Selected")

    def test_toggle_delete_false(self):
        self._view.delete = create_autospec(QPushButton)
        self._view._toggle_delete(False)
        self._view.delete.setText("Delete All")

    def test_toggle_shuffle_true(self):
        self._view.shuffle = MagicMock()
        self._view.delete = create_autospec(QPushButton)
        self._view.shuffle.setEnabled = MagicMock()
        self._view._toggle_shuffle(True)
        self._view.delete.setToolTip.assert_called_once_with("Check box on the right \n to select files for deletion")
        self._view.shuffle.setEnabled.assert_called_once_with(True)
        self._view.delete.setText.assert_called_once_with("Delete All")
        self._view.delete.setEnabled.assert_called_once_with(True)

    def test_toggle_shuffle_false(self):
        self._view.shuffle = MagicMock()
        self._view.delete = create_autospec(QPushButton)
        self._view.shuffle.setEnabled = MagicMock()
        self._view._toggle_shuffle(False)
        self._view.delete.setToolTip.assert_called_once_with(None)
        self._view.shuffle.setEnabled.assert_called_once_with(False)
        self._view.delete.setEnabled.assert_called_once_with(False)

    def test_display_img_none_both(self):
        # current item none
        self._view.viewer.layers = MagicMock()
        self._view.viewer.layers.clear = MagicMock()
        prev = None
        curr = None
        self._view.AICSImage = MagicMock(return_value="data")
        self._view._display_img(curr, prev)
        self._view.viewer.layers.clear.assert_called_once_with()
        self._view.AICSImage.assert_not_called()

    def test_display_img_none_curr(self):
        # current item none
        self._view.viewer.layers = MagicMock()
        self._view.viewer.layers.clear = MagicMock()
        prev = create_autospec(FileItem)
        prev.unhighlight = MagicMock()
        curr = None
        self._view.AICSImage = MagicMock(return_value="data")
        self._view._display_img(curr, prev)

        self._view.viewer.layers.clear.assert_called_once_with()
        prev.unhighlight.assert_called_once_with()
        self._view.AICSImage.assert_not_called()

    def test_display_img(self):
        self._view.viewer.layers = MagicMock()
        self._view.viewer.layers.clear = MagicMock()
        prev = create_autospec(FileItem)
        prev.unhighlight = MagicMock()
        curr = create_autospec(FileItem)
        curr.file_path = MagicMock(return_value="path")
        curr.highlight = MagicMock()

        self._view.viewer.add_image = MagicMock()

        with mock.patch.object(AICSImage, "__init__", lambda x, y: None):
            AICSImage.data = "data"
            self._view._display_img(curr, prev)

            self._view.viewer.layers.clear.assert_called_once_with()
            self._view.viewer.add_image.assert_called_once_with("data")
            curr.highlight.assert_called_once_with()
            prev.unhighlight.assert_called_once_with()

    def test_display_img_unsupported(self):
        self._view.viewer.layers = MagicMock()
        self._view.viewer.layers.clear = MagicMock()
        prev = create_autospec(FileItem)
        prev.unhighlight = MagicMock()
        curr = create_autospec(FileItem)
        curr.file_path = MagicMock(return_value="path")
        curr.highlight = MagicMock()

        self._view.viewer.add_image = MagicMock()
        with mock.patch.object(exceptions.UnsupportedFileFormatError, "__init__", lambda x, y, z: None):
            AICSImage.__init__ = MagicMock(side_effect=exceptions.UnsupportedFileFormatError("x", "y"))
            AICSImage.data = "data"
            self._view.alert = MagicMock()
            self._view._display_img(curr, prev)

            self._view.viewer.layers.clear.assert_called_once_with()
            self._view.viewer.add_image.assert_not_called()
            curr.highlight.assert_not_called()
            prev.unhighlight.assert_called_once_with()
            self._view.alert.assert_called_once_with("AICS Unsupported File Type")
