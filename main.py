import typer
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

app = typer.Typer()

def create_heatmap():
    """
    Generate a heatmap with hardcoded cell colors and content.
    """
    try:
        # Define hardcoded colors (Green, Yellow, Red)
        color_mapping = {
            "Green": (0, 255, 0),
            "Yellow": (255, 255, 0),
            "Red": (255, 0, 0),
        }

        # Define cell-to-color mapping (0: Green, 1: Yellow, 2: Red)
        color_backgrounds = [
            [1, 1, 2, 2, 2],
            [0, 1, 1, 2, 2],
            [0, 0, 1, 1, 2],
            [0, 0, 0, 1, 1],
            [0, 0, 0, 0, 1],
        ]

        # Create a 5x5 matrix with random data (replace with your data if needed)
        data = np.random.rand(5, 5)

        # Create a heatmap using Seaborn
        sns.set()
        ax = sns.heatmap(data, annot=True, fmt=".2f", cmap="YlGnBu", cbar=False)

        # Customize cell background colors based on the cell-to-color mapping
        for i in range(5):
            for j in range(5):
                color_index = color_backgrounds[i][j]
                color = color_mapping["Green"]  # Default to Green
                if color_index == 1:
                    color = color_mapping["Yellow"]
                elif color_index == 2:
                    color = color_mapping["Red"]
                r, g, b = color
                ax.add_patch(plt.Rectangle((j, i), 1, 1, fill=True, color=(r/255, g/255, b/255)))

        # Display the heatmap
        plt.show()

    except Exception as e:
        typer.echo(f"Error: {e}")
        raise typer.Abort()

@app.command()
def run():
    """
    Generate a heatmap with hardcoded cell colors and content.
    """
    create_heatmap()

if __name__ == "__main__":
    app()
