# copyright Ruben Decrop 2012 - 2015
# copyright Chessdevil Consulting BVBA 2015 - 2019

import importlib

class Settings():
    """
    simplified version of django settings handling
    creates attributes on self for all uppercase attributes in settings module
    """

    def __init__(self, settings_module):
        mod = importlib.import_module(settings_module)
        for setting in dir(mod):
            if setting.isupper():
                setting_value = getattr(mod, setting)
                setattr(self, setting, setting_value)

class SettingsProxy():
    """
    A lazy proxy loader for the settings object.
    delays loading of the settings module until needed
    """
    _wrapped = None

    def __init__(self, settings_module):
        """
        :param settings_module: the name in dot notation of the settings module
        """
        self._settings_module = settings_module

    def _setup(self):
        """
        Load the settings module pointed to by the environment variable. This
        is used the first time we need any settings at all, if the user has not
        previously configured the settings manually.
        """
        self._wrapped = Settings(self._settings_module)

    def __getattr__(self, name):
        if self._wrapped is None:
            self._setup()
        return getattr(self._wrapped, name)
