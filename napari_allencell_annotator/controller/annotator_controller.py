import json
from napari_allencell_annotator.view.annotator_view import AnnotatorView, AnnotatorViewMode
from napari_allencell_annotator.util.directories import Directories
import napari

from typing import Dict
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
    """

    def __init__(self, viewer: napari.Viewer):
        # 1 annotation
        # path = str(Directories.get_assets_dir() / "sample3.json")
        # 4 annotations
        # path = str(Directories.get_assets_dir() / "sample.json")
        # 8 annotations
        path = str(Directories.get_assets_dir() / "sample2.json")
        self.annot_data = json.load(open(path))
        # open in add mode
        # self.view = AnnotatorView(napari.Viewer(), data)
        # open in view mode
        self.view = AnnotatorView(viewer, mode=AnnotatorViewMode.VIEW)
        self.view.render_annotations(self.annot_data)
        self.view.show()
        self.curr_img = None
        self.file = None
        self.writer= None

    def start_annotating(self, num_images: int):
        """"""
        # create/write header line of csv

        self.view.set_num_images(num_images)
        self.view.set_mode(mode=AnnotatorViewMode.ANNOTATE)
        self.view.make_annots_editable()
        self.file = open('csv.csv', 'w')
        self.writer = csv.writer(self.file)
        self.write_header()

    def set_curr_img(self, curr_img: Dict[str, str]):
        self.curr_img = curr_img
        self.view.set_curr_index(int(curr_img["Row"]))
        if int(curr_img["Row"]) == self.view.num_images -1:
            self.view.next_btn.setText("Save and Export")

    def write_image_csv(self, prev_img: Dict[str, str]):
        # filename, filepath, fms, annots
        line = [prev_img["File Name"], prev_img["File Path"], prev_img["FMS"]]
        for value in self.view.get_curr_annots():
            line.append(value)
        self.writer.writerow(line)


    def write_header(self):
        header = ["File Name", "File Path", "FMS"]
        for key in self.annot_data.keys():
            header.append(key)
        self.writer.writerow(header)

    def save_and_export(self):
        self.file.close()
