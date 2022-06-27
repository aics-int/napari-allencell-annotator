from napari_allencell_annotator.widgets.file_input import FileInput, FileInputMode


class TestFileInput:
    def test_properties(self):
        expected_mode = FileInputMode.DIRECTORY

        widget = FileInput(mode=expected_mode)
        assert widget.mode == expected_mode