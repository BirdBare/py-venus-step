import time

from src.py_hamilton_step.hamilton.command import HamiltonCommand
from src.py_hamilton_step.hamilton.connection import UnixSocketConnection
from src.py_hamilton_step.hamilton.device import HamiltonDevice

with UnixSocketConnection("/Users/birdbare/Parallels/venus-star") as connection:
    device = HamiltonDevice(connection)
    command = HamiltonCommand()

    while True:
        device.send_command(command)
        time.sleep(1)
