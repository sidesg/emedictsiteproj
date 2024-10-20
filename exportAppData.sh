#!/bin/sh

EXPATH=emedictdata.json

# accept optional argument to overwrite expath

cd app
#Get if condition to work
if [ -d "$EXPATH" ]; then
    read -p "$EXPATH apready exists. Overwrite? [y/N] " confirm
        case "$confirm" in 
            [yY][eE][sS]|[yY])
                docker-compose -f docker-compose.prod.yml exec web python manage.py dumpdata emedict > $EXPATH
                gzip $EXPATH
                ;;
            *)
                exit 1
                ;;
        esac
else   
    docker-compose -f docker-compose.prod.yml exec web python manage.py dumpdata emedict > $EXPATH 
    gzip $EXPATH
fi
