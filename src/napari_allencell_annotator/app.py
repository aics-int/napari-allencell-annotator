import sys

import napari
from PyQt5.QtWidgets import QApplication
from model.main_model import MainModel
from controller.main_controller import MainController
from view.main_view import MainWindow


class App(QApplication):
    def __init__(self, sys_argv, view):
        super(App, self).__init__(sys_argv)
        self.model = MainModel()
        self.main_controller = MainController(self.model)
        self.main_view = MainWindow(view, self.model, self.main_controller)
        view.window.add_dock_widget(self.main_view, area="right")
        self.main_view.show()


if __name__ == '__main__':
    view = napari.Viewer()
    app = App(sys.argv, view)

    sys.exit(app.exec_())

