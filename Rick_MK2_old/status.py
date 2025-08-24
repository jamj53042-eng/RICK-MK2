def show_status(mode="default"):
    if mode == "default":
        print("[Status] Streak: 3 days | Bonus: +15%")
    elif mode == "daily":
        print("[Daily Summary] 2 tasks logged today.")
    elif mode == "weekly":
        print("[Weekly Summary] 12 tasks logged this week.")
    else:
        print(f"[Status] Unknown mode: {mode}")
