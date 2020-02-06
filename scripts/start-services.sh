#!/bin/bash

echo "Starting services"
docker-compose up -d

echo "Collecting static files"
docker exec -i -t webapp_container python3 /home/app/webapp/manage.py collectstatic

echo "Running migrations"
docker exec -i -t webapp_container python3 /home/app/webapp/manage.py migrate