from unittest import mock
from unittest.mock import MagicMock

from napari_allencell_annotator.widgets.list_item import ListItem

from napari_allencell_annotator.widgets.list_item import os


class TestListItem:
    def setup_method(self):
        with mock.patch.object(ListItem, "__init__", lambda x: None):
            self._widget = ListItem()
            self._widget._file_path = 'path'

    def test_file_path(self):
        expected_path = "path"
        assert self._widget.file_path == expected_path

    def test_name(self):
        expected_name = "basepath"
        os.path.basename = MagicMock(return_value="basepath")
        assert self._widget.name == expected_name

    def test_eq(self):
        path = "path"
        with mock.patch.object(ListItem, "__init__", lambda x: None):
            widget_2 = ListItem()
            widget_2._file_path = path
        assert self._widget == widget_2
        assert self._widget == self._widget

    def test_not_eq(self):
        path = "path2"
        with mock.patch.object(ListItem, "__init__", lambda x: None):
            widget_2 = ListItem()
            widget_2._file_path = path
        assert self._widget != widget_2
        assert self._widget == self._widget

    def test_hash(self):
        path = "path"
        with mock.patch.object(ListItem, "__init__", lambda x: None):
            widget_2 = ListItem()
            widget_2._file_path = path
        wid_set = set()
        wid_set.add(self._widget)
        wid_set.add(widget_2)
        assert len(wid_set) == 1

        path = "path2"
        with mock.patch.object(ListItem, "__init__", lambda x: None):
            widget_2 = ListItem()
            widget_2._file_path = path
        wid_set = set()
        wid_set.add(self._widget)
        wid_set.add(widget_2)
        assert len(wid_set) == 2
