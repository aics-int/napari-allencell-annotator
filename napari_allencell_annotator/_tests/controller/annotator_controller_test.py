from unittest import mock
from unittest.mock import MagicMock, create_autospec, patch
from unittest.mock import mock_open

from napari_allencell_annotator.controller.annotator_controller import (
    AnnotatorController,
)
from napari_allencell_annotator.controller.annotator_controller import (
    AnnotatorViewMode,
    AnnotatorView,
)

from napari_allencell_annotator.controller.annotator_controller import napari, csv


class TestAnnotatorController:
    def setup_method(self):
        self._mock_viewer: MagicMock = create_autospec(napari.Viewer)
        with mock.patch("napari_allencell_annotator.controller.annotator_controller.AnnotatorView"):
            self._controller = AnnotatorController(self._mock_viewer)
            self._controller.files_and_annots = {}
            self._controller.view = create_autospec(AnnotatorView)

    def test_set_annot_json_data(self):
        self._controller.annot_json_data = None
        self._controller.set_annot_json_data({})
        assert self._controller.annot_json_data == {}

    def test_set_csv_name(self):
        self._controller.csv_name = None
        self._controller.set_csv_name("name")
        assert self._controller.csv_name == "name"

    def test_start_viewing(self):
        self._controller.annot_json_data = "data"
        self._controller.start_viewing()
        self._controller.view.set_mode.assert_called_once_with(mode=AnnotatorViewMode.VIEW)
        self._controller.view.render_annotations.assert_called_once_with("data")

    def test_stop_viewing(self):
        self._controller.annot_json_data = "data"
        self._controller.stop_viewing()
        self._controller.view.set_mode.assert_called_once_with(mode=AnnotatorViewMode.ADD)
        assert self._controller.annot_json_data is None

    def test_start_annotating_empty(self):
        self._controller.shuffled = None
        self._controller.start_annotating(4, {}, True)

        assert self._controller.files_and_annots == {}
        self._controller.view.set_num_images.assert_called_once_with(4)
        self._controller.view.set_mode.assert_called_once_with(mode=AnnotatorViewMode.ANNOTATE)
        assert self._controller.shuffled == True

    def test_start_annotating(self):
        self._controller.start_annotating(4, {"path": ["lst"]}, False)

        assert self._controller.files_and_annots == {"path": ["lst"]}
        self._controller.view.set_num_images.assert_called_once_with(4)
        self._controller.view.set_mode.assert_called_once_with(mode=AnnotatorViewMode.ANNOTATE)
        assert self._controller.shuffled == False

    def test_stop_annotating(self):
        self._controller.files_and_annots = {"item": 'item'}
        self._controller.write_csv = MagicMock()
        self._controller.curr_img_dict = {"File Path": "path"}
        self._controller.record_annotations = MagicMock()
        self._controller.set_curr_img = MagicMock()
        self._controller.set_csv_name = MagicMock()

        self._controller.stop_annotating()

        self._controller.write_csv.assert_called_once_with()
        self._controller.record_annotations.assert_called_once_with("path")
        self._controller.view.set_curr_index.assert_called_once_with()
        assert self._controller.files_and_annots == {}
        self._controller.view.set_num_images.assert_called_once_with()

        self._controller.view.set_mode.assert_called_once_with(mode=AnnotatorViewMode.ADD)
        self._controller.view.render_default_values.assert_called_once_with()
        self._controller.view.toggle_annots_editable.assert_called_once_with(False)
        self._controller.set_curr_img.assert_called_once_with()
        self._controller.set_csv_name.assert_called_once_with()

    def test_set_curr_img_none(self):
        self._controller.curr_img_dict = {}
        self._controller.set_curr_img(None)
        assert self._controller.curr_img_dict is None
        self._controller.view.render_default_values.assert_not_called()
        self._controller.view.render_values.assert_not_called()

    def test_set_curr_img_less_than_3(self):
        self._controller.files_and_annots["path.png"] = ["path", ""]
        self._controller.view.prev_btn = MagicMock()
        self._controller.view.next_btn = MagicMock()
        self._controller.view.num_images = 5
        dic = {
            "File Path": "path.png",
            "Row": 4,
        }
        self._controller.set_curr_img(dic)

        assert self._controller.curr_img_dict == dic
        self._controller.view.render_default_values.assert_called_once_with()
        assert len(self._controller.files_and_annots) == 1
        assert self._controller.files_and_annots["path.png"] == [
            "path",
            ""
        ]
        self._controller.view.render_values.assert_not_called()
        self._controller.view.set_curr_index.assert_called_once_with(4)
        self._controller.view.next_btn.setEnabled.assert_called_once_with(False)
        self._controller.view.prev_btn.setEnabled.assert_called_once_with(True)

    def test_set_curr_img_more_than_3(self):
        self._controller.files_and_annots["path.png"] = ["path", "", "True", 'hello']
        self._controller.view.prev_btn = MagicMock()
        self._controller.view.next_btn = MagicMock()
        self._controller.view.num_images = 5
        dic = {
            "File Path": "path.png",
            "Row": 0,
        }
        self._controller.set_curr_img(dic)

        assert self._controller.curr_img_dict == dic
        self._controller.view.render_default_values.assert_not_called()
        assert len(self._controller.files_and_annots) == 1
        assert self._controller.files_and_annots["path.png"] == [
            "path",
            "", "True", 'hello'
        ]
        self._controller.view.render_values.assert_called_once_with(['True', 'hello'])
        self._controller.view.set_curr_index.assert_called_once_with(0)
        self._controller.view.next_btn.setEnabled.assert_called_once_with(True)
        self._controller.view.prev_btn.setEnabled.assert_called_once_with(False)

    def test_set_curr_img_empty_strings(self):
        self._controller.files_and_annots["path.png"] = ["path", "", "True", '', '']
        self._controller.view.prev_btn = MagicMock()
        self._controller.view.next_btn = MagicMock()
        self._controller.view.num_images = 5
        dic = {
            "File Path": "path.png",
            "Row": 3,
        }
        self._controller.set_curr_img(dic)

        assert self._controller.curr_img_dict == dic
        self._controller.view.render_default_values.assert_not_called()
        assert len(self._controller.files_and_annots) == 1
        assert self._controller.files_and_annots["path.png"] == [
            "path",
            "", "True", '', ''
        ]
        self._controller.view.render_values.assert_called_once_with(['True', '', ''])
        self._controller.view.set_curr_index.assert_called_once_with(3)
        self._controller.view.next_btn.setEnabled.assert_called_once_with(True)
        self._controller.view.prev_btn.setEnabled.assert_called_once_with(True)

    def test_record_annotations(self):
        prev: str = "path"
        self._controller.files_and_annots = {"path": ["name", "fms"]}
        self._controller.view.get_curr_annots = MagicMock(return_value=[1, 2, 3])
        self._controller.record_annotations(prev)
        assert self._controller.files_and_annots[prev] == ["name", "fms", 1, 2, 3]
        self._controller.view.get_curr_annots.assert_called_once_with()

    @patch("builtins.open", new_callable=mock_open, read_data="data")
    def test_write_csv(self, mock_file):
        self._controller.annot_json_data = {"name": {}, "name2": {}, "name3": {}}
        self._controller.csv_name = "test.csv"
        self._controller.view.annots_order = ["ann1", "ann2", "ann3"]
        self._controller.files_and_annots = {
            "path1.png": ["path1", "", "text", 1, True],
            "path2.png": ["path2", "", "text2", 2, True],
        }
        self._controller.writer = create_autospec(csv.writer)
        self._controller.writer.writerow = MagicMock()

        self._controller.write_csv()

        mock_file.assert_called_once_with("test.csv", "w")
