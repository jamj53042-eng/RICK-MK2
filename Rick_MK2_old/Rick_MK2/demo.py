from .core import StreakTracker, LogManager

def main():
    print("=== Rick MK2 Demo ===")
    tracker = StreakTracker()
    logger = LogManager(tracker)
    streak, bonus = tracker.get_status()
    print(f"[Status] Streak: {streak} days | Bonus: +{bonus}%")
    print(logger.add_entry("Completed Task A"))
    print("[Daily Summary] 2 tasks logged today.")
    print("[Weekly Summary] 12 tasks logged this week.")

if __name__ == "__main__":
    main()
