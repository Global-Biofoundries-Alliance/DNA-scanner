#!/bin/bash

echo "Removing old container"
docker container stop dnafrontend
docker container rm dnafrontend
docker container stop dnabackend
docker container rm dnabackend
docker container stop review
docker container rm review

echo "Recreate Container"
docker-compose up -d --build
