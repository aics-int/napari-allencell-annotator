from unittest import mock
from unittest.mock import MagicMock, create_autospec

from napari_allencell_annotator.widgets.annotation_item import (
    AnnotationItem,
    QLineEdit,
    QGridLayout,
    QWidget,
    QLabel,
    QSpinBox,
    QComboBox,
)


class TestAnnotationItem:
    def setup_method(self):
        with mock.patch.object(AnnotationItem, "__init__", lambda x: None):
            self._item = AnnotationItem()
            self._item.name = create_autospec(QLineEdit)
            self._item.type = create_autospec(QComboBox)
            self._item.default_text = create_autospec(QLineEdit)
            self._item.default_options = create_autospec(QLineEdit)
            self._item.default_num = create_autospec(QSpinBox)
            self._item.default_check = create_autospec(QComboBox)

    def test_fill_vals_text(self):
        self._item.fill_vals_text("name", "default")

        self._item.type.setCurrentText.assert_called_once_with("text")
        self._item.name.setText.assert_called_once_with("name")
        self._item.default_text.setText.assert_called_once_with("default")

    def test_fill_vals_number(self):
        self._item.fill_vals_number("name", 3)

        self._item.type.setCurrentText.assert_called_once_with("number")
        self._item.name.setText.assert_called_once_with("name")
        self._item.default_num.setValue.assert_called_once_with(3)

    def test_fill_vals_check(self):
        self._item.fill_vals_check("name", True)

        self._item.type.setCurrentText.assert_called_once_with("checkbox")
        self._item.name.setText.assert_called_once_with("name")
        self._item.default_check.setCurrentText.assert_called_once_with("checked")

    def test_fill_vals_list(self):
        self._item.fill_vals_list("name", "one", ["one", "two", "three"])

        self._item.type.setCurrentText.assert_called_once_with("dropdown")
        self._item.name.setText.assert_called_once_with("name")
        self._item.default_text.setText.assert_called_once_with("one")
        self._item.default_options.setText.assert_called_once_with("one, two, three")

    def test_type_changed_dropdown(self):
        self._item.layout = create_autospec(QGridLayout)
        widget = create_autospec(QWidget)
        self._item.layout.itemAtPosition(0, 7).widget = MagicMock(return_value=widget)
        self._item.default_options_label = create_autospec(QLabel)

        self._item._type_changed("dropdown")

        widget.setParent.assert_called_once_with(None)
        self._item.layout.removeWidget.assert_called_once_with(widget)

        self._item.default_options.show.assert_called_once_with()
        self._item.default_options_label.show.assert_called_once_with()
        self._item.layout.addWidget.assert_called_once_with(self._item.default_text, 0, 7, 1, 2)

    def test_type_changed_checkbox(self):
        self._item.layout = create_autospec(QGridLayout)
        widget = create_autospec(QWidget)
        self._item.layout.itemAtPosition(0, 7).widget = MagicMock(return_value=widget)
        self._item.default_options_label = create_autospec(QLabel)
        self._item.default_check = MagicMock()
        self._item._type_changed("checkbox")

        widget.setParent.assert_called_once_with(None)
        self._item.layout.removeWidget.assert_called_once_with(widget)

        self._item.default_options.hide.assert_called_once_with()
        self._item.default_options_label.hide.assert_called_once_with()
        self._item.layout.addWidget.assert_called_once_with(self._item.default_check, 0, 7, 1, 2)

    def test_type_changed_number(self):
        self._item.layout = create_autospec(QGridLayout)
        widget = create_autospec(QWidget)
        self._item.layout.itemAtPosition(0, 7).widget = MagicMock(return_value=widget)
        self._item.default_options_label = create_autospec(QLabel)
        self._item.default_num = MagicMock()
        self._item._type_changed("number")

        widget.setParent.assert_called_once_with(None)
        self._item.layout.removeWidget.assert_called_once_with(widget)

        self._item.default_options.hide.assert_called_once_with()
        self._item.default_options_label.hide.assert_called_once_with()
        self._item.layout.addWidget.assert_called_once_with(self._item.default_num, 0, 7, 1, 2)

    def test_type_changed_text(self):
        self._item.layout = create_autospec(QGridLayout)
        widget = create_autospec(QWidget)
        self._item.layout.itemAtPosition(0, 7).widget = MagicMock(return_value=widget)
        self._item.default_options_label = create_autospec(QLabel)

        self._item._type_changed("text")

        widget.setParent.assert_called_once_with(None)
        self._item.layout.removeWidget.assert_called_once_with(widget)

        self._item.default_options.hide.assert_called_once_with()
        self._item.default_options_label.hide.assert_called_once_with()
        self._item.layout.addWidget.assert_called_once_with(self._item.default_text, 0, 7, 1, 2)

    def test_get_data_none_name_text_none_default(self):
        self._item.name.text = MagicMock(return_value=None)
        self._item._unhighlight = MagicMock()
        self._item.highlight = MagicMock()
        self._item.type.currentText = MagicMock(return_value="text")
        self._item.default_text.text = MagicMock(return_value=None)
        assert self._item.get_data() == (False, None, {"default": "", "type": "string"}, " Invalid Name. ")
        self._item._unhighlight.assert_called_once_with(self._item.name)
        self._item.highlight.assert_called_once_with(self._item.name)

    def test_get_data_space_name_text_space_default(self):
        self._item.name.text = MagicMock(return_value=" ")
        self._item._unhighlight = MagicMock()
        self._item.highlight = MagicMock()
        self._item.type.currentText = MagicMock(return_value="text")
        self._item.default_text.text = MagicMock(return_value=" ")
        assert self._item.get_data() == (False, " ", {"default": "", "type": "string"}, " Invalid Name. ")
        self._item._unhighlight.assert_called_once_with(self._item.name)
        self._item.highlight.assert_called_once_with(self._item.name)

    def test_get_data_empty_name_text_empty_default(self):
        self._item.name.text = MagicMock(return_value="")
        self._item._unhighlight = MagicMock()
        self._item.highlight = MagicMock()
        self._item.type.currentText = MagicMock(return_value="text")
        self._item.default_text.text = MagicMock(return_value="")
        assert self._item.get_data() == (False, "", {"default": "", "type": "string"}, " Invalid Name. ")
        self._item._unhighlight.assert_called_once_with(self._item.name)
        self._item.highlight.assert_called_once_with(self._item.name)

    def test_get_data_text_default(self):
        self._item.name.text = MagicMock(return_value="name")
        self._item._unhighlight = MagicMock()
        self._item.highlight = MagicMock()
        self._item.type.currentText = MagicMock(return_value="text")
        self._item.default_text.text = MagicMock(return_value="default")
        assert self._item.get_data() == (True, "name", {"default": "default", "type": "string"}, "")
        self._item._unhighlight.assert_called_once_with(self._item.name)
        self._item.highlight.assert_not_called()

    def test_get_data_default_empty_dropdown_options_none(self):
        self._item.name.text = MagicMock(return_value="name")
        self._item._unhighlight = MagicMock()
        self._item.highlight = MagicMock()
        self._item.default_options.text = MagicMock(return_value=None)
        self._item.type.currentText = MagicMock(return_value="dropdown")
        self._item.default_text.text = MagicMock(return_value="")
        assert self._item.get_data() == (False, "name", {"default": ""}, " Must provide two dropdown options. ")
        self._item._unhighlight.assert_has_calls([mock.call(self._item.name), mock.call(self._item.default_options)])
        self._item.highlight.assert_called_once_with(self._item.default_options)

    def test_get_data_default_not_empty_dropdown_options_one(self):
        self._item.name.text = MagicMock(return_value="name")
        self._item._unhighlight = MagicMock()
        self._item.highlight = MagicMock()
        self._item.default_options.text = MagicMock(return_value="onestring")
        self._item.type.currentText = MagicMock(return_value="dropdown")
        self._item.default_text.text = MagicMock(return_value="default")
        assert self._item.get_data() == (False, "name", {"default": "default"}, " Must provide two dropdown options. ")
        self._item._unhighlight.assert_has_calls([mock.call(self._item.name), mock.call(self._item.default_options)])
        self._item.highlight.assert_called_once_with(self._item.default_options)

    def test_get_data_default_empty_dropdown_options_mult(self):
        self._item.name.text = MagicMock(return_value="name")
        self._item._unhighlight = MagicMock()
        self._item.highlight = MagicMock()
        self._item.default_options.text = MagicMock(return_value="1,2")
        self._item.type.currentText = MagicMock(return_value="dropdown")
        self._item.default_text.text = MagicMock(return_value="")
        assert self._item.get_data() == (True, "name", {"default": "", "options": ["1", "2"], "type": "list"}, "")
        self._item._unhighlight.assert_has_calls([mock.call(self._item.name), mock.call(self._item.default_options)])
        self._item.highlight.assert_not_called()

    def test_get_data_default_not_in_dropdown_options_mult(self):
        self._item.name.text = MagicMock(return_value="name")
        self._item._unhighlight = MagicMock()
        self._item.highlight = MagicMock()
        self._item.default_options.text = MagicMock(return_value="1,2")
        self._item.type.currentText = MagicMock(return_value="dropdown")
        self._item.default_text.text = MagicMock(return_value="3")
        assert self._item.get_data() == (True, "name", {"default": "3", "options": ["1", "2", "3"], "type": "list"}, "")
        self._item._unhighlight.assert_has_calls([mock.call(self._item.name), mock.call(self._item.default_options)])
        self._item.highlight.assert_not_called()

    def test_get_data_default_in_dropdown_options_mult(self):
        self._item.name.text = MagicMock(return_value="name")
        self._item._unhighlight = MagicMock()
        self._item.highlight = MagicMock()
        self._item.default_options.text = MagicMock(return_value=" 1,2,3 ")
        self._item.type.currentText = MagicMock(return_value="dropdown")
        self._item.default_text.text = MagicMock(return_value=" 3")
        assert self._item.get_data() == (True, "name", {"default": "3", "options": ["1", "2", "3"], "type": "list"}, "")
        self._item._unhighlight.assert_has_calls([mock.call(self._item.name), mock.call(self._item.default_options)])
        self._item.highlight.assert_not_called()

    def test_get_data_default_not_in_dropdown_options_mult(self):
        self._item.name.text = MagicMock(return_value="name")
        self._item._unhighlight = MagicMock()
        self._item.highlight = MagicMock()
        self._item.default_options.text = MagicMock(return_value=" 1,2,3 ")
        self._item.type.currentText = MagicMock(return_value="dropdown")
        self._item.default_text.text = MagicMock(return_value=" 4")
        assert self._item.get_data() == (
            True,
            "name",
            {"default": "4", "options": ["1", "2", "3", "4"], "type": "list"},
            "",
        )
        self._item._unhighlight.assert_has_calls([mock.call(self._item.name), mock.call(self._item.default_options)])
        self._item.highlight.assert_not_called()

    def test_get_data_default_exists_dropdown_options_mult_none(self):
        self._item.name.text = MagicMock(return_value="name")
        self._item._unhighlight = MagicMock()
        self._item.highlight = MagicMock()
        self._item.default_options.text = MagicMock(return_value=" 1,2,,3 ")
        self._item.type.currentText = MagicMock(return_value="dropdown")
        self._item.default_text.text = MagicMock(return_value="4")
        assert self._item.get_data() == (
            False,
            "name",
            {"default": "4", "options": ["1", "2", "", "3", "4"], "type": "list"},
            " Invalid options for dropdown. ",
        )
        self._item._unhighlight.assert_has_calls([mock.call(self._item.name), mock.call(self._item.default_options)])
        self._item.highlight.assert_called_once_with(self._item.default_options)

    def test_get_data_default_exists_dropdown_options_mult_space(self):
        self._item.name.text = MagicMock(return_value="name")
        self._item._unhighlight = MagicMock()
        self._item.highlight = MagicMock()
        self._item.default_options.text = MagicMock(return_value=" 1,2, ,3 ")
        self._item.type.currentText = MagicMock(return_value="dropdown")
        self._item.default_text.text = MagicMock(return_value="4")
        assert self._item.get_data() == (
            False,
            "name",
            {"default": "4", "options": ["1", "2", "", "3", "4"], "type": "list"},
            " Invalid options for dropdown. ",
        )
        self._item._unhighlight.assert_has_calls([mock.call(self._item.name), mock.call(self._item.default_options)])
        self._item.highlight.assert_called_once_with(self._item.default_options)

    def test_get_data_default_exists_dropdown_options_mult_trailing_comma(self):
        self._item.name.text = MagicMock(return_value="name")
        self._item._unhighlight = MagicMock()
        self._item.highlight = MagicMock()
        self._item.default_options.text = MagicMock(return_value=" 1,2,3,")
        self._item.type.currentText = MagicMock(return_value="dropdown")
        self._item.default_text.text = MagicMock(return_value="4")
        assert self._item.get_data() == (
            False,
            "name",
            {"default": "4", "options": ["1", "2", "3", "", "4"], "type": "list"},
            " Invalid options for dropdown. ",
        )
        self._item._unhighlight.assert_has_calls([mock.call(self._item.name), mock.call(self._item.default_options)])
        self._item.highlight.assert_called_once_with(self._item.default_options)

    def test_get_data_invalid_dropdown_options_invalid_name(self):
        self._item.name.text = MagicMock(return_value="")
        self._item._unhighlight = MagicMock()
        self._item.highlight = MagicMock()
        self._item.default_options.text = MagicMock(return_value=" 1,2,,3 ")
        self._item.type.currentText = MagicMock(return_value="dropdown")
        self._item.default_text.text = MagicMock(return_value="4")
        assert self._item.get_data() == (
            False,
            "",
            {"default": "4", "options": ["1", "2", "", "3", "4"], "type": "list"},
            " Invalid Name.  Invalid options for dropdown. ",
        )
        self._item._unhighlight.assert_has_calls([mock.call(self._item.name), mock.call(self._item.default_options)])
        self._item.highlight.assert_has_calls([mock.call(self._item.name), mock.call(self._item.default_options)])

    def test_get_data_too_few_dropdown_options_invalid_name(self):
        self._item.name.text = MagicMock(return_value="")
        self._item._unhighlight = MagicMock()
        self._item.highlight = MagicMock()
        self._item.default_options.text = MagicMock(return_value=" 1")
        self._item.type.currentText = MagicMock(return_value="dropdown")
        self._item.default_text.text = MagicMock(return_value="4")
        assert self._item.get_data() == (
            False,
            "",
            {"default": "4"},
            " Invalid Name.  Must provide two dropdown options. ",
        )
        self._item._unhighlight.assert_has_calls([mock.call(self._item.name), mock.call(self._item.default_options)])
        self._item.highlight.assert_has_calls([mock.call(self._item.name), mock.call(self._item.default_options)])

    def test_get_data_number(self):
        self._item.name.text = MagicMock(return_value="name")
        self._item._unhighlight = MagicMock()
        self._item.highlight = MagicMock()
        self._item.type.currentText = MagicMock(return_value="number")
        self._item.default_num = MagicMock()
        self._item.default_num.value = MagicMock(return_value=4)
        assert self._item.get_data() == (True, "name", {"default": 4, "type": "number"}, "")
        self._item._unhighlight.assert_has_calls([mock.call(self._item.name)])
        self._item.highlight.assert_not_called()

    def test_get_data_checked(self):
        self._item.name.text = MagicMock(return_value="name")
        self._item._unhighlight = MagicMock()
        self._item.type.currentText = MagicMock(return_value="checkbox")
        self._item.default_check = MagicMock()
        self._item.default_check.currentText = MagicMock(return_value="checked")
        assert self._item.get_data() == (True, "name", {"default": True, "type": "bool"}, "")
        self._item._unhighlight.assert_has_calls([mock.call(self._item.name)])

    def test_get_data_unchecked(self):
        self._item.name.text = MagicMock(return_value="name")
        self._item._unhighlight = MagicMock()
        self._item.type.currentText = MagicMock(return_value="checkbox")
        self._item.default_check = MagicMock()
        self._item.default_check.currentText = MagicMock(return_value="unchecked")
        assert self._item.get_data() == (True, "name", {"default": False, "type": "bool"}, "")
        self._item._unhighlight.assert_has_calls([mock.call(self._item.name)])

    def test_highlight(self):
        objct = create_autospec(QLineEdit)
        self._item.highlight(objct)
        objct.setStyleSheet.assert_called_once_with("""QLineEdit{border: 1px solid red}""")

    def test_unhighlight(self):
        objct = create_autospec(QLineEdit)
        self._item._unhighlight(objct)
        objct.setStyleSheet.assert_called_once_with("""QLineEdit{}""")
