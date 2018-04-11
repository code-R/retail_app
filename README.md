|Build Status| |License: MIT| |3.5|

# retail_app
This is a sample app for trying few things


Setup Dev Environment


Create Virtual Environment

mkvirtualenv -p `which python3` rstore

workon rstore

pip install -r requirements-direct.txt -r requirements-test.txt

python setup.py develop

Create default conf file using oslo config generator

tox -e genconfig

Run dev server

python run_server.py

curl -H "X-Auth-Token:open-sesame"  http://127.0.0.1:9000/api/v1.0/things




.. |Build Status| image:: https://api.travis-ci.org/code-R/retail_app.svg?branch=master
