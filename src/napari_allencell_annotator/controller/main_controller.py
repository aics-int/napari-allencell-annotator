from aicsimageio import AICSImage, exceptions
from napari.utils.notifications import show_info

class MainController():

    def __init__(self, model, view):
        """"""
        self.model = model
        self.view = view

        self._connect_slots()

    def _connect_slots(self):
        self.view.images.file_widget.currentItemChanged.connect(self.curr_img_change)

    def curr_img_change(self, event):
        self.view.images.curr_image = event.text()
        try:
            img = AICSImage(self.view.images.curr_image)
            img = img.data
            self.view.images.display_img(img)
        except exceptions.UnsupportedFileFormatError:
            show_info("AICS Image Conversion Failed")
