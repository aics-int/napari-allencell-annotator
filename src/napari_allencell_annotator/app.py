import sys

from PyQt5.QtWidgets import QApplication
import model.main_model as MainModel
from controller.main_controller import MainController
from view.main_view import MainWindow


class App(QApplication):
    def __init__(self, sys_argv):
        super(App, self).__init__(sys_argv)
        self.model = MainModel
        self.view = MainWindow()
        self.main_controller = MainController(self.model, self.view)

        self.view.show()


if __name__ == '__main__':
    app = App(sys.argv)

    sys.exit(app.exec_())

