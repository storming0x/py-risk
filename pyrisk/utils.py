import os
import time

# General utils

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