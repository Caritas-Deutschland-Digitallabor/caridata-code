FROM apache/superset:latest

USER root

RUN pip install psycopg2
COPY ./init-superset.sh /bin/init-superset.sh
RUN chmod +x /bin/init-superset.sh

USER superset