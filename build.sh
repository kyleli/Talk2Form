#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Installing the latest version of poetry..."

pip install --upgrade pip

pip install poetry==1.5.0

python -m poetry install

echo "Running 'collectstatic' command..."

python manage.py collectstatic --noinput

echo "Making Migrations"

python3 manage.py makemigrations

echo "Migrating"

python3 manage.py migrate