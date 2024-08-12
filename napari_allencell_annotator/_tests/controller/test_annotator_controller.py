import pytest
from napari_allencell_annotator._tests.fakes.fake_viewer import FakeViewer
from napari_allencell_annotator.view.annotator_view import AnnotatorViewMode

from napari_allencell_annotator.view.i_viewer import IViewer

from napari_allencell_annotator.model.annotation_model import AnnotatorModel

from napari_allencell_annotator.controller.annotator_controller import AnnotatorController


@pytest.fixture
def annotator_model(qtbot) -> AnnotatorModel:
    return AnnotatorModel()


@pytest.fixture
def viewer(qtbot) -> IViewer:
    return FakeViewer()


@pytest.fixture
def annotator_controller(qtbot, annotator_model: AnnotatorModel, viewer: IViewer) -> AnnotatorController:
    return AnnotatorController(annotator_model, viewer)


def test_start_annotating(annotator_controller: AnnotatorController) -> None:
    # ACT
    annotator_controller.start_annotating()

    # ASSERT
    assert annotator_controller.view.mode == AnnotatorViewMode.ANNOTATE
