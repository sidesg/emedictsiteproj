#!/bin/bash

DIRECTORY=.venv

if [ -f "db.sqlite3" ]; then
    echo "Please delete your database file ('db.sqlite3') before making a fresh installation." && exit 1
fi

if [ ! -d "$DIRECTORY" ]; then
    python3 -m virtualenv .venv
else   
    echo "$DIRECTORY exists. No new virtual environment will be created."
fi

source $DIRECTORY/bin/activate
pip install -r requirements.txt

read -p "This script will delete the contents of emedict/migrations. Continue? (Y/N): " confirm \
    && [[ $confirm == [yY] || $confirm == [yY][eE][sS] ]] || exit 1

sudo rm -r emedict/migrations
mkdir emedict/migrations
python manage.py makemigrations emedict
python manage.py migrate
python manage.py loaddata emedictdata.json.gz --app emedict

read -p "Create superuser for site? (Y/N): " confirm \
    && [[ $confirm == [yY] || $confirm == [yY][eE][sS] ]] || exit 1
echo Loading database data
python manage.py createsuperuser
