import dataclasses
import typing

from ..hamilton import (
    HamiltonCommand,
    HamiltonResponse,
    HamiltonStepReturnBlockDataPackage,
    HamiltonStepReturnDescriptionPackage,
)


@dataclasses.dataclass(frozen=True)
class LockUnlockFrontCoverResponse(HamiltonResponse):
    raw_cover_lock_status_flag_as_block_data: str
    cover_lock_status_flag_as_block_data: HamiltonStepReturnBlockDataPackage = dataclasses.field(init=False)

    raw_cover_lock_status_flag: str
    cover_lock_status_flag: HamiltonStepReturnDescriptionPackage = dataclasses.field(init=False)

    def __post_init__(self):
        object.__setattr__(
            self,
            "cover_lock_status_flag_as_block_data",
            HamiltonStepReturnBlockDataPackage.parse_raw_step_return(self.raw_cover_lock_status_flag_as_block_data),
        )
        object.__setattr__(
            self,
            "cover_lock_status_flag",
            HamiltonStepReturnDescriptionPackage.parse_raw_step_return(self.raw_cover_lock_status_flag),
        )


@dataclasses.dataclass(kw_only=True, frozen=True)
class LockUnlockFrontCover(HamiltonCommand):
    front: typing.Literal["unlocked", "locked"] = "locked"

    def as_dict(self) -> dict:
        command_dict = super().as_dict()

        command_dict["front"] = self.front

        return command_dict

    def parse_response(self, data: dict) -> LockUnlockFrontCoverResponse:
        return LockUnlockFrontCoverResponse(
            command_id=data["command_id"],
            raw_cover_lock_status_flag_as_block_data=data["raw_cover_lock_status_flag_as_block_data"],
            raw_cover_lock_status_flag=data["raw_cover_lock_status_flag"],
        )
