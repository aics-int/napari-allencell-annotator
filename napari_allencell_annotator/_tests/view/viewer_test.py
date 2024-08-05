from napari.layers import Points

from napari_allencell_annotator.view.viewer import Viewer, PointsLayerMode
import napari
import numpy as np
import pytest
from napari.utils import Colormap


@pytest.fixture
def viewer() -> Viewer:
    return Viewer(napari.Viewer(show=False))


def test_all_points_layer(viewer: Viewer) -> None:
    # ARRANGE
    viewer.viewer.add_shapes()
    test_points_layer1: Points = viewer.create_points_layer("test1", "blue", True, 2)
    test_points_layer2: Points = viewer.create_points_layer("test2", "blue", True, 2)

    # ACT
    all_points_layer: list[Points] = viewer.get_all_points_layers()

    # ASSERT
    assert len(all_points_layer) == 2
    assert test_points_layer1 in all_points_layer
    assert test_points_layer2 in all_points_layer


def test_create_points_layer(viewer: Viewer) -> None:
    # ACT
    test_points_layer: Points = viewer.create_points_layer("test", "blue", True, 2)

    # ASSERT
    assert test_points_layer in viewer.get_all_points_layers()
    assert len(viewer.get_all_points_layers()) == 1
    assert test_points_layer.name == "test"
    assert test_points_layer.visible
    assert test_points_layer.ndim == 2
    assert len(test_points_layer.data) == 0
    assert test_points_layer.mode == PointsLayerMode.ADD.value


def test_create_points_layer_color(viewer: Viewer) -> None:
    # ACT
    test_points_layer: Points = viewer.create_points_layer("test", "blue", True, 2)
    test_points_layer.data = np.array([[1, 1]])

    # ASSERT
    assert np.array_equal(test_points_layer.face_color[0], Colormap("blue").colors[0])


def test_set_points_layer_mode(viewer: Viewer) -> None:
    # ARRANGE
    test_points_layer: Points = viewer.create_points_layer("test", "blue", True, 2)

    # ACT
    viewer.set_points_layer_mode(test_points_layer, PointsLayerMode.ADD)

    # ASSERT
    assert test_points_layer.mode == PointsLayerMode.ADD.value


def test_get_selected_points(viewer: Viewer) -> None:
    # ARRANGE
    test_points_layer: Points = viewer.create_points_layer("test", "blue", True, 2)
    points: np.array = np.array([[1, 2], [3, 4]])
    test_points_layer.data = points

    # ACT
    selected_points: list[tuple] = viewer.get_selected_points(test_points_layer)

    # ASSERT
    assert selected_points == [(1, 2), (3, 4)]


def test_get_all_point_annotations(viewer: Viewer) -> None:
    # ARRANGE
    test_points_layer1: Points = viewer.create_points_layer("test1", "blue", True, 2)
    test_points_layer2: Points = viewer.create_points_layer("test2", "blue", True, 2)

    points1: np.array = np.array([[1, 2], [3, 4]])
    points2: np.array = np.array([[5, 6], [7, 8]])

    test_points_layer1.data = points1
    test_points_layer2.data = points2

    # ACT
    all_point_annotations: dict[str, list[tuple]] = viewer.get_all_point_annotations()

    # ASSERT
    assert all_point_annotations == {"test1": [(1, 2), (3, 4)], "test2": [(5, 6), (7, 8)]}
