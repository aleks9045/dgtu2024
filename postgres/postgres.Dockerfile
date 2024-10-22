FROM postgres:16.2-alpine3.19

COPY ./postgresql.conf /etc/postgresql.conf

EXPOSE 5432

ENTRYPOINT ["docker-entrypoint.sh"]

CMD ["postgres", "-c", "config_file=/etc/postgresql.conf"]