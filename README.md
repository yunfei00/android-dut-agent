# Android DUT Agent

Android DUT scene-control layer for instrument automation.

## Goals

Provide a stable Python API/CLI for controlling Android DUTs while keeping test logic (CMW500/LTE/WCDMA/GSM) outside this repository.

## Backend

- ADB: device discovery and system-level actions
- uiautomator2: UI/app automation
- dumpsys telephony/telecom: diagnostic network/call-state observation
- Root/vendor adapters: optional fallbacks for lab DUTs

## Current capabilities

- SCREEN_ON / SCREEN_OFF
- AIRPLANE_RECONNECT
- Fast DUT reconnect primitive
- Diagnostic cellular registration observation
- Dial / answer / hang up
- Call-state observation

## Install with uv

```powershell
git clone https://github.com/yunfei00/android-dut-agent.git
cd android-dut-agent
uv sync
adb devices
uv run dut-agent status
```

## Fast reconnect

For CMW500 test flows, use reconnect as a DUT recovery action:

```powershell
uv run dut-agent reconnect
uv run dut-agent reconnect --hold 2 --recovery 3
```

The reconnect command only performs the radio recovery sequence:

```text
airplane ON -> hold -> airplane OFF -> recovery delay -> return
```

It deliberately does **not** claim the CMW500 link is valid. The instrument-side BR/BLER measurement is the authority for link validity and decides whether another reconnect attempt is required.

`wait-network` remains available for diagnostics:

```powershell
uv run dut-agent wait-network --timeout 60
```

Android telephony registry state may lag the real CMW500 link state, so it must not be used as the final pass/fail criterion for instrument tests.

## Call control

```powershell
uv run dut-agent dial 10086
uv run dut-agent status
uv run dut-agent hangup
```

For an incoming call:

```powershell
uv run dut-agent answer
uv run dut-agent status
uv run dut-agent hangup
```

## Architecture boundary

This repository owns DUT actions and reusable DUT scenarios. CMW500 SCPI commands, BR/BLER validation, sensitivity algorithms and test orchestration remain in the instrument automation project.
