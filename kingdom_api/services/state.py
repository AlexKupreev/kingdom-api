"""State Service"""
from math import floor
from random import seed, random
from typing import List

from kingdom_api.models.settings import Settings
from kingdom_api.models.state import State
from kingdom_api.api.schemas import InputSchema

# new type annotation
StatesList = List[State]


class StateService:
    """Basic State logic."""

    STATE_GOLD = "gold"
    STATE_POPULATION = "population"
    STATE_ARMY = "army"
    STATE_ENEMIES = "enemies"

    @classmethod
    def random_init(cls) -> None:
        """Initialize random generator"""
        seed()

    @classmethod
    def random(cls) -> float:
        """Generates random float value in [0.0 .. 1.0)"""
        return random()

    @classmethod
    def fill_state(
        cls,
        state: State,
        settings: Settings,
        user_input: InputSchema,
        last_states: StatesList,
    ) -> State:
        """Wrapper for generation of a state.

        :param state: State object to fill
        :param settings: Settings object
        :param user_input: InputSchema object
        :param last_states: list of last states
        :return: filled State object
        """

        if last_states is None or len(last_states) == 0:
            raise RuntimeError("No previous state exists.")

        # will update state based on a previous turn
        last_state = last_states[0]

        state.game_id = last_state.game_id
        state.gold = last_state.gold
        state.army = last_state.army
        state.enemies = last_state.enemies
        state.population = last_state.population

        state = StateService.change_state_on_user_move(settings, state, user_input)

        state.gold = StateService.calculate_gold(settings, state)
        state.enemies = StateService.calculate_enemies(settings, state)

        if StateService.is_robbing(settings, state):
            army_before = state.army
            # FIXME
            army_remained = StateService.calculate_army_after_battle(settings, state)
            if army_remained < 0:
                # all gold is robbed
                state.gold = 0.0
                state.army = 0
                state.notifications = f"{state.notifications}\nAll gold was robbed by enemies."
                state.population -= army_before
            else:
                state.army = floor(army_remained)
                army_killed = army_before - state.army
                state.population -= army_killed
                state.notifications = f"{state.notifications}\nRobbery attempt prevented by army," \
                                      f"{army_killed} soldiers killed :(."

        if StateService.is_game_failed(state, last_state):
            raise StateGameEndException("No money for further life.")

        return state

    @classmethod
    def fill_initial_state(cls, state: State, settings: Settings) -> State:
        """Wrapper for generation of a state.

        :param state: State object to fill
        :param settings: Settings object
        :return: filled State object
        """

        StateService.random_init()

        state.population = StateService.calculate_gold(settings)
        state.gold = StateService.calculate_gold(settings)
        state.enemies = StateService.calculate_enemies(settings)

        return state

    @classmethod
    def change_state_on_user_move(
        cls, settings: Settings, state: State, user_input: dict
    ) -> State:
        """Change state according to input data.

        :param settings: Settings obj
        :param state: State obj to update
        :param user_input: dict with user input
        :return: updated State
        """
        if user_input.get("increase_army"):
            new_army = state.army + int(user_input.get("increase_army"))
            if new_army < 0:
                raise RuntimeError("Army cannot be negative")
            elif state.population < new_army:
                raise RuntimeError("Army cannot be greater than population")
            else:
                state.army = new_army

        if user_input.get("increase_population"):
            increase = int(user_input.get("increase_population"))
            if increase > 0:
                if increase * settings.new_person_cost > state.gold:
                    available_people = floor(state.gold / settings.new_person_cost)
                    state.gold -= available_people * settings.new_person_cost
                    state.population += available_people
                    state.notifications = (
                        f"{state.notifications}\n"
                        f"Only {available_people} population added"
                    )
                else:
                    state.gold -= increase * settings.new_person_cost
                    state.population += increase

        return state

    @classmethod
    def calculate_gold(cls, settings: Settings, state: State = None) -> float:
        """Calculate amount of remaining gold.

        :param settings: Settings obj
        :param state: State obj
        :return: float
        """

        if state is None:
            return float(settings.initials[StateService.STATE_GOLD])

        working_population = state.population - state.army

        gold = (
            state.gold
            + working_population * settings.gold_earn
            - working_population * settings.gold_spent_worker
            - state.army * settings.gold_spent_army
        )

        return gold

    @classmethod
    def calculate_enemies(cls, settings: Settings, state: State = None) -> int:
        """Calculate enemies.

        :param settings: Settings obj
        :param state: State obj
        :return: float
        """

        if state is None:
            return int(settings.initials[StateService.STATE_ENEMIES])

        # number of enemies increases with free gold available
        # for every enemy as `enemy_gold`
        # and decreases slowly if there are less gold per enemy
        gold_for_existing_enemies = settings.enemy_gold * state.enemies
        gold_excess = state.gold - gold_for_existing_enemies
        if gold_excess > 0:
            enemies = state.enemies + floor(
                settings.enemy_increase * gold_excess / settings.enemy_gold
            )
        else:
            enemies = state.enemies + floor(
                settings.enemy_decrease * gold_excess / settings.enemy_gold
            )

        return int(enemies) if enemies > 0 else 0

    @classmethod
    def calculate_army_after_battle(cls, settings: Settings, state: State) -> int:
        """Calculate army remained after battle with enemies.

        :param settings: Settings object
        :param state: current State object
        :return: amount of soldiers
        """
        army_afterwards = state.army
        enemies_afterwards = state.enemies
        # go through enemies and check if they are killed
        battle_completed = False
        while not battle_completed:
            if enemies_afterwards <= 0:
                battle_completed = True

            for enemy in range(enemies_afterwards):
                rand_value = StateService.random()
                if army_afterwards > 0:
                    if rand_value < settings.win_probability:
                        enemies_afterwards -= 1
                    else:
                        army_afterwards -= 1

                if enemies_afterwards < 0 or army_afterwards < 0:
                    battle_completed = True
                    break

        return army_afterwards

    @classmethod
    def is_game_failed(cls, state: State, last_state: State) -> bool:
        """Is game failed.

        :param state: current State obj
        :param last_state: last State obj
        :return bool:
        """

        # game failed if there is no gold at a current and a previous state
        if state.gold <= 0.0 and last_state.gold <= 0.0:
            return True

        # game failed if there is no population on current state
        if state.population <= 0:
            return True

        return False

    @classmethod
    def is_robbing(cls, settings: Settings, state: State = None) -> bool:
        """Is robbing happens.

        :param settings: Settings obj
        :param state: State obj
        :return bool:
        """

        robbing_probability = settings.rob_default_probability
        # if enemies < army, default robbing probability applied
        # otherwise probability increases
        if state.enemies >= state.army:
            if state.army > 0:
                robbing_probability = settings.rob_default_probability + (
                    settings.rob_extra_probability * state.enemies / state.army
                )
            else:
                robbing_probability = settings.rob_default_probability \
                                      + settings.rob_extra_probability

        rand_value = StateService.random()
        if rand_value < robbing_probability:
            return True

        return False


class StateGameEndException(RuntimeError):
    pass
