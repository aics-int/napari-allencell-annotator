import csv
import os
from pathlib import Path

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QDialog

from napari_allencell_annotator.controller.images_controller import ImagesController

from napari_allencell_annotator.controller.annotator_controller import AnnotatorController
from napari_allencell_annotator.widgets.create_dialog import CreateDialog
import napari
from typing import List, Dict


class MainController(QWidget):
    """
    A class used to combine/communicate between AnnotatorController and ViewController.

    Methods
    -------
    _start_annotating_clicked()
        Verifies that images are added and user wants to proceed, then opens a .csv file dialog.
    stop_annotating()
         Stops annotating in images and annotations views.
    _next_image_clicked()
        Moves to the next image for annotating.
    _prev_image_clicked()
        Moves to the previous image for annotating.
    """

    def __init__(self):
        super().__init__()
        self.napari = napari.Viewer()
        self.napari.window.qt_viewer.dockLayerList.setVisible(False)
        self.napari.window.qt_viewer.dockLayerControls.setVisible(False)
        self.layout = QVBoxLayout()
        self.images = ImagesController(self.napari)
        self.annots = AnnotatorController(self.napari)
        self.layout.addWidget(self.images.view, stretch=1)
        self.layout.addWidget(self.annots.view, stretch=2)
        self.setLayout(self.layout)
        self.show()
        self.napari.window.add_dock_widget(self, area="right")
        self._connect_slots()
        self.already_annotated: Dict[str, List] = None
        self.starting_row: int = -1

    def _connect_slots(self):
        """Connects annotator view buttons start, next, and prev to slots"""
        self.annots.view.start_btn.clicked.connect(self._start_annotating_clicked)

        self.annots.view.next_btn.clicked.connect(self._next_image_clicked)
        self.annots.view.prev_btn.clicked.connect(self._prev_image_clicked)
        self.annots.view.csv_input.file_selected.connect(self._csv_write_selected_evt)
        self.annots.view.save_exit_btn.clicked.connect(self._save_and_exit_clicked)
        self.annots.view.import_btn.clicked.connect(self._import_annots_clicked)
        self.annots.view.annot_input.file_selected.connect(self._csv_import_selected_evt)
        self.annots.view.create_btn.clicked.connect(self._create_clicked)
        self.annots.view.save_json_btn.file_selected.connect(self._json_write_selected_evt)

    def _create_clicked(self):
        """Create dialog window and start viewing on accept."""
        dlg = CreateDialog(self)
        if dlg.exec() == QDialog.Accepted:
            self.already_annotated = None
            self.annots.set_annot_json_data(dlg.new_annot_dict)
            self.annots.start_viewing()

    def _json_write_selected_evt(self, file_list: List[str]):
        """
        Set json file name for writing annotations and write the annotations.

        Ensure that all file names have .json extension and that a
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
            extension = Path(file_path).suffix
            if extension != ".json":
                file_path = file_path + ".json"
            self.annots.view.save_json_btn.setEnabled(False)
            self.annots.write_json(file_path)

    def _csv_import_selected_evt(self, file_list: List[str]):
        """
        Set csv file name for importing annotations.

        Parameters
        ----------
        file_list : List[str]
            The list containing one file name.
        """
        self.already_annotated = None
        if file_list is None or len(file_list) < 1:
            self.images.view.alert("No selection provided")
        else:
            file_path = file_list[0]
            if Path(file_path).suffix == ".json":
                self.annots.read_json(file_path)

            elif Path(file_path).suffix == ".csv":
                proceed: bool = self.annots.view.popup("Would you like to use the images in this csv?")
                file = open(file_path)

                reader = csv.reader(file)
                shuffled = next(reader)[1]
                shuffled = self.str_to_bool(shuffled)
                # annotation data header
                annts = next(reader)[1]
                # skip actual header
                next(reader)
                self.starting_row = None
                if proceed:
                    self.already_annotated = {}

                    row_num: int = 0
                    for row in reader:

                        self.already_annotated[row[0]] = row[1::]
                        if self.starting_row is None:
                            for j in row[3::]:
                                if j is None or j == "":
                                    # if there is a none value for an annotation
                                    self.starting_row = row_num
                                    break
                            row_num = row_num + 1

                    self.images.load_from_csv(self.already_annotated.keys(), shuffled)
                if self.starting_row is None:
                    self.starting_row = 0
                file.close()
                self.annots.get_annotations_csv(annts)

            self.annots.start_viewing()

    def str_to_bool(self, string):
        """
        Convert a string to a bool.

        Parameters
        ----------
        string_ : str
        default : {'raise', False}
            Default behaviour if none of the "true" strings is detected.

        Returns
        -------
        boolean : bool
        """
        if string.lower() == "true":
            return True
        elif string.lower() == "false":
            return False
        else:
            raise ValueError("The value '{}' cannot be mapped to boolean.".format(string))

    def _import_annots_clicked(self):
        """Open file widget for importing csv/json."""
        self.annots.view.annot_input.simulate_click()

    def _csv_write_selected_evt(self, file_list: List[str]):
        """
        Set csv file name for writing annotations.

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
            extension = Path(file_path).suffix
            if extension != ".csv":
                file_path = file_path + ".csv"
            self.annots.set_csv_name(file_path)
            self._setup_annotating()

    def _start_annotating_clicked(self):
        """
        Verify that images are added and user wants to proceed, then
        open a .csv file dialog.

        Alert user if there are no files added.
        """
        if self.images.get_num_files() is None or self.images.get_num_files() < 1:
            self.images.view.alert("Can't Annotate Without Adding Images")
        else:
            proceed: bool = self.annots.view.popup(
                "Once annotating starts both the image set and annotations cannot be "
                "edited.\n Would "
                "you like to continue?"
            )
            if proceed:
                self.annots.view.csv_input.simulate_click()

    def _stop_annotating(self):
        """
        Stop annotating in images and annotations views.

        Display images and annots views.
        """
        if not self.images.view.file_widget.shuffled:
            self.images.view.file_widget.currentItemChanged.disconnect(self.image_selected)
        self.layout.addWidget(self.images.view, stretch=1)
        self.layout.addWidget(self.annots.view, stretch=2)
        self.images.view.show()
        self.annots.stop_annotating()
        self.images.stop_annotating()
        self.images.view.input_file.show()
        self.images.view.input_dir.show()

    def _setup_annotating(self):
        """Hide the file viewer and start the annotating process."""
        dct, shuffled = self.images.get_files_dict()
        if shuffled:
            self.layout.removeWidget(self.images.view)

            self.images.view.hide()
        if self.already_annotated is not None and len(self.already_annotated) > 0:

            self.images.start_annotating(self.starting_row)
            self.annots.start_annotating(self.images.get_num_files(), self.already_annotated, shuffled)
        else:
            self.images.start_annotating()
            self.annots.start_annotating(self.images.get_num_files(), dct, shuffled)
        self.annots.set_curr_img(self.images.curr_img_dict())
        if not shuffled:
            self.images.view.file_widget.currentItemChanged.connect(self.image_selected)
            self.images.view.input_dir.hide()
            self.images.view.input_file.hide()

    def _next_image_clicked(self):
        """
        Move to the next image for annotating.

        If the last image is being annotated, write to csv. If the second
        image is being annotated, enable previous button.
        """
        self.annots.record_annotations(self.images.curr_img_dict()["File Path"])

        self.images.next_img()
        self.annots.set_curr_img(self.images.curr_img_dict())

    def image_selected(self, current, previous):
        if previous:
            self.annots.record_annotations(previous.file_path)
        self.annots.set_curr_img(self.images.curr_img_dict())

    def _prev_image_clicked(self):
        """
        Move to the previous image for annotating.

        If the first image is being annotated, disable button.
        """
        self.annots.record_annotations(self.images.curr_img_dict()["File Path"])
        self.images.prev_img()
        self.annots.set_curr_img(self.images.curr_img_dict())

    def _save_and_exit_clicked(self):
        """Stop annotation if user confirms choice in popup."""
        proceed: bool = self.annots.view.popup("Close this session?")

        if proceed:
            self._stop_annotating()
