
Functionalities
===============

.. function:: enumerate(sequence[, start=0])

    Return an iterator that yields tuples of an index and an item of the *sequence* . (And so on.)


AutoDoc
-------

.. autofunction:: io.open


Module autodoc
--------------

.. automodule:: io
    :members:


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

The :py:func:`enumerate` function can be used for ...


