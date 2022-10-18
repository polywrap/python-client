![Public Release Announcement](https://user-images.githubusercontent.com/5522128/177473887-2689cf25-7937-4620-8ca5-17620729a65d.png)

# Polywrap Python Client

## [Polywrap](https://polywrap.io) is a developer tool that enables easy integration of Web3 protocols into any application. It makes it possible for applications on any platform, written in any language, to read and write data to Web3 protocols.


# Working Features

This MVP Python client enables the execution of **[WebAssembly](https://en.wikipedia.org/wiki/WebAssembly) Polywrappers** *(or just "wrappers")* on a python environment. It's built following the functionality of the [JavaScript Polywrap Client](https://github.com/polywrap/toolchain), which is currently more robust out and battle tested, as it has additional capabilities than this MVP.

In the future, the Polywrap DAO will continue improving this Python capabilities to reach feature parity with the JS stack, as well as the possibiity of creating WASM wrappers with Python code. 

Here you can see which features have been implemented on each language, and make the decision of which one to use for your project.

| Feature | [Python](https://github.com/polywrap/python-client) | [Javascript](https://github.com/polywrap/toolchain) | 
| -- | -- | -- |
| Invoke wrappers | yes | yes |
| polywrap-asyncify | replaced with wasmtime | yes |
| polywrap-uri-resolvers | legacy | refactored |
| polywrap-msgpack| yes, tested 100% | yes |
| Subinvoke | wip | yes |
| Wrap Manifest | WIP | yes |
| Client Config Builder Package | wip | yes |
| Interfaces | pending | yes |
| e2e Tests | tbd | no |
| Creating Plugins | tbd | yes |
| Creating Python Wrappers | in a future version | yes |
> TODO: Update table above according to test harness and maybe mention other wip clients


# Getting Started:

Have questions or want to get involved? Join our community [Discord](https://discord.polywrap.io) or [open an issue](https://github.com/polywrap/toolchain/issues) on Github.

For detailed information about Polywrap and the WRAP standard, visit our [developer documentation](https://docs.polywrap.io/).

## Pre-requisites

- Clone the repo. 
```
git clone https://github.com/polywrap/python-client
```

> ### `python ˆ3.10`
> - Make sure you're running the correct version of python by running: 
> ```
> which python3
> ```
> - If you are using a Linux system or WSL, which comes with Python3.8, then you will need to upgrade from Python3.8 to Python3.10 and also fix the `pip` and `distutil` as upgrading to Python3.10 will break them. You may follow [this guide](https://cloudbytes.dev/snippets/upgrade-python-to-latest-version-on-ubuntu-linux) to upgrade.

> ### `poetry ^1.1.14`
> - To install poetry follow [this guide](https://python-poetry.org/docs/#installation). If you are on MacOS then you can install poetry simply with the following homebrew command 
> ```
> brew install poetry
> ```
> - To make sure you're it's installed properly, run `poetry`
> - Learn more [here](https://python-poetry.org/docs/)



##  Building and Testing

### Poetry 

- We will be using [Poetry](https://python-poetry.org) for building and testing our packages. 
 Each of the package folders consists the `pyproject.toml` file and the `poetry.lock` file. In `pyproject.toml` file, one can find out all the project dependencies and configs related to the package. These files will be utilized by Poetry to install correct dependencies, build, lint and test the package.

- For example, we can **install** deps, **build** and **test** the `polywrap-msgpack` package using Poetry. 

- Install dependencies using Poetry. 
```
poetry install
```
> Make sure your cwd is `polywrap-msgpack` package.
- As we can see in the `pyproject.toml` file, we installed [PyTest](https://docs.pytest.org) package. We will be using the same as our testing framework. 
- Now we are ready to build and test the core package using Poetry and PyTest.
- To build the package run the following command
```
poetry build
```
- You need to activate the venv with poetry using `poetry shell` command before running any other command

### Pytest

In order to assure the integrity of the modules Polywrap Python Client uses [pytest 7.1.3](https://docs.pytest.org/en/7.1.x/contents.html) as a testing framework.

To run the tests locally, from the terminal `cd` into the appropriate module, for example `./toolchain/packages/py/polywrap-wasm` or `./toolchain/packages/py/polywrap-client`, and run this command:
 - `poetry shell` to start env
 - `poetry install` to have all dependencies locally
 - `poetry run pytest` to test your module 

This last command will run a series of scripts that verify that the specific module of the client is performing as expected in your local machine. The output on your console should look something like this:

```c
$ poetry run pytest
>>
================================= test session starts =================================
platform darwin -- Python 3.10.0, pytest-7.1.3, pluggy-1.0.0
rootdir: /Users/robertohenriquez/pycode/polywrap/toolchain/packages/py, configfile: pytest.ini
collected 26 items                                                                    

tests/test_msgpack.py ..........................                                [100%]
```

You should expect to see the tests passing with a 100% accuracy. To better understand and read these outputs, check [this quick guide](https://docs.pytest.org/en/7.1.x/how-to/output.html)

If anything fails (F), or if there are any Warnings raised, you can debug them by running a verbose version of the test suite:
- `poetry run pytests -v` or `poetry run pytests -vv` for even more detail
- Reach out to the devs on the Discord explaining your situation, and what configuration you're using on your machine.


### TOX 
- We are using `tox` to run lint and tests easily. 
- You can list all the testenv defined in the tox config with following command
```
tox -a
```
- To run tests using tox simply run `tox`
- You can run linters with the `tox -e lint` and check type with `tox -e typecheck`. By running `tox -e secure`, you can find security vulnerability if any.
- While developing, you can run `tox -e dev` and apply lint fixes and style formatting.
- As we see the mentioned tests passing, we are ready to update and test the package. 

## For VSCode users
If you use VSCode, open this setup using the workspace file `python-monorepo.code-workspace`:

```
File -> Open Workspace from File...
```
![File -> Open Workspace from File](misc/VScode_OpenWorkspaceFromFile.png)

Each folder is now a project to VSCode. For the Python virtual environments to be picked up automatically, you need to create .vscode/settings.json file in each folder, pointing to the in-project virtual environment created by the poetry.

You can easily find the correct virtual env by running following command in the package for which you want to find it
```
poetry shell
```

Once you get the virtual env, you need to create the following `settings.json` file under the .vscode folder of the given package. 
Ex: in case of polywrap-client package, it would be under:
```
polywrap-client -> .vscode -> settings.json
```

Here's the `settings.json` file we are using for configuring the vscode:
```json
{
  "python.formatting.provider": "black",
  "python.languageServer": "Pylance",
  "python.analysis.typeCheckingMode": "strict",
  "python.defaultInterpreterPath": "/Users/polywrap/Library/Caches/pypoetry/virtualenvs/polywrap-client-abcdef-py3.10"
}
```
You need to put your virtual env path you got from the poetry under: `python.defaultInterpreterPath`

Once you configure this you should be good to go.




## What WASM wrappers can you execute today?

Check these resources to browse a variety available wrappers, for DeFi, decentralised storage, and other development utilites:

- [Wrappers.io](https://wrappers.io/)
- [Polywrap Integrations Repository](https://github.com/polywrap/integrations)

# Example call

Calling a function of a wrapper from the python client is as simple as creating a file in the `xxx TBD` directory, importing the Polywrap Python Client, calling the Uri where the WASM wrapper is hosted, and specifying any required arguments.

```python
# get_eth_txns.py
from polywrap_client import PolywrapClient
from polywrap_core import Uri, InvokerOptions

async def get_eth_transactions(accountAddress):
    client = PolywrapClient()
    #uri = Uri("wrap://ens/defiwrapper.polywrap.eth")
    uri = Uri(f'fs/{Path(__file__).parent.joinpath("cases", "wrap.wasm").absolute()}')
    args = {
        "accountAddress": "'0x123EtherumAddress12312'"
    }
    options = InvokerOptions(uri=uri, method="simpleMethod", args=args, encode_result=False)
    result = await client.invoke(options)
    return result.result

if __name__ == "__main__":
    return get_eth_transactions(portfolio_address)
```


## Creating your own tests

    TODO: It is suggested to follow a [TDD](https://en.wikipedia.org/wiki/Test-driven_development) approach to build your own implementations. 

# Contributing

The Polywrap project is completely open-source and we welcome contributors of all levels. Learn more about how you can contribute [here](https://github.com/polywrap/toolchain#contributing).



# Contact Us:

[Join our discord](https://discord.polywrap.io) and ask your questions right away!


# Resources

- [Polywrap Documentation](https://docs.polywrap.io)
- [Polywrap Integrations Repository](https://github.com/polywrap/integrations)
- [Building tests with Pytest](https://realpython.com/pytest-python-testing/)
- [Running operations concurrently with python's asyncio](https://realpython.com/async-io-python/#the-10000-foot-view-of-async-io)
- [Intro Video](TODO)
