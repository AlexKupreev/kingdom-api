from flask import Flask, url_for
from flask_admin.contrib.sqla import ModelView
from flask_admin import helpers as admin_helpers
from flask_security import SQLAlchemySessionUserDatastore
from flask_wtf import CSRFProtect

from kingdom_api import admin, api
from kingdom_api.extensions import db, security, migrate, \
    apispec, celery, admin_ext


def create_app(testing=False, cli=False):
    """Application factory, used to create application
    """
    app = Flask("kingdom_api")
    app.config.from_object("kingdom_api.config")

    if testing is True:
        app.config["TESTING"] = True

    configure_extensions(app, cli)
    configure_apispec(app)
    register_blueprints(app)
    init_celery(app)

    return app


def configure_extensions(app, cli):
    """configure flask extensions
    """
    from kingdom_api.models import User, Role

    db.init_app(app)

    CSRFProtect(app)

    # TODO do we need to consume `user_datastore` in the further code?
    user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)
    security.init_app(app, user_datastore)

    # jwt.init_app(app)

    if cli is True:
        migrate.init_app(app, db)
    else:
        admin_ext.init_app()
        admin_ext.add_view(ModelView(User, db.session))


def configure_apispec(app):
    """Configure APISpec for swagger support
    """
    apispec.init_app(app, security=[{"jwt": []}])
    apispec.spec.components.security_scheme(
        "jwt", {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
    )
    apispec.spec.components.schema(
        "PaginatedResult",
        {
            "properties": {
                "total": {"type": "integer"},
                "pages": {"type": "integer"},
                "next": {"type": "string"},
                "prev": {"type": "string"},
            }
        },
    )


def register_blueprints(app):
    """register all blueprints for application
    """
    # app.register_blueprint(auth.views.blueprint)
    app.register_blueprint(admin.views.blueprint)
    app.register_blueprint(api.views.blueprint)


def init_celery(app=None):
    app = app or create_app()
    celery.conf.broker_url = app.config["CELERY_BROKER_URL"]
    celery.conf.result_backend = app.config["CELERY_RESULT_BACKEND"]
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        """Make celery tasks work with Flask app context"""

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


# TODO move in appropriate place
# define a context processor for merging flask-admin's template context into the
# flask-security views.
@security.context_processor
def security_context_processor():
    return dict(
        admin_base_template=admin_ext.base_template,
        admin_view=admin_ext.index_view,
        h=admin_helpers,
        get_url=url_for
    )

