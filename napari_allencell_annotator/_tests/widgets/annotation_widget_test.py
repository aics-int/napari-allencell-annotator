from unittest import mock
from unittest.mock import MagicMock, create_autospec

from qtpy.QtCore import QSize

from napari_allencell_annotator.widgets.annotation_widget import AnnotationWidget, AnnotationItem


class TestAnnotationWidget:
    def setup_method(self):
        with mock.patch.object(AnnotationWidget, "__init__", lambda x: None):
            self._widget = AnnotationWidget()

    def test_clear_all(self):
        self._widget.clear = MagicMock()
        self._widget.clear_all()
        self._widget.clear.assert_called_once_with()

    # TODO: EDIT TESTS TO MATCH CURRENT ANNOTATION WIDGET
    # def test_add_existing_item_str(self):
    #     item = create_autospec(AnnotationItem)
    #     self._widget.add_new_item = MagicMock(return_value=item)
    #     self._widget.add_existing_item("name", {"type": "string", "default": "default value"})
    #     self._widget.add_new_item.assert_called_once_with()
    #     item.fill_vals_text.assert_called_once_with("name", "default value")
    #
    # def test_add_existing_item_num(self):
    #     item = create_autospec(AnnotationItem)
    #     self._widget.add_new_item = MagicMock(return_value=item)
    #     self._widget.add_existing_item("name", {"type": "number", "default": 1})
    #     self._widget.add_new_item.assert_called_once_with()
    #     item.fill_vals_number.assert_called_once_with("name", 1)
    #
    # def test_add_existing_item_bool(self):
    #     item = create_autospec(AnnotationItem)
    #     self._widget.add_new_item = MagicMock(return_value=item)
    #     self._widget.add_existing_item("name", {"type": "bool", "default": True})
    #     self._widget.add_new_item.assert_called_once_with()
    #     item.fill_vals_check.assert_called_once_with("name", True)
    #
    # def test_add_existing_item_list(self):
    #     item = create_autospec(AnnotationItem)
    #     self._widget.add_new_item = MagicMock(return_value=item)
    #     self._widget.add_existing_item("name", {"type": "list", "default": "1", "options": ["1", "2", "3"]})
    #     self._widget.add_new_item.assert_called_once_with()
    #     item.fill_vals_list.assert_called_once_with("name", "1", ["1", "2", "3"])

    def test_add_new_item_greater_than_10(self):
        self._widget.count = MagicMock(return_value=10)
        self._widget.setMaximumHeight = MagicMock()

        self._widget.add_new_item()

        self._widget.count.assert_called_once_with()
        self._widget.setMaximumHeight.assert_not_called()

    def test_add_new_item_less_than_10(self):
        with mock.patch.object(AnnotationItem, "__init__", lambda x, y: None):

            item = AnnotationItem("x")
            AnnotationItem.check = MagicMock()
            size = create_autospec(QSize)
            AnnotationItem.sizeHint = MagicMock(return_value=size)
            size.height = MagicMock(return_value=10)

            self._widget.count = MagicMock(return_value=5)
            self._widget.setMaximumHeight = MagicMock()
            assert isinstance(self._widget.add_new_item(), AnnotationItem)

            item.check.stateChanged.connect.assert_called_once()
            item.sizeHint.assert_called_once_with()
            size.height.assert_called_once_with()
            assert len(self._widget.count.mock_calls) == 2
            self._widget.setMaximumHeight.assert_called_once_with(50)

    # def test_remove_item(self):
    #     self._widget.takeItem = MagicMock()
    #     self._widget.row = MagicMock(return_value=5)
    #     self._widget.setMaximumHeight = MagicMock()
    #     self._widget.count = MagicMock(return_value=1)
    #     with mock.patch.object(AnnotationItem, "__init__", lambda x: None):
    #         item = create_autospec(AnnotationItem)
    #         item.sizeHint().height = MagicMock(return_value=4)
    #
    #         self._widget.remove_item(item)
    #         self._widget.takeItem.assert_called_once_with(5)
    #         self._widget.setMaximumHeight.assert_called_once_with(4)

    def test_delete_checked_one_item(self):
        self._widget.count = MagicMock(return_value=3)
        item = create_autospec(AnnotationItem)
        item.check = MagicMock()
        item.check.isChecked = MagicMock(return_value=False)
        item2 = create_autospec(AnnotationItem)
        item2.check = MagicMock()
        item2.check.isChecked = MagicMock(return_value=False)
        item3 = create_autospec(AnnotationItem)
        item3.check = MagicMock()
        item3.check.isChecked = MagicMock(return_value=True)
        self._widget.item = MagicMock(side_effect=[item, item2, item3, item3])
        self._widget.num_checked = 1
        self._widget.remove_item = MagicMock()
        self._widget.annots_selected = MagicMock()

        self._widget.delete_checked()
        assert self._widget.num_checked == 0
        self._widget.remove_item.assert_called_once_with(item3)
        self._widget.annots_selected.emit.assert_called_once_with(False)

    def test_delete_checked_all_items(self):
        self._widget.count = MagicMock(return_value=3)
        item = create_autospec(AnnotationItem)
        item.check = MagicMock()
        item.check.isChecked = MagicMock(return_value=True)
        item2 = create_autospec(AnnotationItem)
        item2.check = MagicMock()
        item2.check.isChecked = MagicMock(return_value=True)
        item3 = create_autospec(AnnotationItem)
        item3.check = MagicMock()
        item3.check.isChecked = MagicMock(return_value=True)
        self._widget.item = MagicMock(side_effect=[item, item, item2, item2, item3, item3])
        self._widget.num_checked = 3
        self._widget.remove_item = MagicMock()
        self._widget.annots_selected = MagicMock()

        self._widget.delete_checked()
        assert self._widget.num_checked == 0
        self._widget.remove_item.assert_has_calls([mock.call(item), mock.call(item2), mock.call(item3)])
        self._widget.annots_selected.emit.assert_called_once_with(False)

    def test_check_evt_true_emit_signal(self):
        item = create_autospec(AnnotationItem)
        item.check = MagicMock()
        item.check.isChecked = MagicMock(return_value=True)
        self._widget.num_checked = 0
        self._widget.annots_selected = MagicMock()

        self._widget._check_evt(item)
        assert self._widget.num_checked == 1
        self._widget.annots_selected.emit.assert_called_once_with(True)

    def test_check_evt_true_no_signal(self):
        item = create_autospec(AnnotationItem)
        item.check = MagicMock()
        item.check.isChecked = MagicMock(return_value=True)
        self._widget.num_checked = 2
        self._widget.annots_selected = MagicMock()

        self._widget._check_evt(item)
        assert self._widget.num_checked == 3
        self._widget.annots_selected.emit.assert_not_called()

    def test_check_evt_false_no_signal(self):
        item = create_autospec(AnnotationItem)
        item.check = MagicMock()
        item.check.isChecked = MagicMock(return_value=False)
        self._widget.num_checked = 2
        self._widget.annots_selected = MagicMock()

        self._widget._check_evt(item)
        assert self._widget.num_checked == 1
        self._widget.annots_selected.emit.assert_not_called()

    def test_check_evt_false_emit_signal(self):
        item = create_autospec(AnnotationItem)
        item.check = MagicMock()
        item.check.isChecked = MagicMock(return_value=False)
        self._widget.num_checked = 1
        self._widget.annots_selected = MagicMock()

        self._widget._check_evt(item)
        assert self._widget.num_checked == 0
        self._widget.annots_selected.emit.assert_called_once_with(False)
