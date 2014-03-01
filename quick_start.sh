#!/bin/bash

echo "Install required packages..."
#pip install -U setuptools
pip install -r requirements.txt

echo "Install FreeROI..."
python setup.py install
