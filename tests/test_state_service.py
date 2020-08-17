import pytest

from flask import url_for
from kingdom_api.models import Settings, State
from kingdom_api.services.state import StateService


def test_change_state_on_user_move_army():

    settings = Settings()
    state = State()
    state.population = 100

    state.army = 10
    user_input = {
        "increase_army": 10,
        "increase_population": 0
    }
    updated_state = StateService.change_state_on_user_move(
        settings, state, user_input
    )
    assert updated_state.army == 20

    state.army = 10
    user_input = {
        "increase_army": "10",
        "increase_population": "0"
    }
    updated_state = StateService.change_state_on_user_move(
        settings, state, user_input
    )
    assert updated_state.army == 20

    state.army = 10
    user_input = {
        "increase_army": -5,
        "increase_population": 0
    }
    updated_state = StateService.change_state_on_user_move(
        settings, state, user_input
    )
    assert updated_state.army == 5

    state.army = 10
    user_input = {
        "increase_army": -10,
        "increase_population": 0
    }
    updated_state = StateService.change_state_on_user_move(
        settings, state, user_input
    )
    assert updated_state.army == 0

    with pytest.raises(RuntimeError, match=r"cannot be greater"):
        state.army = 10
        user_input = {
            "increase_army": 100,
            "increase_population": 0
        }
        updated_state = StateService.change_state_on_user_move(
            settings, state, user_input
        )

    with pytest.raises(RuntimeError, match=r"cannot be negative"):
        state.army = 10
        user_input = {
            "increase_army": -15,
            "increase_population": 0
        }
        updated_state = StateService.change_state_on_user_move(
            settings, state, user_input
        )
