from unittest import mock
from unittest.mock import MagicMock, create_autospec, patch
from unittest.mock import mock_open

from napari_allencell_annotator.controller.annotator_controller import AnnotatorController
from napari_allencell_annotator.controller.annotator_controller import AnnotatorViewMode

from napari_allencell_annotator.controller.annotator_controller import napari


class TestAnnotatorController:
    def setup_method(self):
        self._mock_viewer: MagicMock = create_autospec(napari.Viewer)
        with mock.patch("napari_allencell_annotator.controller.annotator_controller.AnnotatorView"):
            self._controller = AnnotatorController(self._mock_viewer)
            self._controller.annotation_dict = {}

    def test_start_annotating(self):
        self._controller.view.set_num_images = MagicMock()
        self._controller.view.set_mode = MagicMock()
        self._controller.view.make_annots_editable = MagicMock()
        self._controller.file = MagicMock(value=None)

        MockViewMode = create_autospec(AnnotatorViewMode)
        MockViewMode.ANNOTATE = MagicMock()

        self._controller.start_annotating(4)

        self._controller.view.set_num_images.assert_called_once_with(4)
        self._controller.view.set_mode.assert_called_once_with(mode=AnnotatorViewMode.ANNOTATE)
        self._controller.view.make_annots_editable.assert_called_once()

    def test_set_curr_img_not_in(self):
        self._controller.view.set_curr_index = MagicMock()
        self._controller.view.render_default_values = MagicMock()
        self._controller.view.render_values = MagicMock()
        self._controller.view.next_btn.setText = MagicMock()
        self._controller.view.num_images = 3
        dic = {"File Path": "path.png", "File Name": "path", "FMS": "", "Row": 1}
        self._controller.set_curr_img(dic)
        assert self._controller.curr_img == dic
        self._controller.view.render_default_values.assert_called_once_with()
        assert len(self._controller.annotation_dict) == 1
        assert self._controller.annotation_dict["path.png"] == ["path", ""]
        self._controller.view.render_values.assert_not_called()
        self._controller.view.set_curr_index.assert_called_once_with(1)
        self._controller.view.next_btn.setText.assert_called_once_with("Next")

    def test_set_curr_img_in_keys(self):  # TODO
        self._controller.annotation_dict["path.png"] = ["path", "", "text", 2]
        self._controller.view.set_curr_index = MagicMock()
        self._controller.view.render_default_values = MagicMock()
        self._controller.view.render_values = MagicMock()
        self._controller.view.next_btn.setText = MagicMock()
        self._controller.view.num_images = 2
        dic = {"File Path": "path.png", "File Name": "path", "FMS": "", "Row": 1}
        self._controller.set_curr_img(dic)
        assert self._controller.curr_img == dic
        self._controller.view.render_default_values.assert_not_called()
        assert len(self._controller.annotation_dict) == 1
        assert self._controller.annotation_dict["path.png"] == ["path", "", "text", 2]
        self._controller.view.render_values.assert_called_once_with(["text", 2])
        self._controller.view.set_curr_index.assert_called_once_with(1)
        self._controller.view.next_btn.setText.assert_called_once_with("Save and Export")

    def test_record_annotations(self):
        prev: str = "path"
        self._controller.annotation_dict = {"path": []}
        self._controller.view.get_curr_annots = MagicMock(return_value=[1, 2, 3])
        self._controller.record_annotations(prev)
        assert self._controller.annotation_dict[prev] == [1, 2, 3]
        self._controller.view.get_curr_annots.assert_called_once_with()

    @patch("builtins.open", new_callable=mock_open, read_data="data")
    def test_write_to_csv(self, mock_file):  # TODO
        self._controller.csv_name = "test.csv"
        self._controller.view.annots_order = ["ann1", "ann2", "ann3"]
        self._controller.annotation_dict = {"path1.png": ["path1", "", "text", 1, True],
                                            "path2.png": ["path2", "", "text2", 2, True]}
        with patch("napari_allencell_annotator.controller.annotator_controller.csv.writer") as patched:

            mock_write = MagicMock()
            mock_write.writerow = MagicMock()
            patched.return_value = mock_write

        #csv.writer.writerow = MagicMock()

            self._controller.write_to_csv()
            mock_file.assert_called_once_with("test.csv", "w")
            patched.writerow.assert_any_call(mock.call(["path1.png", "path1", "", "text", 1, True]))



