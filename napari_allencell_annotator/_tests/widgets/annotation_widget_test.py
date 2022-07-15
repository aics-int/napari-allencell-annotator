from unittest import mock
from unittest.mock import MagicMock, create_autospec

from napari_allencell_annotator.widgets.annotation_widget import AnnotationWidget
from napari_allencell_annotator.widgets.annotation_item import AnnotationItem


class TestAnnotationWidget:
    def setup_method(self):
        with mock.patch.object(AnnotationWidget, "__init__", lambda x: None):
            self._widget = AnnotationWidget()

    def test_clear_all(self):
        self._widget.clear = MagicMock()
        self._widget.clear_all()
        self._widget.clear.assert_called_once_with()

    def test_remove_item(self):
        self._widget.takeItem = MagicMock()
        self._widget.row = MagicMock(return_value=5)
        self._widget.remove_item("item")
        self._widget.takeItem.assert_called_once_with(5)
