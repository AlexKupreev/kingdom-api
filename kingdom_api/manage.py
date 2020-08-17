import click
from flask.cli import FlaskGroup

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
    from kingdom_api.models import User

    click.echo("create user")
    user = User(
        username="admin", email="admin@example.com", password="password", active=True
    )
    db.session.add(user)
    db.session.commit()
    click.echo("created user admin")


if __name__ == "__main__":
    cli()
