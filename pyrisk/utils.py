import typer
import os
import time
from rich.progress import Progress, SpinnerColumn, TextColumn, TimeElapsedColumn
from rich.console import Console, Theme
from functools import wraps

app = typer.Typer()

theme = Theme({'success': 'bold green', 'error': 'bold red', 'info': 'bold blue', 'warning': 'bold yellow', 'text': 'bold white'})
console = Console(theme=theme)

# General utils

def get_console():
    return console


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
                console.print(f"\nDone!", style='success')
                console.print(f"Elapsed Time: {elapsed_time:.2f} seconds", style='info')
                return result
        return wrapper
    return decorator



def get_or_create_cli_dir_path():
    # Define the name of your hidden directory
    cli_directory_name = ".pyrisk"

    # Get the user's home directory
    user_home_directory = os.path.expanduser("~")

    # Create the hidden directory in the user's home directory
    cli_directory_path = os.path.join(user_home_directory, cli_directory_name)
    os.makedirs(cli_directory_path, exist_ok=True)

    return cli_directory_path

def current_timestamp():
    return int(time.time() * 1000)