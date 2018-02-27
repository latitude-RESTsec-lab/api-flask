# Python3 + Flask

Experimental API to handle SIGRH data using the Python Flask framework.


## Dev environment setup

The developer workstation must have:
* Python 3 (<https://www.python.org/>)
* PyPI (<https://pypi.python.org/pypi>)
* Python libraries described in the file [requirements.txt](requirements.txt)
* Connectivity with an intance of SIGRH database
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

## Program configuration

Some program configurations must be set up in the configuration file (see an sample [config.model.json](config.model.json)) and used as input to the program startup. So, the initialization command should be like this:

```shell
python3 main.py --config CONFIG_FILE_NAME
```

Notes:
in the configuration file, we need to set database connection and web server parameters.

## Some useful links

* [Twisted overview @ stackoverflow](https://stackoverflow.com/questions/5458631/whats-so-cool-about-twisted)
* [HTTP header 'accept' documentation @ Mozilla](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Accept)



