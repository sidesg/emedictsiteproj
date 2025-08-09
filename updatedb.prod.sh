#!/bin/sh

# migrate and load data
docker-compose -f docker-compose.prod.yml exec web python manage.py flush
docker-compose -f docker-compose.prod.yml exec web python manage.py makemigrations emedict
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate
echo "Loading data (might take a while)"
docker-compose -f docker-compose.prod.yml exec web python manage.py loaddata emedictdata.json.gz --app emedict
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic
docker-compose -f docker-compose.prod.yml exec web python manage.py search_index --rebuild

docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser
