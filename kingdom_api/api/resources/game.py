from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required

from kingdom_api.api.schemas import GameSchema
from kingdom_api.models import Game, Settings, State
from kingdom_api.extensions import db
from kingdom_api.commons.pagination import paginate
from kingdom_api.services.settings import SettingsService
from kingdom_api.services.state import StateService


class GameResource(Resource):
    """Single object resource
    ---
    get:
      tags:
        - api
      parameters:
        - in: path
          name: game_id
          schema:
            type: integer
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  game: GameSchema
        404:
          description: game does not exist
    put:
      tags:
        - api
      parameters:
        - in: path
          name: game_id
          schema:
            type: integer
      requestBody:
        content:
          application/json:
            schema:
              GameSchema
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: game updated
                  game: GameSchema
        404:
          description: game does not exists
    delete:
      tags:
        - api
      parameters:
        - in: path
          name: game_id
          schema:
            type: integer
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: game deleted
        404:
          description: game does not exist
    """

    # method_decorators = [jwt_required]

    def get(self, game_id):
        schema = GameSchema()
        game = Game.query.get_or_404(game_id)
        return {"game": schema.dump(game)}

    def put(self, game_id):
        schema = GameSchema(partial=True)
        game = Game.query.get_or_404(game_id)
        game = schema.load(request.json, instance=game)

        db.session.commit()

        return {"msg": "game updated", "game": schema.dump(game)}

    def delete(self, game_id):
        game = Game.query.get_or_404(game_id)
        db.session.delete(game)
        db.session.commit()

        return {"msg": "game deleted"}


class GameList(Resource):
    """Creation and get_all
    ---
    get:
      tags:
        - api
      responses:
        200:
          content:
            application/json:
              schema:
                allOf:
                  - $ref: '#/components/schemas/PaginatedResult'
                  - type: object
                    properties:
                      results:
                        type: array
                        items:
                          $ref: '#/components/schemas/GameSchema'
    post:
      tags:
        - api
      requestBody:
        content:
          application/json:
            schema:
              GameSchema
      responses:
        201:
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: game created
                  game: GameSchema
    """

    # method_decorators = [jwt_required]

    def get(self):
        """Get paginated list of games"""
        schema = GameSchema(many=True)
        query = Game.query
        return paginate(query, schema)

    def post(self):
        """Create new game"""
        schema = GameSchema()
        game = schema.load(request.json)

        settings = SettingsService.initialize(Settings())
        settings.game = game

        state = StateService.fill_initial_state(State(), settings)
        game.states.append(state)

        db.session.add(game)
        db.session.add(settings)
        db.session.add(state)
        db.session.commit()

        return {"msg": "game created", "game": schema.dump(game)}, 201
