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


class NetworkState(str, Enum):
    REGISTERED = "REGISTERED"
    SEARCHING = "SEARCHING"
    OUT_OF_SERVICE = "OUT_OF_SERVICE"
    POWER_OFF = "POWER_OFF"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True)
class DutState:
    serial: str
    screen: ScreenState
    airplane_mode: bool | None
    network_state: NetworkState
    call_state: CallState
