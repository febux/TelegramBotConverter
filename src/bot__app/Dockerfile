FROM python:3.10-alpine

WORKDIR /docker_app

RUN /usr/local/bin/python -m pip install --upgrade pip

COPY ./src /docker_app/src
COPY ./srv /docker_app/srv
COPY setup.py /docker_app/setup.py

RUN pip install -r /docker_app/src/bot__app/requirements.txt

RUN python setup.py install
