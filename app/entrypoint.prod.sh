#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

# python manage.py flush
# python manage.py makemigrations emedict
# python manage.py migrate
# python manage.py loaddata emedictdata.json.gz --app emedict
# python manage.py collectstatic

exec "$@"
