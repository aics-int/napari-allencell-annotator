from enum import Enum
from typing import Any

from qtpy.QtWidgets import QLayout
from qtpy.QtWidgets import QListWidgetItem, QListWidget, QWidget, QHBoxLayout, QLabel


class ItemType(Enum):
    """"""

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

    def __init__(self, parent: QListWidget, name: str, type: ItemType, default: Any, editable_widget: QWidget):
        QListWidgetItem.__init__(self, parent)
        self._type: ItemType = type
        self.default: Any = default
        self.value: Any = default
        self.editable_widget: QWidget = editable_widget
        self.widget = QWidget()

        self.layout = QHBoxLayout()
        self.name = QLabel(name)
        self.layout.addWidget(self.name)
        self.layout.addWidget(self.editable_widget)

        self.editable_widget.setEnabled(True)
        self.layout.setContentsMargins(2, 12, 8, 12)
        self.layout.setSpacing(2)
        self.layout.setSizeConstraint(QLayout.SetMinimumSize)
        self.widget.setLayout(self.layout)
        self.setSizeHint(self.widget.minimumSizeHint())
        parent.setItemWidget(self, self.widget)

    @property
    def type(self) -> ItemType:
        """Annotation type (string, number, bool, list)"""
        return self._type

    def set_default_value(self):
        """Set the value for the annotation to the default."""
        self.set_value(self.default)

    def set_value(self, val: Any):
        """
        Set the value of the annotation.

        Parameters
        ----------
        val : Any
        """
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
        """
        Return the current annotation value.

        Returns
        -------
        Any
        """
        if self._type == ItemType.STRING:
            return self.editable_widget.text()
        elif self._type == ItemType.NUMBER:
            return self.editable_widget.value()
        elif self._type == ItemType.BOOL:
            return self.editable_widget.isChecked()
        elif self._type == ItemType.LIST:
            return self.editable_widget.currentText()

    def highlight(self):
        """Highlight the editable widget in blue."""
        style = ""
        if self._type == ItemType.STRING:
            style = """QLineEdit{border: 1px solid #39a844}"""
        elif self._type == ItemType.NUMBER:
            style = """QSpinBox{border: 1px solid #39a844}"""
        elif self._type == ItemType.BOOL:
            style = """QCheckBox:indicator{border: 1px solid #39a844}"""
        elif self._type == ItemType.LIST:
            style = """QComboBox{border: 1px solid #39a844}"""
        self.editable_widget.setStyleSheet(style)

    def unhighlight(self):
        """Unhighlight the editable widget."""
        style = ""
        if self._type == ItemType.STRING:
            style = """QLineEdit{}"""
        elif self._type == ItemType.NUMBER:
            style = """QSpinBox{}"""
        elif self._type == ItemType.BOOL:
            style = """QCheckBox:indicator{}"""
        elif self._type == ItemType.LIST:
            style = """QComboBox{}"""
        self.editable_widget.setStyleSheet(style)
