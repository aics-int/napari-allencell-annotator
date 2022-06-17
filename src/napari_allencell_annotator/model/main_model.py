from aicsimageio import AICSImage, exceptions
import os

SUPPORTED_FILE_TYPES = ({".jpeg",".png",".jpg", ".czi", ".tiff"});


def get_file_types():
    return SUPPORTED_FILE_TYPES

def is_supported(file):
    _, extension = os.path.splitext(file)
    if extension in SUPPORTED_FILE_TYPES:
        return True
    else:
        return False

def aicsimageio_convert(img):
    return AICSImage(img).data
