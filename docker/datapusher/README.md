# DataPusher

[DataPusher](https://github.com/ckan/datapusher)

Servicio orientado al almacenamiento de datos estructurados. Estos datos son alamncenados dentro de la base de datos de datastore en postgresql.

Se dispone de un dockerfile con los pasos requeridos para desplegar un contenedor que nos provee de dicho servicio.



#### Locale
Es necesario tener configurado el locale dentro del contenedor, debido a que sino no lo está, el servicio no llega a ejecutarse.


```sh
RUN sed -i -e 's/# es_ES.UTF-8 UTF-8/es_ES.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales && \
    update-locale LANG=es_ES.UTF-8


ENV LC_ALL es_ES.UTF-8
ENV LANG es_ES.UTF-8
ENV LANGUAGE es_ES.UTF-8
```
#### Permisos base de datos
Para que este servicio funcione correctamente es necesario crear la base de datos que utilizara datapusher y dar los permisos necesarios para un correcto funcionamiento.

* La creación de la base de datos se hará en la construcción del contenedor de postgresql mediante un [script](https://github.com/juanmaLC/Open-Data/blob/main/docker/postgresql/docker-entrypoint-initdb.d/initDataStore.sh).

* Para añadir los permisos necesarios al usuario creado y la base de datos de datastore es necesaria hacerla manualmente mediante el siguiente comando:

```sh
docker exec ckan /usr/lib/ckan/default/bin/ckan -c /etc/ckan/default/ckan.ini datastore set-permissions | docker exec -i db psql -U ckan_default
```
