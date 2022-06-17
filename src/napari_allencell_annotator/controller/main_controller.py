
from aicsimageio import exceptions

class MainController():
    """Main controller to integrate view and model for image annotations"""
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.view.set_ctrl(self)

        self._connect_slots()

    def _connect_slots(self):
        """Connect signals to slots. """
        self.view.file_widget.currentItemChanged.connect(self.curr_img_change)


    def curr_img_change(self, event):
        """
        Convert new image selection into an AICSImage.
        Alert user of a failed AICS conversion.
        """
        try:
            img = self.model.aicsimageio_convert(event.text())
            self.view.set_curr_img(img)
        except exceptions.UnsupportedFileFormatError:
            self.view.error_alert("AICS Image Conversion Failed")

    def is_supported(self, file):
        """"""
        if self.model.is_supported(file):
            return True
        else:
            return False

