from unittest import mock
from unittest.mock import MagicMock, create_autospec

from napari_allencell_annotator.widgets.list_widget import ListWidget, ListItem


class TestListWidget:
    def setup_method(self):
        with mock.patch.object(ListWidget, "__init__", lambda x: None):
            self._widget = ListWidget()
            self._widget.files = set()
            self._widget.file_order = []
            self._widget.checked = set()

    def test_get_curr_row_none(self):
        self._widget.currentItem = MagicMock(return_value=None)
        assert self._widget.get_curr_row() == -1

    def test_get_curr_row(self):
        item = create_autospec(ListItem)
        self._widget.row = MagicMock(return_value=0)
        self._widget.currentItem = MagicMock(return_value=item)
        assert self._widget.get_curr_row() == 0

    def test_clear_all(self):
        self._widget.setCurrentItem = MagicMock()
        self._widget.clear = MagicMock()
        self._widget.checked= {"item"}
        self._widget.files = {'item'}
        self._widget.file_order = ['item']
        self._widget.clear_all()

        assert self._widget.checked == set()
        assert self._widget.files == set()
        assert self._widget.file_order == []
        self._widget.setCurrentItem.assert_called_once_with(None)
        self._widget.clear.assert_called_once_with()

    def test_clear_for_shuffle(self):
        self._widget.setCurrentItem = MagicMock()
        self._widget.clear = MagicMock()
        self._widget.checked = set('item')
        self._widget.clear = MagicMock()
        self._widget.file_order = 'order'

        ret = self._widget.clear_for_shuff()

        self._widget.setCurrentItem.assert_called_once_with(None)
        assert self._widget.checked == set()
        self._widget.clear.assert_called_once_with()
        assert ret == 'order'

    def test_add_new_item_in_files(self):
        item = "item"
        self._widget.files.add(item)
        self._widget.add_item = MagicMock()
        self._widget.add_new_item(item)
        self._widget.add_item.assert_not_called()

    def test_add_new_item(self):
        file1 = "file1"
        self._widget.add_item = MagicMock()

        self._widget.files_added = MagicMock()
        self._widget.files_added.emit = MagicMock()
        self._widget.add_new_item(file1)
        self._widget.files.add(file1)

        self._widget.add_item.assert_called_once_with(file1)
        self._widget.files_added.emit.assert_called_once_with(True)
        assert self._widget.file_order == [file1]

        file2 = "file2"
        self._widget.add_item = MagicMock()

        self._widget.files_added = MagicMock()
        self._widget.files_added.emit = MagicMock()
        self._widget.add_new_item(file2)
        self._widget.files.add(file2)

        self._widget.add_item.assert_called_once_with(file2)
        self._widget.files_added.emit.assert_not_called()
        assert self._widget.file_order == [file1, file2]

        file2 = "file2"
        self._widget.add_item = MagicMock()

        self._widget.files_added = MagicMock()
        self._widget.files_added.emit = MagicMock()
        self._widget.add_new_item(file2)

        self._widget.add_item.assert_not_called()
        self._widget.files_added.emit.assert_not_called()
        assert self._widget.file_order == [file1, file2]

    def test_add_item(self):
        with mock.patch.object(ListItem, "__init__", lambda w, x, y, z,: None):
            ListItem.check = MagicMock()
            self._widget.add_item("file")

            assert self._widget.files == {'file'}

    def test_remove_item_not_in_files(self):
        item = create_autospec(ListItem)
        item.file_path = MagicMock(return_value='file')
        self._widget.currentItem = MagicMock()
        self._widget.remove_item(item)
        self._widget.currentItem.assert_not_called()

    def test_remove_item_curr_item(self):
        item = create_autospec(ListItem)
        item.file_path = 'file'
        item2 = create_autospec(ListItem)
        item2.file_path = 'file2'
        item3 = create_autospec(ListItem)
        item3.file_path = MagicMock(return_value='file3')
        self._widget.files = {'file', 'file2', 'file3'}
        self._widget.file_order = ['file', 'file2', 'file3']
        self._widget.currentItem = MagicMock(return_value=item2)
        self._widget.row = MagicMock(return_value=1)
        self._widget.setCurrentItem = MagicMock()
        self._widget.takeItem = MagicMock()
        self._widget.files_added = MagicMock()
        self._widget.files_added.emit = MagicMock()

        self._widget.remove_item(item2)
        self._widget.setCurrentItem.assert_called_once_with(None)
        self._widget.takeItem.assert_called_once_with(1)
        assert self._widget.files == {'file', 'file3'}
        assert self._widget.file_order == ['file', 'file3']
        self._widget.files_added.emit.assert_not_called()

    def test_remove_item(self):
        item = create_autospec(ListItem)
        item.file_path = 'file'
        item2 = create_autospec(ListItem)
        item2.file_path = 'file2'
        item3 = create_autospec(ListItem)
        item3.file_path = 'file3'
        self._widget.files = {'file', 'file2', 'file3'}
        self._widget.file_order = ['file', 'file2', 'file3']
        self._widget.currentItem = MagicMock(return_value=item)
        self._widget.row = MagicMock(return_value=2)
        self._widget.setCurrentItem = MagicMock()
        self._widget.takeItem = MagicMock()
        self._widget.files_added = MagicMock()
        self._widget.files_added.emit = MagicMock()

        self._widget.remove_item(item3)
        self._widget.setCurrentItem.assert_not_called()
        self._widget.takeItem.assert_called_once_with(2)
        assert self._widget.files == {'file', 'file2'}
        assert self._widget.file_order == ['file', 'file2']
        self._widget.files_added.emit.assert_not_called()

    def test_remove_item_last(self):
        item = create_autospec(ListItem)
        item.file_path = 'file'
        self._widget.files = {'file'}
        self._widget.file_order = ['file']
        self._widget.currentItem = MagicMock(return_value=None)
        self._widget.row = MagicMock(return_value=0)
        self._widget.setCurrentItem = MagicMock()
        self._widget.takeItem = MagicMock()
        self._widget.files_added = MagicMock()
        self._widget.files_added.emit = MagicMock()

        self._widget.remove_item(item)
        self._widget.setCurrentItem.assert_not_called()
        self._widget.takeItem.assert_called_once_with(0)
        assert self._widget.files == set()
        assert self._widget.file_order == []
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
        item = create_autospec(ListItem)
        item2 = create_autospec(ListItem)
        self._widget.checked = {item, item2}
        self._widget.remove_item = MagicMock()
        self._widget.files_selected = MagicMock()
        self._widget.files_selected.emit = MagicMock()
        self._widget.delete_checked()

        assert self._widget.checked == set()
        self._widget.remove_item.assert_has_calls([mock.call(item), mock.call(item2)])
        self._widget.files_selected.emit.assert_called_once_with(False)

    def test_check_evt_checked(self):
        item = create_autospec(ListItem)
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
        item = create_autospec(ListItem)
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
