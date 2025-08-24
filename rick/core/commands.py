class CommandRegistry:
    def __init__(self, logger):
        self.logger = logger
        self.commands = {}

    def register(self, name, func, description=""):
        self.commands[name] = {"func": func, "desc": description}
        self.logger.debug(f"Registered command: {name}")

    def run(self, name, *args):
        if name in self.commands:
            self.logger.info(f"Running command: {name}")
            return self.commands[name]["func"](*args)
        else:
            self.logger.warning(f"Unknown command: {name}")

    def list_commands(self):
        return {k: v["desc"] for k, v in self.commands.items()}
