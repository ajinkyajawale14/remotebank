# remotebank 
FairMoney Real Time Streaming & Ingesion Data Platform

## Steps to run the python file

1. create virtual env

`virtualenv venv`

2. activate the virtual env

`source venv/bin/activate`

3. install dependencies:

`pip install -r requirements.txt`

4. run the python script

`python3 main.py`

## Steps to run docker container

1. build docker image

`docker build -t remotebank:latest .`

2. run the docker container

`docker run remotebank:latest`

## kafka setup

- set up kafka topic retention policy
`docker exec -it redpanda-0 rpk topic alter-config transactions --set retention.ms=86400000` 

- add 2 partitions in kafka topic-transactions
`docker exec -it redpanda-0 rpk topic add-partitions transactions --num 2`