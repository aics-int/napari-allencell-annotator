from unittest import mock
from unittest.mock import MagicMock, create_autospec, patch
from unittest.mock import mock_open

from napari_allencell_annotator.controller.annotator_controller import AnnotatorController
from napari_allencell_annotator.controller.annotator_controller import csv
from napari_allencell_annotator.controller.annotator_controller import AnnotatorViewMode

from napari_allencell_annotator.controller.annotator_controller import napari


class TestAnnotatorController:
    def setup_method(self):
        self._mock_viewer: MagicMock = create_autospec(napari.Viewer)
        with mock.patch("napari_allencell_annotator.controller.annotator_controller.AnnotatorView"):
            self._controller = AnnotatorController(self._mock_viewer)

    @patch("builtins.open", new_callable=mock_open, read_data="data")
    def test_start_annotating(self, mock_file):
        self._controller.view.set_num_images = MagicMock()
        self._controller.view.set_mode = MagicMock()
        self._controller.view.make_annots_editable = MagicMock()
        csv.writer = MagicMock()
        self._controller.file = MagicMock(value=None)
        self._controller.write_header = MagicMock()

        MockViewMode = create_autospec(AnnotatorViewMode)
        MockViewMode.ANNOTATE = MagicMock()

        self._controller.start_annotating(4)

        self._controller.view.set_num_images.assert_called_once_with(4)
        self._controller.view.set_mode.assert_called_once_with(mode=AnnotatorViewMode.ANNOTATE)
        self._controller.view.make_annots_editable.assert_called_once()

        csv.writer.assert_called_once()
        mock_file.assert_called_once_with("csv.csv", "w")
        self._controller.write_header.assert_called_once()

    def test_set_curr_img(self):
        self._controller.view.set_curr_index = MagicMock()
        self._controller.view.num_images = 3
        self._controller.view.next_btn.setText = MagicMock()
        dic = {"Row": "1"}
        self._controller.set_curr_img(dic)
        assert self._controller.curr_img == dic
        self._controller.view.set_curr_index.assert_called_once_with(1)

        self._controller.view.next_btn.setText.assert_not_called()

    def test_set_curr_img_last(self):
        self._controller.view.set_curr_index = MagicMock()
        self._controller.view.num_images = 3
        self._controller.view.next_btn.setText = MagicMock()
        dic = {"Row": "2"}
        self._controller.set_curr_img(dic)
        assert self._controller.curr_img == dic
        self._controller.view.set_curr_index.assert_called_once_with(2)

        self._controller.view.next_btn.setText.assert_called_once_with("Save and Export")

    def test_write_image_csv(self):
        d = {"File Name": "name", "File Path": "path", "FMS": "", "Row": "0"}
        annots = ['True', 5, 'hello']
        dlist = ["name", "path", "", 'True', 5, 'hello']
        self._controller.view.get_curr_annots = MagicMock(return_value=annots)
        self._controller.writer = MagicMock()
        self._controller.writer.writerow = MagicMock()

        self._controller.write_image_csv(d)
        self._controller.view.get_curr_annots.assert_called_once()
        self._controller.writer.writerow.assert_called_once_with(dlist)

    def test_write_header(self):
        self._controller.annot_data = {"Cell Type": {}, "Number": {}, "Alive": {}}

        header = ["File Name", "File Path", "FMS", "Cell Type", "Number", "Alive"]
        self._controller.writer = MagicMock()
        self._controller.writer.writerow = MagicMock()

        self._controller.write_header()
        self._controller.writer.writerow.assert_called_once_with(header)

    def test_save_and_export(self):
        self._controller.file = MagicMock()
        self._controller.file.close = MagicMock()
        self._controller.write_to_csv()
        self._controller.file.close.assert_called_once_with()
