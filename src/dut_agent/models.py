from dataclasses import dataclass
from enum import Enum


class ScreenState(str, Enum):
    ON = "ON"
    OFF = "OFF"
    UNKNOWN = "UNKNOWN"


class CallState(str, Enum):
    IDLE = "IDLE"
    DIALING = "DIALING"
    RINGING = "RINGING"
    ACTIVE = "ACTIVE"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True)
class DutState:
    serial: str
    screen: ScreenState
    airplane_mode: bool | None
    call_state: CallState
