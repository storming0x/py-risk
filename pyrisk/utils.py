import os
import time
import json


# General utility functions


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


def save_to_json(data, filename):
    """
    Save data to a JSON file.

    Args:
        data: The data to be saved (should be JSON-serializable).
        filename (str): The name of the output JSON file.
    """
    with open(filename, "w") as json_file:
        json.dump(data, json_file, indent=4)
    print(f"Data saved to {filename}")
