FROM python:3.5-alpine

ENV PORT 9000

ENV PBR_VERSION 1.0.2

# Expose port 9000 for application
EXPOSE $PORT

RUN adduser -S retailstore

COPY . /home/retailstore/

RUN chown -R retailstore: /home/retailstore \
    && chmod +x /home/retailstore/entrypoint.sh

WORKDIR /home/retailstore

RUN set -e; \
    apk add --no-cache --virtual .build-deps \
        gcc \
        libc-dev \
        linux-headers \
        musl-dev \
        postgresql-dev \
        python3-dev \
    ; \
    pip install -r requirements-direct.txt; \
    apk del .build-deps;

RUN python setup.py install

USER retailstore

# Execute entrypoint
ENTRYPOINT ["/home/retailstore/entrypoint.sh"]
