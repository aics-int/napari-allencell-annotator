from unittest import mock
from unittest.mock import MagicMock, create_autospec

import pytest

from napari_allencell_annotator.model.combo_key import ComboKey

from napari_allencell_annotator.model.key import Key

from napari_allencell_annotator.view.i_viewer import IViewer

from napari_allencell_annotator._tests.fakes.fake_viewer import FakeViewer

from napari_allencell_annotator.model.annotation_model import AnnotatorModel

from napari_allencell_annotator.view.annotator_view import (
    AnnotatorView,
    AnnotatorViewMode,
    QVBoxLayout,
    QWidget,
    TemplateList,
    QScrollArea,
)
from napari_allencell_annotator.widgets.template_item import TemplateItem


@pytest.fixture
def annotator_model(qtbot) -> AnnotatorModel:
    return AnnotatorModel()


@pytest.fixture
def viewer(qtbot) -> IViewer:
    return FakeViewer()


@pytest.fixture
def annotator_view(qtbot, annotator_model: AnnotatorModel, viewer: IViewer) -> AnnotatorView:
    return AnnotatorView(annotator_model, viewer)


def test_get_curr_annots(annotator_view: AnnotatorView) -> None:

    # ACT
    annotator_view.annot_list.add_item("text", Key("string", ""))
    annotator_view.annot_list.add_item("number", Key("number", 1))
    annotator_view.annot_list.add_item("bool", Key("bool", True))
    annotator_view.annot_list.add_item("list", ComboKey("list", ["a", "b", "c"], "a"))
    annotator_view.annot_list.add_item("point", Key("point_created", None))
    annotator_view.annot_list.add_item("point", Key("point_none", None))
    annotator_view.viewer.create_points_layer("point_created", True, [(0, 0, 0, 0, 0, 0)])
    print(annotator_view.viewer.get_all_point_annotations())

    # add create points
    assert annotator_view.get_curr_annots() == ["", 1, True, "a", [(0, 0, 0, 0, 0, 0)], None]

    # annotator_view.annot_list.item(0).set_value("")
    # annotator_view.annot_list.item(1).set_value(1)
    # annotator_view.annot_list.item(2).set_value(True)
    # annotator_view.annot_list.item().set_value("text")

    # ASSERT


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

    # def test_get_curr_annots(self):
    #     item1 = create_autospec(TemplateItem)
    #     item1.get_value = MagicMock(return_value="ret1")
    #     item2 = create_autospec(TemplateItem)
    #     item2.get_value = MagicMock(return_value="ret2")
    #     item3 = create_autospec(TemplateItem)
    #     item3.get_value = MagicMock(return_value="ret3")
    #     self._view.annot_list = create_autospec(TemplateList)
    #     self._view.annot_list.items = [item1, item2, item3]
    #     assert self._view.get_curr_annots() == ["ret1", "ret2", "ret3"]

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
