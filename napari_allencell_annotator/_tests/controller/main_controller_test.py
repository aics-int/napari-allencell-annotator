from unittest import mock
import pytest
from unittest.mock import MagicMock, create_autospec, patch

from napari_allencell_annotator.view.main_view import (
    MainController,
    ImagesController,
    AnnotatorController,
    QVBoxLayout,
    CreateDialog,
    QDialog,
    Popup,
    QShortcut,
    TemplateItem,
    ItemType,
)
from napari_allencell_annotator.widgets.template_list import QCheckBox
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

    def test_connect_slots(self):
        self._controller.annots.view.start_btn = MagicMock()
        self._controller.annots.view.start_btn.clicked = MagicMock()
        self._controller.annots.view.start_btn.clicked.connect = MagicMock()
        self._controller._start_annotating_clicked = MagicMock()

        self._controller.annots.view.next_btn = MagicMock()
        self._controller.annots.view.next_btn.clicked = MagicMock()
        self._controller.annots.view.next_btn.clicked.connect = MagicMock()
        self._controller._next_image_clicked = MagicMock()

        self._controller.annots.view.prev_btn = MagicMock()
        self._controller.annots.view.prev_btn.clicked = MagicMock()
        self._controller.annots.view.prev_btn.clicked.connect = MagicMock()
        self._controller._prev_image_clicked = MagicMock()

        self._controller.annots.view.csv_input = MagicMock()
        self._controller.annots.view.csv_input.file_selected = MagicMock()
        self._controller.annots.view.csv_input.file_selected.connect = MagicMock()
        self._controller._csv_write_selected_evt = MagicMock()

        self._controller.annots.view.exit_btn = MagicMock()
        self._controller.annots.view.exit_btn.clicked = MagicMock()
        self._controller.annots.view.exit_btn.clicked.connect = MagicMock()
        self._controller._exit_clicked = MagicMock()

        self._controller.annots.view.save_btn = MagicMock()
        self._controller.annots.view.save_btn.clicked = MagicMock()
        self._controller.annots.view.save_btn.clicked.connect = MagicMock()
        self._controller._save = MagicMock()

        self._controller.annots.view.import_btn = MagicMock()
        self._controller.annots.view.import_btn.clicked = MagicMock()
        self._controller.annots.view.import_btn.clicked.connect = MagicMock()
        self._controller._import_annots_clicked = MagicMock()

        self._controller.annots.view.annot_input = MagicMock()
        self._controller.annots.view.annot_input.file_selected = MagicMock()
        self._controller.annots.view.annot_input.file_selected.connect = MagicMock()
        self._controller._csv_json_import_selected_evt = MagicMock()

        self._controller.annots.view.create_btn = MagicMock()
        self._controller.annots.view.create_btn.clicked = MagicMock()
        self._controller.annots.view.create_btn.clicked.connect = MagicMock()
        self._controller._create_clicked = MagicMock()

        self._controller.annots.view.save_json_btn = MagicMock()
        self._controller.annots.view.save_json_btn.file_selected = MagicMock()
        self._controller.annots.view.save_json_btn.file_selected.connect = MagicMock()
        self._controller._json_write_selected_evt = MagicMock()

        self._controller.annots.view.edit_btn = MagicMock()
        self._controller.annots.view.edit_btn.clicked = MagicMock()
        self._controller.annots.view.edit_btn.clicked.connect = MagicMock()
        self._controller._create_clicked = MagicMock()

        self._controller._connect_slots()

        self._controller.annots.view.start_btn.clicked.connect.assert_called_once_with(
            self._controller._start_annotating_clicked
        )
        self._controller.annots.view.next_btn.clicked.connect.assert_called_once_with(
            self._controller._next_image_clicked
        )
        self._controller.annots.view.prev_btn.clicked.connect.assert_called_once_with(
            self._controller._prev_image_clicked
        )
        self._controller.annots.view.csv_input.file_selected.connect.assert_called_once_with(
            self._controller._csv_write_selected_evt
        )
        self._controller.annots.view.save_btn.clicked.connect.assert_called_once_with(self._controller._save)
        self._controller.annots.view.exit_btn.clicked.connect.assert_called_once_with(self._controller._exit_clicked)
        self._controller.annots.view.import_btn.clicked.connect.assert_called_once_with(
            self._controller._import_annots_clicked
        )
        self._controller.annots.view.annot_input.file_selected.connect.assert_called_once_with(
            self._controller._csv_json_import_selected_evt
        )
        self._controller.annots.view.create_btn.clicked.connect.assert_called_once_with(
            self._controller._create_clicked
        )
        self._controller.annots.view.save_json_btn.file_selected.connect.assert_called_once_with(
            self._controller._json_write_selected_evt
        )
        self._controller.annots.view.edit_btn.clicked.connect.assert_called_once_with(self._controller._create_clicked)

    @patch("napari_allencell_annotator.controller.main_controller.CreateDialog.__init__")
    def test_create_clicked_reject(self, mock_init):
        mock_init.return_value = None
        self._controller.annots.get_annot_json_data = MagicMock(return_value=None)
        with mock.patch.object(CreateDialog, "exec", lambda x: None):
            dlg = create_autospec(CreateDialog)
            dlg.exec = MagicMock(return_value=QDialog.Rejected)
            self._controller._create_clicked()
            mock_init.assert_called_once_with(self._controller, None)
            self._controller.annots.set_annot_json_data.assert_not_called()

    @patch("napari_allencell_annotator.controller.main_controller.CreateDialog.__init__")
    def test_create_clicked_accept(self, mock_init):
        mock_init.return_value = None
        self._controller.annots.get_annot_json_data = MagicMock(return_value={})
        with mock.patch.object(CreateDialog, "exec", lambda x: None):
            self._controller.csv_annotation_values = {}
            CreateDialog.exec = MagicMock(return_value=QDialog.Accepted)
            CreateDialog.new_annot_dict = {}

            self._controller._create_clicked()
            self._controller.annots.start_viewing.assert_called_once_with()
            mock_init.assert_called_once_with(self._controller, {})
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
        self._controller.annots.start_viewing.assert_called_once_with(False)

    def test_csv_json_imported_selected_evt_csv_false(self):
        self._controller.str_to_bool = MagicMock(return_value=False)
        self._controller.starting_row = None
        self._controller.csv_annotation_values = {}

        Popup.make_popup = MagicMock(return_value=False)
        path: str = str(Directories.get_test_assets_dir() / "test.csv")
        self._controller._csv_json_import_selected_evt([path])

        assert self._controller.csv_annotation_values is None
        assert self._controller.starting_row == 0
        self._controller.annots.get_annotations_csv.assert_called_once_with('{"name": {}, "name2": {}, "name3": {}}')

        self._controller.annots.read_json.assert_not_called()
        self._controller.annots.start_viewing.assert_called_once_with(False)

    def test_csv_json_imported_selected_evt_csv_true(self):
        self._controller.str_to_bool = MagicMock(return_value=True)
        self._controller.starting_row = None
        self._controller.csv_annotation_values = {}

        Popup.make_popup = MagicMock(return_value=True)
        path: str = str(Directories.get_test_assets_dir() / "test2.csv")
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
        self._controller.annots.start_viewing.assert_called_once_with(True)

    def test_csv_json_imported_selected_evt_csv_true_last_row(self):
        self._controller.str_to_bool = MagicMock(return_value=True)
        self._controller.starting_row = None
        self._controller.csv_annotation_values = {}

        Popup.make_popup = MagicMock(return_value=True)
        path: str = str(Directories.get_test_assets_dir() / "test3.csv")
        self._controller.has_none_annotation = MagicMock(side_effect=[False, False, False, False])
        self._controller._csv_json_import_selected_evt([path])

        assert self._controller.csv_annotation_values == {
            "file.png": ["file", "", "text", "text", "text"],
            "file2.png": ["file2", "", "text", "text", "text"],
            "file3.png": ["file3", "", "text", "text", "text"],
            "file4.png": ["file4", "", "text", "text", "text"],
        }
        assert self._controller.starting_row == 3
        self._controller.annots.get_annotations_csv.assert_called_once_with('{"name": {}, "name2": {}, "name3": {}}')

        self._controller.images.load_from_csv.assert_called_once_with(
            self._controller.csv_annotation_values.keys(), True
        )
        self._controller.annots.read_json.assert_not_called()
        self._controller.annots.start_viewing.assert_called_once_with(True)

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

    def test_str_to_bool_error(self):
        with pytest.raises(ValueError, match="The value 'hello' cannot be mapped to boolean."):
            self._controller.str_to_bool("hello")

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
        self._controller.images.get_num_images = MagicMock(return_value=None)

        self._controller._start_annotating_clicked()
        self._controller.images.get_num_images.assert_called_once()
        self._controller.images.view.alert.assert_called_once_with("Can't Annotate Without Adding Images")

    def test_start_annotating_clicked_zero(self):
        self._controller.images.get_num_images = MagicMock(return_value=0)

        self._controller._start_annotating_clicked()
        assert len(self._controller.images.get_num_images.mock_calls) == 2
        self._controller.images.view.alert.assert_called_once_with("Can't Annotate Without Adding Images")

    def test_start_annotating_clicked_true(self):
        self._controller.images.get_num_images = MagicMock(return_value=1)

        Popup.make_popup.return_value = True
        self._controller._start_annotating_clicked()
        assert len(self._controller.images.get_num_images.mock_calls) == 2
        self._controller.images.view.alert.assert_not_called()
        self._controller.annots.view.csv_input.simulate_click.assert_called_once_with()

    def test_start_annotating_clicked_false(self):
        self._controller.images.get_num_images.return_value = 1
        Popup.make_popup.return_value = False
        self._controller._start_annotating_clicked()
        assert len(self._controller.images.get_num_images.mock_calls) == 2
        self._controller.images.view.alert.assert_not_called()
        self._controller.annots.view.csv_input.simulate_click.assert_not_called()

    def test_stop_annotating_shuffled(self):
        self._controller.images.view.file_widget.shuffled = True
        self._controller.has_new_shuffled_order = None
        self._controller.annotating_shortcuts_off = MagicMock()
        self._controller._stop_annotating()
        self._controller.annotating_shortcuts_off.assert_called_once_with()

        self._controller.images.view.file_widget.currentItemChanged.disconnect.assert_not_called()

        self._controller.layout.addWidget.assert_has_calls(
            [
                mock.call(self._controller.images.view, stretch=1),
                mock.call(self._controller.annots.view, stretch=1),
            ]
        )
        self._controller.images.view.show.assert_called_once_with()
        self._controller.images.stop_annotating.assert_called_once_with()
        self._controller.annots.stop_annotating.assert_called_once_with()

    def test_stop_annotating_shuffled_new_shuff_order_true(self):
        self._controller.images.view.file_widget.shuffled = True
        self._controller.has_new_shuffled_order = True
        self._controller.annotating_shortcuts_off = MagicMock()
        self._controller._stop_annotating()
        self._controller.annotating_shortcuts_off.assert_called_once_with()

        self._controller.images.view.file_widget.currentItemChanged.disconnect.assert_not_called()

        self._controller.layout.addWidget.assert_has_calls(
            [
                mock.call(self._controller.images.view, stretch=1),
                mock.call(self._controller.annots.view, stretch=1),
            ]
        )
        self._controller.images.view.show.assert_called_once_with()
        self._controller.images.stop_annotating.assert_called_once_with()
        self._controller.annots.stop_annotating.assert_called_once_with()

    def test_stop_annotating_shuffled_new_shuff_order_false(self):
        self._controller.images.view.file_widget.shuffled = True
        self._controller.has_new_shuffled_order = False
        self._controller.images.view.shuffle = MagicMock()
        self._controller.annotating_shortcuts_off = MagicMock()
        self._controller._stop_annotating()
        self._controller.annotating_shortcuts_off.assert_called_once_with()

        self._controller.images.view.file_widget.currentItemChanged.disconnect.assert_not_called()
        self._controller.images.view.shuffle.toggled.disconnect.assert_called_once_with(
            self._controller._shuffle_toggled
        )
        assert self._controller.has_new_shuffled_order is None
        self._controller.layout.addWidget.assert_has_calls(
            [
                mock.call(self._controller.images.view, stretch=1),
                mock.call(self._controller.annots.view, stretch=1),
            ]
        )
        self._controller.images.view.show.assert_called_once_with()
        self._controller.images.stop_annotating.assert_called_once_with()
        self._controller.annots.stop_annotating.assert_called_once_with()

    def test_stop_annotating_not_shuffled(self):
        self._controller.has_new_shuffled_order = None
        self._controller.images.view.file_widget.shuffled = False
        self._controller.annotating_shortcuts_off = MagicMock()
        self._controller._stop_annotating()
        self._controller.annotating_shortcuts_off.assert_called_once_with()

        self._controller.images.view.file_widget.currentItemChanged.disconnect.assert_called_once()

        self._controller.layout.addWidget.assert_has_calls(
            [
                mock.call(self._controller.images.view, stretch=1),
                mock.call(self._controller.annots.view, stretch=1),
            ]
        )
        self._controller.images.view.show.assert_called_once_with()
        self._controller.images.stop_annotating.assert_called_once_with()
        self._controller.annots.stop_annotating.assert_called_once_with()

    def test_stop_annotating_not_shuffled_new_shuff_order_true(self):
        self._controller.has_new_shuffled_order = True
        self._controller.images.view.file_widget.shuffled = False
        self._controller.annotating_shortcuts_off = MagicMock()
        self._controller._stop_annotating()
        self._controller.annotating_shortcuts_off.assert_called_once_with()

        self._controller.images.view.file_widget.currentItemChanged.disconnect.assert_called_once()

        self._controller.layout.addWidget.assert_has_calls(
            [
                mock.call(self._controller.images.view, stretch=1),
                mock.call(self._controller.annots.view, stretch=1),
            ]
        )
        self._controller.images.view.show.assert_called_once_with()
        self._controller.images.stop_annotating.assert_called_once_with()
        self._controller.annots.stop_annotating.assert_called_once_with()

    def test_stop_annotating_not_shuffled_new_shuff_order_false(self):
        self._controller.has_new_shuffled_order = False
        self._controller.images.view.shuffle = MagicMock()
        self._controller.images.view.file_widget.shuffled = False
        self._controller.annotating_shortcuts_off = MagicMock()
        self._controller._stop_annotating()
        self._controller.annotating_shortcuts_off.assert_called_once_with()
        self._controller.images.view.file_widget.currentItemChanged.disconnect.assert_called_once()
        self._controller.images.view.shuffle.toggled.disconnect.assert_called_once_with(
            self._controller._shuffle_toggled
        )
        assert self._controller.has_new_shuffled_order is None
        self._controller.layout.addWidget.assert_has_calls(
            [
                mock.call(self._controller.images.view, stretch=1),
                mock.call(self._controller.annots.view, stretch=1),
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

        self._controller.annotating_shortcuts_on = MagicMock()

        self._controller._setup_annotating()
        self._controller.annotating_shortcuts_on.assert_called_once_with()

        self._controller.layout.removeWidget.assert_called_once_with(self._controller.images.view)
        self._controller.images.view.hide.assert_called_once()
        self._controller._fix_csv_annotations.assert_called_once_with({"filepath.png": ["filepath", ""]})
        self._controller.images.start_annotating.assert_called_once_with(0)
        self._controller.annots.start_annotating.assert_called_once_with(
            self._controller.images.get_num_images(), self._controller.csv_annotation_values, True
        )
        self._controller.annots.set_curr_img.assert_called_once_with(self._controller.images.curr_img_dict())
        self._controller.images.view.file_widget.currentItemChanged.connect.assert_not_called()
        self._controller.images.view.input_dir.hide.assert_not_called()
        self._controller.images.view.input_file.hide.assert_not_called()

    def test_setup_annotating_not_csv_annotations(self):
        self._controller.starting_row = None
        self._controller.images.get_files_dict = MagicMock(return_value=({"filepath.png": ["filepath", ""]}, False))
        self._controller.csv_annotation_values = None
        self._controller.annotating_shortcuts_on = MagicMock()

        self._controller._setup_annotating()
        self._controller.annotating_shortcuts_on.assert_called_once_with()
        self._controller.layout.removeWidget.assert_not_called()
        self._controller.images.view.hide.assert_not_called()
        self._controller.images.start_annotating.assert_called_once_with()

        self._controller.annots.start_annotating.assert_called_once_with(
            self._controller.images.get_num_images(), {"filepath.png": ["filepath", ""]}, False
        )
        self._controller.annots.set_curr_img.assert_called_once_with(self._controller.images.curr_img_dict())
        self._controller.images.view.file_widget.currentItemChanged.connect.assert_called_once()
        self._controller.images.view.input_dir.hide.assert_called_once_with()
        self._controller.images.view.input_file.hide.assert_called_once_with()

    def test_annotating_shortcuts_on(self):
        QShortcut.activated = MagicMock()
        QShortcut.activated.connect = MagicMock()
        self._controller._next_image_clicked = MagicMock()
        self._controller._prev_image_clicked = MagicMock()
        self._controller._toggle_check = MagicMock()
        self._controller._shortcut_key_next = create_autospec(QShortcut)
        self._controller._shortcut_key_prev = create_autospec(QShortcut)
        self._controller._shortcut_key_down = create_autospec(QShortcut)
        self._controller._shortcut_key_up = create_autospec(QShortcut)
        self._controller._shortcut_key_check = create_autospec(QShortcut)

        self._controller.annotating_shortcuts_on()

        self._controller._shortcut_key_next.activated.connect.assert_called_once_with(self._controller._next_image_clicked)
        self._controller._shortcut_key_prev.activated.connect.assert_called_once_with(self._controller._prev_image_clicked)
        self._controller._shortcut_key_down.activated.connect.assert_called_once_with(
            self._controller.annots.view.annot_list.next_item
        )
        self._controller._shortcut_key_up.activated.connect.assert_called_once_with(
            self._controller.annots.view.annot_list.prev_item
        )
        self._controller._shortcut_key_check.activated.connect.assert_called_once_with(self._controller._toggle_check)

    def test_annotating_shortcuts_off(self):
        QShortcut.activated = MagicMock()
        QShortcut.activated.disconnect = MagicMock()
        self._controller._next_image_clicked = MagicMock()
        self._controller._prev_image_clicked = MagicMock()
        self._controller._toggle_check = MagicMock()
        self._controller._shortcut_key_next = create_autospec(QShortcut)
        self._controller._shortcut_key_prev = create_autospec(QShortcut)
        self._controller._shortcut_key_down = create_autospec(QShortcut)
        self._controller._shortcut_key_up = create_autospec(QShortcut)
        self._controller._shortcut_key_check = create_autospec(QShortcut)

        self._controller.annotating_shortcuts_off()

        self._controller._shortcut_key_next.activated.disconnect.assert_called_once_with(self._controller._next_image_clicked)
        self._controller._shortcut_key_prev.activated.disconnect.assert_called_once_with(self._controller._prev_image_clicked)
        self._controller._shortcut_key_down.activated.disconnect.assert_called_once_with(
            self._controller.annots.view.annot_list.next_item
        )
        self._controller._shortcut_key_up.activated.disconnect.assert_called_once_with(
            self._controller.annots.view.annot_list.prev_item
        )
        self._controller._shortcut_key_check.activated.disconnect.assert_called_once_with(self._controller._toggle_check)

    def test_toggle_check_none(self):
        item = None
        self._controller.annots.view.annot_list.currentItem = MagicMock(return_value=item)
        self._controller._toggle_check()

    def test_toggle_check_wrong_type(self):
        item = create_autospec(TemplateItem)
        item.type = ItemType.STRING
        self._controller.annots.view.annot_list.currentItem = MagicMock(return_value=item)
        self._controller._toggle_check()

    def test_toggle_check(self):
        item = create_autospec(TemplateItem)
        item.type = ItemType.BOOL
        item.editable_widget = create_autospec(QCheckBox)
        item.get_value = MagicMock(return_value=True)
        item.editable_widget.setChecked = MagicMock()
        self._controller.annots.view.annot_list.currentItem = MagicMock(return_value=item)
        self._controller._toggle_check()
        item.editable_widget.setChecked.assert_called_once_with(False)

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

    def test_unequal_shuffled_fix_csv_annotations_additions_deletions_start_row_alr_annt(self):
        dct = {
            "name3.png": ["name3", ""],
            "name1.png": ["name1", ""],
            "name2.png": ["name2", ""],
            "name7.png": ["name7", ""],
            "name6.png": ["name6", ""],
        }
        self._controller.csv_annotation_values = {
            "name1.png": ["name1", "", True, "hello"],
            "name2.png": ["name2", "", None, "hello"],
            "name3.png": ["name3", "", False, "hello"],
            "name4.png": ["name4", "", True, "hello"],
            "name5.png": ["name5", "", False, "hello"],
        }
        self._controller.starting_row = 1
        self._controller.has_none_annotation = MagicMock(side_effect=[False, False, True])  # set side effect
        self._controller._unequal_shuffled_fix_csv_annotations(dct)

        assert self._controller.csv_annotation_values == {
            "name3.png": ["name3", "", False, "hello"],
            "name1.png": ["name1", "", True, "hello"],
            "name2.png": ["name2", "", None, "hello"],
            "name7.png": ["name7", ""],
            "name6.png": ["name6", ""],
        }

        assert self._controller.starting_row == 2
        self._controller.has_none_annotation.assert_has_calls(
            [mock.call([False, "hello"]), mock.call([True, "hello"]), mock.call([None, "hello"])], any_order=True
        )

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

    def test_equal_shuffled_fix_csv_annotations_additions_end_start_row(self):
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
            "name3.png": ["name3", "", False, "hello"],
            "name4.png": ["name4", "", True, "hello"],
            "name5.png": ["name5", "", False, "hello"],
            "name6.png": ["name6", "", True, "hello"],
        }
        self._controller.starting_row = 5
        self._controller.has_none_annotation = MagicMock(
            side_effect=[False, False, False, False, False, False]
        )  # set side effect
        self._controller._equal_shuffled_fix_csv_annotations(dct)

        assert self._controller.csv_annotation_values == {
            "name5.png": ["name5", "", False, "hello"],
            "name3.png": ["name3", "", False, "hello"],
            "name1.png": ["name1", "", True, "hello"],
            "name2.png": ["name2", "", True, "hello"],
            "name4.png": ["name4", "", True, "hello"],
            "name6.png": ["name6", "", True, "hello"],
        }

        assert self._controller.starting_row == 5
        self._controller.has_none_annotation.assert_has_calls(
            [
                mock.call([True, "hello"]),
                mock.call([False, "hello"]),
                mock.call([True, "hello"]),
                mock.call([True, "hello"]),
                mock.call([True, "hello"]),
                mock.call([False, "hello"]),
            ]
        )

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

    def test_image_selected_previous_none(self):
        self._controller._image_selected("curr", None)
        self._controller.annots.record_annotations.assert_not_called()
        self._controller.annots.set_curr_img.assert_called_once_with(self._controller.images.curr_img_dict())

    def test_image_selected(self):
        prev = MagicMock()
        prev.file_path = "path"
        self._controller._image_selected("current", prev)
        self._controller.annots.record_annotations.assert_called_once_with("path")
        self._controller.annots.set_curr_img.assert_called_once_with(self._controller.images.curr_img_dict())

    def test_exit_clicked_false(self):
        Popup.make_popup = MagicMock(return_value=False)
        self._controller._stop_annotating = MagicMock()
        self._controller._exit_clicked()
        self._controller._stop_annotating.assert_not_called()

    def test_exit_clicked_true(self):
        Popup.make_popup = MagicMock(return_value=True)
        self._controller._stop_annotating = MagicMock()
        self._controller._exit_clicked()
        self._controller._stop_annotating.assert_called_once_with()

    def test_save(self):
        self._controller.annots.save_annotations = MagicMock()
        self._controller.annots.view.save_btn.setEnabled = MagicMock()

        self._controller._save()
        self._controller.annots.save_annotations.assert_called_once_with()
        self._controller.annots.view.save_btn.setEnabled.assert_called_once_with(False)

    def test_has_none_annotation_false(self):
        self._controller.annots.get_annot_json_data = MagicMock(
            return_value={"key1": {}, "key2": {}, "key3": {}, "key4:": {}}
        )
        assert not self._controller.has_none_annotation([True, 5, "h", " "])

    def test_has_none_annotation_len_too_small(self):
        self._controller.annots.get_annot_json_data = MagicMock(
            return_value={"key1": {}, "key2": {}, "key3": {}, "key4:": {}}
        )
        assert self._controller.has_none_annotation([True, 5, "h"])

    def test_has_none_annotation_none(self):
        self._controller.annots.get_annot_json_data = MagicMock(
            return_value={"key1": {}, "key2": {}, "key3": {}, "key4:": {}}
        )
        assert self._controller.has_none_annotation([True, None, "h", " "])

    def test_has_none_annotation_empty_string(self):
        self._controller.annots.get_annot_json_data = MagicMock(
            return_value={"key1": {}, "key2": {}, "key3": {}, "key4:": {}}
        )
        assert self._controller.has_none_annotation([True, 5, "h", ""])
