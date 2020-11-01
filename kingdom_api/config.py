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

# TODO remove
JWT_BLACKLIST_ENABLED = True
JWT_BLACKLIST_TOKEN_CHECKS = ["access", "refresh"]

# Flask-Admin
FLASK_ADMIN_SWATCH = 'cerulean'

CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND_URL")

MAIL_SUPPRESS_SEND = os.getenv("MAIL_SUPPRESS_SEND", ENV == "production")

GAME_SETTINGS_FILE = os.getenv("GAME_SETTINGS_FILE")

# ==== Flask-Security-Too settings for SPA ====

# Simultaneous use API and browser endpoints is possible, but they would have the same auth endpoints.
# TODO check if it is possible to fix

# no forms so no concept of flashing
#SECURITY_FLASH_MESSAGES = False

# Need to be able to route backend flask API calls. Use 'accounts'
# to be the Flask-Security endpoints.
SECURITY_URL_PREFIX = '/auth'

# Turn on all the great Flask-Security features
SECURITY_RECOVERABLE = True
SECURITY_TRACKABLE = True
SECURITY_CHANGEABLE = True
SECURITY_CONFIRMABLE = False
SECURITY_REGISTERABLE = True
SECURITY_UNIFIED_SIGNIN = False

# These need to be defined to handle redirects
# As defined in the API documentation - they will receive the relevant context
SECURITY_POST_CONFIRM_VIEW = "/confirmed"
SECURITY_CONFIRM_ERROR_VIEW = "/confirm-error"
SECURITY_RESET_VIEW = "/reset-password"
SECURITY_RESET_ERROR_VIEW = "/reset-password"
SECURITY_REDIRECT_BEHAVIOR = "spa"

# CSRF protection is critical for all session-based browser UIs

# enforce CSRF protection for session / browser - but allow token-based
# API calls to go through
SECURITY_CSRF_PROTECT_MECHANISMS = ["session", "basic"]
SECURITY_CSRF_IGNORE_UNAUTH_ENDPOINTS = True

# Send Cookie with csrf-token. This is the default for Axios and Angular.
SECURITY_CSRF_COOKIE = {"key": "XSRF-TOKEN"}
WTF_CSRF_CHECK_DEFAULT = False
WTF_CSRF_TIME_LIMIT = None
