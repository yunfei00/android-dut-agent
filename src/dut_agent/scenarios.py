from dataclasses import dataclass
from enum import Enum

from .controller import DutController


class ScenarioName(str, Enum):
    SCREEN_ON = "SCREEN_ON"
    SCREEN_OFF = "SCREEN_OFF"
    AIRPLANE_RECONNECT = "AIRPLANE_RECONNECT"


@dataclass
class ScenarioRunner:
    dut: DutController

    def run(self, name: ScenarioName) -> None:
        if name is ScenarioName.SCREEN_ON:
            self.dut.screen_on()
        elif name is ScenarioName.SCREEN_OFF:
            self.dut.screen_off()
        elif name is ScenarioName.AIRPLANE_RECONNECT:
            self.dut.airplane_cycle(wait_for_network=True)
        else:
            raise ValueError(f"unsupported scenario: {name}")
