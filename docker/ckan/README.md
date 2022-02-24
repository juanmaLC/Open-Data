# Ckan

Repositorio con la configuración necesaria para la construcción de un contenedor con la configuración y paquetes necesarios para desplegar un servicio ckan.

Contiene:
* Un dockerfile para la construcción
* Un archivo de configuración de ejemplo de ckan (ckan.ini)
* Un requeriments.txt con paquetes necesario y extensiones para el correcto funcionamiento.


En el caso de que se quiera partir de un archivo de configuración por defecto (ckan.ini) bastaría con ejecutar el siguiente comando una vez estén en funcionamiento los contenedores:

```sh
docker exec -it ckan /usr/lib/ckan/default/bin/ckan generate config /etc/ckan/default/ckan.ini
```
