FROM ubuntu:20.04



ENV DEBIAN_FRONTEND noninteractive
#ARG POSTGRES_DB
#ARG POSTGRES_USER
#ARG POSTGRES_PASSWORD
ARG CKAN_SITE_URL




RUN apt-get update -y
RUN apt-get upgrade -y 

RUN apt-get install -y python3-dev 
RUN apt-get install -y libpq-dev
RUN apt-get install -y python3-pip
RUN apt-get install -y python3-venv
RUN apt-get install -y git-core
RUN apt-get install -y openjdk-8-jdk




RUN mkdir -p /usr/lib/ckan/default
RUN chown `whoami` /usr/lib/ckan/default
RUN python3 -m venv /usr/lib/ckan/default

RUN /usr/lib/ckan/default/bin/pip install setuptools==44.1.0
RUN /usr/lib/ckan/default/bin/pip install --upgrade pip
RUN /usr/lib/ckan/default/bin/pip install -e 'git+https://github.com/ckan/ckan.git@ckan-2.9.4#egg=ckan[requirements]'
RUN /usr/lib/ckan/default/bin/pip install uwsgi


COPY requeriments.txt /home


RUN /usr/lib/ckan/default/bin/pip install -r /home/requeriments.txt

RUN mkdir -p /etc/ckan/default
RUN chown -R `whoami` /etc/ckan/
RUN ln -s /usr/lib/ckan/default/src/ckan/who.ini /etc/ckan/default/who.ini

COPY ckan.ini /etc/ckan/default/
COPY placeholder-420x220.png /usr/lib/ckan/default/src/ckan/ckan/public/base/images/

RUN cp /usr/lib/ckan/default/src/ckan/wsgi.py /etc/ckan/default/
RUN cp /usr/lib/ckan/default/src/ckan/ckan-uwsgi.ini /etc/ckan/default/


EXPOSE 5000


CMD [ "/usr/lib/ckan/default/bin/ckan", "-c", "/etc/ckan/default/ckan.ini", "run", "--host", "0.0.0.0", "-p", "5000"]



#CMD [ "/usr/lib/ckan/default/bin/uwsgi", "-i", "/etc/ckan/default/ckan-uwsgi.ini" ]



