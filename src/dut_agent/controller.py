import re
import time

import uiautomator2 as u2

from .adb import AdbClient
from .models import CallState, DutState, NetworkState, ScreenState


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
        return value == "1" if value in {"0", "1"} else None

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

    def network_state(self) -> NetworkState:
        raw = self.adb.shell("dumpsys telephony.registry")
        states = [int(x) for x in re.findall(r"mServiceState=(\d+)", raw)]
        if not states:
            states = [int(x) for x in re.findall(r"mVoiceRegState=(\d+)", raw)]
        if 0 in states:
            return NetworkState.REGISTERED
        if 2 in states:
            return NetworkState.SEARCHING
        if 3 in states:
            return NetworkState.POWER_OFF
        if 1 in states:
            return NetworkState.OUT_OF_SERVICE
        return NetworkState.UNKNOWN

    def wait_registered(self, timeout: float = 60.0, poll: float = 1.0) -> None:
        deadline = time.monotonic() + timeout
        last = NetworkState.UNKNOWN
        while time.monotonic() < deadline:
            last = self.network_state()
            if last is NetworkState.REGISTERED:
                return
            time.sleep(poll)
        raise RuntimeError(f"cellular network did not register within {timeout:g}s; last={last.value}")

    def airplane_cycle(
        self,
        hold_seconds: float = 2.0,
        wait_for_network: bool = True,
        register_timeout: float = 60.0,
    ) -> None:
        self.set_airplane_mode(True)
        time.sleep(hold_seconds)
        self.set_airplane_mode(False)
        if wait_for_network:
            self.wait_registered(register_timeout)

    def call_state(self) -> CallState:
        raw = self.adb.shell("dumpsys telecom")
        upper = raw.upper()
        for state in (CallState.RINGING, CallState.DIALING, CallState.ACTIVE):
            if state.value in upper:
                return state
        if "IDLE" in upper:
            return CallState.IDLE
        return CallState.UNKNOWN

    def wait_call_state(self, expected: CallState, timeout: float = 30.0) -> None:
        deadline = time.monotonic() + timeout
        last = CallState.UNKNOWN
        while time.monotonic() < deadline:
            last = self.call_state()
            if last is expected:
                return
            time.sleep(0.5)
        raise RuntimeError(f"call state did not become {expected.value}; last={last.value}")

    def dial(self, number: str, wait_active: bool = False, timeout: float = 30.0) -> None:
        if not re.fullmatch(r"[0-9+*#]+", number):
            raise ValueError("phone number contains unsupported characters")
        self.adb.shell(f"am start -a android.intent.action.CALL -d tel:{number}")
        if wait_active:
            self.wait_call_state(CallState.ACTIVE, timeout)

    def answer_call(self, timeout: float = 10.0) -> None:
        self.adb.shell("input keyevent KEYCODE_CALL")
        self.wait_call_state(CallState.ACTIVE, timeout)

    def hangup_call(self, timeout: float = 10.0) -> None:
        self.adb.shell("input keyevent KEYCODE_ENDCALL")
        self.wait_call_state(CallState.IDLE, timeout)

    def state(self) -> DutState:
        screen = ScreenState.ON if bool(self.ui.info.get("screenOn")) else ScreenState.OFF
        return DutState(
            serial=self.serial,
            screen=screen,
            airplane_mode=self.airplane_mode(),
            network_state=self.network_state(),
            call_state=self.call_state(),
        )
