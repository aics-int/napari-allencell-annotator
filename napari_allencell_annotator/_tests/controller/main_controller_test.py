
from unittest import mock
from unittest.mock import MagicMock, create_autospec, mock_open, patch, Mock

from napari_allencell_annotator.controller.main_controller import (
    MainController,
    ImagesController,
    AnnotatorController,
    QVBoxLayout,
    os,
    CreateDialog,
    QDialog,
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

    def test_create_clicked_reject(self):
        with mock.patch.object(CreateDialog, "__init__", lambda x, y: None):
            with mock.patch.object(CreateDialog, "exec", lambda x: None):
                dlg = create_autospec(CreateDialog)
                dlg.exec = MagicMock(return_value=QDialog.Rejected)
                self._controller._create_clicked()
                self._controller.annots.set_annot_json_data.assert_not_called()

    def test_create_clicked_accept(self):
        with mock.patch.object(CreateDialog, "__init__", lambda x, y: None):
            with mock.patch.object(CreateDialog, "exec", lambda x: None):
                self._controller.already_annotated = {}
                CreateDialog.exec = MagicMock(return_value=QDialog.Accepted)
                CreateDialog.new_annot_dict = {}

                self._controller._create_clicked()
                self._controller.annots.start_viewing.assert_called_once_with()
                assert self._controller.already_annotated is None
                self._controller.annots.set_annot_json_data.assert_called_once_with(CreateDialog.new_annot_dict)

    def test_csv_import_selected_none(self):
        self._controller._csv_import_selected_evt(None)
        self._controller.images.view.alert.assert_called_once_with("No selection provided")

    def test_csv_import_selected_evt_empty(self):
        self._controller._csv_import_selected_evt([])
        self._controller.images.view.alert.assert_called_once_with("No selection provided")
        self._controller.annots.start_viewing.assert_not_called()

    def test_csv_imported_selected_evt_json(self):
        self._controller._csv_import_selected_evt(['path.json'])

        self._controller.annots.read_json.assert_called_once_with('path.json')
        self._controller.annots.start_viewing.assert_called_once_with()

    def test_csv_imported_selected_evt_csv_false(self):
        self._controller.str_to_bool = MagicMock(return_value=False)
        self._controller.starting_row = None
        self._controller.already_annotated = {}

        self._controller.annots.view.popup = MagicMock(return_value=False)
        self._controller._csv_import_selected_evt(['test.csv'])

        assert self._controller.already_annotated is None
        assert self._controller.starting_row == 0
        self._controller.annots.get_annotations_csv.assert_called_once_with('{"name": {}, "name2": {}, "name3": {}}')

        self._controller.annots.read_json.assert_not_called()
        self._controller.annots.start_viewing.assert_called_once_with()

    def test_csv_imported_selected_evt_csv_true(self):
        self._controller.str_to_bool = MagicMock(return_value=True)
        self._controller.starting_row = None
        self._controller.already_annotated = {}

        self._controller.annots.view.popup = MagicMock(return_value=True)
        self._controller._csv_import_selected_evt(['test2.csv'])

        assert self._controller.already_annotated == {'file.png': ['file', '', 'text', 'text', 'text'],
                                                      'file2.png': ['file2', '', 'text', 'text', 'text'],
                                                      'file3.png': ['file3', '', 'text', '', 'text'],
                                                      'file4.png': ['file4', '', 'text', 'text', 'text'],
                                                      'file5.png': ['file5', '', '', '', '']}
        assert self._controller.starting_row == 2
        self._controller.annots.get_annotations_csv.assert_called_once_with('{"name": {}, "name2": {}, "name3": {}}')

        self._controller.images.load_from_csv.assert_called_once_with(self._controller.already_annotated.keys(), True)
        self._controller.annots.read_json.assert_not_called()
        self._controller.annots.start_viewing.assert_called_once_with()

    def test_str_to_bool_true(self):
        assert self._controller.str_to_bool('True')
        assert self._controller.str_to_bool('TRUE')
        assert self._controller.str_to_bool('true')

    def test_str_to_bool_false(self):
        assert not self._controller.str_to_bool('False')
        assert not self._controller.str_to_bool('FALSE')
        assert not self._controller.str_to_bool('false')

    def test_import_annots_clicked(self):
        self._controller._import_annots_clicked()
        self._controller.annots.view.annot_input.simulate_click.assert_called_once_with()

    def test_csv_write_selected_evt_none(self):
        self._controller._csv_write_selected_evt(None)
        self._controller.images.view.alert.assert_called_once_with("No selection provided")

    def test_csv_write_selected_evt_empty(self):
        self._controller._csv_write_selected_evt([])
        self._controller.images.view.alert.assert_called_once_with("No selection provided")

    def test_csv_write_selected_evt_not_csv(self):
        os.path.splitext = MagicMock(return_value=("path", ""))
        self._controller._setup_annotating = MagicMock()
        self._controller._csv_write_selected_evt(["path"])
        self._controller.annots.set_csv_name.assert_called_once_with("path.csv")
        self._controller._setup_annotating.assert_called_once_with()
        self._controller.images.view.alert.assert_not_called()

    def test_csv_write_selected_evt_csv(self):
        os.path.splitext = MagicMock(return_value=("path", ".csv"))
        self._controller._setup_annotating = MagicMock()
        self._controller._csv_write_selected_evt(["path.csv"])
        self._controller.annots.set_csv_name.assert_called_once_with("path.csv")
        self._controller._setup_annotating.assert_called_once_with()
        self._controller.images.view.alert.assert_not_called()

    def test_start_annotating_clicked_none(self):
        self._controller.images.get_num_files = MagicMock(return_value=None)

        self._controller._start_annotating_clicked()
        self._controller.images.get_num_files.assert_called_once()
        self._controller.images.view.alert.assert_called_once_with("Can't Annotate Without Adding Images")

    def test_start_annotating_clicked_zero(self):
        self._controller.images.get_num_files = MagicMock(return_value=0)

        self._controller._start_annotating_clicked()
        assert len(self._controller.images.get_num_files.mock_calls) == 2
        self._controller.images.view.alert.assert_called_once_with("Can't Annotate Without Adding Images")

    def test_start_annotating_clicked_true(self):
        self._controller.images.get_num_files = MagicMock(return_value=1)

        self._controller.annots.view.popup.return_value = True
        self._controller._start_annotating_clicked()
        assert len(self._controller.images.get_num_files.mock_calls) == 2
        self._controller.images.view.alert.assert_not_called()
        self._controller.annots.view.file_input.simulate_click.assert_called_once_with()

    def test_start_annotating_clicked_false(self):
        self._controller.images.get_num_files.return_value = 1
        self._controller.annots.view.popup.return_value = False
        self._controller._start_annotating_clicked()
        assert len(self._controller.images.get_num_files.mock_calls) == 2
        self._controller.images.view.alert.assert_not_called()
        self._controller.annots.view.file_input.simulate_click.assert_not_called()

    def test_stop_annotating_shuffled(self):
        self._controller.images.view.file_widget.shuffled = True
        self._controller._stop_annotating()
        self._controller.images.view.file_widget.currentItemChanged.disconnect.assert_not_called()

        self._controller.layout.addWidget.assert_has_calls(
            [
                mock.call(self._controller.images.view, stretch=1),
                mock.call(self._controller.annots.view, stretch=2),
            ]
        )
        self._controller.images.view.show.assert_called_once_with()
        self._controller.images.stop_annotating.assert_called_once_with()
        self._controller.annots.stop_annotating.assert_called_once_with()

    def test_stop_annotating_not_shuffled(self):
        self._controller.images.view.file_widget.shuffled = False
        self._controller._stop_annotating()
        self._controller.images.view.file_widget.currentItemChanged.disconnect.assert_called_once()

        self._controller.layout.addWidget.assert_has_calls(
            [
                mock.call(self._controller.images.view, stretch=1),
                mock.call(self._controller.annots.view, stretch=2),
            ]
        )
        self._controller.images.view.show.assert_called_once_with()
        self._controller.images.stop_annotating.assert_called_once_with()
        self._controller.annots.stop_annotating.assert_called_once_with()

    def test_setup_annotating_already_annotated(self):
        self._controller.starting_row = 0
        self._controller.images.get_files_dict = MagicMock(return_value=({"filepath.png": ['filepath', '']}, True))
        self._controller.already_annotated = {"filepath.png": ['filepath', '', 'text']}
        self._controller._setup_annotating()
        self._controller.layout.removeWidget.assert_called_once_with(self._controller.images.view)
        self._controller.images.view.hide.assert_called_once()
        self._controller.images.start_annotating.assert_called_once_with(0)

        self._controller.annots.start_annotating.assert_called_once_with(
            self._controller.images.get_num_files(), self._controller.already_annotated,True)
        self._controller.annots.set_curr_img.assert_called_once_with(self._controller.images.curr_img_dict())
        self._controller.images.view.file_widget.currentItemChanged.connect.assert_not_called()

    def test_setup_annotating_not_already_annotated(self):
        self._controller.starting_row = None
        self._controller.images.get_files_dict = MagicMock(return_value=({"filepath.png": ['filepath', '']}, False))
        self._controller.already_annotated = None
        self._controller._setup_annotating()
        self._controller.layout.removeWidget.assert_called_once_with(self._controller.images.view)
        self._controller.images.view.hide.assert_called_once()
        self._controller.images.start_annotating.assert_called_once_with()

        self._controller.annots.start_annotating.assert_called_once_with(
            self._controller.images.get_num_files(), {"filepath.png": ['filepath', '']}, False)
        self._controller.annots.set_curr_img.assert_called_once_with(self._controller.images.curr_img_dict())
        self._controller.images.view.file_widget.currentItemChanged.connect.assert_called_once()

    def test_next_image_clicked_save(self):
        self._controller._next_image_clicked()
        self._controller.annots.record_annotations.assert_called_once_with(self._controller.images.curr_img_dict()["File Path"])
        self._controller.images.next_img.assert_called_once_with()
        self._controller.annots.set_curr_img.assert_called_once_with(self._controller.images.curr_img_dict())

    def test_prev_image_clicked(self):
        self._controller._prev_image_clicked()
        self._controller.annots.record_annotations.assert_called_once_with(
            self._controller.images.curr_img_dict()["File Path"])
        self._controller.images.prev_img.assert_called_once_with()
        self._controller.annots.set_curr_img.assert_called_once_with(self._controller.images.curr_img_dict())

    def test_save_and_exit_clicked_false(self):
        self._controller.annots.view.popup = MagicMock(return_value=False)
        self._controller._stop_annotating = MagicMock()
        self._controller._save_and_exit_clicked()
        self._controller._stop_annotating.assert_not_called()

    def test_save_and_exit_clicked_true(self):
        self._controller.annots.view.popup = MagicMock(return_value=True)
        self._controller._stop_annotating = MagicMock()
        self._controller._save_and_exit_clicked()
        self._controller._stop_annotating.assert_called_once_with()
