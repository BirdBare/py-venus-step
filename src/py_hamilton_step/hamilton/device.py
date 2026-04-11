import asyncio
import json

from .command import HamiltonCommand, HamiltonResponseType
from .connection import HamiltonConnection

POLL_INTERVAL = 0.1  # seconds — tune to your device's typical response time


class HamiltonDevice:
    def __init__(self, connection: HamiltonConnection):
        self.connection = connection
        self.busy: bool = False

    async def execute_command(self, command: HamiltonCommand[HamiltonResponseType]) -> HamiltonResponseType:
        if self.busy:
            raise RuntimeError("Device is busy executing another command")

        await self.connection.send(f"{json.dumps(command.as_dict())}\n")

        if await self.connection.receive() != "CommandAccepted":
            raise RuntimeError(f"Command does not exist on the device: {HamiltonDevice.__name__}")

        self.busy = True

        while True:
            await self.connection.send("get_state\n")
            data = await self.connection.receive()
            if data != "Busy":
                break
            await asyncio.sleep(POLL_INTERVAL)  # yield to event loop instead of spinning

        self.busy = False

        response_data = json.loads(await self.connection.receive())

        if response_data["programmatic_error_description"] != "":
            raise RuntimeError(
                f"Error occurred while executing command: {response_data['programmatic_error_description']}",
            )

        del response_data["programmatic_error_description"]

        return command.parse_response(response_data)
