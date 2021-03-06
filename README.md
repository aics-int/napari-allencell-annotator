# napari-allencell-annotator

[![License BSD-3](https://img.shields.io/pypi/l/napari-allencell-annotator.svg?color=green)](https://github.com/bbridge0200/napari-allencell-annotator/raw/main/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/napari-allencell-annotator.svg?color=green)](https://pypi.org/project/napari-allencell-annotator)
[![Python Version](https://img.shields.io/pypi/pyversions/napari-allencell-annotator.svg?color=green)](https://python.org)
[![tests](https://github.com/bbridge0200/napari-allencell-annotator/workflows/tests/badge.svg)](https://github.com/bbridge0200/napari-allencell-annotator/actions)
[![codecov](https://codecov.io/gh/bbridge0200/napari-allencell-annotator/branch/main/graph/badge.svg)](https://codecov.io/gh/bbridge0200/napari-allencell-annotator)
[![napari hub](https://img.shields.io/endpoint?url=https://api.napari-hub.org/shields/napari-allencell-annotator)](https://napari-hub.org/plugins/napari-allencell-annotator)

A plugin to use with napari to annotate images and export .csv data

The Allen Cell Image Annotator plugin for napari provides an intuitive
graphical user interface to create, add, and export custom image annotations
on large data sets. The Allen Cell Image Annotator is a Python-based open source toolkit
developed at the Allen Institute for Cell Science. This toolkit allows 
users to easily upload, shuffle, and hide images. Users can create annotations (text, checkbox, drop-down, and spinbox) which 
are rendered into a custom user interface and can be applied to the uploaded images. Annotation data 
is exported into a .csv file. 

-   Supports the following image types:
    - `OME-TIFF`
    - `TIFF`
    - `CZI` 
    - `PNG` 
    -   `JPEG` 


----------------------------------

This [napari] plugin was generated with [Cookiecutter] using [@napari]'s [cookiecutter-napari-plugin] template.

<!--
Don't miss the full getting started guide to files up your new package:
https://github.com/napari/cookiecutter-napari-plugin#getting-started

and review the napari docs for plugin developers:
https://napari.org/plugins/index.html
-->

## Installation

You can install `napari-allencell-annotator` via [pip]:

    pip install napari-allencell-annotator



To install latest development version :

    pip install git+https://github.com/bbridge0200/napari-allencell-annotator.git

## Quick Start

In the current version, there are two parts in the plugin: **Image Uploader** and **Annotator**. The **Annotator** allows
users to create new or upload existing annotations and apply those annotations on the image set they create in the **Image Uploader**
section of the plugin. 


To install latest development version :

    pip install git+https://github.com/bbridge0200/napari-allencell-annotator.git


## Contributing

Contributions are very welcome. Tests can be run with [tox], please ensure
the coverage at least stays the same before you submit a pull request.

## License

Distributed under the terms of the [BSD-3] license,
"napari-allencell-annotator" is free and open source software

## Issues

If you encounter any problems, please [file an issue] along with a detailed description.

[napari]: https://github.com/napari/napari
[Cookiecutter]: https://github.com/audreyr/cookiecutter
[@napari]: https://github.com/napari
[MIT]: http://opensource.org/licenses/MIT
[BSD-3]: http://opensource.org/licenses/BSD-3-Clause
[GNU GPL v3.0]: http://www.gnu.org/licenses/gpl-3.0.txt
[GNU LGPL v3.0]: http://www.gnu.org/licenses/lgpl-3.0.txt
[Apache Software License 2.0]: http://www.apache.org/licenses/LICENSE-2.0
[Mozilla Public License 2.0]: https://www.mozilla.org/media/MPL/2.0/index.txt
[cookiecutter-napari-plugin]: https://github.com/napari/cookiecutter-napari-plugin

[file an issue]: https://github.com/bbridge0200/napari-allencell-annotator/issues

[napari]: https://github.com/napari/napari
[tox]: https://tox.readthedocs.io/en/latest/
[pip]: https://pypi.org/project/pip/
[PyPI]: https://pypi.org/
