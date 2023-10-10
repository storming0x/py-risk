import typer
from pyrisk.display_utils import show_spinner, cprint
from pyrisk.network import Network, NetworkLabels

app = typer.Typer()


@app.command()
@show_spinner("Loading...")
def info(
    ctx: typer.Context,
    strat_address: str,
    network: NetworkLabels = NetworkLabels.ETHEREUM.value,
):
    """
    Show information about a specific strategy.
    """
    network_choice = Network[network.upper()]
    cprint(f"To be implemented", style="info")
