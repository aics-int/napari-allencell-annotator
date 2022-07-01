from PyQt5.QtWidgets import QWidget, QVBoxLayout

from napari_allencell_annotator.controller.images_controller import ImagesController

from napari_allencell_annotator.controller.annotator_controller import AnnotatorController
from napari_allencell_annotator.view.annotator_view import AnnotatorViewMode
import napari


class MainController(QWidget):
    def __init__(self):
        super().__init__()
        self.napari = napari.Viewer()
        self.layout = QVBoxLayout()
        self.images = ImagesController(self.napari)
        self.annots = AnnotatorController(self.napari)
        self.layout.addWidget(self.images.view, stretch=1)
        self.layout.addWidget(self.annots.view, stretch=2)
        self.setLayout(self.layout)
        self.show()
        self.napari.window.add_dock_widget(self, area="right")
        self._connect_slots()

    def _connect_slots(self):
            self.annots.view.start_btn.clicked.connect(self.start_annotating)
            self.annots.view.next_btn.clicked.connect(self.next_image)

    def start_annotating(self):
        """"""
        if self.images.get_num_files() is None or self.images.get_num_files() < 1:
            self.images.view.alert("Can't Annotate Without Adding Images")
        else:
            self.layout.removeWidget(self.images.view)
            self.images.view.hide()
            self.images.start_annotating()
            self.annots.start_annotating(self.images.get_num_files())
            self.annots.set_curr_img(self.images.get_curr_img())

    def next_image(self):
        """"""
        if self.annots.view.next_btn.text() == "Save and Export":
            self.annots.save_and_export()
        else:
            self.annots.write_image_csv(self.images.get_curr_img())
            self.images.next_img()
            self.annots.set_curr_img(self.images.get_curr_img())

