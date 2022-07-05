from unittest import mock

from napari_allencell_annotator.widgets.file_input import FileInput, FileInputMode


class TestFileInput:
    def test_properties(self):
        expected_mode = FileInputMode.DIRECTORY
        with mock.patch.object(FileInput, "__init__", lambda x: None):
            self._input = FileInput()
            self._input._mode = expected_mode

        assert self._input.mode == expected_mode
