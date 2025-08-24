from pyfiglet import Figlet
from rich.console import Console
from rich.panel import Panel
import time

console = Console()

def startup_sequence():
    console.clear()

    # Force a font that renders "R" properly
    fig = Figlet(font="slant")
    ascii_art = fig.renderText("RICK")

    console.print(Panel(ascii_art, border_style="cyan"))

    # Flashy sequence
    console.print("[cyan]Rick is waking up...[/cyan]")
    time.sleep(1)
    console.print("[green]Backbone systems online.[/green]")
    time.sleep(1)
    console.print("[magenta]Ready to evolve.[/magenta]")

if __name__ == "__main__":
    startup_sequence()
