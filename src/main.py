import argparse
from os import PathLike

from commands.add.add import add
from commands.prop.prop import set_props
from commands.run.run import run
from commands.set.set import set_server
from commands.version.version import version

parser = argparse.ArgumentParser()

parser.add_argument('command', help="input command(run, set, props, add).")
parser.add_argument('--input', "-i", help="input file option.", type=PathLike)
args = parser.parse_args()

if args.command == "set" :
    set_server()

if args.command == "run" :
    run()

if args.command == "props" :
    set_props()

if args.command == "add" :
    add(args.input)

if args.command == "version" :
    version()