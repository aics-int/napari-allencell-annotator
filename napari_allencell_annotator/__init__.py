from napari_allencell_annotator.controller.main_controller import MainController

try:
    from ._version import version as __version__
except ImportError:
    __version__ = "unknown"

# Do not edit this string manually, always use bumpversion
# Details in CONTRIBUTING.md
__version__ = "0.0.2"


def make_widget():
    return MainController
