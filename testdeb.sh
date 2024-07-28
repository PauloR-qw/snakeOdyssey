#!/bin/bash

sudo dpkg -r snakeodyssey
sudo dpkg-deb -b build/ dist/snakeOdyssey-v$1.deb
sudo dpkg -i dist/snakeOdyssey-v$1.deb