from flask import Blueprint, current_app, jsonify
from flask_restful import Api
from marshmallow import ValidationError
from kingdom_api.extensions import apispec
from kingdom_api.api.resources import UserResource, UserList
from kingdom_api.api.schemas import UserSchema
from kingdom_api.api.resources import GameResource, GameList
from kingdom_api.api.schemas import GameSchema
from kingdom_api.api.resources import StateResource, StateList
from kingdom_api.api.schemas import StateSchema


blueprint = Blueprint("api", __name__, url_prefix="/api/v1")
api = Api(blueprint)


api.add_resource(UserResource, "/users/<int:user_id>", endpoint="user_by_id")
api.add_resource(UserList, "/users", endpoint="users")

api.add_resource(GameResource, "/game/<int:game_id>", endpoint="game_by_id")
api.add_resource(GameList, "/games", endpoint="games")

api.add_resource(StateResource, "/game/<int:game_id>/state/<int:state_id>", endpoint="state_by_id")
api.add_resource(StateList, "/game/<int:game_id>/states", endpoint="states")


@blueprint.before_app_first_request
def register_views():
    apispec.spec.components.schema("UserSchema", schema=UserSchema)
    apispec.spec.path(view=UserResource, app=current_app)
    apispec.spec.path(view=UserList, app=current_app)
    # TODO add games


@blueprint.errorhandler(ValidationError)
def handle_marshmallow_error(e):
    """Return json error for marshmallow validation errors.
    This will avoid having to try/catch ValidationErrors in all endpoints, returning
    correct JSON response with associated HTTP 400 Status (https://tools.ietf.org/html/rfc7231#section-6.5.1)
    """
    return jsonify(e.messages), 400
