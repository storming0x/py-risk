import typer
from pyrisk.group import (
    show_heatmap,
    list_groups,
    show_group_info,
    list_group_strategies,
)
from pyrisk.display_utils import show_spinner
from pyrisk.network import Network, NetworkLabels
from typing import Optional

app = typer.Typer()


@app.command()
@show_spinner("Loading...")
def list(
    ctx: typer.Context,
    network: NetworkLabels = NetworkLabels.ETHEREUM.value,
):
    """
    List risk groups
    """
    network_choice = Network[
        network.upper()
    ]  # Convert input to uppercase for case-insensitive matching
    list_groups(network_choice.value)


@app.command()
@show_spinner("Loading...")
def info(
    ctx: typer.Context,
    group_id: str,
    network: NetworkLabels = NetworkLabels.ETHEREUM.value,
):
    """
    Show information for risk group
    """
    network_choice = Network[
        network.upper()
    ]  # Convert input to uppercase for case-insensitive matching
    show_group_info(group_id, network_choice.value)


@app.command()
@show_spinner("Loading...")
def strats(
    ctx: typer.Context,
    group_id: str,
    network: NetworkLabels = NetworkLabels.ETHEREUM.value,
):
    """
    Show all strategies for a risk group
    """
    network_choice = Network[
        network.upper()
    ]  # Convert input to uppercase for case-insensitive matching
    list_group_strategies(group_id, network_choice.value)


@app.command()
@show_spinner("Loading heatmap...")
def heatmap(
    ctx: typer.Context,
    network: NetworkLabels = NetworkLabels.ETHEREUM.value,
):
    """
    Show heatmap for yearn risk groups on a given network
    """
    network_choice = Network[
        network.upper()
    ]  # Convert input to uppercase for case-insensitive matching
    show_heatmap(network_choice.value)
