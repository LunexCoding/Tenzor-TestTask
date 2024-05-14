from pathlib import Path

from decouple import config


class _SettingsConfig:
    def __init__(self):
        self.__settingsConfigDB = self.__loadSettingsDB()

    def __loadSettingsDB(self):
        __settings = {}
        __settings["LOG"] = dict(
            file=config("LOG_FILE"),
            directory=config("LOG_DIRECTORY")
        )
        __settings["DRIVERS"] = dict(
            directory=config("DRIVERS_DIRECTORY"),
            chrome=Path(config("DRIVERS_DIRECTORY")) / config("CHROME_DRIVER"),
            firefox=Path(config("DRIVERS_DIRECTORY")) / config("FIREFOX_DRIVER")
        )
        return __settings

    @property
    def LogSettings(self):
        return self.__settingsConfigDB["LOG"]

    @property
    def DriversSettings(self):
        return self.__settingsConfigDB["DRIVERS"]


g_settingsConfig = _SettingsConfig()
