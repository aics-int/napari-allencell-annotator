from napari_allencell_annotator.view.annotator_view import (
    AnnotatorView,
    AnnotatorViewMode,
)
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
    set_annot_json_data(dct : Dict[str, Dict])
        Sets annotation data dictionary.

    set_csv_name(name : str)
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

    write_to_csv()
        Writes header and annotations to the csv file.
    """

    def __init__(self, viewer: napari.Viewer):
        # 1 annotation
        # path = str(Directories.get_assets_dir() / "sample3.json")
        # 4 annotations
        # path = str(Directories.get_assets_dir() / "sample.json")
        # 8 annotations
        # path: str = str(Directories.get_assets_dir() / "sample2.json")
        # self.annot_json_data: Dict[str, Dict] = json.load(open(path))

        # dictionary of json info:
        self.annot_json_data: Dict[str, Dict] = None
        # open in view mode
        self.view: AnnotatorView = AnnotatorView(viewer)

        self.view.show()
        # {'File Path' : path, 'Row' : str(row)}
        self.curr_img_dict: Dict[str, str] = None
        self.csv_name: str = None
        # annotation dictionary maps file paths -> [file name, FMS, annot1val, annot2val, ...]
        self.files_and_annots: Dict[str, List[str]] = {}

        self.view.cancel_btn.clicked.connect(self.stop_viewing)

    def set_annot_json_data(self, dct: Dict[str, Dict]):
        """Set annotation data dictionary."""
        self.annot_json_data = dct

    def set_csv_name(self, name: Optional[str] = None):
        """Set csv file name for writing."""
        self.csv_name = name

    def start_viewing(self):
        """Change view to VIEW mode and render annotations."""
        self.view.set_mode(mode=AnnotatorViewMode.VIEW)
        self.view.render_annotations(self.annot_json_data)

    def stop_viewing(self):
        """Change view to ADD mode, reset annotations, and clear annotation json data."""
        self.view.set_mode(mode=AnnotatorViewMode.ADD)
        self.annot_json_data = None

    def start_annotating(self, num_images: int, dct: Dict[str, List[str]]):
        """
        Change annotation view to annotating mode and create files_and_annots with files.

        Parameters
        ----------
        num_images : int
            The total number of images to be annotated.
        dct : Dict[str, List[str]]
            The files to be used. path -> [name, FMS]
        """
        self.files_and_annots = dct
        self.view.set_num_images(num_images)
        self.view.set_mode(mode=AnnotatorViewMode.ANNOTATE)

    def stop_annotating(self):
        """Reset values from annotating and change mode to ADD."""
        self.record_annotations(self.curr_img_dict["File Path"])
        self.write_csv()
        self.view.set_curr_index()
        self.files_and_annots = {}
        self.view.set_num_images()
        self.view.set_mode(mode=AnnotatorViewMode.ADD)
        self.view.render_default_values()
        self.view.toggle_annots_editable(False)
        self.set_curr_img()
        self.set_csv_name()

    def set_curr_img(self, curr_img: Optional[Dict[str, str]] = None):
        """
        Set the current image and add the image to annotations_dict.

        Changes next button if annotating the last image.

        Parameters
        ----------
        curr_img : Dict[str, str]
            The current image {'File Path' : 'path', 'Row' : str(rownum)}
        """
        self.curr_img_dict = curr_img
        if curr_img is not None:
            path: str = curr_img["File Path"]
            # files_and_annots values are lists File Path ->[File Name, FMS, annot1val, annot2val ...]
            # if the file has not been annotated the list is just length 2 [File Name, FMS]
            if len(self.files_and_annots[path]) < 3:
                # if the image is un-annotated render the default values

                self.view.render_default_values()
            else:
                # if the image has been annotated render the values that were entered
                # dictionary list [2::] is [annot1val, annot2val, ...]
                self.view.render_values(self.files_and_annots[path][2::])
            # convert row to int
            self.view.set_curr_index(int(curr_img["Row"]))
            # if at the end disable next
            if int(curr_img["Row"]) == self.view.num_images - 1:
                self.view.next_btn.setEnabled(False)
            # in case we were just on the last image and then went to the previous, re-enable next
            elif int(curr_img["Row"]) == self.view.num_images - 2:
                self.view.next_btn.setEnabled(True)

    def record_annotations(self, prev_img: str):
        """
        Add the outgoing image's annotation values to the files_and_annots.

        Parameters
        ----------
        prev_img : str
            The previous image file path.
        """
        lst: List = self.view.get_curr_annots()
        self.files_and_annots[prev_img] = self.files_and_annots[prev_img][:2:] + lst

    def write_csv(self):
        """write headers and file info"""
        file = open(self.csv_name, "w")
        writer = csv.writer(file)
        header: List[str] = ["Annotations:"]
        for key, dic in self.annot_json_data.items():
            header.append(key)
            header.append(str(dic))
        writer.writerow(header)

        header = ["File Name", "File Path", "FMS"]
        for name in self.view.annots_order:
            header.append(name)
        writer.writerow(header)
        for name, lst in self.files_and_annots.items():
            writer.writerow([name] + lst)
        file.close()
