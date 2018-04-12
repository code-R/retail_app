#!/bin/bash
set -ex

exec uwsgi \
    --ini uwsgi.ini