from typing import List

import numpy as np
from napari.layers import Layer

from napari_allencell_annotator.view.i_viewer import IViewer


class FakeViewer(IViewer):
    def __init__(self):
        super().__init__()

        self._layers = []
        self._alerts = []

    def add_image(self, image: np.ndarray) -> None:
        self._layers.append(image)

    def clear_layers(self) -> None:
        self._layers.clear()

    def alert(self, alert_msg: str) -> None:
        self._alerts.append(alert_msg)

    def get_layers(self) -> List[Layer]:
        return self._layers

    def get_alerts(self) -> List[str]:
        return self._alerts
