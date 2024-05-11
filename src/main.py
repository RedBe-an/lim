import argparse

from commands.run.run import run
from commands.set.set import set_server


parser = argparse.ArgumentParser()

parser.add_argument('command', help="input command(run, set)")
args = parser.parse_args()

if args.command == "set" :
    set_server()

if args.command == "run" :
    run()

