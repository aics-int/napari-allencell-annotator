from unittest import mock
from unittest.mock import MagicMock, patch

from napari_allencell_annotator.widgets.template_list import (
    TemplateList,
    TemplateItem,
    QSpinBox,
    QCheckBox,
    QComboBox,
)


class TestTemplateList:
    def setup_method(self):
        with mock.patch.object(TemplateList, "__init__", lambda x: None):
            self._list = TemplateList()

    def test_items(self):
        self._list._items = []
        assert self._list.items == []

    def test_clear_all(self):
        self._list._items = ["item"]
        self._list.height = 7
        self._list.clear = MagicMock()
        self._list.clear_all()

        self._list.clear.assert_called_once_with()
        assert self._list._items == []
        assert self._list.height == 0

    @patch("napari_allencell_annotator.widgets.template_list.QLineEdit.__init__")
    @patch("napari_allencell_annotator.widgets.template_list.TemplateItem.__init__")
    def test_add_item_string(self, mock_init_temp, mock_init):

        mock_init.return_value = None
        mock_init_temp.return_value = None
        TemplateItem.widget = MagicMock()
        TemplateItem.widget.sizeHint = MagicMock()
        TemplateItem.widget.sizeHint().height = MagicMock(return_value=20)
        self._list.setMaximumHeight = MagicMock()
        self._list._items = []
        self._list.height = 10

        self._list.add_item("name", {"type": "string", "default": "default"})

        mock_init.assert_called_once_with("default")
        mock_init_temp.assert_called_once()
        self._list.items == [mock_init_temp]
        TemplateItem.widget.sizeHint().height.assert_called_once()
        self._list.height = 30
        self._list.setMaximumHeight.assert_called_once_with(30)

    @patch("napari_allencell_annotator.widgets.template_list.QSpinBox.__init__")
    @patch("napari_allencell_annotator.widgets.template_list.TemplateItem.__init__")
    def test_add_item_number(self, mock_init_temp, mock_init):
        QSpinBox.setValue = MagicMock()
        mock_init.return_value = None
        mock_init_temp.return_value = None
        TemplateItem.widget = MagicMock()
        TemplateItem.widget.sizeHint = MagicMock()
        TemplateItem.widget.sizeHint().height = MagicMock(return_value=20)
        self._list.setMaximumHeight = MagicMock()
        self._list._items = []
        self._list.height = 10

        self._list.add_item("name", {"type": "number", "default": "default"})

        mock_init.assert_called_once_with()
        QSpinBox.setValue.assert_called_once_with("default")
        mock_init_temp.assert_called_once()
        self._list.items == [mock_init_temp]
        TemplateItem.widget.sizeHint().height.assert_called_once()
        self._list.height = 30
        self._list.setMaximumHeight.assert_called_once_with(30)

    @patch("napari_allencell_annotator.widgets.template_list.QCheckBox.__init__")
    @patch("napari_allencell_annotator.widgets.template_list.TemplateItem.__init__")
    def test_add_item_bool(self, mock_init_temp, mock_init):
        QCheckBox.setChecked = MagicMock()
        mock_init.return_value = None
        mock_init_temp.return_value = None
        TemplateItem.widget = MagicMock()
        TemplateItem.widget.sizeHint = MagicMock()
        TemplateItem.widget.sizeHint().height = MagicMock(return_value=20)
        self._list.setMaximumHeight = MagicMock()
        self._list._items = []
        self._list.height = 10

        self._list.add_item("name", {"type": "bool", "default": False})

        mock_init.assert_called_once_with()
        QCheckBox.setChecked.assert_called_once_with(False)
        mock_init_temp.assert_called_once()
        self._list.items == [mock_init_temp]
        TemplateItem.widget.sizeHint().height.assert_called_once()
        self._list.height = 30
        self._list.setMaximumHeight.assert_called_once_with(30)

    @patch("napari_allencell_annotator.widgets.template_list.QComboBox.__init__")
    @patch("napari_allencell_annotator.widgets.template_list.TemplateItem.__init__")
    def test_add_item_list(self, mock_init_temp, mock_init):
        QComboBox.addItem = MagicMock()
        QComboBox.setCurrentText = MagicMock()
        mock_init.return_value = None
        mock_init_temp.return_value = None
        TemplateItem.widget = MagicMock()
        TemplateItem.widget.sizeHint = MagicMock()
        TemplateItem.widget.sizeHint().height = MagicMock(return_value=20)
        self._list.setMaximumHeight = MagicMock()
        self._list._items = []
        self._list.height = 10

        self._list.add_item("name", {"type": "list", "default": "default", "options": ["a", "b", "c"]})

        mock_init.assert_called_once_with()
        QComboBox.addItem.assert_has_calls([mock.call("a"), mock.call("b"), mock.call("c")])
        QComboBox.setCurrentText.assert_called_once_with("default")
        mock_init_temp.assert_called_once()
        self._list.items == [mock_init_temp]
        TemplateItem.widget.sizeHint().height.assert_called_once()
        self._list.height = 30
        self._list.setMaximumHeight.assert_called_once_with(30)
