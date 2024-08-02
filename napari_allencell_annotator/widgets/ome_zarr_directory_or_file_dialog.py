from PyQt5.QtWidgets import QListView, QAbstractItemView, QTreeView
from qtpy.QtWidgets import QFileDialog
from napari_allencell_annotator._style import Style


class OmeZarrDirectoryOrFileDialog(QFileDialog):
    """
    A custom QFileDialog that allows the user to select files and zarr directories.
    """
    def __init__(self, parent, title):
        super().__init__(parent, title)
        self.setStyleSheet(Style.get_stylesheet("main.qss"))
        self.currentChanged.connect(self._selected)
        self.setNameFilter("Directories and files (*)")
        self.setOption(QFileDialog.DontUseNativeDialog, True)

    def _selected(self, name: str) -> None:
        """
        Called whenever the user selects a new option in the File Dialog menu.
        """
        self.setFileMode(QFileDialog.Directory | QFileDialog.ExistingFiles)
        self.setNameFilter("Directories and files (*)")
        self.setOption(QFileDialog.DontUseNativeDialog, True)
        self.findChild(QListView, "listView").setSelectionMode(QAbstractItemView.ExtendedSelection)

        f_tree_view: QTreeView = self.findChild(QTreeView)
        if f_tree_view:
            f_tree_view.setSelectionMode(QAbstractItemView.ExtendedSelection)

    def accept(self):
        """
        Called whenever the user is done selecting files and directories.
        """
        self.setFileMode(QFileDialog.Directory | QFileDialog.ExistingFiles)
        self.setNameFilter("Directories and files (*)")
        self.setOption(QFileDialog.DontUseNativeDialog, True)
        self.findChild(QListView, "listView").setSelectionMode(QAbstractItemView.ExtendedSelection)

        f_tree_view: QTreeView = self.findChild(QTreeView)
        if f_tree_view:
            f_tree_view.setSelectionMode(QAbstractItemView.ExtendedSelection)

        super().done(QFileDialog.Accepted)
