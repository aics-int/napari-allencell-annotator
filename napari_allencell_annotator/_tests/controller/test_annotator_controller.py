from napari_allencell_annotator._tests.fakes.fake_viewer import FakeViewer
from napari_allencell_annotator.view.annotator_view import AnnotatorViewMode
from napari_allencell_annotator.controller.annotator_controller import AnnotatorController
from napari_allencell_annotator.view.main_view import MainView

import pytest
from pytestqt import qtbot


def test_start_annotating(qtbot) -> None:
    # ARRANGE
    main_view_simulated: MainView = MainView(FakeViewer())
    qtbot.add_widget(main_view_simulated)
    annotator_controller: AnnotatorController = main_view_simulated.annots

    # ACT
    annotator_controller.start_annotating()

    # ASSERT
    assert annotator_controller.view.mode == AnnotatorViewMode.ANNOTATE
