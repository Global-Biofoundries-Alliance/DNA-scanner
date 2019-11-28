# Backend

The Backend is written in Python. It container the Pinger communication with the vendor APIs. The Controller provides the functions to the Frontend.


# Installation

Check out the project from the git repository. 
At first you have to configure the config.yml file.

Next you can build the Docker-container for the backend by running the following command:

    docker build -t dna-backend /<path>/<to>/<project>/Backend

The default port for the backend ist :8080. With the following command you can run the container for example on port :80 instead of :8080.

    sudo docker run -p 80:8080 dna-backend
