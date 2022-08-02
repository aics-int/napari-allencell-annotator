from unittest import mock
from unittest.mock import create_autospec, MagicMock

from napari_allencell_annotator.widgets.create_dialog import CreateDialog, QPushButton, AnnotationWidget, QLabel
from napari_allencell_annotator.widgets.annotation_item import AnnotationItem


class TestCreateDialog:
    def setup_method(self):
        with mock.patch.object(CreateDialog, "__init__", lambda x: None):
            self._create = CreateDialog()
            self._create.list = create_autospec(AnnotationWidget)

    def test_show_delete_true(self):
        self._create.delete = create_autospec(QPushButton)
        self._create._show_delete(True)
        self._create.delete.show.assert_called_once_with()

    def test_show_delete_false(self):
        self._create.delete = create_autospec(QPushButton)
        self._create._show_delete(False)
        self._create.delete.hide.assert_called_once_with()

    def test_delete_clicked_zero(self):
        self._create.list.num_checked = 0
        self._create._delete_clicked()
        self._create.list.delete_checked.assert_not_called()

    def test_delete_clicked_not_zero(self):
        self._create.list.num_checked = 2
        self._create._delete_clicked()
        self._create.list.delete_checked.assert_called_once_with()

    def test_add_clicked_less_than_9(self):
        self._create.list.count = MagicMock(return_value=8)
        self._create._add_clicked()
        self._create.list.count.assert_called_once_with()
        self._create.list.add_new_item.assert_called_once_with()

    def test_add_clicked_more_than_9(self):
        self._create.list.count = MagicMock(return_value=10)
        self._create.add = MagicMock()
        self._create._add_clicked()
        self._create.list.count.assert_called_once_with()
        self._create.list.add_new_item.assert_called_once_with()
        self._create.add.hide.assert_called_once_with()

    def test_get_annots_none(self):
        self._create.list.count = MagicMock(return_value=0)
        self._create.new_annot_dict = {}
        self._create.error = create_autospec(QLabel)
        self._create.get_annots()
        self._create.error.setText.assert_called_once_with(" Must provide at least one annotation. ")
        assert self._create.new_annot_dict is None

    def test_get_annots_one_valid(self):
        self._create.list.count = MagicMock(return_value=1)
        item = create_autospec(AnnotationItem)
        item.get_data = MagicMock(return_value=(True, "name", {}, ""))
        self._create.list.item = MagicMock(return_value=item)
        self._create.valid_annots_made = MagicMock()
        self._create.new_annot_dict = {}
        self._create.error = create_autospec(QLabel)
        self._create.get_annots()

        self._create.error.setText.assert_called_once_with("")
        assert self._create.new_annot_dict == {"name": {}}
        self._create.valid_annots_made.emit.assert_called_once_with()

    def test_get_annots_one_invalid(self):
        self._create.list.count = MagicMock(return_value=1)
        item = create_autospec(AnnotationItem)
        item.get_data = MagicMock(return_value=(False, "name", {}, "error"))
        self._create.list.item = MagicMock(return_value=item)
        self._create.valid_annots_made = MagicMock()
        self._create.new_annot_dict = {}
        self._create.error = create_autospec(QLabel)
        self._create.get_annots()

        self._create.error.setText.assert_called_once_with(" error")
        assert self._create.new_annot_dict is None

    def test_get_annots_mult_valid(self):
        self._create.list.count = MagicMock(return_value=3)
        item = create_autospec(AnnotationItem)
        item.get_data = MagicMock(return_value=(True, "name", {}, ""))
        item2 = create_autospec(AnnotationItem)
        item2.get_data = MagicMock(return_value=(True, "name2", {}, ""))
        item3 = create_autospec(AnnotationItem)
        item3.get_data = MagicMock(return_value=(True, "name3", {}, ""))
        self._create.list.item = MagicMock(side_effect=[item, item2, item3])
        self._create.valid_annots_made = MagicMock()
        self._create.new_annot_dict = {}
        self._create.error = create_autospec(QLabel)
        self._create.get_annots()

        self._create.error.setText.assert_called_once_with("")
        assert self._create.new_annot_dict == {"name": {}, "name2": {}, "name3": {}}
        self._create.valid_annots_made.emit.assert_called_once_with()

    def test_get_annots_mult_invalid(self):
        self._create.list.count = MagicMock(return_value=3)
        item = create_autospec(AnnotationItem)
        item.get_data = MagicMock(return_value=(True, "name", {}, ""))
        item2 = create_autospec(AnnotationItem)
        item2.get_data = MagicMock(return_value=(False, "name2", {}, "error"))
        item3 = create_autospec(AnnotationItem)
        item3.get_data = MagicMock(return_value=(True, "name3", {}, ""))
        self._create.list.item = MagicMock(side_effect=[item, item2, item3])
        self._create.valid_annots_made = MagicMock()
        self._create.new_annot_dict = {}
        self._create.error = create_autospec(QLabel)
        self._create.get_annots()

        item3.get_data.assert_not_called()
        self._create.error.setText.assert_called_once_with(" error")
        assert self._create.new_annot_dict is None
        self._create.valid_annots_made.emit.assert_not_called()

    def test_get_annots_mult_invalid_duplicate_names(self):
        self._create.list.count = MagicMock(return_value=3)
        item = create_autospec(AnnotationItem)
        item.get_data = MagicMock(return_value=(True, "name", {}, ""))
        item2 = create_autospec(AnnotationItem)
        item2.get_data = MagicMock(return_value=(True, "name2", {}, ""))
        item3 = create_autospec(AnnotationItem)
        item3.get_data = MagicMock(return_value=(False, "name2", {}, "error"))
        item3.highlight = MagicMock()
        item3.name = MagicMock()
        self._create.list.item = MagicMock(side_effect=[item, item2, item3])
        self._create.valid_annots_made = MagicMock()
        self._create.new_annot_dict = {}
        self._create.error = create_autospec(QLabel)
        self._create.get_annots()

        item3.highlight.assert_called_once_with(item3.name)
        self._create.error.setText.assert_called_once_with(" No duplicate names allowed.  error")
        assert self._create.new_annot_dict is None
        self._create.valid_annots_made.emit.assert_not_called()

    def test_get_annots_mult_valid_duplicate_names(self):
        self._create.list.count = MagicMock(return_value=3)
        item = create_autospec(AnnotationItem)
        item.get_data = MagicMock(return_value=(True, "name", {}, ""))
        item2 = create_autospec(AnnotationItem)
        item2.get_data = MagicMock(return_value=(True, "name2", {}, ""))
        item3 = create_autospec(AnnotationItem)
        item3.get_data = MagicMock(return_value=(True, "name2", {}, ""))
        item3.highlight = MagicMock()
        item3.name = MagicMock()
        self._create.list.item = MagicMock(side_effect=[item, item2, item3])
        self._create.valid_annots_made = MagicMock()
        self._create.new_annot_dict = {}
        self._create.error = create_autospec(QLabel)
        self._create.get_annots()

        item3.highlight.assert_called_once_with(item3.name)
        self._create.error.setText.assert_called_once_with(" No duplicate names allowed. ")
        assert self._create.new_annot_dict is None
        self._create.valid_annots_made.emit.assert_not_called()
