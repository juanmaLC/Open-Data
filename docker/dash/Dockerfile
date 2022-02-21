
FROM python:3.9

RUN apt-get update -y
RUN apt-get upgrade -y 



RUN python3 -m venv /usr/lib/dash
RUN /usr/lib/dash/bin/pip install --upgrade pip





RUN /usr/lib/dash/bin/pip install uwsgi
RUN /usr/lib/dash/bin/pip install dash-bootstrap-components
RUN /usr/lib/dash/bin/pip install dash
RUN /usr/lib/dash/bin/pip install pandas
RUN /usr/lib/dash/bin/pip install plotly



COPY app /app
COPY scriptPythonEstadisticas /scriptPythonEstadisticas
WORKDIR app


EXPOSE 8989


CMD [ "/usr/lib/dash/bin/uwsgi", "--ini", "appdash.ini"]




