import json
from napari_allencell_annotator.view.annotator_view import (
    AnnotatorView,
    AnnotatorViewMode,
)
from napari_allencell_annotator.util.directories import Directories
import napari

from typing import Dict, List, Optional
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
    set_csv_name(name : str)
        Sets csv file name for writing.

    stop_annotating()
        Resets values from annotating and changes mode to VIEW

    start_annotating(num_images : int)
        Changes annotation view to annotating mode.

    set_curr_img(curr_img : Dict[str, str])
        Sets the current image and adds the image to annotations_dict..

    record_annotations(prev_img: str)
        Adds the outgoing image's annotation values to the annotation_dict.

    write_to_csv()
        Writes header and annotations to the csv file.
    """

    def __init__(self, viewer: napari.Viewer):
        # 1 annotation
        # path = str(Directories.get_assets_dir() / "sample3.json")
        # 4 annotations
        # path = str(Directories.get_assets_dir() / "sample.json")
        # 8 annotations
        path: str = str(Directories.get_assets_dir() / "sample2.json")
        self.annot_data: Dict[str, Dict[str, str]] = json.load(open(path))
        # open in add mode
        # self.view = AnnotatorView(napari.Viewer(), data)
        # open in view mode
        self.view: AnnotatorView = AnnotatorView(
            viewer, self, mode=AnnotatorViewMode.VIEW
        )
        self.view.render_annotations(self.annot_data)
        self.view.show()
        self.curr_img: Dict[str, str] = None
        self.csv_name: str = None
        self.writer = None
        self.file = None
        # annotation dictionary maps file paths -> [file name, FMS, annot1val, annot2val, ...]
        self.annotation_dict: Dict[str, List[str]] = {}


    def set_csv_name(self, name: Optional[str] = None):
        """Set csv file name for writing."""
        self.csv_name = name

    def stop_annotating(self):
        """Reset values from annotating and change mode to VIEW."""
        self.record_annotations(self.curr_img['File Path'])
        self.write_csv()
        self.view.set_curr_index()
        self.annotation_dict = {}
        self.view.set_num_images()
        self.view.set_mode(mode=AnnotatorViewMode.VIEW)
        self.view.render_default_values()
        self.view.toggle_annots_editable(False)
        self.set_curr_img()
        self.set_csv_name()

    def start_annotating(self, num_images: int, dct : Dict[str,List[str]]):
        """
        Change annotation view to annotating mode.

        Parameters
        ----------
        num_images : int
            The total number of images to be annotated.
        """
        for path, lst in dct.items():
            self.annotation_dict[path] = lst
        self.view.set_num_images(num_images)
        self.view.set_mode(mode=AnnotatorViewMode.ANNOTATE)

    def set_curr_img(self, curr_img: Optional[Dict[str, str]] = None):
        """
        Set the current image and add the image to annotations_dict.

        Changes next button if annotating the last image.

        Parameters
        ----------
        curr_img : Dict[str, str]
            The current image file path, name, fms info, and row.
        """
        self.curr_img = curr_img
        if curr_img is not None:
            self.curr_img = curr_img
            path: str = curr_img["File Path"]
            if len(self.annotation_dict[path]) < 3:

                self.view.render_default_values()
            else:
                self.view.render_values(self.annotation_dict[path][2::])
            self.view.set_curr_index(int(curr_img["Row"]))
            if int(curr_img["Row"]) == self.view.num_images - 1:
                self.view.next_btn.setEnabled(False)
            elif int(curr_img["Row"]) == self.view.num_images - 2:
                self.view.next_btn.setEnabled(True)
                self.view.next_btn.setText("Next >")

    def record_annotations(self, prev_img: str):
        """
        Add the outgoing image's annotation values to the annotation_dict.

        Parameters
        ----------
        prev_img : str
            The previous image file path.
        """
        lst: List = self.view.get_curr_annots()
        self.annotation_dict[prev_img] = (
            self.annotation_dict[prev_img][:2:] + lst
        )

    def write_csv(self):
        """write headers and file info"""
        file = open(self.csv_name, "w")
        writer = csv.writer(file)
        header: List[str] = ["Annotations:"]
        for key, dic in self.annot_data.items():
            header.append(key)
            header.append(str(dic))
        writer.writerow(header)

        header = ["File Name", "File Path", "FMS"]
        for name in self.view.annots_order:
            header.append(name)
        writer.writerow(header)
        for name,lst in self.annotation_dict.items():
            writer.writerow([name] + lst)
        file.close()


