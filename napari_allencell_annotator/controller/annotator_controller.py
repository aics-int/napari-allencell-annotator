import json
from pathlib import Path

from napari_allencell_annotator.model.annotation_model import AnnotatorModel
from napari_allencell_annotator.model.key import Key
from napari_allencell_annotator.util.json_utils import JSONUtils
from napari_allencell_annotator.view.annotator_view import (
    AnnotatorView,
    AnnotatorViewMode,
)
import napari

from typing import Dict, List, Optional, Any
import csv


class AnnotatorController:
    """
    A class used to control the model and view for annotations.

    Inputs
    ----------
    viewer : napari.Viewer
        a napari viewer where the plugin will be used

    Methods
    -------
    set_annot_json_data(dct : dct: Dict[str, Dict[str, Any]])
        Sets annotation data dictionary.

    set_csv_path(path : str)
        Sets csv file name for writing.

    start_viewing()
        Changes view to VIEW mode and render annotations.

    stop_viewing()
        Changes view to ADD mode, resets annotations, and clears annotation json data.

    start_annotating(num_images: int, dct: Dict[str, List[str]])
        Changes annotation view to annotating mode.

    stop_annotating()
        Resets values from annotating and changes mode to VIEW.

    set_curr_img(curr_img_dict : Dict[str, str])
        Sets the current image and adds the image to annotations_dict.

    record_annotations(prev_img: str)
        Adds the outgoing image's annotation values to the files_and_annots.

    read_json(file_path : str)
        Reads a json file into a dictionary and sets annot_json_data.

    read_csv(file_path : str)
        Reads the first line of a csv file into a dictionary and sets annot_json_data.

    write_to_csv()
        Writes header and annotations to the csv file.
    """

    def __init__(self, model: AnnotatorModel, viewer: napari.Viewer):
        self._annotation_model = model

        # open in view mode
        self.view: AnnotatorView = AnnotatorView(model, viewer)

        self.view.show()

        self.view.cancel_btn.clicked.connect(self.stop_viewing)
        # we want to save the annotation for the image that we just switched off of.
        self._annotation_model.image_changed.connect(
            lambda: self.record_annotations(self._annotation_model.get_previous_image_index())
        )

    def write_json(self, file_path: str):
        """
        Write annotation dictionary to a file.

        file_path : str
            file path for json file to write to.
        """

        json_data: str = JSONUtils.dict_to_json_dump(self._annotation_model.get_annotation_keys())
        JSONUtils.write_json_data(json_data, Path(file_path))

    def start_viewing(self, alr_anntd: Optional[bool] = False):
        """Change view to VIEW mode and render annotations."""
        self.view.set_mode(mode=AnnotatorViewMode.VIEW)
        self.view.render_annotations(
            self._annotation_model.get_annotation_keys()
        )  # TODO fix render_annotations to use annoations dict
        # disable edit button if already annotated is True
        self.view.edit_btn.setEnabled(not alr_anntd)

    def stop_viewing(self):
        """Change view to ADD mode, reset annotations, and clear annotation json data."""
        self.view.set_mode(mode=AnnotatorViewMode.ADD)
        self._annotation_model.clear_annotation_keys()

    def start_annotating(self):
        """
        Change annotation view to annotating mode and create files_and_annots with files.

        Parameters
        ----------
        num_images : int
            The total number of images to be annotated.
        dct : Dict[str, List[str]]
            The files to be used. path -> [name, FMS]
        """
        self.view.set_mode(mode=AnnotatorViewMode.ANNOTATE)

        self.view.annot_list.create_evt_listeners()
        # self.view.annot_list.currentItemChanged.connect(self._curr_item_changed)

    def save_annotations(self):
        """Save current annotation data"""
        # save annotations for file we're on
        self.record_annotations(self._annotation_model.get_curr_img_index())
        self.write_csv()

    def stop_annotating(self):
        """Reset values from annotating and change mode to ADD."""
        self.record_annotations(self._annotation_model.get_curr_img_index())

        for idx in range(self._annotation_model.get_num_images()):
            if self._annotation_model.get_image_at(idx) not in self._annotation_model.get_annotations():
                self._annotation_model.add_annotation(self._annotation_model.get_image_at(idx), [])

        self.write_csv()
        # reset optional fields in model to None (pre-annottion state)
        self._annotation_model.set_annotation_started(False)
        self._annotation_model.set_csv_save_path(None)
        self.view.set_mode(AnnotatorViewMode.VIEW)

    def _curr_item_changed(self, current, previous):
        """
        Highlight the new current annotation selection and unhighlight the previous.

        Parameters
        ----------
        current : TemplateItem
        previous : TemplateItem
        """
        if current is not None:
            # test
            current.highlight()
            current.set_focus()
        if previous is not None:
            previous.unhighlight()

    def set_curr_img(self):
        """
        Set the current image and add the image to annotations_dict.

        Changes next button if annotating the last image.

        Parameters

        ----------
        curr_img : Dict[str, str]
            The current image {'File Path' : 'path', 'Row' : str(rownum)}
        """
        if self._annotation_model.get_annotations() is not None:
            path: Path = self._annotation_model.get_curr_img()
            # files_and_annots values are lists File Path ->[File Name, FMS, annot1val, annot2val ...]
            # if the file has not been annotated the list is just length 2 [File Name, FMS]
            if path not in list(self._annotation_model.get_annotations().keys()):
                # if the image is un-annotated render the default values
                self.view.render_default_values()
            else:
                # if the image has been annotated render the values that were entered
                # dictionary list [2::] is [annot1val, annot2val, ...]
                self.view.render_values(self._annotation_model.get_annotations()[path])
            # convert row to int
            self.view.display_current_progress()
            # if at the end disable next
            if self._annotation_model.get_curr_img_index() == self._annotation_model.get_num_images() - 1:
                self.view.next_btn.setEnabled(False)
            else:
                self.view.next_btn.setEnabled(True)
            # if at the start disable prev
            if self._annotation_model.get_curr_img_index() == 0:
                self.view.prev_btn.setEnabled(False)
            else:
                self.view.prev_btn.setEnabled(True)

    def record_annotations(self, record_idx: int):
        """
        Add the image's annotation values to the annotation dictionary

        Parameters
        ----------
        record_idx : int
            The index of the image we should save annotations for
        """
        if record_idx is not None and self._annotation_model.is_annotation_started():  # ignore recording annotations when loading first image or just starting out
            # we're saving annotation for the image we just switched off of.
            self._annotation_model.add_annotation(
                self._annotation_model.get_all_images()[record_idx], self.view.get_curr_annots()
            )

    def read_json(self, file_path: Path):
        # TODO change param to path
        """
        Read a json file into a dictionary and set annot_json_data.

        Parameters
        ----------
        file_path : str
            file path to json file to read from
        """
        json_dict: dict[str, Key] = JSONUtils.json_dump_to_dict(JSONUtils.get_json_data(Path(file_path)))
        self._annotation_model.set_annotation_keys(json_dict)

    def get_annotations_csv(self, annotations: str):
        # TODO change param to path
        """
        Read the first line of a csv file into a dictionary and set annot_json_data.

        Parameters
        ----------
        annotations: str
            a string of annotation dictionary data from the csv
        """
        json_dict: dict[str, Key] = JSONUtils.json_dump_to_dict(annotations)
        self._annotation_model.set_annotation_keys(json_dict)

    def write_csv(self):
        # TODO put into csv utils class
        """write headers and file info"""
        file = open(self._annotation_model.get_csv_save_path(), "w")
        writer = csv.writer(file)
        writer.writerow(["Shuffled:", self._annotation_model.is_images_shuffled()])
        header: List[str] = ["Annotations:", JSONUtils.dict_to_json_dump(self._annotation_model.get_annotation_keys())]
        writer.writerow(header)

        header = ["File Name", "File Path"]
        for name in self.view.annots_order:
            header.append(name)
        writer.writerow(header)
        for path, annotations in self._annotation_model.get_annotations().items():
            writer.writerow([path.name, str(path)] + annotations)
        file.close()
