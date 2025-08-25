import argparse
import json
import os
import sys
from .core import Logger, export_csv, DATA_FILE
# --- emoji/printing helpers ---
def _can_emoji():
    enc = getattr(sys.stdout, "encoding", None) or ""
    return "utf" in enc.lower()

def _print(s: str, *, allow_emoji: bool = True):
    if not allow_emoji or not _can_emoji():
        s = s.encode("ascii", "ignore").decode("ascii")
        s = s.lstrip()
    print(s)
# --- end helpers ---

# Prevent re-running in same process
_ALREADY_RAN = False

def main():
    global _ALREADY_RAN
    if _ALREADY_RAN:
        return
    _ALREADY_RAN = True

    parser = argparse.ArgumentParser(prog="Rick_MK2")
    subparsers = parser.add_subparsers(dest="command")

    # status
    sp_status = subparsers.add_parser("status", help="Show status. Add optional: daily|weekly|full")
    sp_status.add_argument("--json", action="store_true", help="JSON output (machine-readable)")
    sp_status.add_argument("--quiet", action="store_true", help="Suppress non-essential text")
    sp_status.add_argument("--no-emoji", action="store_true", help="Force ASCII-only output")
    sp_status.add_argument("scope", nargs="?", default="summary", choices=["summary", "daily", "weekly", "full"])
    sp_status.add_argument("--compact", action="store_true", help="Compact one-line output")

    # log
    sp_log = subparsers.add_parser("log", help="Add a manual log entry (wrap in quotes)")
    sp_log.add_argument("entry", type=str)
    sp_log.add_argument("--tag", type=str, help="Optional tag for this log entry")

    # undo
    sp_undo = subparsers.add_parser("undo", help="Remove last N log entries (default 1)")
    sp_undo.add_argument("count", nargs="?", type=int, default=1)

    # reset
    sp_reset = subparsers.add_parser("reset", help="Reset streak|log|all (asks for confirmation)")
    sp_reset.add_argument("scope", choices=["streak", "log", "all"])

    # search
    sp_search = subparsers.add_parser("search", help="Search logs by keyword or tag")
    sp_search.add_argument("--from", dest="from_date", type=str, help="Inclusive date YYYY-MM-DD")
    sp_search.add_argument("--to", dest="to_date", type=str, help="Inclusive date YYYY-MM-DD")
    sp_search.add_argument("--fail-empty", action="store_true", help="Exit with code 2 if no results")
    sp_search.add_argument("--json", action="store_true", default=argparse.SUPPRESS, help="JSON output (machine-readable)")
    sp_search.add_argument("--quiet", action="store_true", default=argparse.SUPPRESS, help="Suppress non-essential text")
    sp_search.add_argument("--no-emoji", action="store_true", default=argparse.SUPPRESS, help="Force ASCII-only output")
    sp_search.add_argument("--tag", type=str)
    sp_search.add_argument("--text", type=str)
    sp_search.add_argument("--compact", action="store_true", help="Compact numbered output")
    sp_search.add_argument("--limit", type=int, default=0, help="Limit number of results")

    # export
    sp_export = subparsers.add_parser("export", help="Export logs to CSV")
    sp_export.add_argument("--path", type=str, default="logs_export.csv", help="Output CSV path")

    # help
    subparsers.add_parser("help", help="Show help")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return

    logger = Logger()

    if args.command == "status":
        # compact one-liner (early exit)
        if args.compact:
            if DATA_FILE.exists():
                data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
                logs = data.get("logs", [])
                n = len(logs)
                if n == 0:
                    print("logs:0")
                else:
                    last = logs[-1]
                    tag = last.get("tag")
                    tag_part = f" [tag: {tag}]" if tag else ""
                    print(f'logs:{n} | last:{last.get("time","")} | "{last.get("text","")}"{tag_part}')
            else:
                print("logs:0")
            raise SystemExit(0)  # EARLY EXIT in compact mode

        # JSON (machine-readable)
        if getattr(args, "json", False):
            data = json.loads(DATA_FILE.read_text(encoding="utf-8")) if DATA_FILE.exists() else {}
            logs = data.get("logs", [])
            last = logs[-1] if logs else None
            payload = {"total": len(logs), "last": last}
            print(json.dumps(payload, ensure_ascii=False))
            return

        # pretty (respect --quiet and --no-emoji)
        out = logger.show_status(args.scope)
        if not getattr(args, "quiet", False):
            _print(out or "No status available.", allow_emoji=not getattr(args, "no_emoji", False))
        return

    elif args.command == "log":
        logger.add_log(args.entry, args.tag)
        print(f"✅ Logged: {args.entry}" + (f" [tag: {args.tag}]" if args.tag else ""))
        return

    elif args.command == "undo":
        try:
            logger.undo(args.count)
            print(f"🗑️ Removed last {args.count} log(s).")
        except Exception as e:
            print(f"❌ Undo failed: {e}")
        return

    elif args.command == "reset":
        try:
            logger.reset(args.scope)
            print(f"♻️ Reset: {args.scope}")
        except Exception as e:
            print(f"❌ Reset failed: {e}")
        return

    elif args.command == "search":
        results = logger.search_logs(tag=args.tag, text=args.text)

        # Optional date range filter (inclusive)
        if getattr(args, "from_date", None) or getattr(args, "to_date", None):
            from datetime import datetime as _dt
            fd = None
            td = None
            try:
                fd = _dt.strptime(args.from_date, "%Y-%m-%d").date() if args.from_date else None
                td = _dt.strptime(args.to_date, "%Y-%m-%d").date() if args.to_date else None
            except Exception:
                fd = fd or None; td = td or None  # ignore bad inputs silently
            if fd or td:
                _filtered = []
                for r in results:
                    try:
                        d = _dt.strptime(r.get("time",""), "%Y-%m-%d %I:%M %p").date()
                    except Exception:
                        continue
                    if fd and d < fd: 
                        continue
                    if td and d > td: 
                        continue
                    _filtered.append(r)
                results = _filtered

        # Optional limit
        if getattr(args, "limit", 0):
            results = results[: max(args.limit, 0)]

        n = len(results)

        # Compact mode
        if args.compact:
            if not getattr(args, "quiet", False):
                print(f"found:{n}")
                if results:
                    for i, r in enumerate(results, 1):
                        txt = r.get("text","")
                        time = r.get("time","")
                        tag = r.get("tag")
                        tag_part = f" [tag: {tag}]" if tag else ""
                        print(f"{i}) {txt}{tag_part} ({time})")
            if getattr(args, "fail_empty", False) and n == 0:
                raise SystemExit(2)
            raise SystemExit(0)

        # JSON mode
        if getattr(args, "json", False):
            print(json.dumps({"found": n, "results": results}, ensure_ascii=False))
            if getattr(args, "fail_empty", False) and n == 0:
                raise SystemExit(2)
            return

        # Pretty text
        if not getattr(args, "quiet", False):
            _print(f"🔎 Found {n} logs:", allow_emoji=not getattr(args, "no_emoji", False))
            if results:
                for r in results:
                    txt = r.get("text","")
                    time = r.get("time","")
                    tag = r.get("tag")
                    tag_part = f" [tag: {tag}]" if tag else ""
                    print(f"- {txt} [{time}]{tag_part}")

        if getattr(args, "fail_empty", False) and n == 0:
            raise SystemExit(2)
        return

    elif args.command == "export":
        try:
            export_csv(args.path)
            print(f"✅ Exported logs to: {args.path}")
        except Exception as e:
            print(f"❌ Export failed: {e}")
        return

    elif args.command == "help":
        parser.print_help()
        return

    # Fallback
    parser.print_help()

if __name__ == "__main__":
    main()










