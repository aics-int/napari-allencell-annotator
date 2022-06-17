import sys

import napari
from PyQt5.QtWidgets import QApplication
from controller.main_controller import MainController



class App(QApplication):
    def __init__(self, sys_argv):
        super(App, self).__init__(sys_argv)
        self.model = MainModel

        self.napari = napari.Viewer()
        self.view = ImageViewer(self.napari)
        self.napari.window.add_dock_widget(self.view, area="right")
        self.main_controller = MainController(self.model, self.view)

        self.view.show()


if __name__ == '__main__':
    app = App(sys.argv)

    sys.exit(app.exec_())

