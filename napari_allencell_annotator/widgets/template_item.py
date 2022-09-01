from enum import Enum
from typing import Tuple, Dict, List, Any

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


class ItemType(Enum):
    STRING = "string"
    NUMBER = "number"
    BOOL = "bool"
    LIST = "list"


class TemplateItem(QListWidgetItem):
    """
    A class used to show an annotation template QListWidgetItems.

    Attributes
    ----------
    type : ItemType
    default : Any
    editable_widget : QWidget
    value
    """

    def __init__(self, parent: QListWidget, name : str, type: ItemType, default : Any, editable_widget : QWidget):
        QListWidgetItem.__init__(self, parent)
        self._type = type
        self.default = default
        self.value = default
        self.editable_widget = editable_widget
        self.widget = QWidget()
        self.layout = QHBoxLayout()
        self.name = QLabel(name)
        self.layout.addWidget(self.name)
        self.layout.addWidget(self.editable_widget)

        self.setSizeHint(self.editable_widget.minimumSizeHint())
        parent.setItemWidget(self, self.widget)

        self.editable_widget.setEnabled(True)
        self.layout.setContentsMargins(2, 12, 8, 12)
        self.layout.setSpacing(2)
        self.layout.setSizeConstraint(QLayout.SetMinimumSize)
        self.widget.setLayout(self.layout)

    @property
    def type(self) -> ItemType:
        return self._type

    def set_default_value(self):
        self.set_value(self.default)

    def set_value(self, val : Any):
        if self._type == ItemType.STRING:
            self.editable_widget.setText(val)
        elif self._type == ItemType.NUMBER:
            self.editable_widget.setValue(int(val))
        elif self._type == ItemType.BOOL:
            if isinstance(val, str):
                # val is a str from previous annotation
                self.editable_widget.setChecked(eval(val))
            else:
                # val is bool from default vals
                self.editable_widget.setChecked(val)
        elif self._type == ItemType.LIST:
            self.editable_widget.setCurrentText(val)

    def get_value(self) -> Any:
        if self._type == ItemType.STRING:
            return self.editable_widget.text()
        elif self._type == ItemType.NUMBER:
            return self.editable_widget.value()
        elif self._type == ItemType.BOOL:
            return self.editable_widget.isChecked()
        elif self._type == ItemType.LIST:
            self.editable_widget.currentText()

    # def set_default(self, value : Any):
    #     """
    #     Set the default property to shuffled or unshuffled.
    #
    #     Parameters
    #     ----------
    #     value : Any
    #     """
    #     self._default = value

    # @property
    # def editable_widget(self) -> QWidget:
    #     """
    #     Current editable widget of the item.
    #
    #     Returns
    #     -------
    #     QWidget
    #         the shuffled property.
    #     """
    #     return self._editable_widget

    # def set_editable_widget(self, widget : QWidget):
    #     """
    #     Set the shuffled property to shuffled or unshuffled.
    #
    #     Parameters
    #     ----------
    #     widget : QWidget
    #     """
    #     self._editable_widget = widget

    def highlight(self):
        style = ""
        if self._type == ItemType.STRING:
            style = """QLineEdit{border: 1px solid cyan}"""
        elif self._type == ItemType.NUMBER:
            style = """QSpinBox{border: 1px solid cyan}"""
        elif self._type == ItemType.BOOL:
            style = """QCheckBox{border: 1px solid cyan}"""
        elif self._type == ItemType.LIST:
            style = """QComboBox{border: 1px solid cyan}"""
        self.editable_widget.setStyleSheet(style)

    def _unhighlight(self):
        style = ""
        if self._type == ItemType.STRING:
            style = """QLineEdit{}"""
        elif self._type == ItemType.NUMBER:
            style = """QSpinBox{}"""
        elif self._type == ItemType.BOOL:
            style = """QCheckBox{}"""
        elif self._type == ItemType.LIST:
            style = """QComboBox{border: 1px solid red}"""
        self.editable_widget.setStyleSheet(style)
