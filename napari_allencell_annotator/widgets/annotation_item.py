from typing import Tuple, Dict

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QListWidgetItem, QListWidget, QWidget, QHBoxLayout, QLineEdit, QComboBox, QLabel, QSpinBox, \
    QSizePolicy, QGridLayout, QStyle, QPushButton, QCheckBox
from psygnal._signal import Signal


class AnnotationItem(QListWidgetItem):
    """
    A class used to create custom annotation QListWidgetItems.

    Attributes
    ----------
    """


    def __init__(
        self, parent: QListWidget
    ):
        QListWidgetItem.__init__(self, parent)
        self.widget = QWidget()
        self.layout = QGridLayout()
        name_label = QLabel('Name:')
        self.name = QLineEdit()
        self.name.setPlaceholderText("Enter name")

        type_label = QLabel('Type:')
        self.type = QComboBox()
        self.type.addItems(['text', 'number', 'checkbox', 'dropdown'])
        self.name.setWhatsThis("name")
        self.type.setWhatsThis("type")
        self.name_widget = QWidget()
        name_layout = QHBoxLayout()
        self.check = QCheckBox()
        name_layout.addWidget(self.check)
        name_layout.addWidget(name_label)
        self.name_widget.setLayout(name_layout)
        self.layout.addWidget(self.name_widget, 0,0,1,1)
        self.layout.addWidget(self.name, 0,1,1,2)
        self.layout.addWidget(type_label, 0,3,1,1)
        self.layout.addWidget(self.type, 0,4,1,2)
        default_label = QLabel('Default:')
        self.default_text = QLineEdit()
        self.default_text.setPlaceholderText('Default Text')
        self.default_num = QSpinBox()
        self.default_num.setValue(2)
        self.default_check = QComboBox()
        self.default_check.addItems(['checked', 'unchecked'])
        self.default_options_label = QLabel("Options:")
        self.default_options = QLineEdit()
        self.default_options.setPlaceholderText("Enter a comma separated list of options")

        self.default_options.setSizePolicy(QtWidgets.QSizePolicy.Policy.Ignored,
            QtWidgets.QSizePolicy.Policy.Preferred)
        self.default_options.setMinimumWidth(300)

        sp_retain = QtWidgets.QSizePolicy()
        sp_retain.setRetainSizeWhenHidden(True)
        self.default_options.setSizePolicy(sp_retain)
        self.default_options_label.setSizePolicy(sp_retain)

        self.layout.addWidget(default_label, 0,6,1,1)
        self.layout.addWidget(self.default_text, 0,7,1,2)
        self.layout.addWidget(self.default_options_label, 1,1,1,1)
        self.layout.addWidget(self.default_options, 1,2,1,7)
        self.default_options.hide()
        self.default_options_label.hide()

        self.layout.setContentsMargins(5, 5, 5, 15)

        self.widget.setLayout(self.layout)
        self.setSizeHint(self.widget.sizeHint())
        if parent is not None:
            parent.setItemWidget(self, self.widget)

        self.type.currentTextChanged.connect(self.type_changed)

    def type_changed(self, text : str):
        default_widget = self.layout.itemAtPosition(0,7).widget()
        default_widget.setParent(None)
        self.layout.removeWidget(default_widget)

        if text == 'text':
            self.default_options.hide()
            self.default_options_label.hide()
            self.layout.addWidget(self.default_text,0,7,1,2 )

        elif text == 'number':
            self.default_options.hide()
            self.default_options_label.hide()
            self.layout.addWidget(self.default_num, 0,7,1,2)

        elif text == 'checkbox':
            self.default_options.hide()
            self.default_options_label.hide()
            self.layout.addWidget(self.default_check, 0,7,1,2)
        else :
            self.default_options.show()
            self.default_options_label.show()
            self.layout.addWidget(self.default_text, 0,7,1,2)

    def get_data(self) -> Tuple[bool, str, Dict]:
        valid = True
        name : str = self.name.text()
        if name is None or name.isspace() or len(name) == 0:
            valid = False
            self.name.setStyleSheet(
            """
                        QLineEdit{
                            border: 1px solid red
                        }
                """
        )
        type : str = self.type.currentText()
        dct : Dict = {}

        if type == 'text':
            dct['type'] = 'string'
            dct['default'] = self.default_text.text()
        elif type == 'number':
            dct['type'] = 'number'
            dct['default'] = self.default_num.value()
        elif type == 'checkbox':
            dct['type'] = 'bool'
            if self.default_check.currentText() == 'checked':
                dct['default'] = 'true'
            else:
                dct['default'] = 'false'
        else:
            dct['type'] = 'list'
            dct['default'] = self.default_text.text()
            dct['options'] = self.default_options.text().split(',')
        return valid, name, dct


