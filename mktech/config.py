from typing import Any

import tomlkit as toml
from tomlkit import TOMLDocument
from tomlkit.container import Container
from tomlkit.items import Item


class Config:
    """ Build configuration file. """

    def __init__(self) -> None:
        self.config = TOMLDocument()

    @classmethod
    def from_file(cls, path: str) -> 'Config':
        """ Parse the configuration from an existing file. """

        ctx = cls()
        ctx._init_from_file(path)

        return ctx

    def toml(self) -> TOMLDocument:
        return self.config

    def write(self, path: str, mode: str = 'w') -> None:
        """ Write the configuration to a file. """

        config_toml = self.toml()

        with open(path, mode) as fi:
            if mode == 'a':
                fi.write('\n')

            fi.write(toml.dumps(config_toml))

    def _init_from_file(self, path: str) -> None:
        with open(path, 'r') as fi:
            self.config = toml.parse(fi.read())

    def __getitem__(self, key: str) -> Item | Container:
        return self.config[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.config[key] = value
