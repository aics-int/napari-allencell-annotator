from napari_allencell_annotator.widgets.list_item import ListItem


class TestListItem:
    def test_file_path(self):
        expected_path = "path.txt"
        widget = ListItem(expected_path, None)
        assert widget.file_path == expected_path

    def test_eq(self):
        path = "path.txt"
        widget = ListItem(path, None)
        widget_2 = ListItem(path, None)
        assert widget == widget_2
        assert widget == widget
        widget_2.file_path = "path2.txt"
        assert widget != widget_2



    def test_hash(self):
        expected_path = "path.txt"
        widget = ListItem(expected_path, None)
        expected_path_2 = "path"
        widget_2 = ListItem(expected_path_2, None)
        wid_set = set()
        wid_set.add(widget)
        wid_set.add(widget_2)
        assert len(wid_set) == 2
        widget_3 = ListItem(expected_path, None)
        wid_set.add(widget_3)
        assert len(wid_set) == 2
