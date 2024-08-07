from typing import Tuple, List, Optional, Any

from PyQt5.QtWidgets import QLayoutItem
from qtpy.QtWidgets import QLayout
from qtpy import QtWidgets
from qtpy.QtWidgets import (
    QListWidgetItem,
    QListWidget,
    QWidget,
    QHBoxLayout,
    QLineEdit,
    QComboBox,
    QLabel,
    QSpinBox,
    QGridLayout,
    QCheckBox,
)

from napari_allencell_annotator.model.combo_key import ComboKey
from napari_allencell_annotator.model.key import Key


class AnnotationItem(QListWidgetItem):
    """
    A class used to create custom annotation QListWidgetItems.
    """

    def __init__(self, parent: QListWidget):
        QListWidgetItem.__init__(self, parent)
        self.widget = QWidget()
        self.layout = QGridLayout()
        name_label = QLabel("Name:")

        self.name = QLineEdit()
        self.name.setPlaceholderText("Enter name")

        type_label = QLabel("Type:")
        self.type_selection_combo = QComboBox()
        self.type_selection_combo.addItems(["text", "number", "checkbox", "dropdown", "point"])
        self.name.setWhatsThis("name")
        self.type_selection_combo.setWhatsThis("type")
        self.name_widget = QWidget()
        self.name_layout = QHBoxLayout()
        self.check = QCheckBox()
        self.check.setToolTip("Check box to select this annotation for deletion.")

        self.name_layout.addWidget(self.check)
        self.name_layout.addWidget(name_label)
        self.name_layout.setSizeConstraint(QLayout.SetMinimumSize)
        self.name_widget.setLayout(self.name_layout)
        self.layout.addWidget(self.name_widget, 0, 0, 1, 1)
        self.layout.addWidget(self.name, 0, 1, 1, 2)
        self.layout.addWidget(type_label, 0, 3, 1, 1)
        self.layout.addWidget(self.type_selection_combo, 0, 4, 1, 2)
        self.default_label: QLabel = QLabel("Default:")
        self.default_text = QLineEdit()
        self.default_text.setPlaceholderText("Optional: Default Text")
        self.default_num = QSpinBox()
        self.default_num.setValue(2)
        self.default_check = QComboBox()
        self.default_check.addItems(["checked", "unchecked"])
        self.default_options_label = QLabel("Options:")
        self.default_options = QLineEdit()
        self.default_options.setPlaceholderText("Enter a comma separated list")

        self.default_options.setSizePolicy(QtWidgets.QSizePolicy.Policy.Ignored, QtWidgets.QSizePolicy.Policy.Preferred)
        self.default_options.setMinimumWidth(300)

        sp_retain = QtWidgets.QSizePolicy()
        sp_retain.setRetainSizeWhenHidden(True)
        self.default_options.setSizePolicy(sp_retain)
        self.default_options_label.setSizePolicy(sp_retain)

        self.layout.addWidget(self.default_label, 0, 6, 1, 1)
        self.layout.addWidget(self.default_text, 0, 7, 1, 2)
        self.layout.addWidget(self.default_options_label, 1, 1, 1, 1)
        self.layout.addWidget(self.default_options, 1, 2, 1, 7)
        self.default_options.hide()
        self.default_options_label.hide()

        self.layout.setContentsMargins(5, 5, 5, 15)

        self.widget.setLayout(self.layout)
        self.setSizeHint(self.widget.sizeHint())
        if parent is not None:
            parent.setItemWidget(self, self.widget)

        self.type_selection_combo.currentTextChanged.connect(self._type_changed)

    def fill_vals_text(self, name: str, default: str):
        """
        Fill in item name, default, and type for text.

        Parameters
        ----------
        name : str
            a name for the annotation
        default: str
            a default text value
        """
        self.type_selection_combo.setCurrentText("text")
        self.name.setText(name)
        self.default_text.setText(default)

    def fill_vals_number(self, name: str, default: int):
        """
        Fill in item name, default and type for number.

        Parameters
        ----------
        name : str
            a name for the annotation
        default: int
            a default number value
        """
        self.type_selection_combo.setCurrentText("number")
        self.name.setText(name)
        self.default_num.setValue(default)

    def fill_vals_check(self, name: str, default: bool):
        """
        Fill in name, default, and type for checkbox.

        Parameters
        ----------
        name : str
            a name for the annotation
        default: bool
            a bool default (True -> checked)
        """
        self.type_selection_combo.setCurrentText("checkbox")
        self.name.setText(name)
        if default:
            self.default_check.setCurrentText("checked")
        else:
            self.default_check.setCurrentText("unchecked")

    def fill_vals_list(self, name: str, default: str, options: List[str]):
        """
        Fill in item name, default, options, and type for dropdown.

        Parameters
        ----------
        name : str
            a name for the annotation
        default: str
            a default dropdown option
        options : List[str]
            a list of dropdown options
        """
        self.type_selection_combo.setCurrentText("dropdown")
        self.name.setText(name)
        self.default_text.setText(default)
        self.default_options.setText(", ".join(options))

    def fill_vals_point(self, name: str):
        self.type_selection_combo.setCurrentText("point")
        self.name.setText(name)

    def _type_changed(self, text: str):
        """
        Render the widgets which correspond to the new type

        Parameters
        ----------
        text : str
            the new type selected.
        """
        default_item: QLayoutItem = self.layout.itemAtPosition(0, 7)
        if default_item is not None:
            default_widget: QWidget = default_item.widget()
            default_widget.setParent(None)
            self.layout.removeWidget(default_widget)

        if text == "text":
            self.default_label.show()
            self.default_options.hide()
            self.default_options_label.hide()
            self.layout.addWidget(self.default_text, 0, 7, 1, 2)

        elif text == "number":
            self.default_label.show()
            self.default_options.hide()
            self.default_options_label.hide()
            self.layout.addWidget(self.default_num, 0, 7, 1, 2)

        elif text == "checkbox":
            self.default_label.show()
            self.default_options.hide()
            self.default_options_label.hide()
            self.layout.addWidget(self.default_check, 0, 7, 1, 2)

        elif text == "dropdown":
            self.default_label.show()
            self.default_options.show()
            self.default_options_label.show()
            self.layout.addWidget(self.default_text, 0, 7, 1, 2)

        else:
            self.default_label.hide()
            self.default_options.hide()
            self.default_options_label.hide()

    def get_data(self) -> Tuple[bool, str, Key, str]:
        """
        Highlight any invalid entries and return the data.

        Return True if all data is valid along with str name and a dictionary
        of annotation data.
        Return False if data is invalid, highlight the incorrect entries, and return
        an incomplete dictionary.

        Returns
        ------
        Tuple[bool, str, Dict]
            bool : True if entries are valid.
            str: name of annotation item
            Dict: annotation item data (type, default, options)
            str: error msg if applicable
        """

        # TODO: refactor this mess- bkim 7/1/20-24
        # bool valid if all annotation values are in the correct format
        error = ""
        valid: bool = True
        # test if annotation name is valid
        name: str = self.name.text()
        self._unhighlight(self.name)
        if name is None or name.isspace() or len(name) == 0:
            valid = False
            self.highlight(self.name)
            error = " Invalid Name. "

        key: Optional[Key] = None
        type: str = self.type_selection_combo.currentText()
        # dictionary of annotation type, to annotation keys
        default: Optional[Any] = None
        options: list[str] = []

        if type == "text" or type == "dropdown":
            # grab default text entry
            default = self.default_text.text()
            if default is None or len(default) == 0 or default.isspace():
                default = None
            else:
                default = default.strip()
                # default text exists
                default = default
            if type == "text":
                type = "string"
            else:
                type = "list"
                # type is options
                # comma separate list of options
                options_list = self.default_options.text()
                # unhighlight by default
                self._unhighlight(self.default_options)
                # if there is less than two options provided
                if options_list is None or len(options_list.split(",")) < 2:
                    valid = False
                    self.highlight(self.default_options)
                    error = error + " Must provide two dropdown options. "
                else:
                    options_list = [word.strip() for word in options_list.split(",")]
                    contained: bool = False
                    if default == "":
                        contained = True
                    for item in options_list:
                        # check each item in options
                        if len(item) == 0:
                            valid = False
                            self.highlight(self.default_options)
                            error = error + " Invalid options for dropdown. "
                            break
                        else:
                            if not contained and item == default:
                                contained = True
                    if default not in options_list:
                        error = f"Default value {default} is not in list of valid options"
                        valid = False
                    options = options_list
        elif type == "number":
            # number defaults are required by spinbox, always valid
            type = "number"
            default = self.default_num.value()
        elif type == "checkbox":
            # checkbox type default required by the drop down, always valid
            type = "bool"
            if self.default_check.currentText() == "checked":
                default = True
            else:
                default = False

        else:
            type = "point"
            default = None

        if type == "list":
            key = ComboKey("list", options, default)
        else:
            key = Key(type, default)
        return valid, name, key, error

    def highlight(self, objct: QWidget):
        objct.setStyleSheet("""QLineEdit{border: 1px solid red}""")

    def _unhighlight(self, objct: QWidget):
        objct.setStyleSheet("""QLineEdit{}""")
