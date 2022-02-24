# PostgreSQL

Servicio de base de datos utilizada por el servicio de ckan y datapusher.

Se utiliza la ultima versión disponible de postgresql.

Nos encontramos con un dockerfile básico, que nos configura el usuario administrador de la base de datos y nos añade al contenedor unos [scripts](docker-entrypoint-initdb.d) que se ejecutan a la hora de iniciar por primera vez el contenedor. Su función es la de crear e inicializar las dos bases de datos utilizadas por ckan (datastore_default y ckan_default).



## Cargar base de datos desde un archivo backup
En caso de querer cargar un archivo backup en la base de datos cuando realicemos el docker-compose up, tendriamos que añadir dicho archivo con su correspondiente COPY en el dockerfile y añadir el comando de carga dentro del script [initDB.sh](https://github.com/juanmaLC/Open-Data/blob/main/docker/postgresql/docker-entrypoint-initdb.d/initDB.sh)

Línea de dockerfile:
```sh
COPY fileBackupDB.dump /home
```
