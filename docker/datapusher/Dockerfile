FROM python:3.9

RUN apt-get update -y
RUN apt-get upgrade -y 

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y locales

RUN sed -i -e 's/# es_ES.UTF-8 UTF-8/es_ES.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales && \
    update-locale LANG=es_ES.UTF-8


ENV LC_ALL es_ES.UTF-8
ENV LANG es_ES.UTF-8
ENV LANGUAGE es_ES.UTF-8


RUN python3 -m venv /usr/lib/ckan/datapusher
RUN mkdir /usr/lib/ckan/datapusher/src

WORKDIR /usr/lib/ckan/datapusher/src


RUN git clone -b 0.0.17 https://github.com/ckan/datapusher.git

WORKDIR datapusher


RUN /usr/lib/ckan/datapusher/bin/python3 -m pip install --upgrade pip
RUN /usr/lib/ckan/datapusher/bin/pip install -r requirements.txt 
RUN /usr/lib/ckan/datapusher/bin/python setup.py develop
RUN /usr/lib/ckan/datapusher/bin/pip install uwsgi


EXPOSE 8800

USER www-data:www-data
CMD [ "/usr/lib/ckan/datapusher/bin/uwsgi", "-i", "/usr/lib/ckan/datapusher/src/datapusher/deployment/datapusher-uwsgi.ini" ]
