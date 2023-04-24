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
# CMD [ "python3", "./main.py" ]


# flink command
# RUN apt-get update \
#  && apt-get install -y --no-install-recommends \
#     build-essential \
#     libsnappy-dev \
#     liblz4-dev \
#     libzstd-dev \
#  && rm -rf /var/lib/apt/lists/*

# ENV FLINK_VERSION=1.14.0
# ENV FLINK_PYTHON_VERSION=3.8
# ENV FLINK_HOME=/opt/flink

# RUN curl -o flink.tgz https://archive.apache.org/dist/flink/flink-$FLINK_VERSION/flink-$FLINK_VERSION-bin-scala_2.12.tgz \
#  && tar xfz flink.tgz \
#  && rm flink.tgz \
#  && mv flink-$FLINK_VERSION $FLINK_HOME

# ENV PATH=$PATH:$FLINK_HOME/bin

# RUN pip install apache-flink==${FLINK_VERSION} python-snappy kafka-python
# FROM apache/flink:1.14.0-scala_2.12

# COPY transactions-ml-features-job.py /opt/flink/

# CMD ["python3", "/transactions-ml-features-job.py"]