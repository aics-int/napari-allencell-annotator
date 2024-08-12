import napari
from napari.layers import Points

from napari_allencell_annotator.view.viewer import Viewer, PointsLayerMode
import numpy as np
import pytest
from napari.utils import Colormap


@pytest.fixture
def viewer(make_napari_viewer: napari.Viewer) -> Viewer:
    return Viewer(make_napari_viewer())


def test_get_all_points_layer(viewer: Viewer) -> None:
    # ARRANGE
    viewer.add_image(np.zeros(shape=(2, 2)))
    test_points_layer1: Points = viewer.create_points_layer("test1", True)
    test_points_layer2: Points = viewer.create_points_layer("test2", True)

    # ACT
    all_points_layer: list[Points] = viewer.get_all_points_layers()

    # ASSERT
    assert len(all_points_layer) == 2
    assert test_points_layer1 in all_points_layer
    assert test_points_layer2 in all_points_layer


def test_add_image(viewer: Viewer) -> None:
    # ARRANGE
    test_image = np.zeros(shape=(2, 2))
    # ACT
    viewer.add_image(test_image)

    # ASSERT
    assert len(viewer.get_layers()) == 1
    np.testing.assert_array_equal(viewer.get_layers()[0].data, test_image)


def test_create_points_layer(viewer: Viewer) -> None:
    # ARRANGE
    test_points_data = np.zeros(shape=(1, 2))

    # ACT
    test_points_layer: Points = viewer.create_points_layer("test", True, test_points_data)

    # ASSERT
    assert test_points_layer in viewer.get_all_points_layers()
    assert len(viewer.get_all_points_layers()) == 1
    assert test_points_layer.name == "test"
    np.testing.assert_array_equal(test_points_layer.face_color[0], Colormap("lime").colors[0])
    assert test_points_layer.visible
    np.testing.assert_array_equal(test_points_layer.data, test_points_data)
    assert test_points_layer.ndim == 2


def test_set_points_layer_mode(viewer: Viewer) -> None:
    # ARRANGE
    test_points_layer: Points = viewer.create_points_layer("test", True)

    # ACT
    viewer.set_points_layer_mode(test_points_layer, PointsLayerMode.ADD)

    # ASSERT
    assert test_points_layer.mode == PointsLayerMode.ADD.value


def test_get_selected_points(viewer: Viewer) -> None:
    # ARRANGE
    test_points_layer: Points = viewer.create_points_layer("test", True, np.array([np.zeros(2), np.ones(2)]))

    # ACT
    selected_points: list[tuple] = viewer.get_selected_points(test_points_layer)

    # ASSERT
    assert selected_points == [(0, 0), (1, 1)]


def test_get_all_point_annotations(viewer: Viewer) -> None:
    # ARRANGE
    test_points_layer1: Points = viewer.create_points_layer("test1", True, np.zeros(shape=(1, 2)))
    test_points_layer2: Points = viewer.create_points_layer("test2", True, np.ones(shape=(1, 2)))

    # ACT
    all_point_annotations: dict[str, list[tuple]] = viewer.get_all_point_annotations()

    # ASSERT
    assert all_point_annotations == {"test1": [(0, 0)], "test2": [(1, 1)]}
