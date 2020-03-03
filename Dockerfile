FROM python:3-alpine

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

RUN apk --no-cache add gcc musl-dev
RUN pip3 install --no-cache-dir flask gunicorn[gevent]==19.9.0 connexion[swagger-ui] oslash

COPY api /usr/src/app/api
COPY tx-utils/src /usr/src/app

# install dhall-json executable
RUN wget https://github.com/dhall-lang/dhall-haskell/releases/download/1.30.0/dhall-json-1.6.2-x86_64-linux.tar.bz2
RUN tar --extract --bzip2 --file dhall-json-1.6.2-x86_64-linux.tar.bz2
RUN cp ./bin/dhall-to-json /usr/local/bin

ENTRYPOINT ["gunicorn"]

CMD ["-w", "4", "-b", "0.0.0.0:8080", "api.server:create_app()"]

