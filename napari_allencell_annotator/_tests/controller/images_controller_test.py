from unittest.mock import MagicMock, Mock

from PyQt5 import QtCore


from napari_allencell_annotator.controller.images_controller import ImagesController
from constants.constants import SUPPORTED_FILE_TYPES

class TestImagesController:
    def test_connect_slots(self, qtbot):

        contr = ImagesController()
        contr._connect_slots()
        contr._shuffle_clicked = MagicMock()
        #TODO: not working
        qtbot.click(contr.view.shuffle)
        contr._shuffle_clicked.assert_called_once_with(True)




    def test_shuffle_clicked(self):
        #test when list widget has no items
        contr = ImagesController()
        contr.view.file_widget.clear_for_shuff = MagicMock()
        contr.view.toggle_add = MagicMock()
        contr.view.file_widget.add_item = MagicMock()
        contr._shuffle_clicked(True)
        contr.view.file_widget.clear_for_shuff.assert_called_once_with()
        contr.view.toggle_add.assert_called_once_with(False)
        contr.view.file_widget.add_item.assert_not_called()

        contr.view.file_widget.clear_for_shuff = MagicMock()
        contr.view.toggle_add = MagicMock()
        contr.view.file_widget.add_item = MagicMock()
        contr._shuffle_clicked(False)
        contr.view.file_widget.clear_for_shuff.assert_called_once_with()
        contr.view.toggle_add.assert_called_once_with(True)
        contr.view.file_widget.add_item.assert_not_called()

        #test when list widget has one item
        contr.view.file_widget.add_item = MagicMock()
        contr.view.file_widget.clear_for_shuff.return_value = ["file_1.png"]
        contr._shuffle_clicked(True)
        contr.view.file_widget.add_item.assert_called_once_with("file_1.png", hidden=True)

        contr.view.file_widget.add_item = MagicMock()
        contr._shuffle_clicked(False)
        contr.view.file_widget.add_item.assert_called_once_with("file_1.png", hidden=False)

        #test when list widget has multiple items
        contr.view.file_widget.add_item = MagicMock()
        contr.view.file_widget.clear_for_shuff.return_value = ["file_1.png", "file_2.png", "file_3.png"]
        contr._shuffle_clicked(True)
        assert len(contr.view.file_widget.add_item.mock_calls) == len(contr.view.file_widget.clear_for_shuff.return_value)





    def test_is_supported(self):
        for file_type in SUPPORTED_FILE_TYPES:
            assert ImagesController.is_supported("path" + file_type)
        assert ImagesController.is_supported("path.ome.tiff")
        assert not ImagesController.is_supported("path")
        assert not ImagesController.is_supported("")
        assert not ImagesController.is_supported(".jpg")
        assert not ImagesController.is_supported("path.txt")
        assert not ImagesController.is_supported(None)



