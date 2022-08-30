from unittest import mock
from unittest.mock import MagicMock

from napari_allencell_annotator.widgets.popup import Popup, QMessageBox


class TestPopup:
    def test_popup_yes(self):
        with mock.patch.object(QMessageBox, "__init__", lambda x: None):
            QMessageBox.setText = MagicMock()
            QMessageBox.setStandardButtons = MagicMock()
            QMessageBox.exec = MagicMock(return_value=QMessageBox.Yes)

            assert Popup.make_popup("text")
            QMessageBox.setText.assert_called_once_with("text")
            QMessageBox.setStandardButtons.assert_called_once_with(QMessageBox.No | QMessageBox.Yes)
            QMessageBox.exec.assert_called_once_with()


    def test_popup_no(self):
        with mock.patch.object(QMessageBox, "__init__", lambda x: None):
            QMessageBox.setText = MagicMock()
            QMessageBox.setStandardButtons = MagicMock()
            QMessageBox.exec = MagicMock(return_value=QMessageBox.No)

            assert not Popup.make_popup("text")
            QMessageBox.setText.assert_called_once_with("text")
            QMessageBox.setStandardButtons.assert_called_once_with(QMessageBox.No | QMessageBox.Yes)
            QMessageBox.exec.assert_called_once_with()
