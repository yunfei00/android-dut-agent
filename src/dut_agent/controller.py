import re
import time

import uiautomator2 as u2

from .adb import AdbClient
from .models import CallState, DutState, ScreenState


class DutController:
    def __init__(self, serial: str | None = None):
        self.adb = AdbClient(serial)
        self.serial = self.adb.resolve_serial()
        self.ui = u2.connect(self.serial)

    def screen_on(self) -> None:
        self.ui.screen_on()
        self._wait_screen(True)

    def screen_off(self) -> None:
        self.ui.screen_off()
        self._wait_screen(False)

    def _wait_screen(self, expected: bool, timeout: float = 5.0) -> None:
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            if bool(self.ui.info.get("screenOn")) is expected:
                return
            time.sleep(0.2)
        raise RuntimeError(f"screen state did not become {expected}")

    def airplane_mode(self) -> bool | None:
        value = self.adb.shell("settings get global airplane_mode_on")
        if value in {"0", "1"}:
            return value == "1"
        return None

    def set_airplane_mode(self, enabled: bool) -> None:
        value = "1" if enabled else "0"
        state = "true" if enabled else "false"
        self.adb.shell(f"settings put global airplane_mode_on {value}")
        self.adb.shell(
            "am broadcast -a android.intent.action.AIRPLANE_MODE "
            f"--ez state {state}"
        )
        deadline = time.monotonic() + 5
        while time.monotonic() < deadline:
            if self.airplane_mode() is enabled:
                return
            time.sleep(0.2)
        raise RuntimeError("airplane mode command was not applied")

    def airplane_cycle(self, hold_seconds: float = 2.0) -> None:
        self.set_airplane_mode(True)
        time.sleep(hold_seconds)
        self.set_airplane_mode(False)

    def call_state(self) -> CallState:
        raw = self.adb.shell("dumpsys telecom")
        upper = raw.upper()
        for state in (CallState.RINGING, CallState.DIALING, CallState.ACTIVE):
            if state.value in upper:
                return state
        if "IDLE" in upper:
            return CallState.IDLE
        return CallState.UNKNOWN

    def state(self) -> DutState:
        screen = ScreenState.ON if bool(self.ui.info.get("screenOn")) else ScreenState.OFF
        return DutState(
            serial=self.serial,
            screen=screen,
            airplane_mode=self.airplane_mode(),
            call_state=self.call_state(),
        )
