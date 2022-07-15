from unittest import mock
from unittest.mock import MagicMock

from napari_allencell_annotator.view.annotator_view import (
    AnnotatorView,
    AnnotatorViewMode,
)


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

    def test_reset_annotations(self):
        self._view.annot_list = MagicMock()
        self._view.annotation_item_widgets = ["item"]
        self._view.annots_order = ["item"]
        self._view.default_vals = ["item"]
        self._view.reset_annotations()

        self._view.annot_list.clear.assert_called_once_with()
        assert self._view.annotation_item_widgets == []
        assert self._view.annots_order == []
        assert self._view.default_vals == []

    def test_render_default_values(self):
        self._view.default_vals = []
        self._view.render_values = MagicMock()
        self._view.render_default_values()
        self._view.render_values.assert_called_once_with([])
