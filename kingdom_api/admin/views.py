from flask import request, jsonify, Blueprint, render_template_string, current_app as app
from flask_security import auth_required, permissions_accepted, permissions_required

from kingdom_api.models import User


blueprint = Blueprint("admin", __name__, url_prefix="/admin")


@blueprint.route("/")
@auth_required()
@permissions_accepted("admin")
def dashboard():
    """Dashboard.
    """
    return render_template_string("Hello admin")


@blueprint.route("/user")
@auth_required()
@permissions_accepted("user-profile")
def user():
    """User Dashboard.
    """
    return render_template_string("Hello user")


@blueprint.route("/game")
@auth_required()
@permissions_required("user-profile", "user-game")
def game():
    """Game Dashboard.
    """
    return render_template_string("Hello game")
