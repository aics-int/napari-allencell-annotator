from abc import ABC, abstractmethod
import numpy as np


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
