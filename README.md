# vocationQA
Question &amp; Answer systen for vocational formation

## Instalation

Download project form github::

    git clone https://github.com/ydiazn/vocationQA.git

### Python dependencies

You need python 3.6+ an optionally but recommended venv python
module for virtual environment::

    apt-get install python3-venv

Install python dependencies in virtual environment
```
python3 -m venv env
source env/bin/activate
pip install -r requeriments/local.txt
```

In above example env is virtual environment name.

If you are behind a proxy set proxy virtual environment before installation with pip

    export http_proxy=http://username:password@host:port
    export https_proxy=http://username:password@host:port


## Project config
You must set following environment variable:

* VOCATION_SECRET_KEY

Virtual environments can be set in self virtual environment.
For example for set DB_NAME you can type

    echo 'export VOCATION_SECRET_KEY="76jiorwu6=1&hu=)-cc$b-by-o16#mpcy-frp=^jvp(#=5_"' >> venv/bin/activate

You can edit activate script directly.

For use postgresql you can change database setting by 

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get("VOCATION_DB_NAME"),
        'HOST': os.environ.get("VOCATION_DB_HOST"),
        'PORT': os.environ.get("VOCATION_DB_PORT"),
        'USER': os.environ.get("VOCATION_DB_USER"),
        'PASSWORD': os.environ.get("VOCATION_DB_PASSWORD"),
        'ATOMIC_REQUESTS': True,
    }
}
```
and set the following environment variables:

* VOCATION_DB_NAME
* VOCATION_DB_HOST
* VOCATION_DB_PORT
* VOCATION_DB_USER
* VOCATION_DB_PASSWORD

You must deactivate and active again the virtual environment
after set environment variables in virtual environment. 

## Run project

First asure that virtual environment are active

    source env/bin/activate

Run django migrations and create a superuser

```
python vocationQA/manage.py migrate
python vocationQA/manage.py createsuperuser
```

Finally run django web server::

    python vocationQA/manage.py runserver

and open web browser at http://127.0.0.1:8000

