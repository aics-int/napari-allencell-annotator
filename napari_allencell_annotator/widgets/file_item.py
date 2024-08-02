from pathlib import Path

from qtpy.QtGui import QFont
from qtpy.QtWidgets import QLayout
from qtpy.QtWidgets import (
    QListWidgetItem,
    QListWidget,
    QWidget,
    QHBoxLayout,
    QLabel,
    QCheckBox,
)


class FileItem(QListWidgetItem):
    """
    A class used to create custom QListWidgetItems.

    Attributes
    ----------
    file_path: str
        a path to the file.
    Methods
    -------
    get_name() -> str
        returns the basename of the file.
    unhide()
        shows the file name in label.
    """

    def __init__(self, file_path: Path, parent: QListWidget, hidden: bool = False):
        QListWidgetItem.__init__(self, parent)
        self._file_path: Path = file_path
        self.widget: QWidget = QWidget()
        self.layout: QHBoxLayout = QHBoxLayout()

        self.label: QLabel
        if hidden:
            self.label = QLabel("Image " + str(parent.row(self) + 1))
        else:
            self.label = QLabel(self._make_display_name())
        self.label.setFont(QFont("Arial", 18))

        self.layout.addWidget(self.label, stretch=15)

        self.check: QCheckBox = QCheckBox()
        self.check.setToolTip("Check box to select this image for deletion.")
        self.check.setCheckState(False)
        if hidden:
            self.check.hide()
        self.layout.addWidget(self.check, stretch=1)
        self.layout.addStretch()
        self.layout.setContentsMargins(2, 2, 0, 5)

        self.layout.setSizeConstraint(QLayout.SetMinimumSize)
        self.widget.setLayout(self.layout)

        self.setSizeHint(self.widget.minimumSizeHint())
        if parent is not None:
            parent.setItemWidget(self, self.widget)

    @property
    def file_path(self) -> Path:
        return self._file_path

    def get_file_path_str(self) -> str:
        return str(self._file_path)

    def get_name(self) -> str:
        """Return parent file name for zarr. Otherwise, return file name."""
        if self._file_path.suffix == ".zarr":
            return self._file_path.parent.stem
        else:
            return self._file_path.stem

    def unhide(self) -> None:
        """Display the file name instead of hidden name."""
        self.label.setText(self._make_display_name())
        self.check.show()

    def hide_check(self) -> None:
        """Hide the delete checkbox when annotating."""
        self.check.hide()

    def _make_display_name(self) -> str:
        """
        Truncate long file names

        Returns
        -------
        str
            truncated file name
        """
        path: str = self.get_name()
        if len(path) > 35:
            path = path[0:15] + "..." + path[-17:]
        return path

    def highlight(self):
        """highlight item"""
        self.label.setStyleSheet(
            """QLabel{
                            font-weight: bold;
                            text-decoration: underline;
                        }"""
        )

    def unhighlight(self):
        """unhighlight item"""
        self.label.setStyleSheet("""QLabel{}""")

    def __hash__(self):
        return hash(self._file_path)

    def __eq__(self, other):
        """Compares two ListItems file_path attributes"""
        if not isinstance(other, type(self)):
            return NotImplemented
        return self._file_path == other._file_path
