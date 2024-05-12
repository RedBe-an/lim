import argparse

from commands.prop.prop import set_props
from commands.run.run import run
from commands.set.set import set_server


parser = argparse.ArgumentParser()

parser.add_argument('command', help="input command(run, set)")
parser.add_argument('-f', help="output file")
args = parser.parse_args()

if args.command == "set" :
    set_server()

if args.command == "run" :
    run()

if args.command == "prop" :
    set_props()
