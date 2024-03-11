#!/bin/bash

DIRECTORY=.venv

source $DIRECTORY/bin/activate
cd emedictsite

python manage.py runserver