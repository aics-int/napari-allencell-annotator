from typing import Set
from PyQt5.QtWidgets import QDialog

from napari_allencell_annotator.widgets.file_item import FileItem
from napari_allencell_annotator.widgets.scrollable_popup import ScrollablePopup


class FileScrollablePopup:
    @classmethod
    def make_popup(cls, msg: str, checked_files: Set[FileItem]) -> bool:
        """
        Pop up dialog showing currently checked image files to ask the user yes or no.

        Parameters
        ----------
        msg: str
            Question for the message box.
        checked_files: Set[FileItem]
            The list of currently checked files.

        Returns
        ----------
        bool
            user input, true if 'OK' false if 'Cancel'
        """
        names: Set[str] = set()
        for item in checked_files:
            names.add("--- " + item.get_file_path_str())
        msg_box: ScrollablePopup = ScrollablePopup(msg, names)
        return_value: int = msg_box.exec()
        if return_value == QDialog.Accepted:
            return True
        else:
            return False
