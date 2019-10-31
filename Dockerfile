FROM python:3-alpine

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

RUN pip3 install --no-cache-dir flask gunicorn connexion python-dateutil
RUN pip3 install --no-cache-dir oslash

COPY api /usr/src/app/api
COPY pdsphenotypemapping /usr/src/app/pdsphenotypemapping
COPY tx-utils/src /usr/src/app

ENTRYPOINT ["gunicorn"]

CMD ["-w", "4", "-b", "0.0.0.0:8080", "api.server:create_app()"]

