import click
from flask import current_app
from flask.cli import FlaskGroup
from flask_security import hash_password

from kingdom_api.app import create_app


def create_kingdom_api_app(info):
    return create_app(cli=True)


@click.group(cls=FlaskGroup, create_app=create_kingdom_api_app)
def cli():
    """Main entry point"""


@cli.command("init")
def init():
    """Create a new admin user
    """
    from kingdom_api.extensions import db

    security = current_app.extensions["security"]

    security.datastore.create_role(
        name="admin",
        permissions={"admin", "user-profile", "user-game"},
    )
    security.datastore.create_role(
        name="user",
        permissions={"user-profile", "user-game"}
    )

    security.datastore.create_user(
        username="admin",
        email="admin@example.com",
        password=hash_password("admin"),
        roles=["admin"]
    )
    security.datastore.create_user(
        email="user@example.com",
        password=hash_password("password"),
        roles=["user"]
    )

    db.session.commit()
    click.echo("created users admin and password")


if __name__ == "__main__":
    cli()
