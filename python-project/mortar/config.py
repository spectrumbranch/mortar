""" Application configuration.

This module manages the configuration for the application. If a configuration
file exists in ~/.config/mortar/config.toml, configuration is loaded from it.
Otherwise, the default configuration file is created in that location.
"""

from dataclasses import dataclass, field
import os
from os.path import exists
from typing import cast, Any, Optional

import tomlkit as toml
from tomlkit.items import Table

import mortar.log as log


_xdg_config_home = f"{os.environ['HOME']}/.config"
_xdg_data = f"{os.environ['HOME']}/.local/share/mortar"
_config_dir = f'{_xdg_config_home}/mortar'

_config_path = f'{_config_dir}/config.toml'


class BaseConfig:
    """ Build configuration file. """

    def init_from_file(self, path: str) -> None:
        with open(path, 'r') as fi:
            self.config = toml.parse(fi.read())

    @classmethod
    def from_file(cls, path: str) -> 'BaseConfig':
        """ Parse the configuration from an existing file. """

        ctx = cls()
        ctx.init_from_file(path)

        return ctx

    def write(self, path: str) -> None:
        """ Write the configuration to a file. """

        with open(path, 'w') as fi:
            fi.write(toml.dumps(self.config))

    def __getitem__(self, key: str) -> Any:
        return self.config[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.config[key] = value


@dataclass
class SSH:
    use_ssh: bool = False
    host: Optional[str] = None
    port: Optional[int] = 22

    def toml(self) -> Table:
        ssh = toml.table()

        ssh.add('use_ssh', self.use_ssh)

        if self.host is not None:
            ssh.add('host', self.host)
        if self.port is not None:
            ssh.add('port', self.port)

        return ssh


@dataclass
class Config(BaseConfig):
    data: Optional[str] = None

    log_level: str = 'WARNING'

    ssh: SSH = field(default_factory=SSH)

    def __post_init__(self) -> None:
        """ Initialize the configuration file with arguments. """

        super().__init__()

    @classmethod
    def from_file(cls, path: str) -> 'Config':
        """ Parse the configuration from an existing file. """

        with open(path, 'r') as fi:
            config = toml.parse(fi.read())

        if 'data' not in config:
            data = _xdg_data
        elif not isinstance(config['data'], str):
            raise Exception('str is expected.')
        else:
            data = config['data']

        if 'log_level' not in config:
            log_level = 'WARNING'
        elif not isinstance(config['log_level'], str):
            raise Exception('str is expected.')
        else:
            log_level = config['log_level']

        if not isinstance(config['ssh'], Table):
            raise Exception('Table is expected.')
        else:
            ssh = config['ssh']

            ctx = cls(
                data=data,
                log_level=log_level,
                ssh=SSH(
                    host=ssh.get('host'),
                    port=ssh.get('port')
                )
            )

            if isinstance(ssh['use_ssh'], bool):
                ctx.ssh.use_ssh = ssh['use_ssh']

        return ctx

    def write(self, path: str) -> None:
        """ Write the configuration to a file. """

        self.config = toml.document()

        root = cast(Table, self.config)

        if self.data is not None:
            root.add('data', str(self.data))
        if self.log_level is not None:
            root.add('log_level', str(self.log_level))

        root.add('ssh', self.ssh.toml())

        super().write(path)


if exists(_config_path):
    config = Config.from_file(_config_path)

    log.set_level(config.log_level)
else:
    config = Config()

    config.write(_config_path)
