from typing import Optional
import datetime
import typer
import altair as alt
import pandas as pd
from pyrisk.group_utils import get_risk_group_data, map_group_to_matrix
from pyrisk.utils import get_console

console = get_console()

def show_heatmap(chain_id=1) -> None:
    try:
        # Get and map risk data for heatmap
        group_data = get_risk_group_data(chain_id)
        data = map_group_to_matrix(group_data)
        
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
        console.print(f"\nSaved risk map chart to {filename}", style='text')


    except Exception as e:
        console.print(f"Error: {e}", style='error')
        raise typer.Abort()

    return None




