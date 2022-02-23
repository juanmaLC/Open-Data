# Docker compose

Construcción de las imágenes:

```sh
docker-compose build
```

Levantar los contenedores:

```sh
docker-compose up
```

Parar los contenedores:
```sh
docker-compose down
```

Reiniciar los contenedores


```sh
docker-compose restart 'container'
```


# Uso

Tenemos en uso 6 contenedores, cada uno corriendo un servicio diferente (app dash, ckan, base de datos postgresql, redis y DataPusher).


Inicializar la base de datos de ckan:

```sh
docker exec -it ckan /usr/lib/ckan/default/bin/ckan -c /etc/ckan/default/ckan.ini db init
```

Borrar la base de datos de ckan:
```sh
docker exec -it ckan /usr/lib/ckan/default/bin/ckan -c /etc/ckan/default/ckan.ini db clean
```


Creación de usuario administrador:
```sh
docker exec -it ckan /usr/lib/ckan/default/bin/ckan -c /etc/ckan/default/ckan.ini sysadmin add juanma

```

Actualizar la base de datos (en el caso de que exportemos un backup de una versión anterior a la actual):
```sh
docker exec -it ckan /usr/lib/ckan/default/bin/ckan -c /etc/ckan/default/ckan.ini db upgrade
```

Cargar backup de la base de datos:
```sh
docker exec -it db pg_restore -U ckan_default -c -d ckan_default /home/2022-01-17-databaseCKANpro.dump
```

Recargar los indices de la base de datos:
```sh
docker exec -it ckan /usr/lib/ckan/default/bin/ckan -c /etc/ckan/default/ckan.ini search-index rebuild
```

Dar permisos de lectura al usuario de datapusher:
```sh
docker exec ckan /usr/lib/ckan/default/bin/ckan -c /etc/ckan/default/ckan.ini datastore set-permissions | docker exec -i db psql -U ckan_default
```
