"""Default configuration
Use env var to override
"""
import os

ENV = os.getenv("FLASK_ENV")
DEBUG = ENV == "development"
SECRET_KEY = os.getenv("SECRET_KEY")
# Bcrypt is set as default SECURITY_PASSWORD_HASH, which requires a salt
SECURITY_PASSWORD_SALT = os.getenv("SECURITY_PASSWORD_SALT")

SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI")
SQLALCHEMY_TRACK_MODIFICATIONS = False
# As of Flask-SQLAlchemy 2.4.0 it is easy to pass in options directly to the
# underlying engine. This option makes sure that DB connections from the pool
# are still valid. Important for entire application since many DBaaS options
# automatically close idle connections.
SQLALCHEMY_ENGINE_OPTIONS={"pool_pre_ping": True}

JWT_BLACKLIST_ENABLED = True
JWT_BLACKLIST_TOKEN_CHECKS = ["access", "refresh"]

CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND_URL")

GAME_SETTINGS_FILE = os.getenv("GAME_SETTINGS_FILE")
