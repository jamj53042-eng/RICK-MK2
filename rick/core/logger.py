import logging
import sys

class RickLogger:
    COLORS = {
        "DEBUG": "\033[94m",   # Blue
        "INFO": "\033[96m",    # Light Blue
        "WARNING": "\033[93m", # Yellow
        "ERROR": "\033[91m",   # Red
        "EVENT": "\033[95m",   # Magenta (Special events)
        "ENDC": "\033[0m"
    }

    def __init__(self, name="Rick", silent=False):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
        self.logger.addHandler(handler)
        self.silent = silent

    def _colorize(self, level, msg):
        return f"{self.COLORS.get(level, '')}{msg}{self.COLORS['ENDC']}"

    def debug(self, msg):
        if not self.silent:
            self.logger.debug(self._colorize("DEBUG", msg))

    def info(self, msg):
        if not self.silent:
            self.logger.info(self._colorize("INFO", msg))

    def warning(self, msg):
        self.logger.warning(self._colorize("WARNING", msg))

    def error(self, msg):
        self.logger.error(self._colorize("ERROR", msg))

    def event(self, msg):
        if not self.silent:
            self.logger.info(self._colorize("EVENT", f"[EVENT] {msg}"))
