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

To show the risk map for the ethereum network (chain id = 1) you can use the following command

```bash
pyrisk heatmap --network ethereum
```


TODO

To show information about a specific strategy. Supports v2 and v3 strategies.

```bash
pyrisk strategy [OPTIONS]
```

To show information about a specific vault. Supports v2 and v3 Tokenized Strategies and Meta Vaults.

```bash
pyrisk vault [OPTIONS]
```

## Development

TBD

## Acknowledgements

TBD