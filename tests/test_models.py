from dut_agent.models import CallState, NetworkState, ScreenState


def test_state_values_are_stable():
    assert ScreenState.ON.value == "ON"
    assert NetworkState.REGISTERED.value == "REGISTERED"
    assert CallState.ACTIVE.value == "ACTIVE"
