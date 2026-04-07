import dataclasses
import typing

from ..hamilton import HamiltonCommand, HamiltonResponse


@dataclasses.dataclass(kw_only=True, frozen=True)
class LockUnlockFrontCover(HamiltonCommand):
    front: typing.Literal["unlocked", "locked"] = "locked"

    def as_dict(self) -> dict:
        command_dict = super().as_dict()

        command_dict["front"] = self.front

        return command_dict

    def parse_response(self, data: dict) -> HamiltonResponse: ...
