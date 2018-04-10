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