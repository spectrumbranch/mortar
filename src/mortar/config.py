"""
Application configuration.

This module manages the configuration for the application. If a configuration
file exists in ~/.config/mortar/config.toml, configuration is loaded from it.
Otherwise, the default configuration file is created in that location.
"""

import os
from os.path import exists

from mktech.config2 import BaseConfig, BaseModel
from mktech.path import Path

import mortar.log as log

_xdg_config_home = f"{os.environ['HOME']}/.config"
_xdg_data = f"{os.environ['HOME']}/.local/share/mortar"
_config_dir = f'{_xdg_config_home}/mortar'

_config_path = f'{_config_dir}/config.toml'


class SSH(BaseModel):
    """ SSH client configuration. """

    use_ssh: bool = False
    " If true, use SSH where relevant. "
    host: str | None = None
    " Hostname for remote SSH connections. "
    port: int = 22
    " Port for remote SSH connections. "


class Config(BaseConfig):
    """ Configuration for mortar. """

    data: str = _xdg_data
    " Directory used for application data. "

    log_level: str = 'WARNING'
    " Application logging level. "

    ssh: SSH = SSH()

    def __init__(self, toml_path: Path | str) -> None:
        super().__init__(toml_path)


# On module import, load configuration from an existing configuration file, if
# one exists. Otherwise, initialize configuration defaults and create the
# configuration file.

config = Config(_config_path)

log.set_level(config.log_level)

if not exists(_config_path):
    config.write(_config_path)
