from unittest import mock
from unittest.mock import MagicMock, create_autospec


from napari_allencell_annotator.controller.main_controller import MainController
from napari_allencell_annotator.controller.main_controller import ImagesController
from napari_allencell_annotator.controller.main_controller import AnnotatorController
from napari_allencell_annotator.controller.main_controller import QVBoxLayout



class TestMainController:
    def setup_method(self):
        with mock.patch.object(MainController, "__init__", lambda x: None):
            self._controller = MainController()
            self._controller.images= create_autospec(ImagesController)
            self._controller.images.view = MagicMock()
            self._controller.layout = create_autospec(QVBoxLayout)

            self._controller.annots = create_autospec(AnnotatorController)
            self._controller.annots.view = MagicMock()

    def test_start_annotating_none(self):
        self._controller.images.get_num_files = MagicMock(return_value=None)
        self._controller.images.view.alert = MagicMock()
        self._controller.layout.removeWidget = MagicMock()
        self._controller.images.view.hide = MagicMock()
        self._controller.images.start_annotating = MagicMock()

        self._controller.start_annotating()
        self._controller.images.get_num_files.assert_called_once()
        self._controller.images.view.alert.assert_called_once_with("Can't Annotate Without Adding Images")
        self._controller.layout.removeWidget.assert_not_called()

    def test_start_annotating_zero(self):
        self._controller.images.get_num_files = MagicMock(return_value=0)
        self._controller.images.view.alert = MagicMock()
        self._controller.layout.removeWidget = MagicMock()
        self._controller.images.view.hide = MagicMock()
        self._controller.images.start_annotating = MagicMock()

        self._controller.start_annotating()
        assert len(self._controller.images.get_num_files.mock_calls) == 2

        self._controller.images.view.alert.assert_called_once_with("Can't Annotate Without Adding Images")
        self._controller.layout.removeWidget.assert_not_called()

    def test_start_annotating(self):
        self._controller.images.view.alert = MagicMock()
        self._controller.layout.removeWidget = MagicMock()
        self._controller.images.view.hide = MagicMock()
        self._controller.images.start_annotating = MagicMock()
        self._controller.images.get_num_files = MagicMock(return_value=5)
        self._controller.images.curr_img_dict = MagicMock(return_value='dict')
        self._controller.annots.start_annotating = MagicMock()
        self._controller.annots.set_curr_img = MagicMock()

        self._controller.start_annotating()
        assert len(self._controller.images.get_num_files.mock_calls) == 3

        self._controller.images.view.alert.assert_not_called()
        self._controller.layout.removeWidget.assert_called_once_with(self._controller.images.view)

        self._controller.images.view.hide.assert_called_once_with()
        self._controller.images.start_annotating.assert_called_once_with()
        self._controller.images.curr_img_dict.assert_called_once_with()
        self._controller.annots.start_annotating.assert_called_once_with(5)
        self._controller.annots.set_curr_img.assert_called_once_with('dict')

    def test_next_image_save(self):
        self._controller.annots.view.next_btn.text = MagicMock(return_value= "Save and Export")
        self._controller.annots.write_to_csv = MagicMock()
        self._controller.annots.write_image_csv = MagicMock()

        self._controller.next_image()

        self._controller.annots.view.next_btn.text.assert_called_once_with()
        self._controller.annots.write_to_csv.assert_called_once_with()
        self._controller.annots.write_image_csv.assert_not_called()

    def test_next_image(self):
        self._controller.annots.view.next_btn.text = MagicMock(return_value= "Next")
        self._controller.annots.write_to_csv = MagicMock()
        self._controller.annots.write_image_csv = MagicMock()
        self._controller.images.curr_img_dict = MagicMock(return_value="return")
        self._controller.images.next_img = MagicMock()
        self._controller.annots.set_curr_img = MagicMock()

        self._controller.next_image()

        self._controller.annots.view.next_btn.text.assert_called_once_with()
        self._controller.annots.write_to_csv.assert_not_called()
        self._controller.annots.write_image_csv.assert_called_once_with('return')
        assert len(self._controller.images.curr_img_dict.mock_calls) == 2
        self._controller.images.next_img.assert_called_once_with()
        self._controller.annots.set_curr_img.assert_called_once_with('return')




