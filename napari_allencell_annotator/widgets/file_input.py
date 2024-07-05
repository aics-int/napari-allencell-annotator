from enum import Enum

from qtpy.QtWidgets import QPushButton
from qtpy.QtWidgets import QHBoxLayout, QWidget, QFileDialog
from qtpy.QtCore import Signal
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

    files_selected: Signal = Signal(list)  # signal for multiple files
    dir_selected: Signal = Signal(Path)  # signal for dir selection
    file_selected: Signal = Signal(Path)  # TODO remove this once I refactor

    def __init__(
        self,
        parent: QWidget = None,
        mode: FileInputMode = FileInputMode.FILE,
        placeholder_text: str = None,
    ):
        super().__init__(parent)
        self._mode = mode

        self._input_btn = QPushButton(placeholder_text)
        self._input_btn.clicked.connect(self._select)

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

    def _select(self) -> None:
        if self._mode == FileInputMode.FILE:
            self._select_file()
        elif self._mode == FileInputMode.DIRECTORY:
            self._select_dir()
        elif self._mode == FileInputMode.JSON:
            self._select_json()
        elif self._mode == FileInputMode.CSV:
            self._select_csv()
        elif self._mode == FileInputMode.JSONCSV:
            self._select_csv_or_json()

    def _select_file(self) -> None:
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Select a file",
            options=QFileDialog.Option.DontUseNativeDialog | QFileDialog.Option.DontUseCustomDirectoryIcons,
        )
        self.files_selected.emit([Path(file) for file in files])

    def _select_json(self) -> None:
        file_path_str, _ = QFileDialog.getSaveFileName(
            self,
            "Select or create a json file",
            filter="JSON Files (*.json)",
            options=QFileDialog.Option.DontUseNativeDialog | QFileDialog.Option.DontUseCustomDirectoryIcons,
        )
        self.file_selected.emit(Path(file_path_str))

    def _select_dir(self) -> None:
        dir_path_str: str = QFileDialog.getExistingDirectory(
            self,
            "Select a directory",
            options=QFileDialog.Option.DontUseNativeDialog | QFileDialog.Option.DontUseCustomDirectoryIcons,
        )
        self.dir_selected.emit(Path(dir_path_str))

    def _select_csv(self) -> None:
        file_path_str: str
        file_path_str, _ = QFileDialog.getSaveFileName(
            self,
            "Select or create a csv file",
            filter="CSV Files (*.csv)",
            options=QFileDialog.Option.DontUseNativeDialog | QFileDialog.Option.DontUseCustomDirectoryIcons,
        )
        self.file_selected.emit(Path(file_path_str))

    def _select_csv_or_json(self) -> None:
        # JSONCSV
        file_path_str: str
        file_path_str, _ = QFileDialog.getOpenFileName(
            self,
            "Select a .csv or .json file with annotations",
            filter="CSV Files (*.csv) ;; JSON (*.json)",
            options=QFileDialog.Option.DontUseNativeDialog | QFileDialog.Option.DontUseCustomDirectoryIcons,
        )
        self.file_selected.emit(Path(file_path_str))