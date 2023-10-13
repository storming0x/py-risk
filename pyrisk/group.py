from typing import Optional, Dict
from datetime import datetime
import typer
import altair as alt
import pandas as pd
import webbrowser
import os
from rich.table import Table
from rich.align import Align
from rich import print as rprint
from rich.layout import Layout
from rich.panel import Panel
from rich.console import Console, Group
from rich.text import Text
from rich import box

from pyrisk.network import Network
from pyrisk.group_utils import get_risk_group_data, create_data_matrix, format_score
from pyrisk.display_utils import cprint, format_currency


def list_groups(chain_id: int = 1, force_refresh=False) -> None:
    cprint(f"\nLoading groups for chain {Network.get_label(chain_id)}...", style="text")
    title = f"\nRisk Groups on {Network.get_label(chain_id)}"
    table = Table(title=title)
    table.add_column("Group", justify="left", style="cyan", no_wrap=True)
    table.add_column("TVL (USDC)", justify="right", style="green")
    table.add_column("Likelihood Avg. Score", justify="center", style="magenta")
    table.add_column("Impact Score", justify="center", style="bold red")
    table.add_column("Status", justify="center")
    table.add_column("Strategies w/ Debt", justify="right")

    try:
        group_data = get_risk_group_data(chain_id, force_refresh)
        sorted_group_data = sorted(
            group_data.values(), key=lambda x: x["tvl"], reverse=True
        )
        for group in sorted_group_data:
            formatted_tvl = "{:,.2f}".format(group["tvl"])
            status_color = group["status"].lower()
            status_emoji = f":{status_color}_circle:"
            # Filter out strategies with 0 estimatedTotalAssets
            filtered_strategies = list(
                filter(
                    lambda x: x.get("details", {}).get("totalDebt", 0) != "0",
                    group["strategies"],
                )
            )
            total_strategies = len(filtered_strategies)
            table.add_row(
                group["label"],
                formatted_tvl,
                str(group["medianScore"]),
                str(group["tvlImpact"]),
                status_emoji,
                str(total_strategies),
            )

        cprint(table)

    except Exception as e:
        cprint(f"\nError: {e}", style="error")
        raise typer.Abort()
    return None


def list_group_strategies(group_id: str, chain_id: int = 1, force_refresh=False):
    print(
        f"\nLoading strategies for risk group '{group_id}' on {Network.get_label(chain_id)}..."
    )
    try:
        groups = get_risk_group_data(chain_id, force_refresh)
        group = groups.get(group_id)
        if group is None:
            cprint(
                f"\nError: information for group '{group_id}' not found on {Network.get_label(chain_id)}",
                style="error",
            )
            return None
        else:
            strategies = group["strategies"]
            total_strategies = len(strategies)
            # Sort the filtered strategies by totalDebt in descending order
            sorted_strategies = sorted(
                strategies,
                key=lambda x: int(x.get("details", {}).get("totalDebt", 0)),
                reverse=True,
            )
            table = Table(
                title=f"Strategies in Risk Group '{group_id}' ({total_strategies})"
            )
            table.add_column("Name", justify="left", style="white", no_wrap=True)
            table.add_column("Address", justify="left", style="white", no_wrap=True)
            table.add_column("Total Debt", justify="right", style="white")
            for strategy in sorted_strategies:
                table.add_row(
                    strategy["name"],
                    strategy["address"],
                    strategy.get("details", {}).get("totalDebt", 0),
                )
            cprint(table)

    except Exception as e:
        cprint(f"\nError: {e}", style="error")
        raise typer.Abort()

    return None


def show_group_info(group_id: str, chain_id: int = 1, force_refresh=False) -> None:
    print(
        f"\nLoading information for risk group '{group_id}' on {Network.get_label(chain_id)}..."
    )
    try:
        groups = get_risk_group_data(chain_id, force_refresh)
        group = groups.get(group_id)
        if group is None:
            cprint(
                f"\nError: information for group '{group_id}' not found on {Network.get_label(chain_id)}",
                style="error",
            )
            return None
        else:
            _render_group_info_layout(group)
            # cprint(group)

    except Exception as e:
        cprint(f"\nError: {e}", style="error")
        raise typer.Abort()

    return None

    cprint(
        f"\nLoading {group} information on chain {Network.get_label(chain_id)}...",
        style="text",
    )


def show_heatmap(chain_id: int = 1, force_refresh=False) -> None:
    try:
        # Get and map risk data for heatmap
        groups = get_risk_group_data(chain_id, force_refresh)
        data = create_data_matrix(groups.values())

        # Define data matrix and color mapping
        color_matrix = [
            [1, 1, 2, 2, 2],
            [0, 1, 1, 2, 2],
            [0, 0, 1, 1, 2],
            [0, 0, 0, 1, 1],
            [0, 0, 0, 0, 1],
        ]

        color_meaning = {0: "low", 1: "med", 2: "high"}

        chart_data = []

        for y, row in enumerate(data):
            for x, cell in enumerate(row):
                chart_data.append(
                    {
                        "x": x,
                        "y": y,
                        "text": cell,
                        "color": color_meaning[color_matrix[y][x]],
                    }
                )

        base = alt.Chart(
            pd.DataFrame(chart_data), width=800, height=800, title="risk heatmap"
        ).encode(
            alt.X("x:O").axis(None),
            alt.Y("y:O").axis(None),
        )

        heat = base.mark_rect(strokeWidth=1, stroke="black").encode(
            alt.Color("color:O").scale(
                scheme="redyellowgreen", reverse=True, domain=["low", "med", "high"]
            ),
        )

        text = base.mark_text(dy=-70).encode(alt.Text("text:N"))

        chart = heat + text
        # Get the current time with timezone information
        current_time = datetime.datetime.now(datetime.timezone.utc)
        temp_f = f"heatmap_chain_{chain_id}_{current_time}"
        filename = "".join(c if c.isalnum() or c in ["_", "-"] else "_" for c in temp_f)
        filename += ".html"

        chart.save(filename)
        cprint(f"\nOpening risk map chart {filename} on browser ", style="text")
        cprint(
            f"\nIf the chart does not open automatically, please open it manually in your browser",
            style="info",
        )
        cprint(f"path: {os.path.abspath(filename)}", style="text")
        webbrowser.open(f"file://{os.path.abspath(filename)}")

    except Exception as e:
        cprint(f"\nError: {e}", style="error")
        raise typer.Abort()

    return None


def _render_group_info_layout(group: Dict) -> None:
    strategies = group["strategies"]
    layout = Layout()

    layout.split_column(Layout(name="header"), Layout(name="footer"))
    layout["header"].split_row(
        Layout(name="left"),
        Layout(name="right"),
    )

    _build_risk_scores_layout(group, layout)
    _build_impact_layout(group, layout)
    _build_strategies_layout(strategies, layout)

    # strategies has a table with 3 columns: name, address and totalEstimatedAssets
    table = Table(group["label"], title=f"Risk Group Info")
    table.add_column("Field", justify="left", style="cyan", no_wrap=True)

    rprint(layout)


def _build_risk_scores_layout(group, layout):
    group_label = group["label"]
    risk_score_section_title = (
        f"Yearn :blue_circle: Risk Scores for [b]{group_label}[/b]"
    )
    grid = Table.grid(expand=True)
    grid.add_column(justify="left", ratio=1)
    grid.add_column(justify="center", ratio=1)
    grid.add_row(f"[b]Audit [/b] :white_check_mark:", format_score(group["auditScore"]))
    grid.add_row(
        f"[b]Code Review [/b] :face_with_monocle:",
        format_score(group["codeReviewScore"]),
    )
    grid.add_row(f"[b]Testing[/b] :microscope:", format_score(group["testingScore"]))
    grid.add_row(
        f"[b]Protocol Safety[/b] :shield:", format_score(group["protocolSafetyScore"])
    )
    grid.add_row(f"[b]Complexity[/b] :brain:", format_score(group["complexityScore"]))
    grid.add_row(
        f"[b]Team Knowledge[/b] :handshake:", format_score(group["teamKnowledgeScore"])
    )
    grid.add_row(f"[b]Longevity[/b] :hourglass:", format_score(group["longevityScore"]))
    grid.add_row(Text("─" * 20, style="bold white on blue"))
    grid.add_row(f"[b]Median Score[/b] ", format_score(group["medianScore"]))

    header_panel = Panel(grid, title=risk_score_section_title, style="white on blue")
    layout["left"].update(header_panel)


def _build_impact_layout(group, layout):
    impact_section_title = f"Impact for [b]{group['label']}[/b]"
    grid = Table.grid(expand=True)
    grid.add_column(justify="left", ratio=1)
    grid.add_column(justify="center", ratio=1)
    grid.add_row(f"[b]TVL[/b] :dollar:", format_currency(group["tvl"]))
    grid.add_row(f"[b]TVL Impact[/b] ", format_score(group["tvlImpact"]))
    status_color = group["status"].lower()
    status_emoji = f":{status_color}_circle:"
    grid.add_row(f"[b]Status[/b] ", status_emoji)

    header_panel = Panel(grid, title=impact_section_title, style="white on blue")
    layout["right"].update(header_panel)


def _build_strategies_layout(strategies, layout):
    # Filter the strategies with non-zero totalDebt
    filtered_strategies = list(
        filter(lambda x: x.get("details", {}).get("totalDebt", 0) != "0", strategies)
    )

    # Sort the filtered strategies by totalDebt in descending order
    sorted_strategies = sorted(
        filtered_strategies,
        key=lambda x: int(x.get("details", {}).get("totalDebt", 0)),
        reverse=True,
    )

    strategies_section_title = f"Strategies (Total {len(strategies)})"
    table = Table(title="Strategies in Risk Group")

    # Set a fixed width for the "Name" column (adjust the width as needed)
    table.add_column("Name", justify="left", style="white", no_wrap=True)

    table.add_column("Address", justify="left", style="white", no_wrap=True)
    table.add_column("Total Debt", justify="right", style="white")

    for strategy in sorted_strategies:
        table.add_row(
            strategy["name"],
            strategy["address"],
            strategy.get("details", {}).get("totalDebt", 0),
        )

    footer_panel = Panel(table, title=strategies_section_title, style="white on blue")
    layout["footer"].update(footer_panel)
