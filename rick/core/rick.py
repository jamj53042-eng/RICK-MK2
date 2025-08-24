import time
from rick.core.logger import RickLogger
from rick.core.commands import CommandRegistry

BANNER = r"""
 ____  _       _   _     _ 
|  _ \(_) __ _| |_| |__ (_)
| |_) | |/ _` | __| '_ \| |
|  _ <| | (_| | |_| | | | |
|_| \_\_|\__,_|\__|_| |_|_|
                            
           A I
"""

class Rick:
    def __init__(self, silent=False):
        self.logger = RickLogger(silent=silent)
        self.commands = CommandRegistry(self.logger)
        self.alive = False
        self._register_default_commands()

    def _register_default_commands(self):
        self.commands.register("shutdown", self.shutdown, "Shut Rick down")
        self.commands.register("cleanup", self.cleanup, "Perform cleanup tasks")
        self.commands.register("list", self.list_commands, "List available commands")
        self.commands.register("help", self.list_commands, "Alias for list")

    def boot(self):
        # Flashy boot banner
        for line in BANNER.splitlines():
            if line.strip():
                self.logger.event(line)
                time.sleep(0.05)
        self.logger.event("Boot sequence initiated...")
        time.sleep(0.5)
        self.alive = True
        self.logger.info("Rick is online and ready! Type 'list' to see commands.")

    def shutdown(self):
        self.logger.event("Rick is shutting down...")
        time.sleep(0.4)
        self.alive = False
        self.logger.info("Rick is offline. Bye!")

    def cleanup(self):
        self.logger.debug("Performing cleanup...")
        # Placeholder for real cleanup logic
        time.sleep(0.2)
        self.logger.info("Cleanup complete.")

    def list_commands(self):
        cmds = self.commands.list_commands()
        self.logger.info("Available commands:")
        for name, desc in cmds.items():
            self.logger.info(f" - {name}: {desc}")
