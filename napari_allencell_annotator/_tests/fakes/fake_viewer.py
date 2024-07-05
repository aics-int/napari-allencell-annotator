import numpy as np

from napari_allencell_annotator.view.i_viewer import IViewer


class FakeViewer(IViewer):
    def __init__(self):
        super().__init__()

    def add_image(self, image: np.ndarray) -> None:
        pass

    def clear_layers(self) -> None:
        pass

    def alert(self, alert_msg: str) -> None:
        pass
