from enum import Enum

from qtpy.QtWidgets import QPushButton
from qtpy.QtWidgets import QHBoxLayout, QWidget, QFileDialog
from qtpy.QtCore import Signal
from typing import List, Optional
from pathlib import Path


class FileInputMode(Enum):
    DIRECTORY: str = "dir"
    FILE: str = "file"
    CSV: str = "csv"
    JSONCSV: str = "jsoncsv"
    JSON: str = "json"


class FileInput(QWidget):
    """
    A file input Widget that includes a file dialog for selecting a file / directory
    and a text box to display the selected file
    inputs:
        mode (FileInputMode): file dialog selection type to File, Directory, Csv, JSON/Csv, or JSON .
        initial_text (str): text to display in the widget before a file has been selected
    """

    file_selected: Signal = Signal(list)
    selected_file: Optional[List[Path]] = None

    def __init__(
        self,
        parent: QWidget = None,
        mode: FileInputMode = FileInputMode.FILE,
        placeholder_text: str = None,
    ):
        super().__init__(parent)
        self._mode = mode

        self._input_btn = QPushButton(placeholder_text)
        self._input_btn.clicked.connect(self._select_file)

        layout: QHBoxLayout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self._input_btn)
        self.setLayout(layout)

    @property
    def mode(self) -> FileInputMode:
        return self._mode

    def simulate_click(self) -> None:
        """Simulate a click event to open the file dialog."""
        self._input_btn.clicked.emit()

    def toggle(self, enabled: bool) -> None:
        """
        Enable and un-enable user clicking of the add file button.

        Parameters
        ----------
        enabled : bool
        """
        self._input_btn.setEnabled(enabled)

    def _select_file(self) -> None:  # pragma: no-cover
        file_path: Optional[List[str]]
        if self._mode == FileInputMode.FILE:
            file_path, _ = QFileDialog.getOpenFileNames(
                self,
                "Select a file",
                options=QFileDialog.Option.DontUseNativeDialog | QFileDialog.Option.DontUseCustomDirectoryIcons,
            )
        elif self._mode == FileInputMode.DIRECTORY:
            dir_path_str: str = QFileDialog.getExistingDirectory(
                self,
                "Select a directory",
                options=QFileDialog.Option.DontUseNativeDialog | QFileDialog.Option.DontUseCustomDirectoryIcons,
            )
            if len(dir_path_str) > 0:
                file_path = [dir_path_str]
            else:
                file_path = None
        elif self._mode == FileInputMode.CSV:
            file_path_str: str
            file_path_str, _ = QFileDialog.getSaveFileName(
                self,
                "Select or create a csv file",
                filter="CSV Files (*.csv)",
                options=QFileDialog.Option.DontUseNativeDialog | QFileDialog.Option.DontUseCustomDirectoryIcons,
            )
            if file_path_str is None or file_path_str == "":
                file_path = None
            else:
                file_path = [file_path_str]
        elif self._mode == FileInputMode.JSON:
            file_path_str: str
            file_path_str, _ = QFileDialog.getSaveFileName(
                self,
                "Select or create a json file",
                filter="JSON Files (*.json)",
                options=QFileDialog.Option.DontUseNativeDialog | QFileDialog.Option.DontUseCustomDirectoryIcons,
            )
            if file_path_str is None or file_path_str == "":
                file_path = None
            else:
                file_path = [file_path_str]
        else:
            # JSONCSV
            file_path_str: str
            file_path_str, _ = QFileDialog.getOpenFileName(
                self,
                "Select a .csv or .json file with annotations",
                filter="CSV Files (*.csv) ;; JSON (*.json)",
                options=QFileDialog.Option.DontUseNativeDialog | QFileDialog.Option.DontUseCustomDirectoryIcons,
            )

            if file_path_str is None or file_path_str == "":
                file_path = None
            else:
                file_path = [file_path_str]

        if file_path:
            file_path_obj: List[Path] = self.convert_to_path_object(file_path)
            self.selected_file = file_path_obj
            self.file_selected.emit(file_path_obj)

    def convert_to_path_object(self, file_path_str: List[str]) -> List[Path]:
        return list(map(lambda x: Path(x), file_path_str))
