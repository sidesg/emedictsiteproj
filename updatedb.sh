#!/bin/sh

# migrate and load data
docker-compose exec web python manage.py flush
docker-compose exec web python manage.py makemigrations emedict
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py loaddata emedictdata.json.gz --app emedict
docker-compose exec web python manage.py search_index --rebuild

docker-compose exec web python manage.py createsuperuser