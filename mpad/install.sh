#!/bin/env bash

pyinstaller --add-data ./resources:resources --add-data ./client/build/:client/build app.py --onefile --paths 'venv/lib/python3.10/site-packages'
sudo cp ./dist/app /usr/bin/mpad
