import typer
import time
from functools import wraps
from rich.text import Text
from rich.progress import Progress, SpinnerColumn, TextColumn, TimeElapsedColumn
from rich.console import Console, Theme

# Utilities for displaying information on the command line

app = typer.Typer()

theme = Theme(
    {
        "success": "bold green",
        "error": "bold red",
        "info": "bold blue",
        "warning": "bold yellow",
        "text": "bold white",
    }
)
console = Console(theme=theme)

cprint = console.print


# Custom decorator for showing a spinner with a custom task description
def show_spinner(task_description):
    def decorator(func):
        @wraps(func)
        def wrapper(ctx: typer.Context, *args, **kwargs):
            with Progress(
                SpinnerColumn(),
                TextColumn("[bold white]{task.description}"),
                transient=True,
            ) as progress:
                task = progress.add_task(description=task_description, total=None)
                with progress:
                    start_time = time.time()
                    result = func(ctx, *args, **kwargs)
                    elapsed_time = time.time() - start_time
                progress.remove_task(task)
                cprint(f"\nDone!", style="success")
                cprint(f"Elapsed Time: {elapsed_time:.2f} seconds", style="info")
                return result

        return wrapper

    return decorator


def format_currency(value):
    return Text(f"${value:,.2f}", style="bold green")
