from unittest import mock
from unittest.mock import create_autospec, MagicMock

from napari_allencell_annotator.widgets.template_item import TemplateItem, ItemType, QWidget


class TestTemplateItem:
    def setup_method(self):
        with mock.patch.object(TemplateItem, "__init__", lambda x: None):
            self._item = TemplateItem()

    def test_type(self):
        self._item._type = ItemType.STRING
        assert self._item.type == ItemType.STRING

    def test_set_default_value(self):
        self._item.default = "default"
        self._item.set_value = MagicMock()

        self._item.set_default_value()
        self._item.set_value.assert_called_once_with(self._item.default)

    def test_set_value_string(self):
        self._item._type = ItemType.STRING
        self._item.editable_widget = create_autospec(QWidget)
        self._item.editable_widget.setText = MagicMock()

        self._item.set_value("text")
        self._item.editable_widget.setText.assert_called_once_with("text")

    def test_set_value_num_int(self):
        self._item._type = ItemType.NUMBER
        self._item.editable_widget = create_autospec(QWidget)
        self._item.editable_widget.setValue = MagicMock()

        self._item.set_value(3)
        self._item.editable_widget.setValue.assert_called_once_with(3)

    def test_set_value_num_str(self):
        self._item._type = ItemType.NUMBER
        self._item.editable_widget = create_autospec(QWidget)
        self._item.editable_widget.setValue = MagicMock()

        self._item.set_value("3")
        self._item.editable_widget.setValue.assert_called_once_with(3)

    def test_set_value_bool_str(self):
        self._item._type = ItemType.BOOL
        self._item.editable_widget = create_autospec(QWidget)
        self._item.editable_widget.setChecked = MagicMock()

        self._item.set_value("True")
        self._item.editable_widget.setChecked.assert_called_once_with(True)

    def test_set_value_bool(self):
        self._item._type = ItemType.BOOL
        self._item.editable_widget = create_autospec(QWidget)
        self._item.editable_widget.setChecked = MagicMock()

        self._item.set_value(False)
        self._item.editable_widget.setChecked.assert_called_once_with(False)

    def test_get_value_str(self):
        self._item._type = ItemType.STRING
        self._item.editable_widget = create_autospec(QWidget)
        self._item.editable_widget.text = MagicMock(return_value="return")

        assert self._item.get_value() == "return"

    def test_get_value_num(self):
        self._item._type = ItemType.NUMBER
        self._item.editable_widget = create_autospec(QWidget)
        self._item.editable_widget.value = MagicMock(return_value="return")

        assert self._item.get_value() == "return"

    def test_get_value_bool(self):
        self._item._type = ItemType.BOOL
        self._item.editable_widget = create_autospec(QWidget)
        self._item.editable_widget.isChecked = MagicMock(return_value="return")

        assert self._item.get_value() == "return"

    def test_get_value_list(self):
        self._item._type = ItemType.LIST
        self._item.editable_widget = create_autospec(QWidget)
        self._item.editable_widget.currentText = MagicMock(return_value="return")

        assert self._item.get_value() == "return"

    def test_highlight_string(self):
        self._item._type = ItemType.STRING
        self._item.editable_widget = create_autospec(QWidget)
        self._item.highlight()
        self._item.editable_widget.setStyleSheet.assert_called_once_with("""QLineEdit{border: 1px solid #39a844}""")

    def test_highlight_num(self):
        self._item._type = ItemType.NUMBER
        self._item.editable_widget = create_autospec(QWidget)
        self._item.highlight()
        self._item.editable_widget.setStyleSheet.assert_called_once_with("""QSpinBox{border: 1px solid #39a844}""")

    def test_highlight_bool(self):
        self._item._type = ItemType.BOOL
        self._item.editable_widget = create_autospec(QWidget)
        self._item.highlight()
        self._item.editable_widget.setStyleSheet.assert_called_once_with(
            """QCheckBox:indicator{border: 1px solid #39a844}"""
        )

    def test_highlight_list(self):
        self._item._type = ItemType.LIST
        self._item.editable_widget = create_autospec(QWidget)
        self._item.highlight()
        self._item.editable_widget.setStyleSheet.assert_called_once_with("""QComboBox{border: 1px solid #39a844}""")

    def test_unhighlight_str(self):
        self._item._type = ItemType.STRING
        self._item.editable_widget = create_autospec(QWidget)
        self._item.unhighlight()
        self._item.editable_widget.setStyleSheet.assert_called_once_with("""QLineEdit{}""")

    def test_unhighlight_num(self):
        self._item._type = ItemType.NUMBER
        self._item.editable_widget = create_autospec(QWidget)
        self._item.unhighlight()
        self._item.editable_widget.setStyleSheet.assert_called_once_with("""QSpinBox{}""")

    def test_unhighlight_bool(self):
        self._item._type = ItemType.BOOL
        self._item.editable_widget = create_autospec(QWidget)
        self._item.unhighlight()
        self._item.editable_widget.setStyleSheet.assert_called_once_with("""QCheckBox:indicator{}""")

    def test_unhighlight_list(self):
        self._item._type = ItemType.LIST
        self._item.editable_widget = create_autospec(QWidget)
        self._item.unhighlight()
        self._item.editable_widget.setStyleSheet.assert_called_once_with("""QComboBox{}""")
