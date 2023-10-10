# PyRisk

Cli tools for interacting with [Yearn's](https://yearn.fi) Risk Framework in Python

## Dependencies

- [python3](https://www.python.org/downloads) version 3.8 up to 3.11.

## Installation

### via `pip`

TBD

### via `setuptools`

You can clone the repository and use [`setuptools`](https://github.com/pypa/setuptools) for the most up-to-date version:

```bash
$ git clone https://github.com/storming0x/py-risk
$ cd py-risk
$ python3 setup.py install
```

## Quick Usage

To get help on pyrisk usage on any command you can use

```bash
pyrisk [command] --help
```

List all risk groups in the ethereum network

```bash
pyrisk group list --network ethereum
```

Show detail information about a risk group

```bash
pyrisk group info <group-id> --network ethereum
```

List all strategies related to a risk group

```bash
pyrisk group strats <group-id> --network ethereum
```

To generate an HTML file with the risk group map graph for the ethereum network (chain id = 1) you can use the following command. Check help for other supported networks.

```bash
pyrisk group map --network ethereum
```

To show information about a specific strategy. Supports v2 and v3 strategies.

```bash
pyrisk strat info <strategy-address> [OPTIONS]
```

To show information about a specific vault. Supports v2 and v3 Tokenized Strategies and Meta Vaults.

```bash
pyrisk vault info <vault-address> [OPTIONS]
```

## Development

TBD

## Acknowledgements

TBD
