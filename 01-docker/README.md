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

## Dockerizing Pipelines

* We can run our pipeline in a Docker container by creating a Docker image for it
* `docker build -t test:pandas .` - builds image with base image name of "test" and tag "pandas. `-t` flag is for the tag and `.` specifies that we want to build it from our current directory
* `docker run -it --entrypoint=bash --rm test:pandas` - `-rm` flag cleans state once container is killed
* Once we specify an entrypoint in the Docker image we can run a container and pass an argument using ` docker run -it --rm test:pandas 12`

## Postgres Docker

* We can run Postgres easily locally by using a Docker image
```bash 
docker run -it --rm \
  # Environment variables to pass to container
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  # Volume mapping of internal Docker volumne to persist data
  -v ny_taxi_postgres_data:/var/lib/postgresql \
  # Port mapping localhost >> container
  -p 5432:5432 \
  postgres:18
```

* `uv add --dev pgcli` adds pgcli to our dev dependencies in our pyproject.toml, which means our Docker image wouldn't install it when it runs `RUN uv sync --locked`

## Data Ingestion

* Goal is to put NY Taxi data inside Postgres
* csv is schemaless, whereas Parquet contains a schema so you know the types on read
* `uv run jupyter nbconvert --to=script notebook.ipynb` used to convert jupyter notebook into a Python file
* Following our changes, we can run the script using `uv run python ingest_data.py`
* The script can be paramaterised using the click library. Once paramaterised use `uv run python ingest_data.py --help` to see the options and their sescriptions

## Dockerizing Data Ingestion

* When we dockerize our ingestion script and run it as a container, it will try to communicate with the Postgres container using its own localhost. For it to actually to communicate with the Postgres container, we need to create a Docker network.
* We can do this by running `docker network create pg-network` so that the containers can see eachother
* Once we do this we need to specify the network when we run each container, like so:
```bash
docker run -it --rm \
  --network=pg-network \
  --name pgdatabase \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql \
  -p 5432:5432 \
  postgres:18

# Note how the host is now the name of the Postgres container instead of localhost
docker run -it --rm \
    --network=pg-network \
    taxi_ingest:v001 \
    --pg-user=root \
    --pg-pass=root \
    --pg-host=pgdatabase \
    --pg-port=5432 \
    --pg-db=ny_taxi \
    --target-table=yellow_taxi_trips_2021_1 \
    --chunksize=100000
```

## Docker Compose

* Our docker-compose.yaml file will contain all the information required for the containers we want to run
* When we run `docker-compose up` we create new volumes so our data will no longer be present, so we need to run the ingestion scrip again