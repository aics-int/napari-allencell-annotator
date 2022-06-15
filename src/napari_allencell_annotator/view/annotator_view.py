
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout, QSpinBox, QLineEdit, QCheckBox, QComboBox, QTextEdit, \
    QPushButton


class AnnotatorMenu(QWidget):
    def __init__(self, viewer):
        super().__init__()
        self.label = QLabel("Annotations")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFont(QFont("Arial", 15))

        self.viewer = viewer


        self.setWindowTitle("Annotations Menu")
        self.setGeometry(500, 200, 400, 400)

        self.layout = QGridLayout()
        self.layout.addWidget(self.label, 0, 0, 1, 3)
        self.num_label = QLabel("Number of Cells:")

        self.layout.addWidget(self.num_label, 1, 0, 1, 2)
        self.spin = QSpinBox()
        self.spin.setRange(0, 1000)
        self.layout.addWidget(self.spin, 1, 2, 1, 1)

        self.type_label = QLabel("Type of Cells:")

        self.layout.addWidget(self.type_label, 2, 0, 1, 1)
        self.type = QLineEdit()
        self.layout.addWidget(self.type, 2, 1, 1, 2)

        self.check_box = QCheckBox()
        self.check_box.setText("Live cell at")
        self.check_box.stateChanged.connect(self.select_location)

        self.layout.addWidget(self.check_box, 3, 0, 1, 1)
        self.pos = QLineEdit()
        self.pos.setReadOnly(True)
        self.pos.setPlaceholderText("Click on Position")
        self.layout.addWidget(self.pos, 3, 1, 1, 2)
        self.mitos_label = QLabel("Phase of Mitosis:")

        self.layout.addWidget(self.mitos_label, 4, 0, 1, 1)
        self.drop_down = QComboBox()
        self.drop_down.addItems(
            [
                "none",
                "prophase",
                "metaphase",
                "anaphase",
                "telophase",
                "cytokinesis",
            ]
        )
        self.layout.addWidget(self.drop_down, 4, 1, 1, 2)

        self.desc_label = QLabel("Description of Image:")
        self.layout.addWidget(self.desc_label, 5, 0, 1, 3)

        self.description = QTextEdit()
        self.description.setPlaceholderText("Enter text here...")
        self.layout.addWidget(self.description, 6, 0, 3, 3)

        self.save_btn = QPushButton("Save and Export Annotations")
        self.layout.addWidget(self.save_btn, 9, 0, 1, 3)

        self.setLayout(self.layout)

    def select_location(self):
        if self.check_box.isChecked():
            self.viewer.mouse_double_click_callbacks.append(self.disp_position)

        else:
            self.viewer.mouse_double_click_callbacks.remove(self.disp_position)
            self.pos.setText()

    def disp_position(self, event, bla):
        self.pos.setText(str(self.viewer.cursor.position))
