import subprocess


class AdbError(RuntimeError):
    pass


class AdbClient:
    def __init__(self, serial: str | None = None):
        self.serial = serial

    def _base(self) -> list[str]:
        return ["adb"] + (["-s", self.serial] if self.serial else [])

    def run(self, *args: str, timeout: float = 15.0) -> str:
        proc = subprocess.run(
            self._base() + list(args),
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        if proc.returncode:
            raise AdbError(proc.stderr.strip() or proc.stdout.strip() or "adb failed")
        return proc.stdout.strip()

    def shell(self, command: str, timeout: float = 15.0) -> str:
        return self.run("shell", command, timeout=timeout)

    def resolve_serial(self) -> str:
        if self.serial:
            return self.serial
        lines = self.run("devices").splitlines()[1:]
        devices = [line.split()[0] for line in lines if line.strip().endswith("\tdevice")]
        if len(devices) != 1:
            raise AdbError(f"expected exactly one online DUT, found {len(devices)}")
        self.serial = devices[0]
        return self.serial
