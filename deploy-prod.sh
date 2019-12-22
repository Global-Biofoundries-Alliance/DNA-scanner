#!/bin/bash
mkdir /srv/dnascanner/nginx -p
cp nginx-secure.conf /srv/dnascanner/nginx/

mkdir /srv/dnascanner/cert

docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build --force-recreate 
