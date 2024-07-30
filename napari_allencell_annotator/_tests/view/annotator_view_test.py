from unittest import mock
from unittest.mock import MagicMock, create_autospec

from napari_allencell_annotator.view.annotator_view import (
    AnnotatorView,
    AnnotatorViewMode,
    QVBoxLayout,
    QWidget,
    TemplateList,
    QScrollArea,
)
from napari_allencell_annotator.widgets.template_item import TemplateItem


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

    def test_reset_annotations(self):
        self._view.annot_list = create_autospec(TemplateList)
        self._view.annots_order = ["item"]
        self._view.scroll = create_autospec(QScrollArea)

        self._view._reset_annotations()
        self._view.scroll.setMaximumHeight.assert_called_once_with(600)
        self._view.annot_list.clear_all.assert_called_once_with()
        assert self._view.annots_order == []

    def test_render_default_values(self):
        item1 = create_autospec(TemplateItem)
        item2 = create_autospec(TemplateItem)
        self._view.annot_list = create_autospec(TemplateList)
        self._view.annot_list.items = [item1, item2]
        self._view.render_default_values()
        item1.set_default_value.assert_called_once_with()
        item2.set_default_value.assert_called_once_with()

    def test_render_values_none(self):
        item1 = create_autospec(TemplateItem)
        item2 = create_autospec(TemplateItem)
        self._view.annot_list = create_autospec(TemplateList)
        self._view.annot_list.items = [item1, item2]

        vals = [None, None]

        self._view.render_values(vals)
        item1.set_default_value.assert_called_once_with()
        item2.set_default_value.assert_called_once_with()

    def test_render_values_empty(self):
        item1 = create_autospec(TemplateItem)
        item2 = create_autospec(TemplateItem)
        self._view.annot_list = create_autospec(TemplateList)
        self._view.annot_list.items = [item1, item2]

        vals = ["", ""]

        self._view.render_values(vals)
        item1.set_default_value.assert_called_once_with()
        item2.set_default_value.assert_called_once_with()

    def test_render_values_not_none(self):
        item1 = create_autospec(TemplateItem)
        item2 = create_autospec(TemplateItem)
        self._view.annot_list = create_autospec(TemplateList)
        self._view.annot_list.items = [item1, item2]

        vals = ["val1", "val2"]

        self._view.render_values(vals)
        item1.set_default_value.assert_not_called()
        item1.set_value.assert_called_once_with("val1")
        item2.set_value.assert_called_once_with("val2")

    def test_render_values_mixed(self):
        item1 = create_autospec(TemplateItem)
        item2 = create_autospec(TemplateItem)
        item3 = create_autospec(TemplateItem)
        self._view.annot_list = create_autospec(TemplateList)
        self._view.annot_list.items = [item1, item2, item3]

        vals = [None, "val2", ""]

        self._view.render_values(vals)
        item1.set_default_value.assert_called_once_with()
        item2.set_value.assert_called_once_with("val2")
        item3.set_default_value.assert_called_once_with()

    def test_get_curr_annots(self):
        item1 = create_autospec(TemplateItem)
        item1.get_value = MagicMock(return_value="ret1")
        item2 = create_autospec(TemplateItem)
        item2.get_value = MagicMock(return_value="ret2")
        item3 = create_autospec(TemplateItem)
        item3.get_value = MagicMock(return_value="ret3")
        self._view.annot_list = create_autospec(TemplateList)
        self._view.annot_list.items = [item1, item2, item3]
        assert self._view.get_curr_annots() == ["ret1", "ret2", "ret3"]

    def test_display_mode_add_mode(self):
        self._view._mode = AnnotatorViewMode.ADD
        self._view.add_widget = MagicMock()
        self._view._reset_annotations = MagicMock()
        self._view.layout = create_autospec(QVBoxLayout)
        self._view.layout.count = MagicMock(return_value=3)
        item = create_autospec(TemplateItem)
        widget = create_autospec(QWidget)
        item.widget = MagicMock(return_value=widget)
        self._view.layout.itemAt = MagicMock(return_value=item)

        self._view._display_mode()

        self._view.layout.count.assert_called_once_with()
        item.widget.assert_called_once_with()
        widget.hide.assert_called_once_with()
        self._view.layout.removeItem.assert_called_once_with(item)
        self._view.add_widget.show.assert_called_once_with()
        self._view.layout.addWidget.assert_called_once_with(self._view.add_widget)

    def test_display_mode_view_mode(self):
        self._view._mode = AnnotatorViewMode.VIEW
        self._view.save_json_btn = MagicMock()
        self._view.view_widget = MagicMock()
        self._view.layout = create_autospec(QVBoxLayout)
        self._view.layout.count = MagicMock(return_value=3)
        item = create_autospec(TemplateItem)
        widget = create_autospec(QWidget)
        item.widget = MagicMock(return_value=widget)
        self._view.layout.itemAt = MagicMock(return_value=item)

        self._view._display_mode()

        self._view.layout.count.assert_called_once_with()
        item.widget.assert_called_once_with()
        widget.hide.assert_called_once_with()
        self._view.layout.removeItem.assert_called_once_with(item)
        self._view.view_widget.show.assert_called_once_with()
        self._view.save_json_btn.setEnabled.assert_called_once_with(True)
        self._view.layout.addWidget.assert_called_once_with(self._view.view_widget)

    def test_display_mode_annotate_mode(self):
        self._view._mode = AnnotatorViewMode.ANNOTATE
        self._view.prev_btn = MagicMock()
        self._view.annot_widget = MagicMock()
        self._view.layout = create_autospec(QVBoxLayout)
        self._view.layout.count = MagicMock(return_value=3)
        item = create_autospec(TemplateItem)
        widget = create_autospec(QWidget)
        item.widget = MagicMock(return_value=widget)
        self._view.layout.itemAt = MagicMock(return_value=item)

        self._view._display_mode()

        self._view.layout.count.assert_called_once_with()
        item.widget.assert_called_once_with()
        widget.hide.assert_called_once_with()
        self._view.layout.removeItem.assert_called_once_with(item)
        self._view.annot_widget.show.assert_called_once_with()
        self._view.prev_btn.setEnabled.assert_called_once_with(False)
        self._view.layout.addWidget.assert_called_once_with(self._view.annot_widget)

    def test_render_annotations(self):
        # TODO test with model qtbot
        pass

    def test_render_annotations_one_item(self):
        pass

    def test_create_annot(self):
        self._view.annots_order = ["name1"]
        self._view.annot_list = create_autospec(TemplateList)
        self._view._create_annot("name2", {})
        assert self._view.annots_order == ["name1", "name2"]
        self._view.annot_list.add_item.assert_called_once_with("name2", {})
