import typer
import time

from pyrisk.heatmap import show_heatmap
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
def heatmap(
      network:  NetworkLabels = NetworkLabels.ETHEREUM.value,

):
    """
    Show heatmap for yearn risk groups on a given network
    """

    start_time = time.time()

    network_choice = Network[network.upper()]  # Convert input to uppercase for case-insensitive matching
    show_heatmap(network_choice.value)

    end_time = time.time()

    print(f"Heatmap time elapsed: {end_time - start_time} seconds")