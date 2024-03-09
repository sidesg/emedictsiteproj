DIRECTORY=.venv

if [ ! -d "$DIRECTORY" ]; then
    python3 -m virtualenv .venv
else   
    echo "$DIRECTORY exists"
fi

source .venv/bin/activate
pip install -r requirements.txt

cd emedictsite
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata emedictdata.json.gz --app emedict