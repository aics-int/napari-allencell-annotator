from qtpy.QtWidgets import QMessageBox


class Popup:
    @classmethod
    def make_popup(cls, text: str) -> bool:
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
        msg_box = QMessageBox()
        msg_box.setText(text)
        msg_box.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
        return_value = msg_box.exec()
        if return_value == QMessageBox.Yes:
            return True
        else:
            return False
