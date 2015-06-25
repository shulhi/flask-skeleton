FROM ubuntu:14.10
MAINTAINER Shulhi Sapli <shulhi@gmail.com>

# install dependencies
RUN apt-get -y update && \
    apt-get install -y python libffi-dev python-dev python-pip python-virtualenv libpq-dev python-psycopg2 nginx gunicorn supervisor && \
    rm /bin/sh && ln -s /bin/bash /bin/sh && mkdir -p /deploy/project/app

COPY app/ /deploy/project/app
COPY wsgi.py /deploy/project/
COPY requirements.txt /deploy/project/

RUN virtualenv /deploy/project/ && \
    source /deploy/project/bin/activate && \
    pip install -r /deploy/project/requirements.txt

# Setup nginx
# Setup supervisord
COPY flask.conf /etc/nginx/sites-available/
RUN rm /etc/nginx/sites-enabled/default && \
    ln -s /etc/nginx/sites-available/flask.conf /etc/nginx/sites-enabled/flask.conf && \
    echo "daemon off;" >> /etc/nginx/nginx.conf && \
    mkdir -p /var/log/supervisor

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY gunicorn.conf /etc/supervisor/conf.d/gunicorn.conf

# Start processes
CMD ["/usr/bin/supervisord"]
