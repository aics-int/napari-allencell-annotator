from enum import Enum
from typing import Any

from napari_allencell_annotator.model.annotation_model import AnnotatorModel
from qtpy.QtWidgets import QLayout
from qtpy.QtWidgets import QListWidgetItem, QListWidget, QWidget, QHBoxLayout, QLabel
from qtpy.QtCore import Qt


class ItemType(Enum):
    """"""

    STRING = "string"
    NUMBER = "number"
    BOOL = "bool"
    LIST = "list"
    POINT = "point"


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

    def __init__(
        self,
        parent: QListWidget,
        name: str,
        type: ItemType,
        default: Any,
        editable_widget: QWidget,
        annotator_model: AnnotatorModel,
    ):
        QListWidgetItem.__init__(self, parent)
        self._type: ItemType = type
        self.default: Any = default
        self.value: Any = default
        self.editable_widget: QWidget = editable_widget
        self.widget = QWidget()
        self.parent = parent
        self._annotation_model = annotator_model

        self.layout = QHBoxLayout()
        self.name = QLabel(name)

        if self.type != ItemType.POINT:
            self.layout.addWidget(self.name)
            self.layout.addWidget(self.editable_widget)
            self.editable_widget.setEnabled(True)
        else:
            self.layout.addWidget(self.name, 0)
            self.layout.addWidget(self.editable_widget, 1, alignment=Qt.AlignCenter)
            self.editable_widget.setEnabled(False)

        self.layout.setContentsMargins(2, 12, 8, 12)
        self.layout.setSpacing(2)
        self.layout.setSizeConstraint(QLayout.SetMinimumSize)
        self.widget.setLayout(self.layout)
        self.setSizeHint(self.widget.minimumSizeHint())
        parent.setItemWidget(self, self.widget)
        self.create_evt_listener()

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

    def create_evt_listener(self):
        """Create event listener for editable widget edits to set the current item."""
        if self._type == ItemType.STRING:
            self.editable_widget.textEdited.connect(lambda: self.parent.setCurrentItem(self))
        elif self._type == ItemType.NUMBER:
            self.editable_widget.valueChanged.connect(lambda: self.parent.setCurrentItem(self))
        elif self._type == ItemType.BOOL:
            self.editable_widget.stateChanged.connect(lambda: self.parent.setCurrentItem(self))
        elif self._type == ItemType.LIST:
            self.editable_widget.activated.connect(lambda: self.parent.setCurrentItem(self))
        elif self._type == ItemType.POINT:
            self.editable_widget.clicked.connect(lambda: self.parent.setCurrentItem(self))
            self.editable_widget.clicked.connect(lambda: self._annotation_model.edit_points_layer(self.name.text()))
            self._annotation_model.annotation_started_changed.connect(self._handle_select_button_enabled)
            self._annotation_model.edit_points_layer_changed.connect(
                lambda name: self._handle_select_button_clicked(name)
            )

    def _handle_select_button_enabled(self):
        self.editable_widget.setEnabled(self._annotation_model.is_annotation_started())

    def _handle_select_button_clicked(self, annot_name):
        if self.name.text() == annot_name and self.editable_widget.text() == "Select":
            self.editable_widget.setText("Finish")
        else:
            self.editable_widget.setText("Select")

    def set_focus(self):
        """Set the annotating focus on the widget of the current item."""
        if self._type == ItemType.STRING:
            self.editable_widget.setFocus()
        elif self._type == ItemType.NUMBER:
            self.editable_widget.lineEdit().setFocus()
        elif self._type == ItemType.LIST:
            self.editable_widget.showPopup()

    def highlight(self):
        """Highlight the editable widget in blue."""
        style = ""
        if self._type == ItemType.STRING:
            style = """QLineEdit{border: 1px solid #759e78}"""
        elif self._type == ItemType.NUMBER:
            style = """QSpinBox{border: 1px solid #759e78}"""
        elif self._type == ItemType.BOOL:
            style = """QCheckBox:indicator{border: 1px solid #759e78}"""
        elif self._type == ItemType.LIST:
            style = """QComboBox{border: 1px solid #759e78}"""
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
