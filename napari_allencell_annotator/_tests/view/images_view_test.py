from unittest import mock
from unittest.mock import MagicMock, create_autospec
from napari_allencell_annotator.controller.images_controller import (
    ImagesController,
)
from napari_allencell_annotator.view.images_view import ImagesView, FileItem

from napari_allencell_annotator.view.images_view import AICSImage
from napari_allencell_annotator.view.images_view import napari


class TestImagesView:
    def setup_method(self):
        with mock.patch.object(ImagesView, "__init__", lambda x: None):
            self._view = ImagesView()
            self._view.controller: MagicMock = create_autospec(ImagesController)
            self._view.viewer: MagicMock = create_autospec(napari.Viewer)
            self._view.AICSImage = create_autospec(AICSImage)

    def test_reset_buttons(self):
        self._view._toggle_delete = MagicMock()
        self._view._toggle_shuffle = MagicMock()
        self._view._toggle_shuffle = MagicMock()
        self._view.toggle_add = MagicMock()
        self._view.reset_buttons()
        self._view._toggle_delete.assert_called_once_with(False)

        self._view._toggle_shuffle.assert_called_once_with(False)

        self._view.toggle_add.assert_called_once_with(True)

    def test_update_shuff_text(self):
        # checked
        self._view.shuffle = MagicMock()
        self._view.shuffle.setText = MagicMock()
        self._view._update_shuff_text(True)
        self._view.shuffle.setText.assert_called_once_with("Unshuffle and Unhide")
        # not checked
        self._view.shuffle.setText = MagicMock()
        self._view._update_shuff_text(False)
        self._view.shuffle.setText.assert_called_once_with("Shuffle and Hide")

    def test_delete_clicked(self):
        # test nothing checked
        self._view.file_widget: MagicMock = MagicMock()

        self._view.file_widget.checked = set()
        self._view.alert = MagicMock()
        self._view._delete_clicked()
        self._view.alert.assert_called_once_with("No Images Selected")

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

    def test_toggle_delete(self):
        self._view.delete = MagicMock()
        self._view.delete.setEnabled = MagicMock()
        self._view._toggle_delete(True)
        self._view.delete.setEnabled.assert_called_once_with(True)

        self._view.delete.setEnabled = MagicMock()
        self._view._toggle_delete(False)
        self._view.delete.setEnabled.assert_called_once_with(False)

    def test_toggle_shuffle(self):
        self._view.shuffle = MagicMock()
        self._view.shuffle.setEnabled = MagicMock()
        self._view._toggle_shuffle(True)
        self._view.shuffle.setEnabled.assert_called_once_with(True)

        self._view.shuffle.setEnabled = MagicMock()
        self._view._toggle_shuffle(False)
        self._view.shuffle.setEnabled.assert_called_once_with(False)

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
        # current item none
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
