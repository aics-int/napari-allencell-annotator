from typing import Dict, Optional, Any

from napari_allencell_annotator._style import Style
from qtpy import QtWidgets
from qtpy.QtCore import Qt
from qtpy.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QDialog,
    QVBoxLayout,
    QScrollArea,
    QHBoxLayout,
)
from qtpy.QtCore import Signal

from napari_allencell_annotator.model.annotation_model import AnnotationModel
from napari_allencell_annotator.widgets.annotation_widget import AnnotationWidget


class CreateDialog(QDialog):
    """
    A class that creates up to 10 annotations in a popup dialog.

    Methods
    -------
    get_annots()
        Sets annotation dictionary and emits valid_annots_made signal if all annotations are valid.
    render_annotations()
        Displays the types and defaults for each existing annotation.
    """

    # signal emitted when all annotations created are valid
    valid_annots_made = Signal()

    def __init__(self, model: AnnotationModel, parent=None):
        super().__init__(parent)
        self._annotation_model = model
        self.setStyleSheet(Style.get_stylesheet("main.qss"))

        self.setWindowTitle("Create Annotations")
        self.setMinimumSize(800, 500)

        self.list = AnnotationWidget()

        self.layout = QVBoxLayout()
        if len(self.model.get_annotation_keys()) > 0:
            self.list.add_new_item()
            label = QLabel("Create Annotations")
            label.setAlignment(Qt.AlignCenter)
        else:
            label = QLabel("Edit Annotations")
        label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(label)

        self.scroll = QScrollArea()
        self.scroll.setWidget(self.list)
        self.scroll.setWidgetResizable(True)
        self.layout.addWidget(self.scroll, stretch=15)

        self.add = QPushButton("Add +")
        self.delete = QPushButton("Delete Selected")
        self.delete.setToolTip("Click boxes on the left of items to select for deletion")
        self.cancel = QPushButton("Cancel")  # check: if edit -> cancel go back to view
        self.apply = QPushButton("Apply")
        self.btns = QWidget()
        self.new_annot_dict: Dict[str, Dict] = None
        layout = QHBoxLayout()
        layout.addWidget(self.add)
        layout.addWidget(self.delete)
        sp_retain = QtWidgets.QSizePolicy()
        sp_retain.setRetainSizeWhenHidden(True)
        self.delete.setSizePolicy(sp_retain)
        self.delete.setEnabled(False)
        layout.addWidget(self.cancel)
        layout.addWidget(self.apply)

        self.btns.setLayout(layout)
        self.error = QLabel()
        self.error.setStyleSheet("color: red")
        self.layout.addWidget(self.error)
        self.layout.addWidget(self.btns)

        self.setLayout(self.layout)

        if len(self.model.get_annotation_keys()) > 0:
            self.render_annotations()
        self._connect_slots()

    def _connect_slots(self):
        """Connect signals and slots"""
        self.add.clicked.connect(self._add_clicked)
        self.cancel.clicked.connect(self.reject)
        self.apply.clicked.connect(self.get_annots)
        self.valid_annots_made.connect(self.accept)
        self.delete.clicked.connect(self._delete_clicked)
        self.list.annots_selected.connect(self._show_delete)

    def _show_delete(self, checked: bool):
        """
        Display the delete button

        Parameters
        ----------
        checked : bool
            True if delete is currently hidden.
        """
        self.delete.setEnabled(checked)

    def render_annotations(self):
        """Display the types and defaults for each existing annotation."""
        for key_name, key_info in self._annotation_model.get_annotation_keys():
            self.list.add_existing_item(key_name, key_info)

    def _delete_clicked(self):
        """Delete checked items if there is at least one item checked."""
        if self.list.num_checked > 0:
            self.list.delete_checked()
        if self.list.count() <= 9:
            self.add.show()

    def _add_clicked(self):
        """Add a new item if there are less than 9. Hide add button otherwise."""
        self.list.add_new_item()
        if self.list.count() > 9:
            self.add.hide()

    def get_annots(self):
        """
        Set annotation dictionary to annotation data in list
        and emit valid_annots_made signal if all annotations are valid.

        """

        dct: Dict[str, Key] = {}
        valid = True
        error = ""
        # grab all items from list of annotations
        items = [self.list.item(x) for x in range(self.list.count())]
        # if all items have been deleted annotations are invalid
        if len(items) < 1:
            valid = False
            error = " Must provide at least one annotation. "

        for i in items:
            item_valid, name, key, item_error = i.get_data()
            # sub_dct is annotation data (type,default, options)
            if name in dct.keys():
                valid = False
                i.highlight(i.name)
                error = error + " No duplicate names allowed. "
            dct[name] = key
            if not item_valid:
                valid = False
                error = error + " " + item_error
                break

        # if all values were valid emit signal and set new_annot_dict
        self.error.setText(error)
        if valid:
            self._annotation_model.set_annotation_keys(dct)
            self.valid_annots_made.emit()
        else:
            self._annotation_model.clear_annotation_keys()
