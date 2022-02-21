#!/bin/bash

docker exec -it ckan /usr/lib/ckan/default/bin/ckan -c /etc/ckan/default/ckan.ini db init

docker exec -it ckan /usr/lib/ckan/default/bin/ckan -c /etc/ckan/default/ckan.ini db clean

docker exec -it ckan /usr/lib/ckan/default/bin/ckan -c /etc/ckan/default/ckan.ini db upgrade

docker exec -it db pg_restore -U ckan_default -c -d ckan_default /home/2022-01-17-databaseCKANpro.dump


docker exec -it ckan /usr/lib/ckan/default/bin/ckan -c /etc/ckan/default/ckan.ini search-index rebuild


docker exec ckan /usr/lib/ckan/default/bin/ckan -c /etc/ckan/default/ckan.ini datastore set-permissions | docker exec -i db psql -U ckan_default


#docker exec -it ckan /usr/lib/ckan/default/bin/ckan -c /etc/ckan/default/ckan.ini sysadmin add juanma
