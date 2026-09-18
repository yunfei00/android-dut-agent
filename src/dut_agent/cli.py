import argparse
from dataclasses import asdict

from .controller import DutController
from .scenarios import ScenarioName, ScenarioRunner


def main() -> None:
    parser = argparse.ArgumentParser(prog="dut-agent")
    parser.add_argument("--serial")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("status")
    sub.add_parser("screen-on")
    sub.add_parser("screen-off")

    cycle = sub.add_parser("airplane-cycle")
    cycle.add_argument("--hold", type=float, default=2.0)

    wait_net = sub.add_parser("wait-network")
    wait_net.add_argument("--timeout", type=float, default=60.0)

    dial = sub.add_parser("dial")
    dial.add_argument("number")
    dial.add_argument("--wait-active", action="store_true")
    dial.add_argument("--timeout", type=float, default=30.0)

    answer = sub.add_parser("answer")
    answer.add_argument("--timeout", type=float, default=10.0)

    hangup = sub.add_parser("hangup")
    hangup.add_argument("--timeout", type=float, default=10.0)

    args = parser.parse_args()
    dut = DutController(args.serial)

    if args.command == "status":
        print(asdict(dut.state()))
    elif args.command == "screen-on":
        ScenarioRunner(dut).run(ScenarioName.SCREEN_ON)
    elif args.command == "screen-off":
        ScenarioRunner(dut).run(ScenarioName.SCREEN_OFF)
    elif args.command == "airplane-cycle":
        ScenarioRunner(dut).run(ScenarioName.AIRPLANE_CYCLE, hold_seconds=args.hold)
    elif args.command == "wait-network":
        dut.wait_registered(args.timeout)
    elif args.command == "dial":
        dut.dial(args.number, args.wait_active, args.timeout)
    elif args.command == "answer":
        dut.answer_call(args.timeout)
    elif args.command == "hangup":
        dut.hangup_call(args.timeout)
