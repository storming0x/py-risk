"""This module provides the command line interface for the py_risk package."""
# pyrisk/cli.py
import typer
from pyrisk import group_cli

from typing import Optional

from pyrisk import __app_name__, __version__

app = typer.Typer(name=__app_name__, help="CLI tools for interacting with Yearn's Risk Framework in Python")

def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} version {__version__}")
        raise typer.Exit()
    
app.add_typer(group_cli.app, name="group", help="Commands for interacting with Yearn's Risk Groups")
    
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



