# data-engineering-zoomcamp-docker-workshop

## Docker

### What is Docker?

* Docker containers are isolated environments that can be differernt and are seperate from our host machine
* Whatever happens on the container is isolated from the rest of the system
* When we create a Docker image 

### Working with Docker
 
`docker run -it` - run in interactive terminal

* Every time we run a new Docker container, we create a container from a Docker image
* The Docker image contains a complete snapshot of the OS and anything else required for the container
* The Docker container is stateless - if we kill the container and run it again, we return to the state defined in the image
* `docker run it python:3.13.11-slim` - "python" is the image name and "3.13.11-slim" is the tag
* The above opens in a python prompt, to open in a bash session instead of python we can overwrite the entry point using `docker run -it --entrypoint=bash python:3.13.11-slim`
* To kill your active containers run `docker rm $(docker ps -aq)`

### Persisting state/data

* Volumes are used to persist data for a Docker container
* We can make the data available on the host machine and then mount the volume to the Docker container as well
* `docker run -it --entrypoint=bash -v $(pwd)/test:/app/test python:3.13.11-slim` - in this command we map a volume from our host machine to the `~/app/test` directory in the Docker container 

## Virtual Environments

* Isolated environment that contains python and required dependencies for your project
* Not a true isolated environment like Docker
* `uv` package is a popular Python framework for managing virtual environments
* `uv init --python 3.13` can be used to create a virtual environment with a specific version of python
* `uv run python -V` - will create a python virtual environment called ".venv" and output the version of Python in the virtual env
* `uv add` can be used to add dependencies to the virtual environment

