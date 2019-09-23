FROM python:3-alpine as base

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

RUN pip3 install --no-cache-dir flask gunicorn connexion

COPY api/openAPI3 /usr/src/app/api
COPY pdsphenotypemapping /usr/src/app/pdsphenotypemapping

EXPOSE 8080

ENTRYPOINT ["gunicorn"]

CMD ["-w", "4", "-b", "0.0.0.0:8080", "api.server:create_app()"]

FROM base as test

RUN pip3 install --no-cache-dir pytest
RUN pip3 install --no-cache-dir requests
COPY test /usr/src/app/test

ENV PYTHONPATH=/usr/src/app

ENTRYPOINT ["pytest"]
CMD ["-s"]
