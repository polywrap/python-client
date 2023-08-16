# Polywrap Python Client Examples

This directory contains examples of how to use the Polywrap Python client.

## Running the Examples

### Install Dependencies

```
poetry install
```

> NOTE: if you don't have Poetry installed, you can follow the instructions [here](https://python-poetry.org/docs/#installation).

### Run the Examples

```
poetry run pytest
```

> We are using markdown_pytest plugin to run the examples. You can find more information about it [here](https://pypi.org/project/markdown-pytest/).

### Run a Specific Example

```
poetry run pytest <example_name>
```

For example:

```
poetry run pytest ens.md
```
