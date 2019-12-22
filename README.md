
# DNA-scanner
Web-application for rapid checking of multiple-DNA sequences for feasibility and time of DNA synthesis with multiple vendors.


# Installation
## First steps
Check out the project from the git repository.

First the configuration file *config.yml* in the directory *Backend* must be customized.

The application runs in docker-container, therefore docker and docker-compose must be installed.

## Development installation 
In the development environment, a database is made available within a container. This is not the case in the production environment, because this is not recommend for production use. 

Use the shell script *deploy.sh* to start the environment. The script will run docker-compose with the *docker-compose.yml* and it will be extended by the *docker-compose.override.yml*.
```
    chmod 775 deploy.sh
    sudo ./deploy.sh
```
By default the *./Backend/config.yml* has the database credentials as configured in the *docker-compose.override.yml*. 

By default the volumes of the database are bind to */srv/dnascanner/db/* to persist the data. You can make the saved information temporary by removing the volume shown below from the *docker-compose.override.yml*.

` - /srv/dnascanner/db:/var/lib/mysql`

### Force Rebuild
You can force an rebuild without caching using the skript *rebuild.sh*.
```
    chmod 775 rebuild.sh
    sudo ./rebuild.sh
```
## Production installation
The production environment requires a seperate database. You can configure it in *./Backend/config.yml*. In the production environment the database must be separate, because it is not recommend to run a database inside of a container for production use.

Certificates for https are required for the productive environment. The certificates must be placed in `/srv/dnascanner/cert/`. In the following code we create the directory and generate self-signed certificates. Alternatively you can put your own certificates there. The certificates are configured in the file *nginx-secure.conf*.
```
    mkdir /srv/dnascanner/cert -p
    sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /srv/dnascanner/cert/cert.key -out /srv/dnascanner/cert/cert.crt
```
The *nginx-secure.conf* will be used as default. You can also place an specific nginx configuration file in **/srv/dnascanner/nginx/**.

Use the shell script *deploy-prod.sh* to start the environment. The script will run docker-compose with the *docker-compose.yml* and it will be extended by the *docker-compose.prod.yml*.
```
    chmod 775 deploy-prod.sh
    sudo ./deploy-prod.sh
```

 


