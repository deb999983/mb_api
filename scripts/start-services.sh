#!/bin/bash

echo "Starting services"
docker-compose up -d

echo "Waiting for mysql to be ready"
docker exec -i -t mb_api_container ./home/app/mb_api/scripts/wait-for-mysql.sh "database"

echo "Collecting static files"
docker exec -i -t mb_api_container python3 /home/app/mb_api/manage.py collectstatic

echo "Running migrations"
docker exec -i -t mb_api_container python3 /home/app/mb_api/manage.py migrate