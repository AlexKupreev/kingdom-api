"""Extensions registry
All extensions here are used as singletons and
initialized in application factory
"""
from flask_sqlalchemy import SQLAlchemy
from passlib.context import CryptContext
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from celery import Celery
from flask_security import Security
from flask_admin import Admin

from kingdom_api.commons.apispec import APISpecExt


db = SQLAlchemy()
security = Security()
# TODO should be removed as all auth is handled by flask_security?
jwt = JWTManager()
ma = Marshmallow()
migrate = Migrate()
apispec = APISpecExt()
# TODO remove pwd_context
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
celery = Celery()
admin_ext = Admin(template_mode='bootstrap4')
