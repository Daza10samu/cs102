#! /usr/bin/env python3

import argparse
import pathlib

from life import GameOfLife
from life_gui import GUI


def main():
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument("--rows", "-r", type=int, default=20, help="Count of rows")
    argument_parser.add_argument("--cols", "-c", type=int, default=20, help="Count of cols")
    argument_parser.add_argument("--csize", type=int, default=40, help="Cell size")
    argument_parser.add_argument("--speed", type=float, default=10, help="Speed of game")
    argument_parser.add_argument("--rand", action="store_true", default=False, help="Random grid")
    argument_parser.add_argument(
        "--max_gen", type=float, default=float("inf"), help="Max generation count"
    )
    argument_parser.add_argument(
        "--source", type=str, default="", help="Path to file with first generation"
    )
    argument_parser.add_argument("--spath", type=str, default="grid", help="Path to save file")
    args = argument_parser.parse_args()
    if args.source != "":
        life = GameOfLife.from_file(pathlib.Path(args.source))
    else:
        life = GameOfLife(
            size=(args.rows, args.cols), randomize=args.rand, max_generations=args.max_gen
        )
    console = GUI(life, cell_size=args.csize, save_path=args.spath, speed=args.speed)
    console.run()


if __name__ == "__main__":
    main()
