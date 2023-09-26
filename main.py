import typer
import matplotlib.pyplot as plt
import numpy as np

app = typer.Typer()

def create_heatmap(data, color_backgrounds):
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

                ax.add_patch(plt.Rectangle((j, len(data) - 1 - i), 1, 1, fill=True, color=(r, g, b)))
                ax.text(j + 0.5, len(data) - 1 - i + 0.5, cell_text, ha='center', va='center', fontsize=10, color='black')

        # Hide axis labels
        ax.axis('off')

        # Display the heatmap
        plt.show()

    except Exception as e:
        typer.echo(f"Error: {e}")
        raise typer.Abort()

@app.command()
def heatmap():
    """
    Show risk heatmap for yearn strategy groups
    """
    # Define data matrix and color mapping
    data_matrix = [
        [["string1", "string2", "string3"], "string2", "string3", "string4", "string5"],
        ["string6", "string7", "string8", "string9", "string10"],
        ["string11", "string12", "string13", "string14", "string15"],
        ["string16", "string17", "string18", "string19", "string20"],
        ["string21", "string22", "string23", "string24", "string25"],
    ]

    color_matrix = [
        [1, 1, 2, 2, 2],
        [0, 1, 1, 2, 2],
        [0, 0, 1, 1, 2],
        [0, 0, 0, 1, 1],
        [0, 0, 0, 0, 1],
    ]

    create_heatmap(data_matrix, color_matrix)

@app.command(name="strategy")
def strategy_data():
    """
    List information about a specific strategy
    """
    print("Strategy Data")

if __name__ == "__main__":
    app()

