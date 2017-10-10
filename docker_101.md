# Use Docker Container to start and stop groups of hosts

`docker-compose up`

`docker-compose down`

Configuration is in `docker-compose.yml`.


# Working with Docker directly

## See what's running

`docker ps -a`

## Get a shell on a running container

`docker-exec -it alpha /bin/bash`

## Get rid of containers
### Kill a running container

`docker kill alpha`

### Remove a killed container so that you can re-use its name

`docker rm alpha`

## All in one fell swoop

`docker rm $(docker kill $(docker ps -aq))`
