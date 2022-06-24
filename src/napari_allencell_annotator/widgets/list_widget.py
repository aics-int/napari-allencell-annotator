from PyQt5.QtWidgets import QListWidget, QAbstractItemView, QWidget
from typing import Set

from qtpy.QtCore import Signal

from napari_allencell_annotator.widgets.list_item import ListItem


class ListWidget(QListWidget):
    items_selected = Signal(bool)
    def __init__(self):
        QListWidget.__init__(self)
        self.checked: Set[ListItem] = set()
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.files : Set[str] = set()
        #self.itemChanged.connect(self.checked)

    def add_item(self, file: str):
        if file not in self.files:
            self.files.add(file)
            item = ListItem(file, self)
            item.check.stateChanged.connect(lambda: self.check_evt(item))


    def _remove_item(self, item: ListItem):
        if item.file_path in self.files:
            self.takeItem(self.row(item))
            self.files.remove(item.file_path)

    def delete_selected(self):
        for item in self.checked:
            self._remove_item(item)
        self.checked.clear()
        self.items_selected.emit(False)

    def check_evt(self,item: ListItem):
        if item.check.isChecked():
            self.checked.add(item)
            if len(self.checked) == 1:
                self.items_selected.emit(True)
        elif item in self.checked:
            self.checked.remove(item)
            if len(self.checked) == 0:
                self.items_selected.emit(False)


