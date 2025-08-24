import argparse

def main():
    parser = argparse.ArgumentParser(prog="rick")
    subparsers = parser.add_subparsers(dest="command")

    # status command
    sp_status = subparsers.add_parser("status", help="Show current streak and bonus")
    sp_status.set_defaults(func=lambda args: print("Status: streak=0, bonus=0"))

    # log command
    sp_log = subparsers.add_parser("log", help="Log a new task")
    sp_log.set_defaults(func=lambda args: print("Task logged!"))

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()
