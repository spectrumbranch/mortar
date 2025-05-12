"""
Use SSH remote sessions.

This module provides facilities to use SSH remote sessions. Copying files using
scp is supported, as is executing arbitrary commands over SSH.
"""

from enum import Enum, auto

from mortar import process
from mortar.process import CompletedProcess


class Command(Enum):
    """ Supported SSH operations. """

    SSH = auto()
    " Secure shell "
    SCP = auto()
    " Secure file copy "


class SSH:
    """ Execute SSH operations between the local host and a remote host. """
    def __init__(
        self, host: str | None = None, port: int | None = None
    ) -> None:
        self.host: str | None = host
        " Remote host name "
        self.port: int | None = port
        " Remote host port "

    def scp_to(self, local: str, remote: str) -> CompletedProcess[bytes]:
        """ Copy a file from the local host to the remote host. """

        args = self._build_args(Command.SCP, self.port)

        cmd = ['scp'] + args + [local, f'{self.host}:/{remote}']

        result = process.run(cmd)

        return result

    def scp_from(self, remote: str, local: str) -> CompletedProcess[bytes]:
        """ Copy a file from the remote host to the local host. """

        args = self._build_args(Command.SCP, self.port)

        cmd = ['scp'] + args + [f'{self.host}:/{remote}', local]

        result = process.run(cmd)

        return result

    def run(self, command: list[str]) -> CompletedProcess[bytes]:
        """
        Execute a command on the remote host over an SSH connection.

        command is a sequence representing the command name and its
        space-separated arguments.

        Return a CompletedProcess instance with the result.
        """

        args = self._build_args(Command.SSH, self.port)

        ssh_command = ['ssh'] + args + [self.host] + command

        return process.run(ssh_command)

    @staticmethod
    def _build_args(command: Command, port: int | None) -> list[str]:
        args = []

        if port is not None:
            if command == Command.SSH:
                args.append('-p')
            elif command == Command.SCP:
                args.append('-P')

            args.append(str(port))

        return args
