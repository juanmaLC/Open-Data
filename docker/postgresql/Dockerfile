FROM postgres:latest



# Allow connections; we don't map out any ports so only linked docker containers can connect
RUN echo "host all  all    0.0.0.0/0  md5" >> /var/lib/postgresql/data/pg_hba.conf


# Customize default user/pass/db
ARG POSTGRES_DB
ARG POSTGRES_USER
ARG POSTGRES_PASSWORD


COPY 2022-01-17-databaseCKANpro.dump /home 

#pg_restore -U ckan_default -c -d ckan_default /home/2022-01-17-databaseCKANpro.dump
#docker exec ckan /usr/lib/ckan/default/bin/ckan -c /etc/ckan/default/ckan.ini datastore set-permissions | docker exec -i db psql -U ckan_default



# Include datastore setup scripts
ADD docker-entrypoint-initdb.d /docker-entrypoint-initdb.d


