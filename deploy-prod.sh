#!/bin/bash

echo "Copy nginx configuration to /srv/dnascanner/nginx/ "
mkdir /srv/dnascanner/nginx -p
cp nginx-secure.conf /srv/dnascanner/nginx/

echo "Create directory /srv/dnascanner/cert/ for certificates"
mkdir /srv/dnascanner/cert

echo "Deleting old container before recreate"
docker container stop dnafrontend
docker container rm dnafrontend
docker container stop dnabackend
docker container rm dnabackend

echo "Start container"
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build --force-recreate 
