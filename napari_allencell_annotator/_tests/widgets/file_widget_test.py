from unittest import mock
from unittest.mock import MagicMock, create_autospec

from napari_allencell_annotator.widgets.files_widget import FilesWidget, FileItem


class TestFileWidget:
    def setup_method(self):
        with mock.patch.object(FilesWidget, "__init__", lambda x: None):
            self._widget = FilesWidget()
            self._widget._shuffled = False
            self._widget.files_dict = {}
            self._widget.checked = set()

    def test_shuffled(self):
        assert not self._widget.shuffled
        self._widget._shuffled = True
        assert self._widget.shuffled

    def test_get_curr_row_none(self):
        self._widget.currentItem = MagicMock(return_value=None)
        assert self._widget.get_curr_row() == -1

    def test_get_curr_row(self):
        item = create_autospec(FileItem)
        self._widget.row = MagicMock(return_value=0)
        self._widget.currentItem = MagicMock(return_value=item)
        assert self._widget.get_curr_row() == 0

    def test_clear_all(self):
        self._widget._shuffled = True
        self._widget.setCurrentItem = MagicMock()
        self._widget.clear = MagicMock()
        self._widget.shuffled_files_dict = {"item": []}
        self._widget.checked = {"item"}
        self._widget.files_dict = {"item": []}
        self._widget.clear_all()

        assert self._widget._shuffled == False
        assert self._widget.checked == set()
        assert self._widget.files_dict == {}
        assert self._widget.shuffled_files_dict == {}
        self._widget.setCurrentItem.assert_called_once_with(None)
        self._widget.clear.assert_called_once_with()

    def test_set_shuff_order(self):
        self._widget.shuffled_files_dict = {"item": {}}
        self._widget.set_shuff_order({"item2": {}})
        assert self._widget.shuffled_files_dict == {"item2": {}}

    def test_set_shuff_order_none(self):
        self._widget.shuffled_files_dict = {"item": {}}
        self._widget.set_shuff_order()
        assert self._widget.shuffled_files_dict == {}

    def test_clear_for_shuffle(self):
        self._widget._shuffled = False
        self._widget.shuffled_files_dict = {"item": {}}
        self._widget.setCurrentItem = MagicMock()
        self._widget.clear = MagicMock()
        self._widget.checked = set("item")
        self._widget.clear = MagicMock()
        self._widget.files_dict = {"item": []}

        ret = self._widget.clear_for_shuff()

        assert self._widget.shuffled_files_dict == {}
        assert self._widget._shuffled == True
        self._widget.setCurrentItem.assert_called_once_with(None)
        assert self._widget.checked == set()
        self._widget.clear.assert_called_once_with()
        assert ret == {"item": []}

    def test_add_new_item_in_files(self):
        item = "item"
        self._widget.files_dict[item] = {}
        self._widget.add_new_item(item)
        self._widget.files_dict[item] == {}

    def test_add_new_item(self):
        with mock.patch.object(FileItem, "__init__", lambda w, x, y, z,: None):
            FileItem.check = MagicMock()
            FileItem.get_name = MagicMock(return_value="name")
            self._widget.files_added = MagicMock()

            self._widget.add_new_item("file")
            FileItem.check.stateChanged.connect.assert_called_once()
            FileItem.get_name = MagicMock(return_value="name")

            self._widget.files_added.emit.assert_called_once_with(True)
            assert len(self._widget.files_dict) == 1
            assert self._widget.files_dict == {"file": ["name", ""]}

    def test_add_new_item_two(self):
        with mock.patch.object(FileItem, "__init__", lambda w, x, y, z,: None):
            self._widget.files_dict = {"file": ["name", ""]}
            FileItem.get_name = MagicMock(return_value="name")
            self._widget.files_added = MagicMock()

            FileItem.check = MagicMock()
            self._widget.add_new_item("file2")
            FileItem.check.stateChanged.connect.assert_called_once()

            self._widget.files_added.emit.assert_not_called()
            assert self._widget.files_dict == {"file": ["name", ""], "file2": ["name", ""]}

    def test_add_new_item_repeat(self):
        with mock.patch.object(FileItem, "__init__", lambda w, x, y, z,: None):
            self._widget.files_dict = {"file": ["name", ""], "file2": ["name", ""]}

            FileItem.get_name = MagicMock(return_value="name")
            FileItem.check = MagicMock()
            self._widget.files_added = MagicMock()
            self._widget.add_new_item("file2")
            FileItem.check.stateChanged.connect.assert_not_called()

            self._widget.files_added.emit.assert_not_called()
            assert self._widget.files_dict == {"file": ["name", ""], "file2": ["name", ""]}

    def test_add_item(self):
        with mock.patch.object(FileItem, "__init__", lambda w, x, y, z,: None):
            FileItem.check = MagicMock()
            self._widget.add_item("file")
            FileItem.check.stateChanged.connect.assert_called_once()

    def test_remove_item_not_in_files(self):
        item = create_autospec(FileItem)
        item.file_path = MagicMock(return_value="file")
        self._widget.currentItem = MagicMock()
        self._widget.remove_item(item)
        self._widget.currentItem.assert_not_called()

    def test_remove_item_curr_item(self):
        item = create_autospec(FileItem)
        item.file_path = "file"
        item2 = create_autospec(FileItem)
        item2.file_path = "file2"
        item3 = create_autospec(FileItem)
        item3.file_path = MagicMock(return_value="file3")
        self._widget.files_dict = {"file": ["name", ""], "file2": ["name", ""], "file3": ["name", ""]}

        self._widget.currentItem = MagicMock(return_value=item2)
        self._widget.row = MagicMock(return_value=1)
        self._widget.setCurrentItem = MagicMock()
        self._widget.takeItem = MagicMock()
        self._widget.files_added = MagicMock()

        self._widget.remove_item(item2)
        self._widget.setCurrentItem.assert_called_once_with(None)
        self._widget.takeItem.assert_called_once_with(1)
        assert self._widget.files_dict == {"file": ["name", ""], "file3": ["name", ""]}

        self._widget.files_added.emit.assert_not_called()

    def test_remove_item(self):
        item = create_autospec(FileItem)
        item.file_path = "file"
        item2 = create_autospec(FileItem)
        item2.file_path = "file2"
        item3 = create_autospec(FileItem)
        item3.file_path = "file3"
        self._widget.files_dict = {"file": ["name", ""], "file2": ["name", ""], "file3": ["name", ""]}

        self._widget.currentItem = MagicMock(return_value=item)
        self._widget.row = MagicMock(return_value=2)
        self._widget.setCurrentItem = MagicMock()
        self._widget.takeItem = MagicMock()
        self._widget.files_added = MagicMock()

        self._widget.remove_item(item3)
        self._widget.setCurrentItem.assert_not_called()
        self._widget.takeItem.assert_called_once_with(2)
        assert self._widget.files_dict == {"file": ["name", ""], "file2": ["name", ""]}

        self._widget.files_added.emit.assert_not_called()

    def test_remove_item_last(self):
        item = create_autospec(FileItem)
        item.file_path = "file"
        self._widget.files_dict = {"file": ["name", ""]}

        self._widget.currentItem = MagicMock(return_value=None)
        self._widget.row = MagicMock(return_value=0)
        self._widget.setCurrentItem = MagicMock()
        self._widget.takeItem = MagicMock()
        self._widget.files_added = MagicMock()

        self._widget.remove_item(item)
        self._widget.setCurrentItem.assert_not_called()
        self._widget.takeItem.assert_called_once_with(0)
        assert self._widget.files_dict == {}
        self._widget.files_added.emit.assert_called_once_with(False)

    def test_delete_checked_empty(self):
        self._widget.checked = set()
        self._widget.remove_item = MagicMock()
        self._widget.files_selected = MagicMock()
        self._widget.files_selected.emit = MagicMock()
        self._widget.delete_checked()

        assert self._widget.checked == set()
        self._widget.remove_item.assert_not_called()
        self._widget.files_selected.emit.assert_called_once_with(False)

    def test_delete_checked(self):
        item = create_autospec(FileItem)
        item2 = create_autospec(FileItem)
        self._widget.checked = {item, item2}
        self._widget.remove_item = MagicMock()
        self._widget.files_selected = MagicMock()
        self._widget.files_selected.emit = MagicMock()
        self._widget.delete_checked()

        assert self._widget.checked == set()
        self._widget.remove_item.assert_has_calls([mock.call(item), mock.call(item2)], any_order=True)
        self._widget.files_selected.emit.assert_called_once_with(False)

    def test_check_evt_checked(self):
        item = create_autospec(FileItem)
        item.check = MagicMock()
        item.check.isChecked = MagicMock(return_value=True)
        self._widget.files_selected = MagicMock()
        self._widget.files_selected.emit = MagicMock()

        self._widget._check_evt(item)
        assert self._widget.checked == {item}
        self._widget.files_selected.emit.assert_called_once_with(True)

        self._widget.files_selected.emit = MagicMock()

        self._widget._check_evt(item)
        assert self._widget.checked == {item}
        self._widget.files_selected.emit.assert_not_called()

    def test_check_evt_not_checked(self):
        item = create_autospec(FileItem)
        item.check = MagicMock()
        item.check.isChecked = MagicMock(return_value=False)
        self._widget.files_selected = MagicMock()
        self._widget.files_selected.emit = MagicMock()

        self._widget._check_evt(item)
        assert self._widget.checked == set()
        self._widget.files_selected.emit.assert_not_called()

        self._widget.checked = {item}
        self._widget.files_selected.emit = MagicMock()

        self._widget._check_evt(item)
        assert self._widget.checked == set()
        self._widget.files_selected.emit.assert_called_once_with(False)
