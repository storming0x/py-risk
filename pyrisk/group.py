from typing import Optional
import datetime
import typer
import altair as alt
import pandas as pd
from rich.table import Table
from pyrisk.network import Network
from pyrisk.group_utils import get_risk_group_data, create_data_matrix
from pyrisk.utils import cprint, save_to_json

def list_groups(chain_id:int=1) -> None:
    cprint(f"\nLoading groups for chain {Network.get_label(chain_id)}...", style='text')
    title = f"\nRisk Groups in {Network.get_label(chain_id)}"
    table = Table(title=title)
    table.add_column("Group", justify="left", style="cyan", no_wrap=True)
    table.add_column("TVL (USDC)", justify="right", style="green")
    table.add_column("Likelihood Avg. Score", justify="center", style="magenta")
    table.add_column("Impact Score", justify="center", style="bold red")

    try:
        group_data = get_risk_group_data(chain_id)
        sorted_group_data = sorted(group_data.values(), key=lambda x: x['tvl'], reverse=True)
        for group in sorted_group_data:
            formatted_tvl = '{:,.2f}'.format(group['tvl'])  
            table.add_row(group['label'], formatted_tvl, str(group['medianScore']), str(group['tvlImpact']))

        cprint(table)
          
    except Exception as e:
        cprint(f"\nError: {e}", style='error')
        raise typer.Abort()
    return None

def show_heatmap(chain_id:int=1) -> None:
    try:
        # Get and map risk data for heatmap
        groups = get_risk_group_data(chain_id)
        data = create_data_matrix(groups.values())
        
        # Define data matrix and color mapping
        color_matrix = [
            [1, 1, 2, 2, 2],
            [0, 1, 1, 2, 2],
            [0, 0, 1, 1, 2],
            [0, 0, 0, 1, 1],
            [0, 0, 0, 0, 1],
        ]
        
        color_meaning = {0: 'low', 1: 'med', 2: 'high'}

        chart_data = []

        for y, row in enumerate(data):
            for x, cell in enumerate(row):
                chart_data.append({'x': x, 'y': y, 'text': cell, 'color': color_meaning[color_matrix[y][x]]})

        base = (
            alt.Chart(pd.DataFrame(chart_data), width=800, height=800, title='risk heatmap')
            .encode(
                alt.X('x:O').axis(None),
                alt.Y('y:O').axis(None),
            )
        )

        heat = (
            base
            .mark_rect(strokeWidth=1, stroke='black')
            .encode(
                alt.Color('color:O').scale(scheme='redyellowgreen', reverse=True, domain=['low', 'med', 'high']),
            )
        )

        text = (
            base
            .mark_text(dy=-70)
            .encode(
                alt.Text('text:N')
            )
        )

        chart = heat + text
        # Get the current time with timezone information
        current_time = datetime.datetime.now(datetime.timezone.utc)
        filename = f'heatmap_chain_{chain_id}_{current_time}.html'

        chart.save(filename)
        cprint(f"\nSaved risk map chart to {filename}", style='text')


    except Exception as e:
        cprint(f"\nError: {e}", style='error')
        raise typer.Abort()

    return None