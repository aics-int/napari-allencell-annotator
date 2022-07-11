from unittest import mock
from unittest.mock import MagicMock, create_autospec

from napari_allencell_annotator.controller.main_controller import (
    MainController,
)
from napari_allencell_annotator.controller.main_controller import (
    ImagesController,
)
from napari_allencell_annotator.controller.main_controller import (
    AnnotatorController,
)
from napari_allencell_annotator.controller.main_controller import (
    QVBoxLayout,
    os,
)


class TestMainController:
    def setup_method(self):
        with mock.patch.object(MainController, "__init__", lambda x: None):
            self._controller = MainController()
            self._controller.images = create_autospec(ImagesController)
            self._controller.images.view = MagicMock()
            self._controller.layout = create_autospec(QVBoxLayout)

            self._controller.annots = create_autospec(AnnotatorController)
            self._controller.annots.view = MagicMock()

    def test_file_selected_evt_none(self):
        self._controller._file_selected_evt(None)
        self._controller.images.view.alert.assert_called_once_with(
            "No selection provided"
        )

    def test_file_selected_evt_empty(self):
        self._controller._file_selected_evt([])
        self._controller.images.view.alert.assert_called_once_with(
            "No selection provided"
        )

    def test_file_selected_evt_not_csv(self):
        os.path.splitext = MagicMock(return_value=("path", ""))
        self._controller._setup_annotating = MagicMock()
        self._controller._file_selected_evt(["path"])
        self._controller.annots.set_csv_name.assert_called_once_with(
            "path.csv"
        )
        self._controller._setup_annotating.assert_called_once_with()
        self._controller.images.view.alert.assert_not_called()

    def test_file_selected_evt_csv(self):
        os.path.splitext = MagicMock(return_value=("path", ".csv"))
        self._controller._setup_annotating = MagicMock()
        self._controller._file_selected_evt(["path.csv"])
        self._controller.annots.set_csv_name.assert_called_once_with(
            "path.csv"
        )
        self._controller._setup_annotating.assert_called_once_with()
        self._controller.images.view.alert.assert_not_called()

    def test_start_annotating_none(self):
        self._controller.images.get_num_files = MagicMock(return_value=None)

        self._controller.start_annotating()
        self._controller.images.get_num_files.assert_called_once()
        self._controller.images.view.alert.assert_called_once_with(
            "Can't Annotate Without Adding Images"
        )

    def test_start_annotating_zero(self):
        self._controller.images.get_num_files = MagicMock(return_value=0)

        self._controller.start_annotating()
        assert len(self._controller.images.get_num_files.mock_calls) == 2
        self._controller.images.view.alert.assert_called_once_with(
            "Can't Annotate Without Adding Images"
        )

    def test_start_annotating_true(self):
        self._controller.images.get_num_files = MagicMock(return_value=1)
        self._controller.annots.view.popup.return_value = True
        self._controller.start_annotating()
        assert len(self._controller.images.get_num_files.mock_calls) == 2
        self._controller.images.view.alert.assert_not_called()
        self._controller.annots.view.file_input.simulate_click.assert_called_once_with()

    def test_start_annotating_false(self):
        self._controller.images.get_num_files.return_value = 1
        self._controller.annots.view.popup.return_value = False
        self._controller.start_annotating()
        assert len(self._controller.images.get_num_files.mock_calls) == 2
        self._controller.images.view.alert.assert_not_called()
        self._controller.annots.view.file_input.simulate_click.assert_not_called()

    def test_stop_annotating(self):
        self._controller.stop_annotating()
        self._controller.layout.addWidget.assert_has_calls(
            [
                mock.call(self._controller.images.view, stretch=1),
                mock.call(self._controller.annots.view, stretch=2),
            ]
        )
        self._controller.images.view.show.assert_called_once_with()
        self._controller.images.stop_annotating.assert_called_once_with()
        self._controller.annots.stop_annotating.assert_called_once_with()

    def test_setup_annotating(self):
        self._controller._setup_annotating()
        self._controller.layout.removeWidget.assert_called_once_with(
            self._controller.images.view
        )
        self._controller.images.view.hide.assert_called_once()
        self._controller.images.start_annotating.assert_called_once()
        self._controller.annots.start_annotating.assert_called_once_with(
            self._controller.images.get_num_files()
        )
        self._controller.annots.set_curr_img.assert_called_once_with(
            self._controller.images.curr_img_dict()
        )

    def test_next_image_save(self):
        self._controller.annots.view.next_btn.text = MagicMock(
            return_value="Finish"
        )
        self._controller.annots.write_to_csv = MagicMock()
        self._controller.annots.record_annotations = MagicMock()
        self._controller.images.curr_img_dict = MagicMock(
            return_value={"File Path": "path", "Row": "2"}
        )
        self._controller.annots.view.prev_btn.setEnabled = MagicMock()

        self._controller.next_image()

        self._controller.annots.view.next_btn.text.assert_called_once_with()
        self._controller.annots.write_to_csv.assert_called_once_with()
        self._controller.annots.record_annotations.assert_called_once_with(
            "path"
        )
        self._controller.annots.view.prev_btn.setEnabled.assert_not_called()

    def test_next_image(self):
        self._controller.annots.view.next_btn.text = MagicMock(
            return_value="Next"
        )
        self._controller.annots.write_to_csv = MagicMock()
        self._controller.annots.record_annotations = MagicMock()
        self._controller.images.curr_img_dict = MagicMock(
            return_value={"File Path": "path", "Row": "1"}
        )

        self._controller.images.next_img = MagicMock()
        self._controller.annots.set_curr_img = MagicMock()
        self._controller.annots.view.prev_btn.setEnabled = MagicMock()

        self._controller.next_image()

        self._controller.annots.view.next_btn.text.assert_called_once_with()
        self._controller.annots.write_to_csv.assert_not_called()
        self._controller.annots.record_annotations.assert_called_once_with(
            "path"
        )
        assert len(self._controller.images.curr_img_dict.mock_calls) == 3
        self._controller.images.next_img.assert_called_once_with()
        self._controller.annots.view.prev_btn.setEnabled.assert_called_once_with(
            True
        )
        self._controller.annots.set_curr_img.assert_called_once_with(
            {"File Path": "path", "Row": "1"}
        )

    def test_prev_image(self):
        self._controller.annots.record_annotations = MagicMock()
        self._controller.images.curr_img_dict = MagicMock(
            return_value={"File Path": "path", "Row": "1"}
        )
        self._controller.images.prev_img = MagicMock()
        self._controller.annots.set_curr_img = MagicMock()
        self._controller.annots.view.prev_btn.setEnabled = MagicMock()

        self._controller.prev_image()

        self._controller.annots.record_annotations.assert_called_once_with(
            "path"
        )

        assert len(self._controller.images.curr_img_dict.mock_calls) == 3
        self._controller.images.prev_img.assert_called_once_with()
        self._controller.annots.set_curr_img.assert_called_once_with(
            {"File Path": "path", "Row": "1"}
        )
        self._controller.annots.view.prev_btn.setEnabled.assert_not_called()

    def test_prev_image_zero(self):
        self._controller.annots.record_annotations = MagicMock()

        self._controller.images.curr_img_dict = MagicMock(
            return_value={"File Path": "path", "Row": "0"}
        )
        self._controller.images.prev_img = MagicMock()
        self._controller.annots.set_curr_img = MagicMock()
        self._controller.annots.view.prev_btn.setEnabled = MagicMock()

        self._controller.prev_image()

        self._controller.annots.record_annotations.assert_called_once_with(
            "path"
        )

        assert len(self._controller.images.curr_img_dict.mock_calls) == 3
        self._controller.images.prev_img.assert_called_once_with()
        self._controller.annots.set_curr_img.assert_called_once_with(
            {"File Path": "path", "Row": "0"}
        )
        self._controller.annots.view.prev_btn.setEnabled.assert_called_once_with(
            False
        )
