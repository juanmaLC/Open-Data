# Dashboard

Servicio web para el muestreo de las estadísticas recopiladas durante el funcionamiento del servicio de ckan.
Estas estadísticas son recopiladas filtrando el log de peticiones de nginx (GET, POST, PUT).

Un resumen del procedimiento llevado a cabo sería el siguiente:

* Primero se procede a leer el log diario de ngix y se filtra, quedándonos solo con las peticiones que se realizan al servidor que son o una descarga (desde url o datastore) o una visita a alguno de los recursos que conforman los datasets. esta funcionalidad se puede consultar en la función getLogNginx().
* Una vez que tenemos un dataframe filtrado con los datos que nos interesa, lo recorremos y contamos el numero de visitas o descargas y se guardan en un documento JSON. También se cuentan las descargas y visitas que se realizan al portal cada mes. Como elemento adicional también se cuenta con mapa donde se localiza la geolocalización de los usuarios del portal.
* También se muestra información como un ranking de los formatos que aloja el portal y el numero total de datasets y resources que aloja en el tiempo.


Estos archivivos de filtrado pueden ser encontrados en el directorio [scriptPythonEstadisticas](https://github.com/juanmaLC/Open-Data/tree/main/docker/dash/scriptPythonEstadisticas).



### UWSGI
La aplicación web de muestreo de estadísticas está desarrollada en python, con el apoyo del framework [dash](https://plotly.com/dash/) y desplegada con [UWSGI](https://uwsgi-docs.readthedocs.io/en/latest/).

El código fuente de la aplicación está localizado en el directorio [app](https://github.com/juanmaLC/Open-Data/tree/main/docker/dash/app).
