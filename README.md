# napari-allencell-annotator

[![License BSD-3](https://img.shields.io/pypi/l/napari-allencell-annotator.svg?color=green)](https://github.com/bbridge0200/napari-allencell-annotator/raw/main/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/napari-allencell-annotator.svg?color=green)](https://pypi.org/project/napari-allencell-annotator)
[![Python Version](https://img.shields.io/pypi/pyversions/napari-allencell-annotator.svg?color=green)](https://python.org)
[![tests](https://github.com/bbridge0200/napari-allencell-annotator/workflows/tests/badge.svg)](https://github.com/bbridge0200/napari-allencell-annotator/actions)
[![codecov](https://codecov.io/gh/bbridge0200/napari-allencell-annotator/branch/main/graph/badge.svg)](https://codecov.io/gh/bbridge0200/napari-allencell-annotator)
[![napari hub](https://img.shields.io/endpoint?url=https://api.napari-hub.org/shields/napari-allencell-annotator)](https://napari-hub.org/plugins/napari-allencell-annotator)

A plugin that enables image annotation/scoring and writes annotations to a .csv file. 
Plugin provided by the Allen Institute for Cell Science.

The Allen Cell Image Annotator plugin for napari provides an intuitive
graphical user interface to create annotation templates, annotate large 
image sets using these templates, and save image annotations to a csv file. 
The Allen Cell Image Annotator is a Python-based open source toolkit 
developed at the Allen Institute for Cell Science for both blind, unbiased and un-blind 
microscope image annotating. This toolkit supports easy image set selection
from a file finder and creation of annotation templates (text, checkbox, drop-down, spinbox, and point).
With napari's multi-dimensional image viewing capabilities, the plugin seamlessly allows users to
view each image and write annotations into the custom template.
Annotation templates can be written to a json file for sharing or re-using. After annotating,
the annotation template, image file list, and the annotation values 
are conveniently saved to csv file, which can be re-opened for further annotating. 

-   Supports the following image types:
    - `OME-TIFF`
    - `TIFF`
    - `CZI` 
    - `PNG` 
    - `JPEG`
    - `OME-ZARR`


----------------------------------

This [napari] plugin was generated with [Cookiecutter] using [@napari]'s [cookiecutter-napari-plugin] template.

<!--
Don't miss the full getting started guide to files up your new package:
https://github.com/napari/cookiecutter-napari-plugin#getting-started

and review the napari docs for plugin developers:
https://napari.org/plugins/index.html
-->

## Installation using Command Line
### 1. Install the plugin
- Create and activate a virtual environment. We recommend using conda and python 3.10.
  - To create and activate a conda virtual environment, run the following commands one line at a time.

      ```
      conda create -n napari_annotator python=3.10
      conda activate napari_annotator
      ```
    
  - To create and activate a venv virtual environment, run the following commands.
    - Windows
        ```
        python -m venv venv
        venv\Scripts\activate
        ```
    - MacOS/Unix
        ```
        python -m venv venv
        source venv/bin/activate
        ```

- Install Napari and the annotator plugin by running
  ```
  python -m pip install "napari[all]"
  python -m pip install napari-allencell-annotator
  ```

- Open Napari by running ```napari``` and verify that **napari-allencell-annotator** is listed in the **Plugins** tab.
- **Not working?** Try using conda forge instead of pip. 
  - Ex: ```conda install -c conda-forge napari instead of python -m pip install "napari[all]"```


### 2. Launch the Plugin

- If **napari-allencell-annotator** is listed in **Plugins**, click it to launch. 
- If it is not listed 
  - **Install/Uninstall Plugins** ⇨ check the box next to **napari-allencell-annotator** ⇨ **close** ⇨ **Plugins** ⇨ **napari-allencell-annotator** .


## Installation from Napari Hub
If you have previously installed Napari on your machine, you can follow these steps to install the plugin from Napari Hub.

### 1. Install the Plugin
- Open Napari
- Go to **Plugins** ⇨ **Install/Uninstall Plugins...**
- Find **napari-allencell-annotator** in **Available Plugins**
- Click **Install**
- Close the window after the installation finishes

### 2. Launch the Plugin
- Click **Plugins** ⇨ **napari-allencell-annotator**
  - You might have to restart Napari for the annotator to appear in the plugin list.
  - If you still can't see the plugin, go to **Install/Uninstall Plugins** ⇨ check the box next to **napari-allencell-annotator**.

## Quick Start

1. Open napari
2. Start the plugin 
   - Open napari, go to **Plugins** ⇨ **napari-allencell-annotator**.
3. Create or import annotations and add images to annotate.

For more detailed usage instructions, check out this [document](napari_allencell_annotator/assets/AnnotatorInstructions.pdf) 
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
