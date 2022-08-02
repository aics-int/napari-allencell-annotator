from unittest import mock
from unittest.mock import MagicMock, create_autospec

from napari_allencell_annotator.widgets.file_input import FileInput, FileInputMode, QPushButton


class TestFileInput:
    def setup_method(self):
        expected_mode = FileInputMode.DIRECTORY
        with mock.patch.object(FileInput, "__init__", lambda x: None):
            self._input = FileInput()
            self._input._mode = expected_mode

    def test_mode(self):
        expected_mode = FileInputMode.DIRECTORY
        assert self._input.mode == expected_mode

    def test_simulate_click(self):
        self._input._input_btn = create_autospec(QPushButton)
        self._input._input_btn.clicked = MagicMock()
        self._input.simulate_click()
        self._input._input_btn.clicked.emit.assert_called_once_with()

    def test_toggle(self):
        self._input._input_btn = MagicMock()
        self._input.toggle(True)
        self._input._input_btn.setEnabled.assert_called_once_with(True)
