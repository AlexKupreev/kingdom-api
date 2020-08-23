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
    poetry install

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


Authentication
**************

Flask-Security-Too is used for handling auth.
By default, session authentication is used (login form in browser etc.).

If Single Page Application to be used as admin application, additional configuration should be set:

.. code::

    APPLICATION_IS_SPA=True

If this setting is True, application will be configured according to https://flask-security-too.readthedocs.io/en/stable/spa.html .
These settings are set in `kingdom_api/config.py` and can be adjusted as needed.
Default auth operations are performed as follows:

* authorization

.. code::

    curl -X POST -H "Content-Type: application/json" -d '{"email": "admin@example.com", "password": "admin"}' http://localhost:5000/api/accounts/login?include_auth_token

    response headers:
    Content-Type: application/json
    Content-Length: 438
    Content-Type: application/json
    Set-Cookie: XSRF-TOKEN=IjAzNmU3YmJkZDcxNGUwZGQ3MjNjZDI0MDI1MzAxOWMxOThmMmM5Mjgi.X0Eqag.EbsmOaAynHGRc-WOTvlBO0-YUyA; Path=/
    Vary: Cookie
    Set-Cookie: session=.eJwlj0FqRDEMQ--SdSl24sT2XOZjOzEthWn5f2ZVevcGZiWE9ED6LUee6_oot8f5XG_l-JzlVkIrhQ-doUqiKT0M2TzWouFQu6dhzaYdq7ZgrYw2Y0CqLE3iyY5ijDrSBjUe0d09dIgsILJsROnMTgqS6TqbJwK20RvOXvaQ57XO1xo2bYN3NK0SEFoqMU0T89kTxm7Hdebx-P5a992HNha7z8lIC7bUFnOTtTdADVTJuh_K5vI6IjZyrfvjZX_Myg27CsKoKO-tSwWlv38yolLQ.X0Eqaw.yFBFD3mVvlqN5wakrjlZwCb4j18; HttpOnly; Path=/
    Server: Werkzeug/1.0.1 Python/3.7.3
    Date: Sat, 22 Aug 2020 14:23:39 GMT

    response:
    {
      "meta": {
        "code": 200
      },
      "response": {
        "csrf_token": "IjAzNmU3YmJkZDcxNGUwZGQ3MjNjZDI0MDI1MzAxOWMxOThmMmM5Mjgi.X0Eqag.EbsmOaAynHGRc-WOTvlBO0-YUyA",
        "user": {
          "authentication_token": "WyIxIiwiJDUkcm91bmRzPTUzNTAwMCQ1a1VERFJVdnhvYjBHR2pmJEZlVlZtd01ERUpNSy56NzZmd0JUUXdPVElZUnJsTmpZV0pqQTBuNC85ai8iLCI3YTkzNjczNjVkYTI0MDQxYWY5NDc0ZGE4YWJkNWYwNiJd.X0Eqag.6XagKOIUcpgYcMbaac9fvygV8Us",
          "id": "1"
        }
      }
    }

Full list of endpoints is here: https://flask-security-too.readthedocs.io/en/stable/_static/openapi_view.html


Notes on CSRF usage and additional improvements can be found on https://flask-security-too.readthedocs.io/en/stable/patterns.html


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
