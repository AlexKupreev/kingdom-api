"""Settings Service"""
import os
import yaml

from flask import current_app

from kingdom_api.models.settings import Settings


class SettingsService:
    """Basic Settings logic."""

    INITIALS_ROOT = "initials"
    INITIALS = ["gold", "population", "army", "enemies"]

    GAME_SETTINGS_ROOT = "settings"
    GAME_SETTINGS = [
        "gold_earn",
        "gold_spent_worker",
        "gold_spent_army",
        "new_person_cost",
        "win_probability",
        "rob_default_probability",
        "rob_extra_probability",
        "enemy_gold",
        "enemy_increase",
        "enemy_decrease",
        "uncertain_gold",
        "uncertain_population",
        "uncertain_army",
    ]

    @classmethod
    def load_game_conf(cls) -> dict:
        """Load game configuration.

        :return: dict of settings
        """
        settings_file = current_app.config.get("GAME_SETTINGS_FILE")
        if not settings_file:
            raise RuntimeError("GAME_SETTINGS_FILE is not set")

        settings_file = os.path.join(os.path.dirname(current_app.instance_path),
                                     "kingdom_api",
                                     settings_file)
        if not os.path.isfile(settings_file):
            raise RuntimeError(f"Configuration file {settings_file} not found")

        with open(settings_file) as f:
            settings = yaml.safe_load(f)

        return settings

    @classmethod
    def initialize(cls, settings: Settings) -> Settings:
        """Init settings at the start from configuration.

        :param settings: Settings model
        :return: Settings model - filled with data
        """

        settings_obj = SettingsService.load_game_conf()

        for entry in SettingsService.GAME_SETTINGS:
            value = settings_obj.get(SettingsService.GAME_SETTINGS_ROOT, {}).get(
                entry, None
            )
            if value is None:
                raise RuntimeError(f"Entry {entry} is missing in settings.")

            setattr(settings, entry, value)

        for entry in SettingsService.INITIALS:
            value = settings_obj.get(SettingsService.INITIALS_ROOT, {}).get(entry, None)
            if value is None:
                raise RuntimeError(f"Entry {entry} is missing in settings.")

            settings.initials[entry] = value

        return settings
