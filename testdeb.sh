#!/bin/bash

# Antes compilar código Python com:
# python3.10 setup.py build

sudo dpkg -r snakeodyssey
sudo dpkg-deb -b build/ dist/snakeOdyssey-v$1.deb
sudo dpkg -i dist/snakeOdyssey-v$1.deb