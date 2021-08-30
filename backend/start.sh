#!/bin/sh
pip install -r requirements.txt

python manage.py collectstatic --noinput
python manage.py makemigrations recipes
python manage.py makemigrations users
python manage.py migrate
python manage.py loaddata fixtures.json

gunicorn api_foodgram.wsgi:application --bind 0.0.0.0
