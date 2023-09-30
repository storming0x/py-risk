""" Py Risk Entry point script"""
# pyrisk/__main__.py
from pyrisk import cli, __app_name__, __version__

def main():
    cli.app(prog_name=__app_name__)

if __name__ == "__main__":
    main()