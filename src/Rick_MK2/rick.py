import argparse
from datetime import datetime
from .core import Logger

def main():
    parser = argparse.ArgumentParser(prog="Rick_MK2")
    subparsers = parser.add_subparsers(dest="command")

    # status
    sp_status = subparsers.add_parser("status", help="Show status. Add optional: daily|weekly|full")
    sp_status.add_argument("scope", nargs="?", default="summary")

    # log
    sp_log = subparsers.add_parser("log", help="Add a manual log entry (wrap in quotes)")
    sp_log.add_argument("entry", type=str)
    sp_log.add_argument("--tag", type=str, help="Optional tag for this log entry")

    # undo
    sp_undo = subparsers.add_parser("undo", help="Remove last N log entries (default 1)")
    sp_undo.add_argument("count", type=int, nargs="?", default=1)

    # reset
    sp_reset = subparsers.add_parser("reset", help="Reset streak|log|all (asks for confirmation)")
    sp_reset.add_argument("scope", type=str)

    # search
    sp_search = subparsers.add_parser("search", help="Search logs by keyword or tag")
    sp_search.add_argument("--tag", type=str, help="Filter by tag")
    sp_search.add_argument("--text", type=str, help="Filter by text keyword")

    # help
    subparsers.add_parser("help", help="Show help")

    args = parser.parse_args()
    logger = Logger()

    if args.command == "status":
        logger.show_status(args.scope)
    elif args.command == "log":
        logger.add_log(args.entry, args.tag)
    elif args.command == "undo":
        logger.undo(args.count)
    elif args.command == "reset":
        logger.reset(args.scope)
    elif args.command == "search":
        logger.search_logs(tag=args.tag, text=args.text)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
