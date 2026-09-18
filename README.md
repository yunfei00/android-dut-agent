# Android DUT Agent

Android DUT scene-control layer for instrument automation.

## Goals

Provide a stable Python API/CLI for controlling Android DUTs while keeping test logic (CMW500/LTE/WCDMA/GSM) outside this repository.

## Backend

- ADB: device discovery and system-level actions
- uiautomator2: UI/app automation
- dumpsys telephony/telecom: network and call-state observation
- Root/vendor adapters: optional fallbacks for lab DUTs

## Current capabilities

- SCREEN_ON / SCREEN_OFF
- AIRPLANE_RECONNECT
- Cellular registration state and wait
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

## Phase 2 validation

```powershell
uv run dut-agent status
uv run dut-agent wait-network --timeout 60

uv run dut-agent airplane-cycle --hold 2 --timeout 60
uv run dut-agent status

uv run dut-agent dial 10086
uv run dut-agent status
uv run dut-agent hangup
```

For an incoming call:

```powershell
uv run dut-agent status
uv run dut-agent answer
uv run dut-agent status
uv run dut-agent hangup
```

> Android vendors expose telephony state differently. Phase 2 deliberately verifies real state and fails explicitly. Hardware validation will determine whether vendor/root adapters are needed.

## Architecture boundary

This repository owns DUT actions and reusable DUT scenarios. CMW500 SCPI commands, sensitivity algorithms, BLER decisions and test orchestration remain in the instrument automation project.
