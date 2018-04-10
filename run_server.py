import os

from paste import httpserver
from paste.deploy import loadapp

app_dir = os.path.dirname(os.path.realpath(__file__))
ini_path = '{}/etc/retailstore/retailstore-paste.ini'.format(app_dir)

wsgi_app = loadapp('config:' + ini_path)
httpserver.serve(wsgi_app, host='127.0.0.1', port=8080)