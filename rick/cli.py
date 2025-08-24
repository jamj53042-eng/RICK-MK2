import cmd
from .rpg import RPGSystem

class RickCLI(cmd.Cmd):
    intro = "Rick MK2 online! 🚀\nType 'help' for commands."
    prompt = ">>> "

    def __init__(self, debug=False):
        super().__init__()
        self.rpg = RPGSystem()
        self.debug = debug

    def do_status(self, arg):
        """Show current status."""
        print(self.rpg.status())

    def do_challenge(self, arg):
        """Attempt a challenge: challenge [easy|medium|hard]"""
        if not arg:
            print("Usage: challenge [easy|medium|hard]")
            return
        print(self.rpg.attempt_challenge(arg.strip()))

    def do_results(self, arg):
        """Show recent results."""
        print(self.rpg.get_results())

    def do_perks(self, arg):
        print("Available perks: quick_learner, lucky, strong")  # static for now

    def do_unlock(self, arg):
        if arg.strip() in ["quick_learner", "lucky", "strong"]:
            self.rpg.perks.append(arg.strip())
            print(f"Perk unlocked: {arg.strip()}")
        else:
            print("Unknown perk.")

    def do_exit(self, arg):
        """Exit the program."""
        return True

def main():
    RickCLI().cmdloop()
