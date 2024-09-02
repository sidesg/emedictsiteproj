#!/bin/sh

# migrate and load data
docker-compose -f docker-compose.prod.yml exec web python manage.py flush
docker-compose -f docker-compose.prod.yml exec web python manage.py makemigrations emedict
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate
docker-compose -f docker-compose.prod.yml exec web python manage.py loaddata emedictdata.json.gz --app emedict