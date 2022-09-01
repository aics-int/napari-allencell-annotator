from typing import Dict, Any, List

from qtpy.QtWidgets import QLineEdit, QCheckBox, QComboBox, QSpinBox
from qtpy.QtWidgets import QAbstractScrollArea, QSizePolicy
from qtpy.QtWidgets import QListWidget

from napari_allencell_annotator.widgets.template_item import TemplateItem, ItemType
from napari_allencell_annotator._style import Style



class TemplateList(QListWidget):
    """
    A class used to create a QListWidget for annotation templates.

    Attributes
    ----------
    items : List[TemplateItem]

    """

    def __init__(self):
        QListWidget.__init__(self)

        self.setStyleSheet(Style.get_stylesheet("main.qss"))
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        #todo single selection
        self._items = []
        self.height = 0



    @property
    def items(self) -> List[TemplateItem]:
        return self._items


    def clear_all(self):

        self.clear()
        self._items = []
        self.setMaximumHeight(600)
        self.height = 0

    def add_item(self, name : str, dct : Dict[str, Any]):
        """
        Add annotation template item from dictionary entries.

        Parameters
        ----------
        name : str
            annotation name.
        dictn : Dict[str, Any]
            annotation type, default, and options.
        """

        annot_type: str = dct["type"]
        default : Any = dct["default"]
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
            if default:
                widget.setChecked(True)
        elif annot_type == "list":
            annot_type = ItemType.LIST
            widget = QComboBox()
            for opt in dct["options"]:
                widget.addItem(opt)
            widget.setCurrentText(default)
        item = TemplateItem(self,name,annot_type, default,widget)

        self._items.append(item)

        self.height = self.height + item.widget.sizeHint().height()
        self.setMaximumHeight(self.height)


    #add method for create keyboard shortcuts and take away keyboard stuff
