# Python3 + Flask API 

# 
Simple syntax, 
flexible use of databases with native SQL queries.

## Dev environment setup

The developer workstation must have:
* Python 3 (<https://www.python.org/>)
* PyPI (<https://pypi.python.org/pypi>)
* Python libraries described in the file [requirements.txt](requirements.txt)
* Connectivity with a intance of SIGRH database
* Docker CE (optional: it is required only to run the app in a Docker container)

## Running with Docker

```shell
# command to build the image using the Dockerfile
docker build -t IMAGE_NAME .
# command to create and run the a container instance 
docker run -d --name CONTAINER_NAME -p 8000:5000 IMAGE_NAME
# command to test the API
curl http://localhost:8000/api/servidores 
```
