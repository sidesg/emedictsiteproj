#!/bin/bash
# Activate virtualenv and run Django server

DIRECTORY=.venv

source $DIRECTORY/bin/activate

python manage.py runserver