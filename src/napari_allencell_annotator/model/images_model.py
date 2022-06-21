from aicsimageio import AICSImage
import os
import numpy

SUPPORTED_FILE_TYPES = ({".jpeg", ".png", ".jpg", ".czi", ".tiff"});


def is_supported(file_name: str) -> bool:
    """
    Check if the provided file name is a supported file.

    This function checks if the file name extension is in
    the supported file types set.

    Parameters
    ----------
    file_name : str
        Name of the file to check.

    Returns
    -------
    bool
        True if the file is supported.
    """
    _, extension = os.path.splitext(file_name)
    if extension in SUPPORTED_FILE_TYPES:
        return True
    else:
        return False


def aicsimageio_convert(file_name: str) -> numpy.uint8:
    """
    Convert the img provided to an AICSImage and return the numpy array.

    Parameters
    ----------
    file_name : str
        Name of the file to convert.

    Returns
    -------
    numpy.uint8
        Numpy array data from AICSImage conversion.
    """
    return AICSImage(file_name).data
