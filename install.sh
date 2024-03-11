#!/bin/bash

DIRECTORY=.venv

if [ ! -d "$DIRECTORY" ]; then
    python3 -m virtualenv .venv
else   
    echo "$DIRECTORY exists"
fi

source $DIRECTORY/bin/activate
pip install -r requirements.txt

read -p "This script will delete the contents of emedict/migrations. Continue? (Y/N): " confirm 
    && [[ $confirm == [yY] || $confirm == [yY][eE][sS] ]] || exit 1

cd emedictsite
sudo rm -r emedict/migrations
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata emedictdata.json.gz --app emedict

python manage.py createsuperuser