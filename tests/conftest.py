import json
import pytest

from dotenv import load_dotenv

from kingdom_api.models import User
from kingdom_api.app import create_app
from kingdom_api.extensions import db as _db

from pytest_factoryboy import register
from tests.factories import UserFactory

register(UserFactory)


@pytest.fixture
def app():
    load_dotenv(".testenv")
    app = create_app(testing=True)
    return app


@pytest.fixture
def db(app):
    _db.app = app

    with app.app_context():
        _db.create_all()

    yield _db

    _db.session.close()
    _db.drop_all()


@pytest.fixture
def admin_user(db):
    user = User(username="admin", email="admin@admin.com", password="admin")

    db.session.add(user)
    db.session.commit()

    return user


@pytest.fixture
def client(app, db):
    with app.test_client() as client:
        yield client


@pytest.fixture
def admin_headers(admin_user, client):
    data = {"username": admin_user.username, "password": "admin"}
    rep = client.post(
        "/auth/login",
        data=json.dumps(data),
        headers={"content-type": "application/json"},
    )

    tokens = json.loads(rep.get_data(as_text=True))
    return {
        "content-type": "application/json",
        "authorization": "Bearer %s" % tokens["access_token"],
    }


@pytest.fixture
def admin_refresh_headers(admin_user, client):
    data = {"username": admin_user.username, "password": "admin"}
    rep = client.post(
        "/auth/login",
        data=json.dumps(data),
        headers={"content-type": "application/json"},
    )

    tokens = json.loads(rep.get_data(as_text=True))
    return {
        "content-type": "application/json",
        "authorization": "Bearer %s" % tokens["refresh_token"],
    }
