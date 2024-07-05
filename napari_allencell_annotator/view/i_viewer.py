from abc import ABC, abstractmethod
import numpy as np
from napari.layers import Layer
from typing import List


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