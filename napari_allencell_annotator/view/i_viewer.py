from abc import ABC, abstractmethod
import numpy as np
from napari.layers import Layer, Points
from typing import List, Tuple


class IViewer(ABC):
    def __init__(self):
        """Base abstract class for the viewer"""
        super().__init__()

    @abstractmethod
    def add_image(self, image: np.ndarray) -> None:
        pass

    @abstractmethod
    def clear_layers(self) -> None:
        pass

    @abstractmethod
    def alert(self, alert_msg: str) -> None:
        pass

    @abstractmethod
    def get_layers(self) -> List[Layer]:
        pass

    @abstractmethod
    def _get_all_points_layers(self) -> List[Points]:
        pass

    @abstractmethod
    def create_points_layer(self, name: str, color: str, visible: bool, ndim: int) -> Points:
        pass

    @abstractmethod
    def get_selected_points(self, point_layer: Points) -> List[Tuple]:
        pass

    @abstractmethod
    def get_all_point_annotations(self) -> dict[str, list[tuple]]:
        pass
