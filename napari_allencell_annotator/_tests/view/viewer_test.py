from napari.layers import Points

from napari_allencell_annotator.view.viewer import Viewer, PointsLayerMode
import napari
import numpy as np
import pytest

@pytest.fixture
def viewer() -> Viewer:
    return Viewer(napari.Viewer(show=False))


def test_set_points_layer_mode(viewer: Viewer) -> None:
    # ARRANGE
    points_layer: Points = viewer.viewer.add_points(None)

    # ACT
    viewer.set_points_layer_mode(points_layer, PointsLayerMode.ADD)

    # ASSERT
    assert points_layer.mode == PointsLayerMode.ADD.value


def test_get_selected_points(viewer: Viewer) -> None:
    # ARRANGE
    points: np.array = np.array([[1, 2], [3, 4]])
    points_layer: Points = viewer.viewer.add_points(points)

    # ACT
    selected_points: list[tuple] = viewer.get_selected_points(points_layer)

    # ASSERT
    assert selected_points == [(1, 2), (3, 4)]


def test_get_all_point_annotations(viewer: Viewer) -> None:
    # ARRANGE
    points1: np.array = np.array([[1, 2], [3, 4]])
    points2: np.array = np.array([[5, 6], [7, 8]])

    viewer.viewer.add_points(points1, name="test1")
    viewer.viewer.add_points(points2, name="test2")

    # ACT
    all_point_annotations: dict[str, list[tuple]] = viewer.get_all_point_annotations()

    # ASSERT
    assert all_point_annotations == {"test1": [(1, 2), (3, 4)], "test2": [(5, 6), (7, 8)]}
