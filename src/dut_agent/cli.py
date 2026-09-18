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
    args = parser.parse_args()

    dut = DutController(args.serial)
    if args.command == "status":
        print(asdict(dut.state()))
    elif args.command == "screen-on":
        ScenarioRunner(dut).run(ScenarioName.SCREEN_ON)
    elif args.command == "screen-off":
        ScenarioRunner(dut).run(ScenarioName.SCREEN_OFF)
    elif args.command == "airplane-cycle":
        dut.airplane_cycle(args.hold)
