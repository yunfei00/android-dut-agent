from dataclasses import dataclass
from enum import Enum

from .controller import DutController


class ScenarioName(str, Enum):
    SCREEN_ON = "SCREEN_ON"
    SCREEN_OFF = "SCREEN_OFF"
    AIRPLANE_CYCLE = "AIRPLANE_CYCLE"


@dataclass
class ScenarioRunner:
    dut: DutController

    def run(self, name: ScenarioName, *, hold_seconds: float = 2.0) -> None:
        if name is ScenarioName.SCREEN_ON:
            self.dut.screen_on()
        elif name is ScenarioName.SCREEN_OFF:
            self.dut.screen_off()
        elif name is ScenarioName.AIRPLANE_CYCLE:
            self.dut.airplane_cycle(hold_seconds)
        else:
            raise ValueError(f"unsupported scenario: {name}")
