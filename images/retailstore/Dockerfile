FROM ubuntu:16.04

ENV PORT 9000

# Expose port 9000 for application
EXPOSE $PORT

RUN set -x && \
    apt-get -qq update && \
    apt-get -y install \
    git \
    curl \
    netcat \
    netbase \
    python3 \
    python3-setuptools \
    python3-pip \
    python3-dev \
    python3-dateutil \
    ca-certificates \
    gcc \
    g++ \
    make \
    libffi-dev \
    libssl-dev \
    libpq-dev \
    --no-install-recommends \
    && python3 -m pip install -U pip \
    && apt-get clean \
    && rm -rf \
        /var/lib/apt/lists/* \
        /tmp/* \
        /var/tmp/* \
        /usr/share/man \
        /usr/share/doc \
        /usr/share/doc-base

RUN useradd -ms /bin/bash retailstore

COPY . /home/retailstore/

RUN chown -R retailstore: /home/retailstore \
    && chmod +x /home/retailstore/entrypoint.sh

WORKDIR /home/retailstore
RUN pip3 install -r requirements-direct.txt
RUN python3 setup.py install

USER retailstore

# Execute entrypoint
ENTRYPOINT ["/home/retailstore/entrypoint.sh"]