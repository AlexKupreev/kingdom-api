import pytest

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
        StateService.change_state_on_user_move(
            settings, state, user_input
        )

    with pytest.raises(RuntimeError, match=r"cannot be negative"):
        state.army = 10
        user_input = {
            "increase_army": -15,
            "increase_population": 0
        }
        StateService.change_state_on_user_move(
            settings, state, user_input
        )


def test_calculate_battle_results():
    settings = Settings()
    state = State()

    settings.win_probability = 0.5

    # no army/enemies
    state.army = 0
    state.enemies = 0
    winner_flag, army_killed, enemies_killed = StateService.calculate_battle_results(
        settings, state, lambda: 0)

    assert winner_flag == 0
    assert army_killed == 0
    assert enemies_killed == 0

    # no enemies
    state.army = 10
    state.enemies = 0
    winner_flag, army_killed, enemies_killed = StateService.calculate_battle_results(
        settings, state, lambda: 0)

    assert winner_flag == 1
    assert army_killed == 0
    assert enemies_killed == 0

    # no army
    state.army = 0
    state.enemies = 10
    winner_flag, army_killed, enemies_killed = StateService.calculate_battle_results(
        settings, state, lambda: 0)

    assert winner_flag == -1
    assert army_killed == 0
    assert enemies_killed == 0

    # army wins killall
    state.army = 10
    state.enemies = 2
    winner_flag, army_killed, enemies_killed = StateService.calculate_battle_results(
        settings, state, lambda: 0)

    assert winner_flag == 1
    assert army_killed == 0
    assert enemies_killed == 2

    # enemies win killall
    state.army = 3
    state.enemies = 10
    winner_flag, army_killed, enemies_killed = StateService.calculate_battle_results(
        settings, state, lambda: 0.7)

    assert winner_flag == -1
    assert army_killed == 3
    assert enemies_killed == 0

    def rand_generator(input_list):
        for item in input_list:
            yield item

    # army is greater
    state.army = 2
    state.enemies = 1

    rnd = rand_generator([0.0, 0.1])
    winner_flag, army_killed, enemies_killed = StateService.calculate_battle_results(
        settings, state, lambda: next(rnd))

    assert winner_flag == 1
    assert army_killed == 0
    assert enemies_killed == 1

    state.army = 2
    state.enemies = 1
    rnd = rand_generator([0.8, 0.0])
    winner_flag, army_killed, enemies_killed = StateService.calculate_battle_results(
        settings, state, lambda: next(rnd))

    assert winner_flag == 1
    assert army_killed == 1
    assert enemies_killed == 1

    state.army = 2
    state.enemies = 1
    winner_flag, army_killed, enemies_killed = StateService.calculate_battle_results(
        settings, state, lambda: 0.8)

    assert winner_flag == -1
    assert army_killed == 2
    assert enemies_killed == 0
