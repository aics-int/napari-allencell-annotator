from unittest import mock
from unittest.mock import MagicMock, create_autospec

from napari_allencell_annotator.controller.main_controller import (
    MainController,
    ImagesController,
    AnnotatorController,
    QVBoxLayout,
    CreateDialog,
    QDialog,
)
from napari_allencell_annotator.util.directories import Directories


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
                self._controller.csv_annotation_values = {}
                CreateDialog.exec = MagicMock(return_value=QDialog.Accepted)
                CreateDialog.new_annot_dict = {}

                self._controller._create_clicked()
                self._controller.annots.start_viewing.assert_called_once_with()
                assert self._controller.csv_annotation_values is None
                self._controller.annots.set_annot_json_data.assert_called_once_with(CreateDialog.new_annot_dict)

    def test_json_write_selected_evt_none(self):
        self._controller._json_write_selected_evt(None)
        self._controller.images.view.alert.assert_called_once_with("No selection provided")

    def test_json_write_selected_evt_empty(self):
        self._controller._json_write_selected_evt([])
        self._controller.images.view.alert.assert_called_once_with("No selection provided")

    def test_json_write_selected_evt_not_json(self):
        self._controller._setup_annotating = MagicMock()
        self._controller._json_write_selected_evt(["path"])
        self._controller.annots.view.save_json_btn.setEnabled.assert_called_once_with(False)
        self._controller.annots.write_json.assert_called_once_with("path.json")

    def test_json_write_selected_evt_json(self):
        self._controller._setup_annotating = MagicMock()
        self._controller._json_write_selected_evt(["path.json"])
        self._controller.annots.view.save_json_btn.setEnabled.assert_called_once_with(False)
        self._controller.annots.write_json.assert_called_once_with("path.json")

    def test_csv_json_import_selected_none(self):
        self._controller._csv_json_import_selected_evt(None)
        self._controller.images.view.alert.assert_called_once_with("No selection provided")

    def test_csv_json_import_selected_evt_empty(self):
        self._controller._csv_json_import_selected_evt([])
        self._controller.images.view.alert.assert_called_once_with("No selection provided")
        self._controller.annots.start_viewing.assert_not_called()

    def test_csv_json_imported_selected_evt_json(self):
        self._controller._csv_json_import_selected_evt(["path.json"])

        self._controller.annots.read_json.assert_called_once_with("path.json")
        self._controller.annots.start_viewing.assert_called_once_with()

    def test_csv_json_imported_selected_evt_csv_false(self):
        self._controller.str_to_bool = MagicMock(return_value=False)
        self._controller.starting_row = None
        self._controller.csv_annotation_values = {}

        self._controller.annots.view.popup = MagicMock(return_value=False)
        path: str = str(Directories.get_assets_dir() / "test.csv")
        self._controller._csv_json_import_selected_evt([path])

        assert self._controller.csv_annotation_values is None
        assert self._controller.starting_row == 0
        self._controller.annots.get_annotations_csv.assert_called_once_with('{"name": {}, "name2": {}, "name3": {}}')

        self._controller.annots.read_json.assert_not_called()
        self._controller.annots.start_viewing.assert_called_once_with()

    def test_csv_json_imported_selected_evt_csv_true(self):
        self._controller.str_to_bool = MagicMock(return_value=True)
        self._controller.starting_row = None
        self._controller.csv_annotation_values = {}

        self._controller.annots.view.popup = MagicMock(return_value=True)
        path: str = str(Directories.get_assets_dir() / "test2.csv")
        self._controller.has_none_annotation = MagicMock(side_effect=[False, False, True])
        self._controller._csv_json_import_selected_evt([path])

        assert self._controller.csv_annotation_values == {
            "file.png": ["file", "", "text", "text", "text"],
            "file2.png": ["file2", "", "text", "text", "text"],
            "file3.png": ["file3", "", "text", "", "text"],
            "file4.png": ["file4", "", "text", "text", "text"],
            "file5.png": ["file5", "", "", "", ""],
        }
        assert self._controller.starting_row == 2
        self._controller.annots.get_annotations_csv.assert_called_once_with('{"name": {}, "name2": {}, "name3": {}}')

        self._controller.images.load_from_csv.assert_called_once_with(
            self._controller.csv_annotation_values.keys(), True
        )
        self._controller.annots.read_json.assert_not_called()
        self._controller.annots.start_viewing.assert_called_once_with()

    def test_shuffle_toggled_true(self):
        self._controller.has_new_shuffled_order = False

        self._controller._shuffle_toggled(True)
        assert self._controller.has_new_shuffled_order
        self._controller.images.view.shuffle.toggled.disconnect.assert_called_once_with(
            self._controller._shuffle_toggled
        )

    def test_shuffle_toggled_false(self):
        self._controller.has_new_shuffled_order = False

        self._controller._shuffle_toggled(False)
        assert not self._controller.has_new_shuffled_order
        self._controller.images.view.shuffle.toggled.disconnect.assert_not_called()

    def test_str_to_bool_true(self):
        assert self._controller.str_to_bool("True")
        assert self._controller.str_to_bool("TRUE")
        assert self._controller.str_to_bool("true")

    def test_str_to_bool_false(self):
        assert not self._controller.str_to_bool("False")
        assert not self._controller.str_to_bool("FALSE")
        assert not self._controller.str_to_bool("false")

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
        self._controller._setup_annotating = MagicMock()
        self._controller._csv_write_selected_evt(["path"])
        self._controller.annots.set_csv_path.assert_called_once_with("path.csv")
        self._controller._setup_annotating.assert_called_once_with()
        self._controller.images.view.alert.assert_not_called()

    def test_csv_write_selected_evt_csv(self):
        self._controller._setup_annotating = MagicMock()
        self._controller._csv_write_selected_evt(["path.csv"])
        self._controller.annots.set_csv_path.assert_called_once_with("path.csv")
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
        self._controller.annots.view.csv_input.simulate_click.assert_called_once_with()

    def test_start_annotating_clicked_false(self):
        self._controller.images.get_num_files.return_value = 1
        self._controller.annots.view.popup.return_value = False
        self._controller._start_annotating_clicked()
        assert len(self._controller.images.get_num_files.mock_calls) == 2
        self._controller.images.view.alert.assert_not_called()
        self._controller.annots.view.csv_input.simulate_click.assert_not_called()

    def test_stop_annotating_shuffled(self):
        self._controller.images.view.file_widget.shuffled = True
        self._controller.has_new_shuffled_order = None
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

    def test_stop_annotating_shuffled_new_shuff_order_true(self):
        self._controller.images.view.file_widget.shuffled = True
        self._controller.has_new_shuffled_order = True
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

    def test_stop_annotating_shuffled_new_shuff_order_false(self):
        self._controller.images.view.file_widget.shuffled = True
        self._controller.has_new_shuffled_order = False
        self._controller.images.view.shuffle = MagicMock()
        self._controller._stop_annotating()
        self._controller.images.view.file_widget.currentItemChanged.disconnect.assert_not_called()
        self._controller.images.view.shuffle.toggled.disconnect.assert_called_once_with(
            self._controller._shuffle_toggled
        )
        assert self._controller.has_new_shuffled_order is None
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
        self._controller.has_new_shuffled_order = None
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

    def test_stop_annotating_not_shuffled_new_shuff_order_true(self):
        self._controller.has_new_shuffled_order = True
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

    def test_stop_annotating_not_shuffled_new_shuff_order_false(self):
        self._controller.has_new_shuffled_order = False
        self._controller.images.view.shuffle = MagicMock()
        self._controller.images.view.file_widget.shuffled = False
        self._controller._stop_annotating()
        self._controller.images.view.file_widget.currentItemChanged.disconnect.assert_called_once()
        self._controller.images.view.shuffle.toggled.disconnect.assert_called_once_with(
            self._controller._shuffle_toggled
        )
        assert self._controller.has_new_shuffled_order is None
        self._controller.layout.addWidget.assert_has_calls(
            [
                mock.call(self._controller.images.view, stretch=1),
                mock.call(self._controller.annots.view, stretch=2),
            ]
        )
        self._controller.images.view.show.assert_called_once_with()
        self._controller.images.stop_annotating.assert_called_once_with()
        self._controller.annots.stop_annotating.assert_called_once_with()

    def test_setup_annotating_csv_annotations(self):
        self._controller.images.get_files_dict = MagicMock(return_value=({"filepath.png": ["filepath", ""]}, True))
        self._controller.starting_row = 0
        self._controller.csv_annotation_values = {"filepath.png": ["filepath", "", "text"]}
        self._controller._fix_csv_annotations = MagicMock()

        self._controller._setup_annotating()

        self._controller.layout.removeWidget.assert_called_once_with(self._controller.images.view)
        self._controller.images.view.hide.assert_called_once()
        self._controller._fix_csv_annotations.assert_called_once_with({"filepath.png": ["filepath", ""]})
        self._controller.images.start_annotating.assert_called_once_with(0)
        self._controller.annots.start_annotating.assert_called_once_with(
            self._controller.images.get_num_files(), self._controller.csv_annotation_values, True
        )
        self._controller.annots.set_curr_img.assert_called_once_with(self._controller.images.curr_img_dict())
        self._controller.images.view.file_widget.currentItemChanged.connect.assert_not_called()
        self._controller.images.view.input_dir.hide.assert_not_called()
        self._controller.images.view.input_file.hide.assert_not_called()

    def test_setup_annotating_not_csv_annotations(self):
        self._controller.starting_row = None
        self._controller.images.get_files_dict = MagicMock(return_value=({"filepath.png": ["filepath", ""]}, False))
        self._controller.csv_annotation_values = None

        self._controller._setup_annotating()
        self._controller.layout.removeWidget.assert_not_called()
        self._controller.images.view.hide.assert_not_called()
        self._controller.images.start_annotating.assert_called_once_with()

        self._controller.annots.start_annotating.assert_called_once_with(
            self._controller.images.get_num_files(), {"filepath.png": ["filepath", ""]}, False
        )
        self._controller.annots.set_curr_img.assert_called_once_with(self._controller.images.curr_img_dict())
        self._controller.images.view.file_widget.currentItemChanged.connect.assert_called_once()
        self._controller.images.view.input_dir.hide.assert_called_once_with()
        self._controller.images.view.input_file.hide.assert_called_once_with()

    def test_fix_csv_annotations_keys_equal_shuffled(self):
        dct = {
            "name2.png": ["name2", ""],
            "name5.png": ["name5", ""],
            "name3.png": ["name3", ""],
            "name1.png": ["name1", ""],
            "name4.png": ["name4", ""],
        }
        self._controller.csv_annotation_values = {
            "name1.png": ["name1", "", True, "hello"],
            "name2.png": ["name2", "", "", "hello"],
            "name3.png": ["name3", "", False, ""],
            "name4.png": ["name4", "", True, "hello"],
            "name5.png": ["name5", "", "", ""],
        }
        self._controller.has_new_shuffled_order = True
        self._controller._equal_shuffled_fix_csv_annotations = MagicMock()

        self._controller._fix_csv_annotations(dct)
        self._controller._equal_shuffled_fix_csv_annotations.assert_called_once_with(dct)

    def test_fix_csv_annotations_keys_equal_not_shuffled(self):
        dct = {
            "name1.png": ["name1", ""],
            "name2.png": ["name2", ""],
            "name3.png": ["name3", ""],
            "name4.png": ["name4", ""],
            "name5.png": ["name5", ""],
        }
        self._controller._equal_shuffled_fix_csv_annotations = MagicMock()
        self._controller.csv_annotation_values = {
            "name1.png": ["name1", "", True, "hello"],
            "name2.png": ["name2", "", "", "hello"],
            "name3.png": ["name3", "", False, ""],
            "name4.png": ["name4", "", True, "hello"],
            "name5.png": ["name5", "", "", ""],
        }
        self._controller.has_new_shuffled_order = False

        self._controller._fix_csv_annotations(dct)
        self._controller._equal_shuffled_fix_csv_annotations.assert_not_called()

    def test_fix_csv_annotations_keys_not_equal_shuffled(self):
        dct = {
            "name2.png": ["name2", ""],
            "name3.png": ["name3", ""],
            "name1.png": ["name1", ""],
            "name4.png": ["name4", ""],
            "name6.png": ["name6", ""],
        }
        self._controller.csv_annotation_values = {
            "name1.png": ["name1", "", True, "hello"],
            "name2.png": ["name2", "", "", "hello"],
            "name3.png": ["name3", "", False, ""],
            "name4.png": ["name4", "", True, "hello"],
            "name5.png": ["name5", "", "", ""],
        }
        self._controller._equal_shuffled_fix_csv_annotations = MagicMock()
        self._controller._unequal_shuffled_fix_csv_annotations = MagicMock()
        self._controller.has_new_shuffled_order = True

        self._controller._fix_csv_annotations(dct)
        self._controller._equal_shuffled_fix_csv_annotations.assert_not_called()
        self._controller._unequal_shuffled_fix_csv_annotations.assert_called_once_with(dct)

    def test_fix_csv_annotations_keys_not_equal_not_shuffled(self):
        dct = {
            "name2.png": ["name2", ""],
            "name5.png": ["name5", ""],
            "name6.png": ["name6", ""],
            "name7.png": ["name7", ""],
        }
        self._controller.csv_annotation_values = {
            "name1.png": ["name1", "", True, "hello"],
            "name2.png": ["name2", "", "", "hello"],
            "name3.png": ["name3", "", False, ""],
            "name4.png": ["name4", "", True, "hello"],
            "name5.png": ["name5", "", "", ""],
        }
        self._controller.has_new_shuffled_order = False
        self._controller._equal_shuffled_fix_csv_annotations = MagicMock()
        self._controller._unequal_shuffled_fix_csv_annotations = MagicMock()
        self._controller._unequal_unshuffled_fix_csv_annotations = MagicMock()

        self._controller._fix_csv_annotations(dct)
        self._controller._equal_shuffled_fix_csv_annotations.assert_not_called()
        self._controller._unequal_shuffled_fix_csv_annotations.assert_not_called()
        self._controller._unequal_unshuffled_fix_csv_annotations.assert_called_once_with(dct)

    def test_unequal_unshuffled_fix_csv_annotations_deletions_additions_same_start_row(self):
        dct = {
            "name2.png": ["name2", ""],
            "name5.png": ["name5", ""],
            "name6.png": ["name6", ""],
            "name7.png": ["name7", ""],
        }
        self._controller.csv_annotation_values = {
            "name1.png": ["name1", "", True, "hello"],
            "name2.png": ["name2", "", "", "hello"],
            "name3.png": ["name3", "", False, ""],
            "name4.png": ["name4", "", True, "hello"],
            "name5.png": ["name5", "", "", ""],
        }
        self._controller.starting_row = 1
        self._controller.has_none_annotation = MagicMock(return_value=True)  # set side effect
        self._controller._unequal_unshuffled_fix_csv_annotations(dct)

        assert self._controller.csv_annotation_values == {
            "name2.png": ["name2", "", "", "hello"],
            "name5.png": ["name5", "", "", ""],
            "name6.png": ["name6", ""],
            "name7.png": ["name7", ""],
        }
        assert self._controller.starting_row == 0
        self._controller.has_none_annotation.assert_called_once_with(["", "hello"])

    def test_unequal_unshuffled_fix_csv_annotations_deletions_additions_diff_start_row(self):
        dct = {
            "name1.png": ["name1", ""],
            "name5.png": ["name5", ""],
            "name6.png": ["name6", ""],
            "name7.png": ["name7", ""],
        }
        self._controller.csv_annotation_values = {
            "name1.png": ["name1", "", True, "hello"],
            "name2.png": ["name2", "", "", "hello"],
            "name3.png": ["name3", "", False, ""],
            "name4.png": ["name4", "", True, "hello"],
            "name5.png": ["name5", "", "", ""],
        }
        self._controller.starting_row = 1
        self._controller.has_none_annotation = MagicMock(return_value=True)  # set side effect
        self._controller._unequal_unshuffled_fix_csv_annotations(dct)

        assert self._controller.csv_annotation_values == {
            "name1.png": ["name1", "", True, "hello"],
            "name5.png": ["name5", "", "", ""],
            "name6.png": ["name6", ""],
            "name7.png": ["name7", ""],
        }
        assert self._controller.starting_row == 1
        self._controller.has_none_annotation.assert_called_once_with(["", ""])

    def test_unequal_unshuffled_fix_csv_annotations_deletions_end_start_row(self):
        dct = {"name1.png": ["name1", ""], "name3.png": ["name3", ""], "name4.png": ["name4", ""]}
        self._controller.csv_annotation_values = {
            "name1.png": ["name1", "", True, "hello"],
            "name2.png": ["name2", "", "", "hello"],
            "name3.png": ["name3", "", False, "hello"],
            "name4.png": ["name4", "", True, "hello"],
            "name5.png": ["name5", "", "", ""],
        }
        self._controller.starting_row = 1
        self._controller.has_none_annotation = MagicMock(side_effect=[False, False])  # set side effect
        self._controller._unequal_unshuffled_fix_csv_annotations(dct)

        assert self._controller.csv_annotation_values == {
            "name1.png": ["name1", "", True, "hello"],
            "name3.png": ["name3", "", False, "hello"],
            "name4.png": ["name4", "", True, "hello"],
        }
        assert self._controller.starting_row == 2
        self._controller.has_none_annotation.assert_has_calls(
            [mock.call([False, "hello"]), mock.call([True, "hello"])], any_order=True
        )

    def test_unequal_unshuffled_fix_csv_annotations_additions_end_start_row(self):
        dct = {
            "name1.png": ["name1", ""],
            "name2.png": ["name2", ""],
            "name3.png": ["name3", ""],
            "name4.png": ["name4", ""],
            "name5.png": ["name5", ""],
            "name6.png": ["name6", ""],
            "name7.png": ["name7", ""],
        }
        self._controller.csv_annotation_values = {
            "name1.png": ["name1", "", True, "hello"],
            "name2.png": ["name2", "", True, "hello"],
            "name3.png": ["name3", "", False, "hello"],
            "name4.png": ["name4", "", True, "hello"],
            "name5.png": ["name5", "", False, "hello"],
        }
        self._controller.starting_row = 4
        self._controller.has_none_annotation = MagicMock(return_value=False)  # set side effect
        self._controller._unequal_unshuffled_fix_csv_annotations(dct)

        assert self._controller.csv_annotation_values == {
            "name1.png": ["name1", "", True, "hello"],
            "name2.png": ["name2", "", True, "hello"],
            "name3.png": ["name3", "", False, "hello"],
            "name4.png": ["name4", "", True, "hello"],
            "name5.png": ["name5", "", False, "hello"],
            "name6.png": ["name6", ""],
            "name7.png": ["name7", ""],
        }
        assert self._controller.starting_row == 5
        self._controller.has_none_annotation.assert_called_once_with([False, "hello"])

    def test_unequal_shuffled_fix_csv_annotations_additions_middle_start_row(self):
        dct = {
            "name3.png": ["name3", ""],
            "name1.png": ["name1", ""],
            "name2.png": ["name2", ""],
            "name7.png": ["name7", ""],
            "name4.png": ["name4", ""],
            "name6.png": ["name6", ""],
            "name5.png": ["name5", ""],
        }
        self._controller.csv_annotation_values = {
            "name1.png": ["name1", "", True, "hello"],
            "name2.png": ["name2", "", True, "hello"],
            "name3.png": ["name3", "", False, "hello"],
            "name4.png": ["name4", "", True, "hello"],
            "name5.png": ["name5", "", False, "hello"],
        }
        self._controller.starting_row = 4
        self._controller.has_none_annotation = MagicMock(side_effect=[False, False, False])  # set side effect
        self._controller._unequal_shuffled_fix_csv_annotations(dct)

        assert self._controller.csv_annotation_values == {
            "name3.png": ["name3", "", False, "hello"],
            "name1.png": ["name1", "", True, "hello"],
            "name2.png": ["name2", "", True, "hello"],
            "name7.png": ["name7", ""],
            "name4.png": ["name4", "", True, "hello"],
            "name6.png": ["name6", ""],
            "name5.png": ["name5", "", False, "hello"],
        }

        assert self._controller.starting_row == 3
        self._controller.has_none_annotation.assert_has_calls(
            [mock.call([False, "hello"]), mock.call([True, "hello"]), mock.call([True, "hello"])], any_order=True
        )

    def test_unequal_shuffled_fix_csv_annotations_additions_zero_start_row(self):
        dct = {
            "name6.png": ["name6", ""],
            "name5.png": ["name5", ""],
            "name3.png": ["name3", ""],
            "name1.png": ["name1", ""],
            "name2.png": ["name2", ""],
            "name7.png": ["name7", ""],
            "name4.png": ["name4", ""],
        }
        self._controller.csv_annotation_values = {
            "name1.png": ["name1", "", True, "hello"],
            "name2.png": ["name2", "", True, "hello"],
            "name3.png": ["name3", "", False, "hello"],
            "name4.png": ["name4", "", True, "hello"],
            "name5.png": ["name5", "", False, "hello"],
        }
        self._controller.starting_row = 4
        self._controller.has_none_annotation = MagicMock()
        self._controller._unequal_shuffled_fix_csv_annotations(dct)

        assert self._controller.csv_annotation_values == {
            "name6.png": ["name6", ""],
            "name5.png": ["name5", "", False, "hello"],
            "name3.png": ["name3", "", False, "hello"],
            "name1.png": ["name1", "", True, "hello"],
            "name2.png": ["name2", "", True, "hello"],
            "name7.png": ["name7", ""],
            "name4.png": ["name4", "", True, "hello"],
        }

        assert self._controller.starting_row == 0
        self._controller.has_none_annotation.assert_not_called()

    def test_unequal_shuffled_fix_csv_annotations_deletions_last_start_row(self):
        dct = {
            "name3.png": ["name3", ""],
            "name1.png": ["name1", ""],
            "name4.png": ["name4", ""],
            "name2.png": ["name2", ""],
        }
        self._controller.csv_annotation_values = {
            "name1.png": ["name1", "", True, "hello"],
            "name2.png": ["name2", "", True, "hello"],
            "name3.png": ["name3", "", False, "hello"],
            "name4.png": ["name4", "", True, "hello"],
            "name5.png": ["name5", "", False, "hello"],
        }
        self._controller.starting_row = 4
        self._controller.has_none_annotation = MagicMock(side_effect=[False, False, False, False])
        self._controller._unequal_shuffled_fix_csv_annotations(dct)

        assert self._controller.csv_annotation_values == {
            "name3.png": ["name3", "", False, "hello"],
            "name1.png": ["name1", "", True, "hello"],
            "name4.png": ["name4", "", True, "hello"],
            "name2.png": ["name2", "", True, "hello"],
        }

        assert self._controller.starting_row == 3
        self._controller.has_none_annotation.assert_called()

    def test_unequal_shuffled_fix_csv_annotations_additions_delete_all_zero_start_row(self):
        dct = {"name7.png": ["name7", ""], "name6.png": ["name6", ""], "name8.png": ["name8", ""]}
        self._controller.csv_annotation_values = {
            "name1.png": ["name1", "", True, "hello"],
            "name2.png": ["name2", "", True, "hello"],
            "name3.png": ["name3", "", False, "hello"],
            "name4.png": ["name4", "", True, "hello"],
            "name5.png": ["name5", "", False, "hello"],
        }
        self._controller.starting_row = 4
        self._controller.has_none_annotation = MagicMock()
        self._controller._unequal_shuffled_fix_csv_annotations(dct)

        assert self._controller.csv_annotation_values == {
            "name7.png": ["name7", ""],
            "name6.png": ["name6", ""],
            "name8.png": ["name8", ""],
        }

        assert self._controller.starting_row == 0
        self._controller.has_none_annotation.assert_not_called()

    def test_unequal_shuffled_fix_csv_annotations_additions_deletions_end_start_row(self):
        dct = {
            "name3.png": ["name3", ""],
            "name1.png": ["name1", ""],
            "name2.png": ["name2", ""],
            "name7.png": ["name7", ""],
            "name6.png": ["name6", ""],
        }
        self._controller.csv_annotation_values = {
            "name1.png": ["name1", "", True, "hello"],
            "name2.png": ["name2", "", True, "hello"],
            "name3.png": ["name3", "", False, "hello"],
            "name4.png": ["name4", "", True, "hello"],
            "name5.png": ["name5", "", False, "hello"],
        }
        self._controller.starting_row = 4
        self._controller.has_none_annotation = MagicMock(side_effect=[False, False, False])  # set side effect
        self._controller._unequal_shuffled_fix_csv_annotations(dct)

        assert self._controller.csv_annotation_values == {
            "name3.png": ["name3", "", False, "hello"],
            "name1.png": ["name1", "", True, "hello"],
            "name2.png": ["name2", "", True, "hello"],
            "name7.png": ["name7", ""],
            "name6.png": ["name6", ""],
        }

        assert self._controller.starting_row == 3
        self._controller.has_none_annotation.assert_has_calls(
            [mock.call([False, "hello"]), mock.call([True, "hello"]), mock.call([True, "hello"])], any_order=True
        )

    def test_equal_shuffled_fix_csv_annotations_additions_middle_start_row(self):
        dct = {
            "name5.png": ["name5", ""],
            "name3.png": ["name3", ""],
            "name1.png": ["name1", ""],
            "name2.png": ["name2", ""],
            "name4.png": ["name4", ""],
            "name6.png": ["name6", ""],
        }
        self._controller.csv_annotation_values = {
            "name1.png": ["name1", "", True, "hello"],
            "name2.png": ["name2", "", True, "hello"],
            "name3.png": ["name3", "", "", "hello"],
            "name4.png": ["name4", "", True, "hello"],
            "name5.png": ["name5", "", False, "hello"],
            "name6.png": ["name6", "", "", ""],
        }
        self._controller.starting_row = 2
        self._controller.has_none_annotation = MagicMock(side_effect=[False, True])  # set side effect
        self._controller._equal_shuffled_fix_csv_annotations(dct)

        assert self._controller.csv_annotation_values == {
            "name5.png": ["name5", "", False, "hello"],
            "name3.png": ["name3", "", "", "hello"],
            "name1.png": ["name1", "", True, "hello"],
            "name2.png": ["name2", "", True, "hello"],
            "name4.png": ["name4", "", True, "hello"],
            "name6.png": ["name6", "", "", ""],
        }

        assert self._controller.starting_row == 1
        self._controller.has_none_annotation.assert_has_calls(
            [mock.call([False, "hello"]), mock.call(["", "hello"])], any_order=True
        )

    def test_equal_shuffled_fix_csv_annotations_additions_zero_start_row(self):
        dct = {
            "name6.png": ["name6", ""],
            "name3.png": ["name3", ""],
            "name1.png": ["name1", ""],
            "name2.png": ["name2", ""],
            "name4.png": ["name4", ""],
            "name5.png": ["name5", ""],
        }
        self._controller.csv_annotation_values = {
            "name1.png": ["name1", "", True, "hello"],
            "name2.png": ["name2", "", True, "hello"],
            "name3.png": ["name3", "", "", "hello"],
            "name4.png": ["name4", "", True, "hello"],
            "name5.png": ["name5", "", False, "hello"],
            "name6.png": ["name6", "", "", ""],
        }
        self._controller.starting_row = 2
        self._controller.has_none_annotation = MagicMock(return_value=True)  # set side effect
        self._controller._equal_shuffled_fix_csv_annotations(dct)

        assert self._controller.csv_annotation_values == {
            "name5.png": ["name5", "", False, "hello"],
            "name3.png": ["name3", "", "", "hello"],
            "name1.png": ["name1", "", True, "hello"],
            "name2.png": ["name2", "", True, "hello"],
            "name4.png": ["name4", "", True, "hello"],
            "name6.png": ["name6", "", "", ""],
        }

        assert self._controller.starting_row == 0
        self._controller.has_none_annotation.assert_called_once_with(["", ""])

    def test_next_image_clicked_save(self):
        self._controller._next_image_clicked()
        self._controller.annots.record_annotations.assert_called_once_with(
            self._controller.images.curr_img_dict()["File Path"]
        )
        self._controller.images.next_img.assert_called_once_with()
        self._controller.annots.set_curr_img.assert_called_once_with(self._controller.images.curr_img_dict())

    def test_prev_image_clicked(self):
        self._controller._prev_image_clicked()
        self._controller.annots.record_annotations.assert_called_once_with(
            self._controller.images.curr_img_dict()["File Path"]
        )
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

    def test_has_none_annotation_false(self):
        self._controller.annots.annot_json_data = {"key1": {}, "key2": {}, "key3": {}, "key4:": {}}
        assert not self._controller.has_none_annotation([True, 5, "h", " "])

    def test_has_none_annotation_len_too_small(self):
        self._controller.annots.annot_json_data = {"key1": {}, "key2": {}, "key3": {}, "key4:": {}}
        assert self._controller.has_none_annotation([True, 5, "h"])

    def test_has_none_annotation_none(self):
        self._controller.annots.annot_json_data = {"key1": {}, "key2": {}, "key3": {}, "key4:": {}}
        assert self._controller.has_none_annotation([True, None, "h", " "])

    def test_has_none_annotation_empty_string(self):
        self._controller.annots.annot_json_data = {"key1": {}, "key2": {}, "key3": {}, "key4:": {}}
        assert self._controller.has_none_annotation([True, 5, "h", ""])
