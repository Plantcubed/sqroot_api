#!/bin/bash
clear
echo "deleting database"
sudo rm db.sqlite3
echo "deleting migration files"
rm recipes/migrations/*
rm controls/migrations/*
rm actuators/migrations/*
rm sensors/migrations/*
rm direct/migrations/*
rm log/migrations/*
rm revisions/migrations/*
rm users/migrations/*
echo "create new migrations"
python3 manage.py makemigrations actuators
python3 manage.py makemigrations sensors
python3 manage.py makemigrations controls
python3 manage.py makemigrations recipes
python3 manage.py makemigrations direct
python3 manage.py makemigrations revisions
python3 manage.py makemigrations users
echo "changing db permissions"
sudo chmod 766 db.sqlite3
echo "migrate data"
python3 manage.py migrate
echo "add initial data"
python3 manage.py loaddata actuators/fixtures/initial_actuators.json
python3 manage.py loaddata sensors/fixtures/initial_sensors.json
python3 manage.py loaddata controls/fixtures/initial_control.json
python3 manage.py loaddata revisions/fixtures/initial_revisions.json
python3 manage.py loaddata recipes/fixtures/initial_recipes.json
python3 manage.py loaddata direct/fixtures/initial_direct.json
echo "restarting uWSGI"
python3 manage.py createsuperuser --username=admin --email=rich@rckco.com
sudo service uwsgi restart



