"""This module provides the command line interface for the py_risk package."""
# pyrisk/cli.py

from pyrisk.heatmap import show_heatmap
from typing import Optional

import typer

from pyrisk import __app_name__, __version__

app = typer.Typer(name=__app_name__, help="CLI tools for interacting with Yearn's Risk Framework in Python")

def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} version {__version__}")
        raise typer.Exit()
    
@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None, "--version", "-v",  help="Show the application's version and exit.", callback=_version_callback, is_eager=True
    ),
) -> None:
    """
    CLI tools for interacting with Yearn's Risk Framework in Python
    """
    return None

@app.command()
def heatmap():
    """
    Show risk heatmap for yearn strategy groups
    """
    show_heatmap()
