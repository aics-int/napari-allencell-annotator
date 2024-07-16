import csv
import itertools
from pathlib import Path

from napari_allencell_annotator.model.annotation_model import AnnotatorModel
from napari_allencell_annotator.util.file_utils import FileUtils
from napari_allencell_annotator.view.images_view import ImagesView
from qtpy import QtCore
from qtpy.QtWidgets import QFrame, QShortcut
from qtpy.QtWidgets import QVBoxLayout, QDialog
from qtpy.QtGui import QKeySequence

from napari_allencell_annotator.controller.annotator_controller import AnnotatorController
from napari_allencell_annotator.model.images_model import ImagesModel
from napari_allencell_annotator.widgets.create_dialog import CreateDialog
from napari_allencell_annotator.widgets.template_item import ItemType, TemplateItem
from napari_allencell_annotator.widgets.popup import Popup
from napari_allencell_annotator.view.viewer import Viewer
from napari_allencell_annotator.view.i_viewer import IViewer

import napari
from typing import List, Dict, Union, Any


class MainView(QFrame):
    """
    Main plugin view displayed.

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

    def __init__(self, napari_viewer: napari.Viewer):
        super().__init__()
        # init viewer and parts of the plugin
        self._viewer: IViewer = Viewer(napari_viewer)
        self._annotator_model = AnnotatorModel()

        # ImagesView and Controller
        self._images_view = ImagesView(self._annotator_model, self._viewer)
        self._images_view.show()

        self.annots = AnnotatorController(self._annotator_model, self._viewer)

        # set layout and add sub views
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self._images_view, stretch=1)
        self.layout().addWidget(self.annots.view, stretch=1)

        # key shortcuts
        self._shortcut_key_next = QShortcut(QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_Greater), self)
        self._shortcut_key_prev = QShortcut(QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_Less), self)
        self._shortcut_key_down = QShortcut(QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_Return), self)
        self._shortcut_key_up = QShortcut(QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.SHIFT + QtCore.Qt.Key_Return), self)
        self._shortcut_key_check = QShortcut(QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.SHIFT + QtCore.Qt.Key_Space), self)

        self._connect_slots()
        self.show()

    def _connect_slots(self):
        """Connects annotator view buttons to slots"""
        self.annots.view.start_btn.clicked.connect(self._start_annotating_clicked)

        self.annots.view.next_btn.clicked.connect(self._next_image_clicked)
        self.annots.view.prev_btn.clicked.connect(self._prev_image_clicked)
        self.annots.view.csv_input.file_selected.connect(self._csv_write_selected_evt)
        self.annots.view.save_btn.clicked.connect(self._save)
        self.annots.view.exit_btn.clicked.connect(self._exit_clicked)
        self.annots.view.import_btn.clicked.connect(self._import_annots_clicked)
        self.annots.view.annot_input.file_selected.connect(self._csv_json_import_selected_evt)
        self.annots.view.create_btn.clicked.connect(self._create_clicked)
        self.annots.view.save_json_btn.file_selected.connect(self._json_write_selected_evt)
        self.annots.view.edit_btn.clicked.connect(self._create_clicked)

        # handle events
        self._annotator_model.image_changed.connect(self._image_selected)

    def _create_clicked(self):
        """Create dialog window for annotation creation and start viewing on accept event."""

        dlg = CreateDialog(self._annotator_model, parent=self)
        if dlg.exec() == QDialog.Accepted:
            self.annots.start_viewing()

    def _json_write_selected_evt(self, file_path: Path):
        """
        Set json file name and write the annotations to the file.

        Ensure that all file names have .json extension and that a
        file name is selected. Disable save json button.

        Parameters
        ----------
        file_list : List[str]
            The list containing one file name.
        """
        extension = file_path.suffix
        if extension != ".json":
            file_path = file_path.with_suffix(".json")
        self.annots.view.save_json_btn.setEnabled(False)
        self.annots.write_json(file_path)

    def _csv_json_import_selected_evt(self, file_path: Path):
        """
        Read annotations from csv or json file. Read/Save csv images and annotation data if user chooses to.

        Parameters
        ----------
        file_list : List[str]
            The list containing one file name.
        """
        # todo bad file: json or csv --> send back to add
        if file_path is None:
            self._viewer.alert("No selection provided")
        else:
            use_annots: bool = False
            if file_path.suffix == ".json":
                self.annots.read_json(file_path)

            elif file_path.suffix == ".csv":
                use_annots = Popup.make_popup(
                    "Would you like to use the images and annotation values from "
                    "this csv in addition to the annotation template?\n\n "
                    "\n Note: any currently listed images will be cleared."
                )
                file = open(file_path)
                reader = csv.reader(file)
                shuffled: str = next(reader)[1]
                # shuffled = self.str_to_bool(shuffled)
                # annotation data header
                annts = next(reader)[1]
                # set annotation Key dict in model with json header info
                self.annots.get_annotations_csv(annts)
                # skip actual header
                next(reader)
                image_list: list[Path] = []
                if use_annots:
                    # init annotations dict and fill with data from csv
                    self._annotator_model.set_annotations({})

                for row in reader:
                    # for each line, add data to already annotated and check if there are null values
                    # if null, starting row for annotations is set
                    path: Path = Path(row[1])
                    image_list.append(path)
                    if use_annots:
                        self._annotator_model.add_annotation(path, row[2:])
                    # self._images_view.add_new_item(path)
                # start at row 0 if annotation data was not used from csv
                file.close()
            self._annotator_model.set_all_images(image_list)
            self.annots.start_viewing(use_annots)

    def _shuffle_toggled(self, checked: bool):
        """
        Set has_new_shuffled_order to True if images are shuffled.

        Slot function used to record if csv imported image lists
        are given a new shuffle order before annotating. Slot disconnected once
        images have been shuffled once.

        Parameters
        ----------
        checked : bool
            True if shuffle button is pressed "Shuffle and Hide" mode. False if pressed in "Unhide" mode.
        """
        if checked:
            # images have been shuffled, have to adjust order
            self._annotator_model.set_images_shuffled(True)
            self._images_view.shuffle.toggled.disconnect(self._shuffle_toggled)

    def str_to_bool(self, string) -> bool:
        """
        Convert a string to a bool.

        Parameters
        ----------
        string_ : str

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

    def _csv_write_selected_evt(self, file_path: Path):
        """
        Set csv file name for writing annotations and call _setup_annotating.

        Ensure that all file names have .csv extension and that a
        file name is selected.

        Parameters
        ----------
        file_list : List[str]
            The list containing one file name.
        """
        extension = file_path.suffix
        if extension != ".csv":
            file_path = file_path.with_suffix(".csv")
        self._annotator_model.set_csv_save_path(file_path)
        self._setup_annotating()

    def _start_annotating_clicked(self):
        """
        Verify that images are added and user wants to proceed, then
        open a .csv file dialog.

        Alert user if there are no files added.
        """
        if self._annotator_model.get_num_images() < 1:
            self._viewer.alert("Can't Annotate Without Adding Images")
        else:
            proceed: bool = Popup.make_popup(
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
        self.layout().addWidget(self._images_view, stretch=1)
        self.layout().addWidget(self.annots.view, stretch=1)
        self._images_view.show()
        self.annots.stop_annotating()

        self._images_view.input_file.show()
        self._images_view.input_dir.show()
        self._images_view.shuffle.show()
        self._images_view.delete.show()
        self.annotating_shortcuts_off()

    def _setup_annotating(self):
        """
        Remove images view if shuffled/hidden annotating and start annotation.

        Pass in annotation values if there are any.
        """
        starting_idx: int = 0
        # init annotations dictionary to store data
        if self._annotator_model.get_annotations() is None:
            # there aren't preloaded annotations from a csv, so create an empty set
            self._annotator_model.set_annotations({})

        else:
            # we have preloaded annotations from a csv, reorder so already annotated images are at the front

            old_images_list: list[Path] = self._annotator_model.get_all_images()
            new_images_list: list[Path] = []
            self._annotator_model.empty_image_list()  # reset images list
            for annot_path, annot_list in self._annotator_model.get_annotations().items():
                # if the image with the existing annotations exists
                if annot_path in old_images_list:
                    # if the annotation is complete move to front
                    if annot_list and len(annot_list) == len(self._annotator_model.get_annotation_keys()):
                        new_images_list.insert(0, annot_path)
                        old_images_list.remove(annot_path)
                        starting_idx = starting_idx + 1
                    else:
                        # otherwise add to back
                        new_images_list.append(annot_path)
                        old_images_list.remove(annot_path)

            # use all images if not shuffled, shuffled image list if it is shuffled
            if not self._annotator_model.is_images_shuffled():
                self._annotator_model.set_all_images(new_images_list + old_images_list)
            else:
                self._annotator_model.set_shuffled_images(new_images_list + old_images_list)

            # if all images annotated, start at 1 minus index
            if starting_idx >= self._annotator_model.get_num_images():
                starting_idx = starting_idx - 1

        self.annotating_shortcuts_on()
        if self._annotator_model.is_images_shuffled():
            # remove file list if blind annotation
            self.layout().removeWidget(self._images_view)
            self._images_view.hide()
            self.annots.start_annotating()

        # TODO: CODE TO READ ANNOTATIONS IF ALREADY EXISTS
        else:
            # start annotating from beginning with just file info
            self._images_view.start_annotating()
            self.annots.start_annotating()

        # remove this
        # self.annots.set_curr_img()
        if not self._annotator_model.is_images_shuffled():
            # alter images view to fit annotation mode
            self._images_view.hide_image_paths()

        # set first image
        self._annotator_model.set_previous_image_index(self._annotator_model.get_curr_img_index())
        self._annotator_model.set_curr_img_index(starting_idx)
        self._annotator_model.set_annotation_started(True)



    def annotating_shortcuts_on(self):
        """Create annotation keyboard shortcuts and connect them to slots."""

        self._shortcut_key_next.activated.connect(self._next_image_clicked)
        self._shortcut_key_prev.activated.connect(self._prev_image_clicked)
        self._shortcut_key_down.activated.connect(self.annots.view.annot_list.next_item)
        self._shortcut_key_up.activated.connect(self.annots.view.annot_list.prev_item)
        self._shortcut_key_check.activated.connect(self._toggle_check)

    def annotating_shortcuts_off(self):
        """Disconnect signals and slots for annotation shortcuts"""
        self._shortcut_key_next.activated.disconnect(self._next_image_clicked)
        self._shortcut_key_prev.activated.disconnect(self._prev_image_clicked)
        self._shortcut_key_down.activated.disconnect(self.annots.view.annot_list.next_item)
        self._shortcut_key_up.activated.disconnect(self.annots.view.annot_list.prev_item)
        self._shortcut_key_check.activated.disconnect(self._toggle_check)

    def _toggle_check(self):
        """Toggle the checkbox state if the current annotation is a checkbox."""
        curr: TemplateItem = self.annots.view.annot_list.currentItem()
        if curr is not None and curr.type == ItemType.BOOL:
            curr.editable_widget.setChecked(not curr.get_value())

    # def _fix_csv_annotations(self, dct: Dict[str, List[str]]):
    #     """
    #     Change csv_annotation_values to reflect any edits to the image list.
    #
    #     Image list could have been shuffled or had items added/deleted.
    #
    #     Parameters
    #     ----------
    #     dct : Dict[str, List[str]]
    #         the image list dictionary file path -> [file name, fms]
    #     """
    #     dct_keys = dct.keys()
    #     alr_anntd_keys = self.csv_annotation_values.keys()
    #     # dct_keys is the dictionary from the images list. may have been edited
    #     # alr_anntd_keys was read in from csv. has not been edited
    #
    #     # remove this
    #     if not list(map(lambda x: str(x), dct_keys)) == alr_anntd_keys:
    #         # if dct .keys is not equal (order not considered) to aa.keys
    #         # means files were either added/deleted
    #         if self.has_new_shuffled_order:
    #             # if dct .keys is not equal (minus order ) to aa.keys. and SHUFFLED
    #             self._unequal_shuffled_fix_csv_annotations(dct)
    #
    #         else:
    #             self._unequal_unshuffled_fix_csv_annotations(dct)
    #     else:
    #         # dct keys and aakeys are equal (except for order)
    #         if self.has_new_shuffled_order:
    #             self._equal_shuffled_fix_csv_annotations(dct)
    #         # if dct.keys == aakeys and NOT SHUFFLED then no changes

    # def _unequal_unshuffled_fix_csv_annotations(self, dct: Dict[str, List[str]]):
    #     """
    #     Change csv_annotation_values to reflect any edits insertions/deletions to the image list.
    #
    #     Find a new starting row if old starting row image was deleted or if new un-annotated images
    #     are the first un-annotated images.
    #
    #     Parameters
    #     ----------
    #     dct : Dict[str, List[str]]
    #         the image list dictionary file path -> [file name, fms]
    #     """
    #     dct_keys = dct.keys()
    #     alr_anntd_keys = self.csv_annotation_values.keys()
    #     new_starting_row_found: bool = False
    #     new_csv_annotations = {}
    #     # order has not been changed/shuffled since upload
    #     # need to add/delete files from already annotated and get a new starting row in case the
    #     # file deleted or added is now the first file with a null annotation
    #     for old_file, row in zip(alr_anntd_keys, range(len(alr_anntd_keys))):
    #         # remove this
    #         if old_file in list(map(lambda x: str(x), dct_keys)):
    #             # old file wasn't removed from files
    #             new_csv_annotations[old_file] = self.csv_annotation_values[old_file]
    #             if not new_starting_row_found:
    #                 if row >= self.starting_row:
    #                     # every file at index before the original starting row was fully annotated
    #                     # if we are past that point in csv_annotation_values then we need to test if we
    #                     # have found a new none annotation value
    #                     if self.has_none_annotation(self.csv_annotation_values[old_file][2::]):
    #                         self.starting_row = len(new_csv_annotations) - 1
    #                         new_starting_row_found = True
    #
    #         # if old_file not in dct_keys dont add it
    #     if len(new_csv_annotations) < len(dct):
    #         # items were added into dct that were not in already annotated
    #         if not new_starting_row_found:
    #             # start on first new item from dct which has not been annotated
    #             self.starting_row = len(new_csv_annotations)
    #             new_starting_row_found = True
    #         for file in list(dct_keys)[len(new_csv_annotations) : :]:
    #             # remove this
    #             new_csv_annotations[file] = dct[file]
    #
    #     if not new_starting_row_found:
    #         self.starting_row = len(new_csv_annotations) - 1
    #     self.csv_annotation_values = new_csv_annotations

    # def _unequal_shuffled_fix_csv_annotations(self, dct: Dict[str, List[str]]):
    #     """
    #     Change csv_annotation_values to reflect any edits insertions/deletions to the image list and shuffling.
    #
    #     Find a new starting row if old starting row image was deleted or if new un-annotated images
    #     are the first un-annotated images.
    #
    #     Reorder the csv_annotation_values keys so that the GUI will read/write
    #     the csv image list in this new shuffled order. This will help with saving progress
    #     when blindly annotating a large image set.
    #
    #     Parameters
    #     ----------
    #     dct : Dict[str, List[str]]
    #         the image list dictionary file path -> [file name, fms]
    #     """
    #     # it has been either shuffled and is now blind or it was given a new shuffle order
    #     # want to save this order in case csv has unshuffled image order, annotation is supposed to be blind
    #     # and next time the csv is opened it will be in insertion order still
    #     dct_keys = dct.keys()
    #     alr_anntd_keys = self.csv_annotation_values.keys()
    #     new_starting_row_found: bool = False
    #     new_csv_annotations = {}
    #     # remove this
    #     for new_file, dct_index in zip(list(map(lambda x: str(x), dct_keys)), range(len(dct_keys))):
    #
    #         if new_file not in alr_anntd_keys:
    #             # only possible to encounter a new file in middle when shuffling has happened
    #             # file added to dct
    #             # remove this
    #             new_csv_annotations[new_file] = dct[Path(new_file)]
    #
    #             if not new_starting_row_found:
    #                 # just added a new, unannotated file
    #                 self.starting_row = dct_index
    #                 new_starting_row_found = True
    #
    #         elif new_file in alr_anntd_keys:
    #             new_csv_annotations[new_file] = self.csv_annotation_values[new_file]
    #             if not new_starting_row_found:
    #                 # todo: could try an optimize this by storing csv_annotation_values indexes
    #                 if self.has_none_annotation(self.csv_annotation_values[new_file][2::]):
    #                     self.starting_row = dct_index
    #                     new_starting_row_found = True
    #     if not new_starting_row_found:
    #         self.starting_row = len(new_csv_annotations) - 1
    #     self.csv_annotation_values = new_csv_annotations
    #
    # def _equal_shuffled_fix_csv_annotations(self, dct: Dict[str, List[str]]):
    #     """
    #     Change csv_annotation_values to reflect shuffling.
    #
    #     Parameters
    #     ----------
    #     dct : Dict[str, List[str]]
    #         the image list dictionary file path -> [file name, fms]
    #     """
    #     dct_keys = dct.keys()
    #     new_starting_row_found: bool = False
    #     new_csv_annotations = {}
    #     # remove this
    #     for new_file, dct_index in itertools.zip_longest(list(map(lambda x: str(x), dct_keys)), range(len(dct_keys))):
    #         new_csv_annotations[new_file] = self.csv_annotation_values[new_file]
    #         if not new_starting_row_found:
    #             if self.has_none_annotation(self.csv_annotation_values[new_file][2::]):
    #                 self.starting_row = dct_index
    #                 new_starting_row_found = True
    #     if not new_starting_row_found:
    #         self.starting_row = len(new_csv_annotations) - 1
    #     self.csv_annotation_values = new_csv_annotations

    def _next_image_clicked(self):
        """
        Move to the next image for annotating.

        If the last image is being annotated, write to csv. If the second
        image is being annotated, enable previous button.
        """

        self._annotator_model.set_previous_image_index(self._annotator_model.get_curr_img_index())
        self._annotator_model.set_curr_img_index(self._annotator_model.get_curr_img_index() + 1)
        # This dispatches a signal which updates  annotations dictionary and sets the next image
        self.annots.view.save_btn.setEnabled(True)

    def _prev_image_clicked(self):
        """
        Move to the previous image for annotating.

        If the first image is being annotated, disable button.
        """
        self._annotator_model.set_previous_image_index(self._annotator_model.get_curr_img_index())
        self._annotator_model.set_curr_img_index(self._annotator_model.get_curr_img_index() - 1)
        self.annots.view.save_btn.setEnabled(True)

    def _image_selected(self):
        """
        Record the annotations for the previously selected image and set current image.

        Called only when annotating un-blind and users select an image from the list.
        """
        self.annots.view.save_btn.setEnabled(True)
        self.annots.set_curr_img()

    def _exit_clicked(self):
        """Stop annotation if user confirms choice in popup."""
        proceed: bool = Popup.make_popup("Close this session? Your work will be saved.")
        if proceed:
            self._stop_annotating()

        self._images_view.update_num_files_label(self._annotator_model.get_num_images())

    def _save(self):
        """Save and write current annotations."""
        self.annots.save_annotations()
        self.annots.view.save_btn.setEnabled(False)

    def has_none_annotation(self, lst: List[Union[str, int, bool]]) -> bool:
        """
        Test if the given list has any empty string or None values.
        Returns
        -------
        bool
            True if null values are in the list.
        """

        if len(lst) < len(self._annotator_model.get_annotation_keys().keys()):
            return True
        else:
            for item in lst:
                if item is None or item == "":
                    return True
        return False
