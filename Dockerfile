# python image
FROM python:3.9-slim-buster 

# setting up working dir
WORKDIR /remotebank

# copy dir content to container
COPY requirements.txt  ./requirements.txt
COPY main.py ./main.py
# COPY . /remotebank

# execute venv
RUN pip install -r requirements.txt

# run command
CMD [ "python3", "./main.py" ]
