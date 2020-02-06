#!/bin/bash

echo "Starting services"
docker-compose up -d

echo "Collecting static files"
docker exec -i -t mb_api_container python3 /home/app/mb_api/manage.py collectstatic

echo "Running migrations"
docker exec -i -t mb_api_container python3 /home/app/mb_api/manage.py migrate