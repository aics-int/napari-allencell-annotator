from PyQt5.QtWidgets import QDialog

from qtpy.QtWidgets import QMessageBox
from napari_allencell_annotator.widgets.scrollable_popup import ScrollablePopup
from typing import Set


class FileScrollablePopup:
    @classmethod
    def make_popup(cls, msg: str, checked_files) -> bool:
        """
        Pop up dialog to ask the user yes or no.

        Parameters
        ----------
        text : str
            question for the message box.

        Returns
        ----------
        bool
            user input, true if 'Yes' false if 'No'

        """
        names: Set[str] = set()
        for item in checked_files:
            names.add("--- " + item.file_path)
        msg_box = ScrollablePopup(msg, names)
        return_value = msg_box.exec()
        if return_value == QDialog.Accepted:
            return True
        else:
            return False
