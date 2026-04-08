import dataclasses
import typing

from ..hamilton import HamiltonCommand, HamiltonResponse, HamiltonStepReturnBlockDataPackage


@dataclasses.dataclass(frozen=True)
class Channel1000ulTipPickupResponse(HamiltonResponse):
    raw_channel_sequences_with_recovery_data: str
    channel_sequences_with_recovery_data: HamiltonStepReturnBlockDataPackage = dataclasses.field(init=False)

    def __post_init__(self):
        object.__setattr__(
            self,
            "channel_sequences_with_recovery_data",
            HamiltonStepReturnBlockDataPackage.parse_raw_step_return(self.raw_channel_sequences_with_recovery_data),
        )


@dataclasses.dataclass(kw_only=True, frozen=True)
class ChannelConfig:
    channel_number: typing.Literal[1, 2, 3, 4, 5, 6, 7, 8]
    sequence_labware: str
    sequence_position: str


@dataclasses.dataclass(kw_only=True, frozen=True)
class Channel1000ulTipPickup(HamiltonCommand):
    channel_configs: tuple[ChannelConfig, ...]

    def as_dict(self) -> dict:
        command_dict = super().as_dict()

        # zip channel configs into associated lists
        command_dict["channel_number"] = [config.channel_number for config in self.channel_configs]
        command_dict["sequence_labware"] = [config.sequence_labware for config in self.channel_configs]
        command_dict["sequence_position"] = [config.sequence_position for config in self.channel_configs]

        return command_dict

    def parse_response(self, data: dict) -> Channel1000ulTipPickupResponse:
        return Channel1000ulTipPickupResponse(
            command_id=data["command_id"],
            raw_channel_sequences_with_recovery_data=data["raw_channel_sequences_with_recovery_data"],
        )
