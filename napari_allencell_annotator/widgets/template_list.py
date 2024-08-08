from typing import Any, List

from PyQt5.QtWidgets import QPushButton
from qtpy import QtWidgets
from qtpy.QtWidgets import QLineEdit, QCheckBox, QComboBox, QSpinBox
from qtpy.QtWidgets import QSizePolicy
from qtpy.QtWidgets import QListWidget

from napari_allencell_annotator.model.combo_key import ComboKey
from napari_allencell_annotator.model.key import Key
from napari_allencell_annotator.widgets.template_item import TemplateItem, ItemType
from napari_allencell_annotator._style import Style


class TemplateList(QListWidget):
    """
    A class used to create a QListWidget for annotation templates.

    Properties
    ----------
    items : List[TemplateItem]

    """

    def __init__(self):
        QListWidget.__init__(self)

        self.setStyleSheet(Style.get_stylesheet("main.qss"))
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # todo single selection
        self._items: List[TemplateItem] = []
        self.height: int = 0
        self.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)

    @property
    def items(self) -> List[TemplateItem]:
        """
        Item property.

        Returns
        -------
        List[TemplateItem]
            a list of items.
        """
        return self._items

    def next_item(self):
        """Move the current item down one annotation."""
        curr_row = self.currentRow()
        if curr_row < len(self._items) - 1:
            next_row = curr_row + 1
            self.setCurrentRow(next_row)
        else:
            # if at last start over
            self.setCurrentRow(0)

    def prev_item(self):
        """Move the current item up one annotation."""
        curr_row = self.currentRow()
        if curr_row > 0:
            next_row = curr_row - 1
            self.setCurrentRow(next_row)

    def create_evt_listeners(self):
        """Create annotating event listeners for each item."""
        for item in self.items:
            item.create_evt_listener()

    def clear_all(self):
        """
        Clear all data.

        Reset height, items, list.
        """

        self.clear()
        self._items = []

        self.height = 0

    def add_item(self, name: str, key: Key | ComboKey) -> TemplateItem:
        """
        Add annotation template item from dictionary entries.

        Parameters
        ----------
        name : str
            annotation name.
        dct : Dict[str, Any]
            annotation type, default, and options.
        """
        annot_type = str(key.get_type())
        default: Any = key.get_default_value()
        widget = None
        if annot_type == "string":
            annot_type = ItemType.STRING
            widget = QLineEdit(default)
        elif annot_type == "number":
            annot_type = ItemType.NUMBER
            widget = QSpinBox()
            widget.setValue(default)
        elif annot_type == "bool":
            annot_type = ItemType.BOOL
            widget = QCheckBox()
            widget.setChecked(default)
        elif annot_type == "list":
            annot_type = ItemType.LIST
            widget = QComboBox()
            if isinstance(key, ComboKey):
                for opt in key.get_options():
                    widget.addItem(opt)
            widget.setCurrentText(default)
        else:
            annot_type = ItemType.POINT
            widget = QPushButton("Select")
            widget.setFixedWidth(200)

        item = TemplateItem(self, name, annot_type, default, widget)

        self._items.append(item)

        self.height = self.height + item.widget.sizeHint().height()
        self.setMaximumHeight(self.height)

        return item
