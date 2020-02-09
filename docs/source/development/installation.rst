
Installation
============

Download project form github::

    git clone https://github.com/ydiazn/vocationQA.git

Python dependencies
---------------------------

You need python 3.6+ an optionally but recommended venv python
module for virtual environment::

    apt-get install python3-venv

Install python dependencies in virtual environment::

    python3 -m venv env
    source env/bin/activate
    pip install -r requeriments/local.txt

In above example env is virtual environment name.

If you are behind a proxy set proxy virtual environment before installation with pip::

    export http_proxy=http://username:password@host:port
    export https_proxy=http://username:password@host:port


Project config
---------------------

You must set following environment variables:

* DB_NAME
* DB_HOST
* DB_PORT
* DB_USER
* DB_PASSWORD
* SECRET_KEY
* DJANGO_SETTINGS_MODULE

Virtual environment can be set in self virtual environment.
For example for set DB_NAME type::

    echo 'export DB_NAME=vocationQA' >> venv/bin/activate

You can edit activate script directly.
For custom installation set DJANGO_SETTINGS_MODULE variable as following::

   echo 'export DJANGO_SETTINGS_MODULE='vocationQA.settings.local' >> venv/bin/activate

Run project
-----------

First asure that virtual environment are active::

    source env/bin/activate

Run django migrations and create a superuser::

    python vocationQA/manage.py migrate
    python vocationQA/manage.py createsuperuser

Finally run django web server::

    python vocationQA/manage.py runserver

and open web browser at http://127.0.0.1:8000


