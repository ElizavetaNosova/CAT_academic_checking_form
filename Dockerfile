FROM tiangolo/uwsgi-nginx-flask:python3.6-alpine3.7

MAINTAINER Elizaveta Nosova "lizanosova@yandex.ru"

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

ENTRYPOINT [ "python" ]

CMD [ "api.py" ]
