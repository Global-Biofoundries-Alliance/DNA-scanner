# DNA-scanner
Python library for rapid checking of multiple-DNA sequences for feasibility and time of DNA synthesis with multiple vendors


# Installation
## First steps
Check out the project from the git repository.

At first you have to configure the *config.yml* file in the *Backend* directory. 

The App uses Docker  and Docker-compose for deployment. You have to install both.
## Development installation 
For Developlment use there is included an Docker-Container for the Database. Production environment won't include the database, because this is not recommend in production use. 

To start the environment use the Shell-Script *deploy.sh* to run the docker-compose. Maybe you need to make the script executable and run it as sudo.
The Script will run docker-compose with the *docker-compose.yml* and it will be extended by the *docker-compose.override.yml*.

By default the *./Backend/config.yml* has the database credentials as configured in the *docker-compose.override.yml*. 

By default the volumes of the database are bind to */srv/dnascanner/db/* to persist the data. You can make the saved information temporary by  removing the volume shown below from the *docker-compose.override.yml*.

` - /srv/dnascanner/db:/var/lib/mysql`

## Production installation
The production environment a seperate database is needed and configured in *./Backend/config.yml*, because for production use it is not recommend to run a database inside of a container.

To start the environment use the Shell-Script *deploy-prod.sh* to run the docker-compose. Maybe you need to make the script executable and run it as sudo.
The Script will run docker-compose with the *docker-compose.yml* and it will be extended by the *docker-compose.prod.yml*.
 

