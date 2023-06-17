#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Installing the latest version of poetry..."

pip install --upgrade pip

pip install poetry==1.5.0

rm poetry.lock

poetry lock

python -m poetry install

echo "Running 'collectstatic' command..."

python manage.py collectstatic --noinput

python manage.py makemigrations

python manage.py migrate

python manage.py createsuperuser

kyleseanli@gmail.com

kyleseanli@gmail.com

12345abcde

12345abcde