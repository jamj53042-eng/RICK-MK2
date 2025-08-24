from rich.console import Console
from rich.logging import RichHandler
import logging

console = Console()

def get_logger(name: str):
    logging.basicConfig(
        level="NOTSET", 
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(console=console)]
    )
    logger = logging.getLogger(name)

    # Add custom levels for fun
    logging.addLevelName(25, "SUCCESS")
    def success(self, message, *args, **kwargs):
        if self.isEnabledFor(25):
            self._log(25, message, args, **kwargs)
    logging.Logger.success = success

    return logger
