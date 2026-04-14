import dataclasses
import typing

from ..venus import VenusCommand, VenusResponse, VenusStepReturnBlockDataPackage


@dataclasses.dataclass(frozen=True)
class Channel1000ulCoreGripGetPlateResponse(VenusResponse):
    raw_get_plate_data_with_recovery_details: str
    get_plate_data_with_recovery_details: VenusStepReturnBlockDataPackage = dataclasses.field(init=False)
    raw_channel_sequences_with_recovery_details: str
    channel_sequences_with_recovery_details: VenusStepReturnBlockDataPackage | None = dataclasses.field(init=False)

    def __post_init__(self):
        object.__setattr__(
            self,
            "get_plate_data_with_recovery_details",
            VenusStepReturnBlockDataPackage.parse_raw_step_return(self.raw_get_plate_data_with_recovery_details),
        )
        if self.raw_channel_sequences_with_recovery_details == "":
            object.__setattr__(self, "channel_sequences_with_recovery_details", None)
        else:
            object.__setattr__(
                self,
                "channel_sequences_with_recovery_details",
                VenusStepReturnBlockDataPackage.parse_raw_step_return(
                    self.raw_channel_sequences_with_recovery_details,
                ),
            )


_transport_mode_setting_by_name = {
    "Plate only": 0,
    "Lid only": 1,
    "Plate with lid": 2,
}


@dataclasses.dataclass(kw_only=True, frozen=True)
class Channel1000ulCoreGripGetPlateCommand(VenusCommand):
    transport_mode: typing.Literal["Plate only", "Lid only", "Plate with lid"] = "Plate only"
    plate_sequence_labware: str | None = None
    lid_sequence_labware: str | None = None

    # Gripper tool parameters
    gripper_tool_sequence_labware: str
    used_front_channel: typing.Literal[2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16] = 8

    # Grip parameters
    grip_height_mm: float = 3
    grip_width_mm: float
    opening_width_before_access: float

    # Advanced
    # grip_force: typing.Literal[
    #    "Grip Force 1",
    #    "Grip Force 2",
    #    "Grip Force 3",
    #    "Grip Force 4",
    #    "Grip Force 5",
    #    "Grip Force 6",
    #    "Grip Force 7",
    #    "Grip Force 8",
    #    "Grip Force 9",
    # ] = "Grip Force 5"
    # Most likely does not apply if we overwrite the grip width...

    grip_speed_mm_per_s: float = 277.8
    z_speed_mm_per_s: float = 128.7
    check_if_plate_exists: bool = False

    def as_dict(self) -> dict:
        command_dict = super().as_dict()

        args = command_dict["args"]

        args["transport_mode"] = _transport_mode_setting_by_name[self.transport_mode]
        args["plate_sequence_labware"] = str(self.plate_sequence_labware)
        args["lid_sequence_labware"] = str(self.lid_sequence_labware)
        args["gripper_tool_sequence_labware"] = self.gripper_tool_sequence_labware
        args["used_front_channel"] = self.used_front_channel
        args["grip_height_mm"] = self.grip_height_mm
        args["grip_width_mm"] = self.grip_width_mm
        args["opening_width_before_access"] = self.opening_width_before_access
        args["grip_speed_mm_per_s"] = self.grip_speed_mm_per_s
        args["z_speed_mm_per_s"] = self.z_speed_mm_per_s
        args["check_if_plate_exists"] = int(self.check_if_plate_exists)

        return command_dict

    @staticmethod
    def parse_response(data: dict) -> Channel1000ulCoreGripGetPlateResponse:
        return Channel1000ulCoreGripGetPlateResponse(
            command_id=data["command_id"],
            raw_get_plate_data_with_recovery_details=data["raw_get_plate_data_with_recovery_details"],
            raw_channel_sequences_with_recovery_details=data["raw_channel_sequences_with_recovery_details"],
        )
