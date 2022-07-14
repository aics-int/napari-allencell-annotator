import os

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QDialog

from napari_allencell_annotator.controller.images_controller import (
    ImagesController,
)

from napari_allencell_annotator.controller.annotator_controller import (
    AnnotatorController,
)
from napari_allencell_annotator.widgets.create_dialog import (
    CreateDialog,
)
import napari
from typing import List


class MainController(QWidget):
    """
    A class used to combine/communicate between AnnotatorController and ViewController.

    Methods
    -------
    start_annotating()
        Verifies that images are added and user wants to proceed, then opens a .csv file dialog.
    stop_annotating()
         Stops annotating in images and annotations views.
    next_image()
        Moves to the next image for annotating.
    prev_image()
        Moves to the previous image for annotating.
    """

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
        """Connects annotator view buttons start, next, and prev to slots"""
        self.annots.view.start_btn.clicked.connect(self.start_annotating)

        self.annots.view.next_btn.clicked.connect(self.next_image)
        self.annots.view.prev_btn.clicked.connect(self.prev_image)
        self.annots.view.file_input.file_selected.connect(self._file_selected_evt)
        self.annots.view.save_exit_btn.clicked.connect(self.save_and_exit)
        self.annots.view.import_btn.clicked.connect(self.import_annots)
        self.annots.view.annot_input.file_selected.connect(
            self._csv_file_selected_evt
        )
        self.annots.view.create_btn.clicked.connect(self.create_clicked)

    def create_clicked(self):
        dlg = CreateDialog(self)
        if dlg.exec() == QDialog.Accepted:
            self.annots.set_annot_data(dlg.data)
            self.annots.start_viewing()
        else:
            print("Cancel!")
# todo enforce unique names, enforce option is in the options, write what warning is, fix sizing issue/styling q for brian
    #  , testing, new PR,
    # todo PR: then do writing to json bit
    # todotest/bug fix


    def _csv_file_selected_evt(self, file_list: List[str]):
        """
        Set csv file name for importing annotations.

        Parameters
        ----------
        file_list : List[str]
            The list containing one file name.
        """

        if file_list is None or len(file_list) < 1:
            self.images.view.alert("No selection provided")
        else:
            # TODO save csv, ask if image set will be used, render annotations/images if relevant, alter state so that a new csv is not selected if a csv is uploaded?
            file_path = file_list[0]
            # switch to view mode after creating/passing the json

    def import_annots(self):
        self.annots.view.annot_input.simulate_click()

    def _file_selected_evt(self, file_list: List[str]):
        """
        Set csv file name for writing to the selected file.

        Ensure that all file names have .csv extension and that a
        file name is selected.

        Parameters
        ----------
        file_list : List[str]
            The list containing one file name.
        """
        if file_list is None or len(file_list) < 1:
            self.images.view.alert("No selection provided")
        else:
            file_path = file_list[0]
            _, extension = os.path.splitext(file_path)
            if extension != ".csv":
                file_path = file_path + ".csv"
            self.annots.set_csv_name(file_path)
            self._setup_annotating()

    def start_annotating(self):
        """
        Verify that images are added and user wants to proceed, then
        open a .csv file dialog.

        Alert user if there are no files added.
        """
        if (
                self.images.get_num_files() is None
                or self.images.get_num_files() < 1
        ):
            self.images.view.alert("Can't Annotate Without Adding Images")
        else:
            proceed: bool = self.annots.view.popup(
                "Once annotating starts both the image set and annotations cannot be "
                "edited.\n Would "
                "you like to continue?"
            )
            if proceed:
                self.annots.view.file_input.simulate_click()

    def stop_annotating(self):
        """
        Stop annotating in images and annotations views.

        Display images and annots views.
        """
        self.layout.addWidget(self.images.view, stretch=1)
        self.layout.addWidget(self.annots.view, stretch=2)
        self.images.view.show()
        self.annots.stop_annotating()
        self.images.stop_annotating()

    def _setup_annotating(self):
        """Hide the file viewer and start the annotating process."""
        self.layout.removeWidget(self.images.view)
        self.images.view.hide()
        self.images.start_annotating()
        self.annots.start_annotating(self.images.get_num_files(), self.images.get_files_dict())
        self.annots.set_curr_img(self.images.curr_img_dict())

    def next_image(self):
        """
        Move to the next image for annotating.

        If the last image is being annotated, write to csv. If the second
        image is being annotated, enable previous button.
        """
        self.annots.record_annotations(self.images.curr_img_dict()["File Path"])

        self.images.next_img()
        self.annots.set_curr_img(self.images.curr_img_dict())
        if self.images.curr_img_dict()["Row"] == "1":
            self.annots.view.prev_btn.setEnabled(True)

    def save_and_exit(self):
        proceed: bool = self.annots.view.popup("Close this session?")

        if proceed:
            self.stop_annotating()

    def prev_image(self):
        """
        Move to the previous image for annotating.

        If the first image is being annotated, disable button.
        """
        self.annots.record_annotations(self.images.curr_img_dict()["File Path"])
        self.images.prev_img()
        self.annots.set_curr_img(self.images.curr_img_dict())
        if self.images.curr_img_dict()["Row"] == "0":
            self.annots.view.prev_btn.setEnabled(False)
