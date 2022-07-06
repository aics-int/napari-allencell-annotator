from unittest import mock
from unittest.mock import MagicMock, create_autospec

import napari_allencell_annotator.view.annotator_view

from napari_allencell_annotator.view.annotator_view import AnnotatorView, AnnotatorViewMode

from napari_allencell_annotator.view.annotator_view import QLineEdit


class TestAnnotatorView:
    def setup_method(self):
        with mock.patch.object(AnnotatorView, "__init__", lambda x: None):
            self._view = AnnotatorView()
            self._view._mode = AnnotatorViewMode.ADD

    def test_mode(self):
        assert self._view.mode == AnnotatorViewMode.ADD

    def test_set_mode(self):
        expected = AnnotatorViewMode.VIEW
        self._view._display_mode = MagicMock()
        self._view.set_mode(expected)
        assert self._view._mode == self._view.mode == expected
        self._view._display_mode.assert_called_once_with()

    def test_set_num_images(self):
        self._view.set_num_images(4)
        assert self._view.num_images == 4

    def test_set_curr_index(self):
        self._view.num_images = 4
        self._view.progress_bar = MagicMock()
        self._view.progress_bar.setText = MagicMock()
        self._view.set_curr_index(2)
        self._view.progress_bar.setText.assert_called_once_with("3 of 4 Images")
        assert self._view.curr_index == 2

    def test_render_annotations(self):
        dic = {"name1": {}, "name2": {}}
        self._view._create_annot = MagicMock()
        self._view.annot_list = MagicMock()
        self._view.annot_list.setMaximumHeight = MagicMock()
        self._view.render_annotations(dic)
        assert self._view.annotation_item_widgets == []
        self._view.annot_list.setMaximumHeight.assert_called_once_with(45.5*2)
        self._view._create_annot.assert_has_calls([mock.call("name1", {}), mock.call("name2", {})])


