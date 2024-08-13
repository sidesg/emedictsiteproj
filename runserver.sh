#!/bin/bash
# Activate virtualenv and run Django server

DIRECTORY=.venv

activate () {
  . $DIRECTORY/bin/activate
}

activate
python manage.py runserver
