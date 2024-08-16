from unittest import mock
from unittest.mock import MagicMock, patch, create_autospec

from PyQt5.QtWidgets import QPushButton, QLineEdit

from napari_allencell_annotator.model.combo_key import ComboKey

from napari_allencell_annotator.model.key import Key
from napari_allencell_annotator.widgets.template_item import ItemType

from napari_allencell_annotator.widgets.template_list import (
    TemplateList,
    TemplateItem,
    QSpinBox,
    QCheckBox,
    QComboBox,
)
import pytest


@pytest.fixture()
def template_list(qtbot) -> TemplateList:
    return TemplateList()


def test_add_item_string(template_list: TemplateList) -> None:

    # ACT
    template_list.add_item("test_name", Key("string", "test_default"))

    # ASSERT
    assert template_list.count() == 1
    item: TemplateItem = template_list.item(0)
    assert item.name.text() == "test_name"
    assert item.type == ItemType.STRING
    assert item.default == "test_default"
    assert isinstance(item.editable_widget, QLineEdit)

    # test template_list.items
    assert len(template_list.items) == 1
    assert template_list.items[0] == item


def test_add_item_number(template_list: TemplateList) -> None:
    # ACT
    template_list.add_item("test_name", Key("number", 0))

    # ASSERT
    assert template_list.count() == 1
    item: TemplateItem = template_list.item(0)
    assert item.name.text() == "test_name"
    assert item.type == ItemType.NUMBER
    assert item.default == 0
    assert isinstance(item.editable_widget, QSpinBox)
    assert item.editable_widget.value() == 0

    # test template_list.items
    assert len(template_list.items) == 1
    assert template_list.items[0] == item


def test_add_item_bool(template_list: TemplateList) -> None:
    # ACT
    template_list.add_item("test_name", Key("bool", True))

    # ASSERT
    assert template_list.count() == 1
    item: TemplateItem = template_list.item(0)
    assert item.name.text() == "test_name"
    assert item.type == ItemType.BOOL
    assert item.default
    assert isinstance(item.editable_widget, QCheckBox)
    assert item.editable_widget.isChecked()

    # test template_list.items
    assert len(template_list.items) == 1
    assert template_list.items[0] == item


def test_add_item_list(template_list: TemplateList) -> None:
    # ACT
    template_list.add_item("test_name", ComboKey(list, ["test_default", "test_other_option"], "test_default"))

    # ASSERT
    assert template_list.count() == 1
    item: TemplateItem = template_list.item(0)
    assert item.name.text() == "test_name"
    assert item.type == ItemType.LIST
    assert item.default == "test_default"
    assert isinstance(item.editable_widget, QComboBox)
    assert item.editable_widget.itemText(0) == "test_default"
    assert item.editable_widget.itemText(1) == "test_other_option"
    assert item.editable_widget.currentText() == "test_default"

    # test template_list.items
    assert len(template_list.items) == 1
    assert template_list.items[0] == item


def test_add_item_point(template_list: TemplateList) -> None:
    # ACT
    template_list.add_item("test_name", Key("point", None))

    # ASSERT
    assert template_list.count() == 1
    item: TemplateItem = template_list.item(0)
    assert item.name.text() == "test_name"
    assert item.type == ItemType.POINT
    assert item.default is None
    assert isinstance(item.editable_widget, QPushButton)
    assert item.editable_widget.text() == "Select"

    # test template_list.items
    assert len(template_list.items) == 1
    assert template_list.items[0] == item


class TestTemplateList:
    def setup_method(self):
        with mock.patch.object(TemplateList, "__init__", lambda x: None):
            self._list = TemplateList()

    def test_items(self):
        self._list._items = []
        assert self._list.items == []

    def test_next_item_last(self):
        self._list._items = [1, 2, 3, 4]
        self._list.setCurrentRow = MagicMock()
        self._list.currentRow = MagicMock(return_value=3)
        self._list.next_item()
        self._list.setCurrentRow.assert_called_once_with(0)

    def test_next_item(self):
        self._list._items = [1, 2, 3, 4]
        self._list.setCurrentRow = MagicMock()
        self._list.currentRow = MagicMock(return_value=2)
        self._list.next_item()
        self._list.setCurrentRow.assert_called_once_with(3)

    def test_prev_item_zero(self):
        self._list.setCurrentRow = MagicMock()
        self._list.currentRow = MagicMock(return_value=0)
        self._list.prev_item()
        self._list.setCurrentRow.assert_not_called()

    def test_prev_item(self):
        self._list.setCurrentRow = MagicMock()
        self._list.currentRow = MagicMock(return_value=1)
        self._list.prev_item()
        self._list.setCurrentRow.assert_called_once_with(0)

    def test_create_evt_listeners(self):
        item1 = create_autospec(TemplateItem)
        item2 = create_autospec(TemplateItem)
        item3 = create_autospec(TemplateItem)
        self._list._items = [item1, item2, item3]
        self._list.create_evt_listeners()
        item1.create_evt_listener.assert_called_once_with()
        item2.create_evt_listener.assert_called_once_with()
        item3.create_evt_listener.assert_called_once_with()

    def test_clear_all(self):
        self._list._items = ["item"]
        self._list.height = 7
        self._list.clear = MagicMock()
        self._list.clear_all()

        self._list.clear.assert_called_once_with()
        assert self._list._items == []
        assert self._list.height == 0


# TODO fix tests
# @patch("napari_allencell_annotator.widgets.template_list.QLineEdit.__init__")
# @patch("napari_allencell_annotator.widgets.template_list.TemplateItem.__init__")
# def test_add_item_string(self, mock_init_temp, mock_init):
#
#     mock_init.return_value = None
#     mock_init_temp.return_value = None
#     TemplateItem.widget = MagicMock()
#     TemplateItem.widget.sizeHint = MagicMock()
#     TemplateItem.widget.sizeHint().height = MagicMock(return_value=20)
#     self._list.setMaximumHeight = MagicMock()
#     self._list._items = []
#     self._list.height = 10
#
#     self._list.add_item("name", {"type": "string", "default": "default"})
#
#     mock_init.assert_called_once_with("default")
#     mock_init_temp.assert_called_once()
#     self._list.items == [mock_init_temp]
#     TemplateItem.widget.sizeHint().height.assert_called_once()
#     self._list.height = 30
#     self._list.setMaximumHeight.assert_called_once_with(30)


# @patch("napari_allencell_annotator.widgets.template_list.QSpinBox.__init__")
# @patch("napari_allencell_annotator.widgets.template_list.TemplateItem.__init__")
# def test_add_item_number(self, mock_init_temp, mock_init):
#     QSpinBox.setValue = MagicMock()
#     mock_init.return_value = None
#     mock_init_temp.return_value = None
#     TemplateItem.widget = MagicMock()
#     TemplateItem.widget.sizeHint = MagicMock()
#     TemplateItem.widget.sizeHint().height = MagicMock(return_value=20)
#     self._list.setMaximumHeight = MagicMock()
#     self._list._items = []
#     self._list.height = 10
#
#     self._list.add_item("name", {"type": "number", "default": "default"})
#
#     mock_init.assert_called_once_with()
#     QSpinBox.setValue.assert_called_once_with("default")
#     mock_init_temp.assert_called_once()
#     self._list.items == [mock_init_temp]
#     TemplateItem.widget.sizeHint().height.assert_called_once()
#     self._list.height = 30
#     self._list.setMaximumHeight.assert_called_once_with(30)
#
# @patch("napari_allencell_annotator.widgets.template_list.QCheckBox.__init__")
# @patch("napari_allencell_annotator.widgets.template_list.TemplateItem.__init__")
# def test_add_item_bool(self, mock_init_temp, mock_init):
#     QCheckBox.setChecked = MagicMock()
#     mock_init.return_value = None
#     mock_init_temp.return_value = None
#     TemplateItem.widget = MagicMock()
#     TemplateItem.widget.sizeHint = MagicMock()
#     TemplateItem.widget.sizeHint().height = MagicMock(return_value=20)
#     self._list.setMaximumHeight = MagicMock()
#     self._list._items = []
#     self._list.height = 10
#
#     self._list.add_item("name", {"type": "bool", "default": False})
#
#     mock_init.assert_called_once_with()
#     QCheckBox.setChecked.assert_called_once_with(False)
#     mock_init_temp.assert_called_once()
#     self._list.items == [mock_init_temp]
#     TemplateItem.widget.sizeHint().height.assert_called_once()
#     self._list.height = 30
#     self._list.setMaximumHeight.assert_called_once_with(30)
#
# @patch("napari_allencell_annotator.widgets.template_list.QComboBox.__init__")
# @patch("napari_allencell_annotator.widgets.template_list.TemplateItem.__init__")
# def test_add_item_list(self, mock_init_temp, mock_init):
#     QComboBox.addItem = MagicMock()
#     QComboBox.setCurrentText = MagicMock()
#     mock_init.return_value = None
#     mock_init_temp.return_value = None
#     TemplateItem.widget = MagicMock()
#     TemplateItem.widget.sizeHint = MagicMock()
#     TemplateItem.widget.sizeHint().height = MagicMock(return_value=20)
#     self._list.setMaximumHeight = MagicMock()
#     self._list._items = []
#     self._list.height = 10
#
#     self._list.add_item("name", {"type": "list", "default": "default", "options": ["a", "b", "c"]})
#
#     mock_init.assert_called_once_with()
#     QComboBox.addItem.assert_has_calls([mock.call("a"), mock.call("b"), mock.call("c")])
#     QComboBox.setCurrentText.assert_called_once_with("default")
#     mock_init_temp.assert_called_once()
#     self._list.items == [mock_init_temp]
#     TemplateItem.widget.sizeHint().height.assert_called_once()
#     self._list.height = 30
#     self._list.setMaximumHeight.assert_called_once_with(30)
