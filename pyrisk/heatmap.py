from typing import Optional
import typer
import altair as alt
import pandas as pd
from pyrisk.risk_data import get_risk_data

def show_heatmap(chain_id=1) -> None:
    try:
        # Get risk data
        data = get_risk_data(chain_id)
        
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

        heat + text

    except Exception as e:
        typer.echo(f"Error: {e}")
        raise typer.Abort()

    return None




