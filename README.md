# Android DUT Agent

Android DUT scene-control layer for instrument automation.

## Goals

Provide a stable Python API/CLI for controlling Android DUTs while keeping test logic (CMW500/LTE/WCDMA/GSM) outside this repository.

## Backend

- ADB: device discovery and system-level actions
- uiautomator2: UI/app automation
- dumpsys/telecom: call and device-state observation
- Root/vendor adapters: optional fallbacks for lab DUTs

## Initial scenarios

- SCREEN_ON
- SCREEN_OFF
- AIRPLANE_RECONNECT

Planned: GSM MO/MT call, answer/hangup, app scenarios, network registration checks and reusable composite scenarios.

## Install

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .
```

Connect a phone with USB debugging enabled, then:

```powershell
adb devices
dut-agent status
dut-agent screen-on
dut-agent screen-off
dut-agent airplane-cycle
```

> Airplane-mode control varies by Android version/vendor and permission/root state. The controller verifies state and fails explicitly instead of assuming a command succeeded.
