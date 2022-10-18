# Polywrap python client

[Polywrap](https://polywrap.io/#/) is a developer tool that enables easy integration of Web3 protocols into any application. It makes it possible for applications on any platform, written in any language, to read and write data to Web3 protocols.

## Setup for building and testing
- Requirement: Python ^3.10, Poetry ^1.1.14
- If you are using a linux system or WSL, which comes with Python3.8, then you will need to upgrade Python3.8 to Python3.10 and also fix the pip and distutil as upgrading to Python3.10 will break them. You may follow [this guide](https://cloudbytes.dev/snippets/upgrade-python-to-latest-version-on-ubuntu-linux) to upgrade.
- To install poetry follow [this guide](https://python-poetry.org/docs/#installation). If you are on macos then you can install poetry simply with the following homebrew command
```
brew install poetry
```
- Clone the repo. 
```
git clone https://github.com/polywrap/python-client
```
- We will be using [Poetry](https://python-poetry.org) for building and testing our packages. 

- Each of the package folders consists the pyproject.toml file and the poetry.lock file. In pyproject.toml file, one can find out all the project dependencies and configs related to the package. These files will be utilized by Poetry to install correct dependencies, build, lint and test the package.

- For example, we can install deps, build and test the polywrap-msgpack package using Poetry. 

- Install dependencies using Poetry. 
```
poetry install
```
> Make sure your cwd is `polywrap-msgpack` package.
- As we can see in the pyproject.toml file, we installed [PyTest](https://docs.pytest.org) package. We will be using the same as our testing framework. 
- Now we are ready to build and test the core package using Poetry and PyTest.
- To build the package run the following command
```
poetry build
```
- You need to activate the venv with poetry using `poetry shell` command before running any other command
- We are using tox to run lint and tests easily. You can list all the testenv defined in the 
tox config with following command
```
tox -a
```
- To run tests using tox simply run `tox`
- You can run linters with the `tox -e lint` and check type with `tox -e typecheck`. By running `tox -e secure`, you can find security vulnerability if any.
- While developing, you can run `tox -e dev` and apply lint fixes and style formatting.
- As we see the mentioned tests passing, we are ready to update and test the package. 

## For VSCode users
If you use VSCode, open this setup using the workspace file python-monorepo.code-workspace:

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
