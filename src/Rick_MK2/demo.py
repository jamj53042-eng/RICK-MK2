from Rick_MK2.rick import RickMK2

def run_demo():
    rick = RickMK2()
    print("\n--- Initial Status ---")
    print(rick.status())

    print("\n--- Logging a few tasks ---")
    rick.log("✔️ Completed Task A (+15%)")
    rick.log("✔️ Completed Task B (+20%)")
    rick.log("❌ Skipped Task C (streak reset risk)")

    print("\n--- Status After Logging (daily) ---")
    print(rick.status("daily"))

    print("\n--- Weekly Overview ---")
    print(rick.status("weekly"))

if __name__ == "__main__":
    run_demo()
