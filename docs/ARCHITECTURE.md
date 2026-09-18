# Architecture

The project separates **atomic DUT actions** from **test orchestration**.

```text
cmw500_auto_test
      |
 scenario orchestration
      |
  DutController
   /    |     \
 ADB   u2   telecom
      |
 Android DUT
```

## Boundary

This repository does not contain CMW500 SCPI commands, sensitivity algorithms, BLER decisions, or instrument test results.

## Layers

1. Transport/device: ADB discovery, serial selection, uiautomator2 connection.
2. Atomic actions: screen, airplane mode, app/UI, call operations.
3. State observation: screen, airplane, call/network state.
4. Reusable DUT scenarios: compositions of atomic actions.
5. External orchestration: CMW500 decides when a scenario runs.

## Planned scenario families

- Display: screen on/off, unlock.
- Registration recovery: airplane cycle, wait for registration.
- Calls: GSM/WCDMA MO, MT, answer, hangup, wait active.
- Apps: launch/stop, UI actions, foreground/background.
- Workloads: video, download, game or product-specific scenarios.

Every action should verify its post-condition when practical. Vendor/root-specific behavior belongs behind adapters rather than in scenario logic.
