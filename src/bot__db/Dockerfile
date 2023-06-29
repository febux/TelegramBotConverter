FROM python:3.10-alpine

WORKDIR /docker_app

RUN /usr/local/bin/python -m pip install --upgrade pip

RUN apk add --no-cache gcc musl-dev linux-headers

COPY ./src /docker_app/src
COPY ./srv /docker_app/srv
COPY setup.py /docker_app/setup.py

RUN pip install -r /docker_app/src/bot__db/requirements.txt
RUN apk update && apk add libpq-dev python3-dev
RUN export PATH=/usr/lib/postgresql/14.8/bin/:$PATH
RUN pip install psycopg2

RUN python setup.py install
