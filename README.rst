Requirements
------------

* poetry

Configuration
-------------

* Rename and set environment variables:

  * ``.example.env`` -> ``.env`` - development server
  * ``.example.testenv`` -> ``.testenv`` - testing setup

* Specific variables:

  * ``CELERY_BROKER_URL`` - broker connection in format

  .. code::

     redis://:password@hostname:port/db_number

  * ``CELERY_RESULT_BACKEND_URL`` - backend connection in format

  .. code::

     redis://:password@hostname:port/db_number


Development using virtual environment
-------------------------------------

Running the backend
*******************

To have an instance up and running locally:

* Go to

.. code::

    poetry shell

* Init database:

.. code::

    manage db upgrade
    manage init

* Run worker (redis backend should be running - e.g. ``$ redis-server``)

.. code::

    celery worker -A kingdom_api.celery_app:app --loglevel=info

* Run development server (will be available at ``http://127.0.0.1:5000/`` or ``http://localhost:5000/``)

.. code::

    manage run

* Alternatively run gunicorn as wsgi server (available at ``http://127.0.0.1:8000``)

.. code::

    gunicorn kingdom_api.wsgi:app


Testing and linting
*******************

* Go to

.. code::

    poetry shell

* You can use pytest, tox, as well as flake8 and black like

.. code::

    pytest
    tox
    tox -e lint
    flake8
    black .

* Also you can use them from outside of shell:

.. code::

    poetry run pytest
    poetry run flake8
    poetry run black .
