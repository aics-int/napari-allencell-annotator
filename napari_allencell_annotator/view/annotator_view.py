from enum import Enum
from typing import Dict, List

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QLineEdit, QSpinBox, QCheckBox, QComboBox, \
    QGridLayout, QListWidget, QScrollArea, QListWidgetItem, QPushButton, QAbstractScrollArea
import napari


class AnnotatorViewMode(Enum):
    """
    Mode for view.

    ADD is used when there is not an annotation set selected
    VIEW is used when an annotation set has been made/selected, but annotating has not started.
    ANNOTATE is used when the image set is finalized and annotating has started.
    """
    ADD = "add"
    VIEW = "view"
    ANNOTATE = "annotate"


class AnnotatorView(QWidget):
    """
    A class used to create a view for annotations.

    Inputs
    ----------
    viewer : napari.Viewer
        a napari viewer where the plugin will be used
    mode : AnnotatorViewMode
        a mode for the view

    Methods
    -------
    mode() -> AnnotatorViewMode

    set_mode(mode: AnnotatorViewMode)

    set_num_images(num: int)
        Sets the total images to be annotated.

    set_curr_index(num: int)
        Sets the index of the currently selected image.

    get_curr_annots() -> List
        Returns the current annotation values in a list form.

    make_annots_editable()
        Enables the annotations for editing.

    render_annotations(data : Dict[str,Dict[str, str]]))
        Renders GUI elements from the dictionary of annotations.
    """

    def __init__(self, viewer: napari.Viewer,
                 mode: AnnotatorViewMode = AnnotatorViewMode.ADD):
        super().__init__()
        self._mode = mode
        label = QLabel("Annotations")
        label.setAlignment(Qt.AlignCenter)
        label.setFont(QFont("Arial", 15))
        self.layout = QGridLayout()
        self.layout.addWidget(label, 0, 0, 1, 4)

        self.annot_list = QListWidget()

        self.scroll = QScrollArea()
        self.scroll.setWidget(self.annot_list)
        self.scroll.setWidgetResizable(True)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.scroll.setStyleSheet('''QScrollBar:vertical {
            width:10px;    
            margin: 0px 0px 0px 0px;
        }''')
        style = '''QScrollBar::handle:vertical {border: 0px solid red; border-radius: 
        2px;} '''
        self.scroll.setStyleSheet(self.scroll.styleSheet() + style)
        self.layout.addWidget(self.scroll, 1, 0, 10, 4)

        self.num_images: int = None
        self.curr_index: int = None

        # Add widget visible in ADD mode
        self.add_widget = QWidget()
        add_layout = QHBoxLayout()
        self.create_btn = QPushButton("Create Annotations")
        self.create_btn.setEnabled(True)
        self.import_btn = QPushButton("Import Existing Annotations")
        self.import_btn.setEnabled(True)

        add_layout.addWidget(self.create_btn, stretch=2)
        add_layout.addWidget(self.import_btn, stretch=2)
        self.add_widget.setLayout(add_layout)
        self.layout.addWidget(self.add_widget, 12, 0, 1, 4)
        self.add_widget.hide()

        # view widget visible in VIEW mode
        self.view_widget = QWidget()
        view_layout = QHBoxLayout()
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setEnabled(False)
        self.start_btn = QPushButton("Start Annotating")
        self.start_btn.setEnabled(True)

        view_layout.addWidget(self.cancel_btn, stretch=1)
        view_layout.addWidget(self.start_btn, stretch=3)
        self.view_widget.setLayout(view_layout)
        self.layout.addWidget(self.view_widget, 12, 0, 1, 4)
        self.view_widget.hide()

        # annot widget visible in ANNOTATE mode
        self.annot_widget = QWidget()
        annot_layout = QGridLayout()
        self.back_btn = QPushButton("< Previous")
        self.back_btn.setEnabled(False)
        self.next_btn = QPushButton("Next >")
        self.next_btn.setEnabled(True)
        self.progress_bar = QLabel()
        annot_layout.addWidget(self.progress_bar, 0, 1, 1, 2)
        annot_layout.addWidget(self.back_btn, 1, 0, 1, 2)
        annot_layout.addWidget(self.next_btn, 1, 2, 1, 2)
        self.annot_widget.setLayout(annot_layout)
        self.layout.addWidget(self.annot_widget, 12, 0, 2, 4)
        self.view_widget.hide()

        self._display_mode()
        self.annotation_item_widgets: List[QWidget] = []

        self.setLayout(self.layout)
        self.viewer: napari.Viewer = viewer

    @property
    def mode(self) -> AnnotatorViewMode:
        return self._mode

    def set_mode(self, mode: AnnotatorViewMode):
        self._mode = mode
        self._display_mode()

    def set_num_images(self, num: int):
        """Set the total number of images to be annotated"""
        self.num_images = num

    def set_curr_index(self, num: int):
        """Set the index of the currently selected image and display it on progress bar."""
        self.curr_index = num
        self.progress_bar.setText("{} of {} Images".format(self.curr_index + 1, self.num_images))

    def get_curr_annots(self) -> List:
        """
        Return the current annotation values in a list.

        Returns
        ----------
        List
            a list of annotation values.
        """
        annots = []
        for i in self.annotation_item_widgets:
            value = ""
            if isinstance(i, QLineEdit):
                value = i.text()
            elif isinstance(i, QSpinBox):
                value = i.value()
            elif isinstance(i, QCheckBox):
                value = i.checkState()
            elif isinstance(i, QComboBox):
                value = i.currentData()
            annots.append(value)
        return annots

    def make_annots_editable(self):
        """Enable the annotation widgets for editing. """
        for i in self.annotation_item_widgets:
            i.setEnabled(True)

    def _display_mode(self):
        """Render GUI buttons visible depending on the mode."""
        if self._mode == AnnotatorViewMode.ADD:
            self.annot_list.clear()
            self.annot_widget.hide()
            self.view_widget.hide()
            self.add_widget.show()
        elif self._mode == AnnotatorViewMode.VIEW:
            self.annot_widget.hide()
            self.view_widget.show()
            self.add_widget.hide()

        elif self._mode == AnnotatorViewMode.ANNOTATE:
            self.annot_widget.show()
            self.view_widget.hide()
            self.add_widget.hide()

    def render_annotations(self, data: Dict[str, Dict[str, str]]):
        """
        Read annotation dictionary into individual annotations.

        Parameters
        ----------
        data : Dict[str, Dict[str, str]]
            The dictionary of annotation types.
        """
        self.annotation_item_widgets = []
        if len(data) < 9:
            self.annot_list.setMaximumHeight(45.5*len(data))
        for name in data.keys():
            self._create_annot(name, data[name])

    def _create_annot(self, name: str, dictn: Dict[str, str]):
        """
        Create annotation widgets from dictionary entries.

        Parameters
        ----------
        name : str
            annotation name.
        dictn : Dict[str]
            annotation types and data.
        """
        widget = QWidget()
        layout = QHBoxLayout()
        label = QLabel(name)
        layout.addWidget(label, stretch=1)
        annot_type: str = dictn['type']
        if annot_type == "string":
            item = QLineEdit(dictn['default'])
        elif annot_type == "number":
            item = QSpinBox()
            item.setValue(dictn['default'])
        elif annot_type == "bool":
            item = QCheckBox()
            if dictn['default'] == 'true' or dictn['default']:
                item.setChecked(True)
        elif annot_type == "list":
            item = QComboBox()
            for opt in dictn['options']:
                item.addItem(opt)
            item.setCurrentText(dictn['default'])
        else:
            return  # TODO
        layout.addWidget(item, stretch=2)
        item.setEnabled(False)
        self.annotation_item_widgets.append(item)
        # layout.addStretch()
        layout.setContentsMargins(2,12,8,12)
        layout.setSpacing(2)
        widget.setLayout(layout)
        print(widget.minimumHeight())
        list_item = QListWidgetItem(self.annot_list)
        list_item.setSizeHint(widget.minimumSizeHint())
        self.annot_list.setItemWidget(list_item, widget)
