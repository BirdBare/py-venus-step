import json

from .command import HamiltonCommand
from .connection import HamiltonConnection


class HamiltonDevice:
    def __init__(self, connection: HamiltonConnection):
        self.connection = connection
        self._active_command: HamiltonCommand | None = None

    def send_command(self, command: HamiltonCommand):
        self._active_command = command
        self.connection.send(f"{json.dumps(command.as_dict())}\n")

    def get_response(self):
        if self._active_command is None:
            raise RuntimeError("No active command to get response")

        active_command = self._active_command
        self._active_command = None

        return active_command.parse_response(json.loads(self.connection.receive()))
