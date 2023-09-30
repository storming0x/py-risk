from typing import Optional
import typer
import matplotlib.pyplot as plt
import numpy as np

from pyrisk.risk_data import get_risk_data

def show_heatmap(chain_id=1) -> None:
    # Define data matrix and color mapping
    color_matrix = [
        [1, 1, 2, 2, 2],
        [0, 1, 1, 2, 2],
        [0, 0, 1, 1, 2],
        [0, 0, 0, 1, 1],
        [0, 0, 0, 0, 1],
    ]
    
    data_matrix = get_risk_data(chain_id)
    # Define row and column labels
    row_labels = ["Row 1", "Row 2", "Row 3", "Row 4", "Row 5"]
    column_labels = ["Rare", "Unlikely", "Even Chance", "Likely", "Almost Certain"]

    create_heatmap(data_matrix, color_matrix, row_labels, column_labels)

def create_heatmap(data, color_backgrounds, row_labels, column_labels) -> None:
    try:
        # Define colors (Green, Yellow, Red)
        color_mapping = {
            "Green": (0, 255, 0),
            "Yellow": (255, 255, 0),
            "Red": (255, 0, 0),
        }

        # Create a figure and axis
        fig, ax = plt.subplots(figsize=(6, 6))

        # Set axis limits
        ax.set_xlim(0, len(data[0]))
        ax.set_ylim(0, len(data))

        # Create a grid of cells with text content and colored backgrounds
        for i, row in enumerate(data):
            for j, cell_content in enumerate(row):
                if isinstance(cell_content, list):
                    # Join the list of strings into a single string with newlines
                    cell_text = "\n".join(cell_content)
                else:
                    cell_text = cell_content

                color_index = color_backgrounds[i][j]
                color = color_mapping["Green"]  # Default to Green
                if color_index == 1:
                    color = color_mapping["Yellow"]
                elif color_index == 2:
                    color = color_mapping["Red"]
                r, g, b = [c / 255 for c in color]

                # Draw the cell with borders
                cell = plt.Rectangle((j, len(data) - 1 - i), 1, 1, fill=True, color=(r, g, b), edgecolor='black')
                ax.add_patch(cell)
                ax.text(j + 0.5, len(data) - 1 - i + 0.5, cell_text, ha='center', va='center', fontsize=10, color='black')

        # Add lines separating each cell on the inside
        for i in range(1, len(data[0])):
            ax.axvline(i, color='black', linewidth=2)
        for i in range(1, len(data)):
            ax.axhline(i, color='black', linewidth=2)

        # Set tick labels for Y and X axes
        ax.set_xticks(np.arange(len(data[0])) + 0.5)
        ax.set_yticks(np.arange(len(data)) + 0.5)
        ax.set_xticklabels(column_labels, rotation=90)
        ax.set_yticklabels(row_labels)

        # Hide axis labels
        ax.axis('off')

        # Display the heatmap
        plt.show()

    except Exception as e:
        typer.echo(f"Error: {e}")
        raise typer.Abort()




