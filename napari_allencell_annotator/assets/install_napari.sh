#!/bin/bash
# script to install napari as well as napari-allencell-annotator
conda create -n napari_annotator python=3.9 anaconda
conda activate napari_annotator

# if no python 3.9 install it and activate it
python -m pip install --upgrade pip
python -m pip install "napari[all]"
python -m pip install napari-allencell-annotator
napari
