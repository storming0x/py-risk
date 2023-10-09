import typer
from pyrisk.heatmap import show_heatmap
from pyrisk.utils import show_spinner
from pyrisk.network import Network, NetworkLabels
from typing import Optional

app = typer.Typer()

@app.command()
def list(
      network:  NetworkLabels = NetworkLabels.ETHEREUM.value,
):
    """
    List risk groups
    """
    print(f"TBD: Listing risk groups for {network}")

@app.command()
def info(
      group: str,
      network:  NetworkLabels = NetworkLabels.ETHEREUM.value,
):
    """
    Show information for risk group
    """
    print(f"TBD: Showing info for risk group {group} on {network}")



@app.command()
@show_spinner("Loading heatmap...")
def heatmap(
      ctx: typer.Context,
      network:  NetworkLabels = NetworkLabels.ETHEREUM.value,
):
    """
    Show heatmap for yearn risk groups on a given network
    """
    network_choice = Network[network.upper()]  # Convert input to uppercase for case-insensitive matching
    show_heatmap(network_choice.value)