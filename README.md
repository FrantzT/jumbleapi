# Jumble API

## Table of contents

- Introduction
- Requirements
- Installation
- Configuration
- Developer

## Introduction

This is a demo deployment of an API server which is an implementation of a jumble word algorithm.

FastAPI Python's framework was used for the creation of the API server and it has been prepared to be deployed to ```minikube``` Kubernetes cluster by Helm chart.

The API consist of two endpoints:
- ```/api/jumble?word=<word>```

Query passed to the above endpoint (were the \<word> is the actual word to be jumbled) will result in a jumbled word.
eg. ```/api/jumble?word=test``` will return JSON object: ```{"jumbled_word":"etst"}```

- ```/api/audit```

Accessing the above endpoint will return last 10 queries as JSON objects to the server including access path and the actual query (eg.```{"url":"/api/audit","query":null}```).
eg.:
```
[...]
{"audit":{"log":{"level":"INFO","type":"access","timestamp":"2023-01-24 01:47:14,668","message":"GET /api/audit"},"req":{"url":"/api/audit","query":null},"res":{"statusCode":200,"body":{"statusCode":200,"status":"OK"}}}
[...]
```
Documentation for the used packages:

[FastAPI](https://fastapi.tiangolo.com/)

[Docker](https://docs.docker.com/get-started/) 

[Helm](https://helm.sh/docs/)

[minikube](https://minikube.sigs.k8s.io/docs/)




## Requirements

Configuration has been created and tested with the following packages:

```
python3 (v3.11)
docker (engine v20.10.23)

pip install fastapi
pip install "uvicorn[standard]"
pip install httpx 
pip install pytest 

helm (v3.11.0)
minikube (v1.28.0)
jq (v.1.6)
```

## Installation

### Jumbled API server

### Prerequisite 

Application requires helm and minikube applications to be installed on the system for the deployment.
jq is an additional package helping to pretty JSON output.

[Helm installation instructions]: https://helm.sh/docs/intro/install/
[Minikube installation instructions]: https://minikube.sigs.k8s.io/docs/start/
[jq installation instructions]: https://stedolan.github.io/jq/download/

Once installed clone the application files from the git repository 
and use helm to deploy it to the minikube cluster.

```
git clone https://github.com/FrantzT/jumbleapi.git

# minikube

minikube start 

# Helm chart deployment

cd jumbleapi

cd helm/jumbleapi

helm install jumbleapi .

# Verify instalation

helm ls
```
To verify successful installation test the endpoints with the following commands:

```
# retrive the service URL for jumbleapi service

MINIKUBE_SVC_URL=$(minikube service jumbleapi --url)

# test for endpoint /api/jumble/ 

curl $MINIKUBE_SVC_URL/api/jumble/?word=test -H "Accept: application/json" | jq .

{
  "jumbled_word": "tets"
}


# test for endpoint /api/audit 

curl $MINIKUBE_SVC_URL/api/audit -H "Accept: application/json" | jq .

[
  {
    "audit": {
      "log": {
        "level": "INFO",
        "type": "access",
        "timestamp": "2023-01-24 01:47:07,734",
        "message": "GET /api/audit"
      },
      "req": {
        "url": "/api/audit",
        "query": null
      },
      "res": {
        "statusCode": 200,
        "body": {
          "statusCode": 200,
          "status": "OK"
        }
      }
    }
  }
[...]
]
```

### pytest

```
cd jumbleapi/test

# execute

pytest
```
pytest will run set of 4 tests checking the connectivity and server response.



### Development environment setup

### Prerequisite 

Development requires installation of the packages (paragraph Requirements of this document)
as well as installation of applications required for the JumbleAPI server itself (previous paragraph).

Docker is an additional required package.

Once the packages have been installed clone the application files from the git repository.

```
git clone https://github.com/FrantzT/jumbleapi.git
```
### Development

```
cd jumbleapi

$ tree

.
├── Dockerfile
├── README.md
├── app
│   ├── __init__.py
│   ├── audit_logger.py
│   ├── audit_logger_formatter.py
│   ├── favicon.ico
│   └── main.py
├── helm
│   └── jumbleapi
│       ├── Chart.yaml
│       ├── templates
│       │   ├── NOTES.txt
│       │   ├── _helpers.tpl
│       │   ├── deployment.yaml
│       │   ├── service.yaml
│       │   └── serviceaccount.yaml
│       └── values.yaml
├── log
│   └── audit.log
├── requirements.txt
└── test
    ├── __init__.py
    ├── log
    │   └── audit.log
    └── test_main.py

app/

app/main.py

Main module of the application containing core functions.

app/audit_logger.py

Module containing functions responsible for managing log file and stream.

app/audit_logger_formatter.py

Module containing functions responsible for formating the JSON output for the log objects.

app/test_main.py

Basic pytest module.  


helm/

helm/templates/deployment.yaml

Helm chart template containing definitions of the deployment variables.

helm/templates/service.yaml

Helm chart template containing definitions of the service variables.

helm/values.yaml

Default values for the chart deployment.

test/test_main.py

pytest test units
```

### Development instructions

All the necessary development and test of the application 
can be performed in your local python environment (preferably python venv).
You can start the local server locally 
and it will deliver your changes instantly to the endpoints.

```
cd jumbleapi

# run the uvicorn server in the --reload development mode 
# to instantly apply your code changes to the application

uvicorn app.main:app --reload

The server API document tools (openapi) can be accessed in the browse at the URL:

http://127.0.0.1:8000/docs

```
After the code changes has been completed 
create Docker image and push it to the docker repository.
The Dockerfile file consists instructions for the docker image build.
All aditional packages required durning development need to be added to
the requirments.txt file or specifed in the Dockerfile itself.

```
cd jumbleapi # location of the Dockerfile build instructions file
docker build -t jumbleapi .
docker tag jumbleapi <repository>/<application_name>:<tag>
docker login # connect to the repository
docker push <repository>/<application_name>:<tag>
```
Once the images have been created 
and successfully delivered follow instructions from the paragraph
```Installation > Jumbled API server > Prerequisite``` 
to test your changes.

## Configuration notes

The configuration is a basic framework and as such has simplified structure.
There are some matters needed to be explained.

### File persistence.

The setup uses a file to collect logs for the audit. 
The file itself is located in directory ```jumbleapi/app/log/audit.log```
The ```minikube``` need to start with the mount option, so the directory 
within your local environment will be used as a mount point for the cluster node
and allow pods to mount it as Directory and share the file access between them.
The volume configuration is hardcoded within the file
```jumbleapi/helm/jumbleapi/templates/deployment.yaml```
. Keep that in mind in case you would like to move it to a different location.
As such the method of storage is insecure and should not be used in the production environment.
It is set up this way just for the ease of test within local environment.

```
[...]
         volumeMounts: 
            - name: audit-log
              mountPath: /code/log
[...]
      volumes:
        - name: audit-log
          hostPath:
            path: /data
            type: Directory
[...]
```
### helm chart values.yaml

The ```minikube``` deployment has default value of the ```replicaCount: 2```.

You can increase and decrease the value depending on your scalability needs.

```repository: pawelzaatdocker/jumbleapi``` is a hardcoded value for the v1.0.1 of the application.

## Developer

Please [contact me](mailto:pawel.a.zajac@gmail.com) would you have any questions or comments.


