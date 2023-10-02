from enum import Enum

class Network(Enum):
    ETHEREUM = 1
    OPTIMISM = 10
    FANTOM = 250
    ARBITRUM_ONE = 42161
    # POLYGON = 137

class NetworkLabels(str, Enum):
    ETHEREUM = "ethereum"
    OPTIMISM = "optimism"
    FANTOM = "fantom"
    ARBITRUM_ONE = "arbitrum_one"


# Custom callback function to convert string input to enum value
def network_callback(value):
    try:
        return Network[value.upper()]  # Convert input to uppercase for case-insensitive matching
    except KeyError:
        raise ValueError(f"Invalid network: {value}")
