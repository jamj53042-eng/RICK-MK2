import argparse
from .core import StreakTracker, LogManager

tracker = StreakTracker()
logger = LogManager(tracker)

def main():
    parser = argparse.ArgumentParser(prog="rick")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("status", help="Show current streak and bonus")
    log_parser = subparsers.add_parser("log", help="Log a new task")
    log_parser.add_argument("task", help="Task description")

    args = parser.parse_args()

    if args.command == "status":
        streak, bonus = tracker.get_status()
        print(f"[Status] Streak: {streak} days | Bonus: +{bonus}%")
        entries = logger.get_today_entries()
        if entries:
            print("[Today’s log]")
            for e in entries:
                print(" -", e)
        else:
            print("[Today’s log] No entries yet.")

    elif args.command == "log":
        entry = logger.add_entry(args.task)
        streak, bonus = tracker.get_status()
        print(f"[Log] Added entry: {entry}")
        print(f"[Updated] Streak: {streak} days | Bonus: +{bonus}%")

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
