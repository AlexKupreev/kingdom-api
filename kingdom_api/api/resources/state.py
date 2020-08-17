from datetime import datetime
from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required

from kingdom_api.api.schemas import InputSchema, StateSchema
from kingdom_api.models import Game, State
from kingdom_api.extensions import db
from kingdom_api.commons.pagination import paginate
from kingdom_api.services.state import StateService, StateGameEndException


class StateResource(Resource):
    """Single object resource
    ---
    get:
      tags:
        - api
      parameters:
        - in: path
          name: state_id
          schema:
            type: integer
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  state: StateSchema
        404:
          description: state does not exist
    put:
      tags:
        - api
      parameters:
        - in: path
          name: state_id
          schema:
            type: integer
      requestBody:
        content:
          application/json:
            schema:
              StateSchema
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: state updated
                  state: StateSchema
        404:
          description: state does not exists
    delete:
      tags:
        - api
      parameters:
        - in: path
          name: state_id
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
                    example: state deleted
        404:
          description: state does not exist
    """

    # method_decorators = [jwt_required]

    def get(self, game_id, state_id):
        schema = StateSchema()
        state = State.query.get_or_404(state_id)
        return {"state": schema.dump(state)}


class StateList(Resource):
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
                          $ref: '#/components/schemas/StateSchema'
    post:
      tags:
        - api
      requestBody:
        content:
          application/json:
            schema:
              StateSchema
      responses:
        201:
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: new state
                  state: StateSchema
    """

    # method_decorators = [jwt_required]

    def get(self, game_id):
        Game.query.get_or_404(game_id)

        schema = StateSchema(many=True)
        query = State.query.filter_by(game_id=game_id)
        return paginate(query, schema)

    def post(self, game_id):
        """User move."""
        input_schema = InputSchema()
        user_input = input_schema.load(request.json)

        game = Game.query.get_or_404(game_id)

        num_states = 1
        last_items = State.query.filter_by(game_id=game_id).order_by(db.desc(State.id))\
            .limit(num_states).all()
        if len(last_items) < 1:
            raise RuntimeError("Empty state items list.")
        last_state = last_items[0]
        last_state.reaction_move = str(input_schema.dump(user_input))

        schema = StateSchema()
        try:
            state = StateService.fill_state(State(), game.settings, user_input, [last_state])
            game.updated = datetime.now()
            game.states.append(state)

            db.session.commit()
        except StateGameEndException:
            return {"msg": "game completed", "state": schema.dump(last_state)}, 200

        return {"msg": "new state", "state": schema.dump(state)}, 201
