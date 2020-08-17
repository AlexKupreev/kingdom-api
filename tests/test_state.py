from flask import url_for
from kingdom_api.models import Game, Settings, State
from kingdom_api.services.state import StateService


def test_create_state(app, client, db):

    game = Game()
    game.name = "test"

    settings = Settings()
    settings.game = game

    state = State()
    state.population = 100
    state.gold = 100
    state.army = 0
    state.enemies = 0
    game.states.append(state)

    db.session.add(game)
    db.session.add(settings)
    db.session.add(state)
    db.session.commit()

    game = db.session.query(Game).first()

    app.config["SERVER_NAME"] = "localhost.localdomain"

    with app.app_context():
        states_url = url_for("api.states", game_id=game.id, _external=False)

    # test bad data
    data = {"username": "created"}

    rep = client.post(states_url, json=data)
    assert rep.status_code == 400

    # test army increase
    data = {
        "increase_army": 20,
        "increase_population": 0
    }

    rep = client.post(states_url, json=data)
    assert rep.status_code == 201

    state = db.session.query(State).filter_by(game_id=game.id).order_by(db.desc(State.id)).first()

    assert state.army == 20
