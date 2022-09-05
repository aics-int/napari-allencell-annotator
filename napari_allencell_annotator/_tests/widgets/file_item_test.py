from unittest import mock
from unittest.mock import create_autospec, MagicMock

from napari_allencell_annotator.widgets.file_item import FileItem, QLabel, QCheckBox


class TestFileItem:
    def setup_method(self):
        with mock.patch.object(FileItem, "__init__", lambda x: None):
            self._widget = FileItem()
            self._widget._file_path = "path"

    def test_file_path(self):
        expected_path = "path"
        assert self._widget.file_path == expected_path

    def test_get_name(self):
        self._widget._file_path = "dir/path.png"
        assert self._widget.get_name() == "path"

    def test_unhide(self):
        self._widget.label = create_autospec(QLabel)
        self._widget.check = create_autospec(QCheckBox)
        self._widget.unhide()
        self._widget.label.setText.assert_called_once_with(self._widget._make_display_name())
        self._widget.check.setCheckable.assert_called_once_with(True)

    def test_make_display_name_less_than(self):
        self._widget.get_name = MagicMock(return_value="name")
        assert "name" == self._widget._make_display_name()

    def test_make_display_name_equal_to_36(self):
        name = "12345678901234567890123456789012345"
        self._widget.get_name = MagicMock(return_value=name)
        assert name == self._widget._make_display_name()

    def test_make_display_name_greater_than(self):
        name = "12345678901234567890123456789012345678"
        self._widget.get_name = MagicMock(return_value=name)
        disp = self._widget._make_display_name()
        assert len(disp) == 35
        assert disp == "123456789012345...23456789012345678"

    def test_highlight(self):
        self._widget.label = create_autospec(QLabel)
        self._widget.highlight()
        self._widget.label.setStyleSheet.assert_called_once_with(
            """QLabel{
                            font-weight: bold;
                            text-decoration: underline;
                        }"""
        )

    def test_unhighlight(self):
        self._widget.label = create_autospec(QLabel)
        self._widget.unhighlight()
        self._widget.label.setStyleSheet.assert_called_once_with("""QLabel{}""")

    def test_eq(self):
        path = "path"
        with mock.patch.object(FileItem, "__init__", lambda x: None):
            widget_2 = FileItem()
            widget_2._file_path = path
        assert self._widget == widget_2
        assert self._widget == self._widget

    def test_not_eq(self):
        path = "path2"
        with mock.patch.object(FileItem, "__init__", lambda x: None):
            widget_2 = FileItem()
            widget_2._file_path = path
        assert self._widget != widget_2
        assert self._widget == self._widget

    def test_hash(self):
        path = "path"
        with mock.patch.object(FileItem, "__init__", lambda x: None):
            widget_2 = FileItem()
            widget_2._file_path = path
        wid_set = set()
        wid_set.add(self._widget)
        wid_set.add(widget_2)
        assert len(wid_set) == 1

        path = "path2"
        with mock.patch.object(FileItem, "__init__", lambda x: None):
            widget_2 = FileItem()
            widget_2._file_path = path
        wid_set = set()
        wid_set.add(self._widget)
        wid_set.add(widget_2)
        assert len(wid_set) == 2
