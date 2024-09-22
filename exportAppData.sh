#!/bin/sh

EXPATH=emedictdata.json.gz

# accept optional argument to overwrite expath

#Get if condition to work
if [ -d "app/$EXPATH" ]; then
    read -p "$EXPATH apready exists. Overwrite? [y/N] " confirm
        case "$confirm" in 
            [yY][eE][sS]|[yY])
                docker-compose exec web python manage.py dumpdata emedict -o $EXPATH
                ;;
            *)
                exit 1
                ;;
        esac
else   
    docker-compose exec web python manage.py dumpdata emedict -o $EXPATH
fi
