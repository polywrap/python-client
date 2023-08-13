
# Polywrap Python Client Contributor Guide

Polywrap DAO welcomes any new contributions! This guide is meant to help people get over the initial hurdle of figuring out how to use git and make a contribution.

If you've already contributed to other open source projects, contributing to the Polywrap Python project should be pretty similar and you can probably figure it out by guessing. Experienced contributors might want to just skip ahead and open up a pull request But if you've never contributed to anything before, or you just want to see what we consider best practice before you start, this is the guide for you!

- [Polywrap Python Client Contributor Guide](#polywrap-python-client-contributor-guide)
  - [Imposter syndrome disclaimer](#imposter-syndrome-disclaimer)
  - [Code of Conduct](#code-of-conduct)
  - [Development Environment](#development-environment)
  - [Getting and maintaining a local copy of the source code](#getting-and-maintaining-a-local-copy-of-the-source-code)
  - [Choosing a version of python](#choosing-a-version-of-python)
  - [Installing poetry](#installing-poetry)
  - [Installing dependencies](#installing-dependencies)
  - [Running tests](#running-tests)
    - [Debugging with Pytest](#debugging-with-pytest)
    - [Creating your own tests for the client](#creating-your-own-tests-for-the-client)
  - [Running linters](#running-linters)
    - [Running isort by itself](#running-isort-by-itself)
    - [Running black by itself](#running-black-by-itself)
    - [Running bandit by itself](#running-bandit-by-itself)
    - [Running pyright by itself](#running-pyright-by-itself)
  - [Using tox to run linters and tests](#using-tox-to-run-linters-and-tests)
    - [List all the testenv defined in the tox config](#list-all-the-testenv-defined-in-the-tox-config)
    - [Run tests](#run-tests)
    - [Run linters](#run-linters)
    - [Run type checkers](#run-type-checkers)
    - [Find security vulnerabilities, if any](#find-security-vulnerabilities-if-any)
    - [Dev environment](#dev-environment)
  - [VSCode users: Improved dev experience](#vscode-users-improved-dev-experience)
    - [Picking up the virtual environments automatically](#picking-up-the-virtual-environments-automatically)
  - [Making a new branch \& pull request](#making-a-new-branch--pull-request)
    - [Commit message tips](#commit-message-tips)
    - [Sharing your code with us](#sharing-your-code-with-us)
    - [Checklist for a great pull request](#checklist-for-a-great-pull-request)
  - [Code Review](#code-review)
  - [Style Guide for polywrap python client](#style-guide-for-polywrap-python-client)
    - [String Formatting](#string-formatting)
  - [Making documentation](#making-documentation)
  - [Where should I start?](#where-should-i-start)
    - [Claiming an issue](#claiming-an-issue)
  - [Resources](#resources)

## Imposter syndrome disclaimer

_We want your help_. No really, we do.

There might be a little voice inside that tells you you're not ready; that you need to do one more tutorial, or learn another framework, or write a few more blog posts before you can help with this project.

I assure you, that's not the case.

This document contains some contribution guidelines and best practices, but if you don't get it right the first time we'll try to help you fix it.

The contribution guidelines outline the process that you'll need to follow to get a patch merged. By making expectations and process explicit, we hope it will make it easier for you to contribute.

And you don't just have to write code. You can help out by writing documentation, tests, or even by giving feedback about this work. (And yes, that includes giving feedback about the contribution guidelines.)

If have questions or want to chat, we have a [discord server](https://discord.polywrap.io) where you can ask questions, or you can put them in [GitHub issues](https://github.com/polywrap/python-client/issues) too.

Thank you for contributing!

This section is adapted from [this excellent document from @adriennefriend](https://github.com/adriennefriend/imposter-syndrome-disclaimer)

## Code of Conduct

Polywrap python client contributors are asked to adhere to the [Python Community Code of Conduct](https://www.python.org/psf/conduct/). 

## Development Environment

Unix (Linux/Mac) is the preferred operating system to use while contributing to Polywrap python client. If you're using Windows, we recommend setting up [Windows Subsystem for Linux](https://docs.microsoft.com/en-us/windows/wsl/install-win10).


## Getting and maintaining a local copy of the source code

There are lots of different ways to use git, and it's so easy to get into a messy state that [there's a comic about it](https://xkcd.com/1597/).  So... if you get stuck, remember, even experienced programmers sometimes just delete their trees and copy over the stuff they want manually.

If you're planning to contribute, first you'll want to [get a local copy of the source code (also known as "cloning the repository")](https://help.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository)

`git clone git@github.com:polywrap/python-client.git`

Once you've got the copy, you can update it using

`git pull`

You're also going to want to have your own "fork" of the repository on GitHub.
To make a fork on GitHub, read the instructions at [Fork a
repo](https://help.github.com/en/github/getting-started-with-github/fork-a-repo).
A fork is a copy of the main repository that you control, and you'll be using
it to store and share your code with others.  You only need to make the fork once.

Once you've set up your fork, you will find it useful to set up a git remote for pull requests:

`git remote add myfork git@github.com:MYUSERNAME/python-client.git`

Replace MYUSERNAME with your own GitHub username.

## Choosing right version of python

Polywrap python client uses python 3.10 as its preferred version of choice. The newer python version may also work fine but we haven't tested it so we strongly recommend you to use the `python 3.10`.

- Make sure you're running the correct version of python by running: 
```
python3 --version
```
> If you are using a Linux system or WSL, which comes with Python3.8, then you will need to upgrade from Python3.8 to Python3.10 and also fix the `pip` and `distutil` as upgrading to Python3.10 will break them. You may follow [this guide](https://cloudbytes.dev/snippets/upgrade-python-to-latest-version-on-ubuntu-linux) to upgrade.

## Installing poetry

Polywrap python client uses poetry as its preffered project manager. We recommend installing the latest version of the poetry and if you are already have it installed make sure it's newer than version `1.1.14`.

- To install poetry follow [this guide](https://python-poetry.org/docs/#installation). 
- If you are on MacOS then you can install poetry simply with the following homebrew command 
```
brew install poetry
```
> To make sure you're it's installed properly, run `poetry`. Learn more [here](https://python-poetry.org/docs/)

## Installing dependencies

Each of the package directory consists of the `pyproject.toml` file and the `poetry.lock` file. In `pyproject.toml` file, one can find out all the project dependencies and configs related to the package. These files will be utilized by Poetry to install correct dependencies, build, publish the package.

For example, we can **install** deps and **build** the `polywrap-msgpack` package using Poetry. 

- Install dependencies using poetry
```
poetry install
```

- Build the package using poetry
```
poetry build
```

- Update dependencies using poetry
```
poetry update
```

> Make sure your cwd is the appropriate module, for example `polywrap-msgpack`, `polywrap-wasm` or `polywrap-client`.

## Running tests

In order to assure the integrity of the python modules Polywrap Python Client uses [pytest 7.1.3](https://docs.pytest.org/en/7.1.x/contents.html) as a testing framework.

As we can see in the `pyproject.toml` files, we installed the [PyTest](https://docs.pytest.org) package. We will be using it as our testing framework. 
Before running tests, make sure you have installed all required dependencies using `poetry install` command. 

You need to activate the virtualenv with poetry using the `shell` command before running any other command
```
poetry shell
```

Once activated you can directly run the `pytest` by just executing following command:
```
pytest
```

If you don't want to activate the virtualenv for entire shell and just want to execute one particular command in the virtualenv, you can use `poetry run` command below:
```
poetry run pytest
```


This last command will run a series of scripts that verify that the specific module of the client is performing as expected in your local machine. The output on your console should look something like this:

```
$ poetry run pytest
>>
================================= test session starts =================================
platform darwin -- Python 3.10.0, pytest-7.1.3, pluggy-1.0.0
rootdir: /Users/polywrap/pycode/polywrap/toolchain/packages/py, configfile: pytest.ini
collected 26 items                                                                    

tests/test_msgpack.py ........................                                  [100%]
```

### Debugging with Pytest

You should expect to see the tests passing with a 100% accuracy. To better understand these outputs, read [this quick guide](https://docs.pytest.org/en/7.1.x/how-to/output.html). If any of the functionality fails (marked with an 'F'), or if there are any Warnings raised, you can debug them by running a verbose version of the test suite:
- `poetry run pytests -v` or `poetry run pytests -vv` for even more detail
- Reach out to the devs on the [Discord](https://discord.polywrap.io) explaining your situation, and what configuration you're using on your machine.


## Creating your own tests for the client

By creating tests you can quickly experiment with the Polywrap Client and its growing set of wrappers. Since Pytest is already set up on the repo, go to the `polywrap-client\tests\` directory, and take a look at how some of the functions are built. You can use similar patterns to mod your own apps and build new prototypes with more complex functionality.

Here's a good guide to learn about [building tests with Pytest](https://realpython.com/pytest-python-testing/) and [here's the official documentation](https://docs.pytest.org/en/latest/contents.html).

## Running linters

Polywrap python client uses a few tools to improve code quality and readability:

- `isort` sorts imports alphabetically and by type
- `black` provides automatic style formatting.  This will give you basic [PEP8](https://www.python.org/dev/peps/pep-0008/) compliance. (PEP8 is where the default python style guide is defined.)
- `pylint` provides additional code "linting" for more complex errors like unused imports.
- `pydocstyle` helps ensure documentation styles are consistent.
- `bandit` is more of a static analysis tool than a linter and helps us find potential security flaws in the code.
- `pyright` helps ensure type definitions are correct when provided.

### Running isort by itself

To format the imports using isort, you run `isort --profile black` followed by the filename. You will have to add `--profile black` when calling isort to make it compatible with Black formatter. For formatting a particular file name filename.py.

```bash
isort --profile black filename.py
```

Alternatively, you can run isort recursively for all the files by adding `.` instead of filename

```bash
isort --profile black .
```

### Running black by itself

To format the code, you run `black` followed by the filename you wish to reformat.  For formatting a particular file name filename.py.

```bash
black filename.py
```

In many cases, it will make your life easier if you only run black on
files you've changed because you won't have to scroll through a pile of
auto-formatting changes to find your own modifications.  However, you can also
specify a whole folder using ```./```

### Running pylint by itself

pylint helps identify and flag code quality issues, potential bugs, and adherence to coding standards. By analyzing Python code, Pylint enhances code readability, maintains consistency, and aids in producing more robust and maintainable software.

To run pylint on all the code we scan, use the following:

```bash
pylint PACKAGE_NAME
```

You can also run it on individual files:

```bash
pylint filename.py
```

Checkout [pylint documentation](https://docs.pylint.org/) for more information.

### Running pydocstyle by itself

Pydocstyle is a tool for enforcing documentation conventions in Python code. It checks adherence to the PEP 257 style guide, ensuring consistent and well-formatted docstrings. By promoting clear and standardized documentation, pydocstyle improves code readability, fosters collaboration, and enhances overall code quality.

To run pydocstyle on all the code we scan, use the following:

```bash
pydocstyle PACKAGE_NAME
```

You can also run it on individual files:

```bash
pydocstyle filename.py
```

Checkout [pydocstyle documentation](https://www.pydocstyle.org/en/stable/) for more information.

### Running bandit by itself

To run it on all the code we scan, use the following:

```bash
bandit -r PACKAGE_NAME
```

You can also run it on individual files:

```bash
bandit filename.py
```

Bandit helps you target manual code review, but bandit issues aren't always things that need to be fixed, just reviewed.  If you have a bandit finding that doesn't actually need a fix, you can mark it as reviewed using a `# nosec` comment.  If possible, include details as to why the bandit results are ok for future reviewers.  For example, we have comments like `#nosec uses static https url above` in cases where bandit prompted us to review the variable being passed to urlopen().

Checkout [bandit documentation](https://bandit.readthedocs.io/en/latest/) for more information.

### Running pyright by itself

To check for static type checking, you run `pyright` followed by the filename you wish to check static type for. pyright checks the type annotations you provide and reports any type mismatches or missing annotations. For static type checking for a particular file name filename.py

```bash
pyright filename.py
```

Alternatively, you can run pyright on directory as well. For static type checking for a directory

```bash
pyright .
```

for someone who is new or are not familiar to python typing here are few resource - 
[pyright documentation](https://microsoft.github.io/pyright/#/), and [Python typing documentation](https://docs.python.org/3/library/typing.html)


## Using tox to run linters and tests 
We are using [`tox`](https://tox.wiki/en) to run lint and tests even more easily. Below are some basic commands to get you running. 

### List all the testenv defined in the tox config
```
tox -a
```
### Run tests
```
tox
```
### Run linters
```
tox -e lint
```
### Run type checkers
```
tox -e typecheck
```

### Find security vulnerabilities, if any
```
tox -e secure
```

### Dev environment
Use this command to only apply lint fixes and style formatting.
```
tox -e dev
```

- After running these commands we should see all the tests passing and commands executing successfully, which means that we are ready to update and test the package.
- To create your own tox scripts, modify the `tox.ini` file in the respective module.

## VSCode users: Improved dev experience
If you use VSCode, we have prepared a pre-configured workspace that improves your dev experience. So when you open VScode, set up the workspace file `python-monorepo.code-workspace` by going to:

```
File -> Open Workspace from File...
```
![File -> Open Workspace from File](misc/VScode_OpenWorkspaceFromFile.png)

Each folder is now a project to VSCode. This action does not change the underlying code, but facilitates the development process. So our file directory should look like this now:

![all modules have their respective folder, along with a root folder](misc/VScode_workspace.png)

> Note: You might have to do this step again next time you close and open VS code!

### Picking up the virtual environments automatically
We will need to create a `.vscode/settings.json` file in each module's folder, pointing to the in-project virtual environment created by the poetry.

- You can easily find the path to the virtual env by running following command in the package for which you want to find it for:
```
poetry shell
```

- Once you get the path virtual env, you need to create the following `settings.json` file under the `.vscode/` folder of the given package. For example, in case of `polywrap-client` package, it would be under
`./polywrap-client/.vscode/settings.json`


Here's the structure `settings.json` file we are using for configuring the vscode. Make sure you update your virtual env path you got from poetry as the `python.defaultInterpreterPath` argument:
```json
{
  "python.formatting.provider": "black",
  "python.languageServer": "Pylance",
  "python.analysis.typeCheckingMode": "strict",
  "python.defaultInterpreterPath": "/Users/polywrap/Library/Caches/pypoetry/virtualenvs/polywrap-client-abcdef-py3.10"
}
```

Keep in mind that these venv paths will vary for each module you run `poetry shell` on. Once you configure these `setting.json` files correctly on each module you should be good to go!

## Making a new branch & pull request

Git allows you to have "branches" with variant versions of the code.  You can see what's available using `git branch` and switch to one using `git checkout branch_name`.

To make your life easier, we recommend that the `dev` branch always be kept in sync with the repo at `https://github.com/polywrap/python-client`, as in you never check in any code to that branch.  That way, you can use that "clean" dev branch as a basis for each new branch you start as follows:

```bash
git checkout dev
git pull
git checkout -b my_new_branch
```

>Note: If you accidentally check something in to dev and want to reset it to match our dev branch, you can save your work using `checkout -b` and then do a `git reset` to fix it:
>```bash
>git checkout -b saved_branch
>git reset --hard origin/dev
>```
>You do not need to do the `checkout` step if you don't want to save the changes you made.

When you're ready to share that branch to make a pull request, make sure you've checked in all the files you're working on.  You can get a list of the files you modified using `git status` and see what modifications you made using `git diff`

Use `git add FILENAME` to add the files you want to put in your pull request, and use `git commit` to check them in.  Try to use [a clear commit message](https://chris.beams.io/posts/git-commit/) and use the [Conventional Commits](https://www.conventionalcommits.org/) format.  

### Commit message tips

We usually merge pull requests into a single commit when we accept them, so it's fine if you have lots of commits in your branch while you figure stuff out, and we can fix your commit message as needed then.  But if you make sure that at least the title of your pull request follows the [Conventional Commits](https://www.conventionalcommits.org/) format that you'd like for that merged commit message, that makes our job easier!

GitHub also has some keywords that help us link issues and then close them automatically when code is merged.  The most common one you'll see us use looks like `fixes: #123456`. You can put this in the title of your PR (what usually becomes the commit message when we merge your code), another line in the commit message, or any comment in the pull request to make it work.  You and read more about [linking a pull request to an issue](https://docs.github.com/en/issues/tracking-your-work-with-issues/linking-a-pull-request-to-an-issue) in the GitHub documentation.

### Sharing your code with us

Once your branch is ready and you've checked in all your code, push it to your fork:

```bash
git push myfork
```

From there, you can go to [our pull request page](https://github.com/polywrap/python-client/pulls) to make a new pull request from the web interface.

### Checklist for a great pull request

Here's a quick checklist to help you make sure your pull request is ready to go:

1. Have I run the tests locally?
   - Run the command `pytest` (See also [Running Tests](#running-tests))
   - GitHub Actions will run the tests for you, but you can often find and fix issues faster if you do a local run of the tests.
2. Have I run the code linters and fixed any issues they found?
   - We recommend using `tox` to easily run this (See also [Running Linters](#running-linters))
   - GitHub Actions will run the linters for you too if you forget! (And don't worry, even experienced folk forget sometimes.)
   - You will be responsible for fixing any issue found by the linters before your code can be merged.
3. Have I added any tests I need to prove that my code works?
   - This is especially important for new features or bug fixes.
4. Have I added or updated any documentation if I changed or added a feature?
   - New features are often documented as docstrings and doctests alongside the code  (See [Making documentation](#making-documentation) for more information.)
5. Have I used [Conventional Commits](https://www.conventionalcommits.org/) to format the title of my pull request?
6. If I closed a bug, have I linked it using one of [GitHub's keywords](https://docs.github.com/en/issues/tracking-your-work-with-issues/linking-a-pull-request-to-an-issue)? (e.g. include the text `fixed #1234`)
7. Have I checked on the results from GitHub Actions?
   - GitHub Actions will run all the tests, linters and type checkers for you.  If you can, try to make sure everything is running cleanly with no errors before leaving it for a human code reviewer!
   - As of this writing, tests take less than 20 minutes to run once they start, but they can be queued for a while before they start.  Go get a cup of tea/coffee or work on something else while you wait!

## Code Review

Once you have created a pull request (PR), GitHub Actions will try to run all the tests on your code.  If you can, make any modifications you need to make to ensure that they all pass, but if you get stuck a reviewer will see if they can help you fix them.  Remember that you can run the tests locally while you're debugging; you don't have to wait for GitHub to run the tests (see the [Running tests](#running-tests) section above for how to run tests).

Someone will review your code and try to provide feedback in the comments on GitHub.  Usually it takes a few days, sometimes up to a week.  The core contributors for this project work on it as part of their day jobs and are usually on different timezones, so you might get an answer a bit faster during their work week.

If something needs fixing or we have questions, we'll work back and forth with you to get that sorted.  We usually do most of the chatting directly in the pull request comments on GitHub, but if you're stuck you can also stop by our [discord server](https://discord.polywrap.io) to talk with folk outside of the bug.

>Another useful tool is `git rebase`, which allows you to change the "base" that your code uses.  We most often use it as `git rebase origin/dev` which can be useful if a change in the dev tree is affecting your code's ability to merge.  Rebasing is a bit much for an intro document, but [there's a git rebase tutorial here](https://www.atlassian.com/git/tutorials/rewriting-history/git-rebase) that you may find useful if it comes up.

Once any issues are resolved, we'll merge your code.  Yay!

In rare cases, the code won't work for us and we'll let you know.  Sometimes this happens because someone else has already submitted a fix for the same bug, (Issues marked [good first issue](https://github.com/polywrap/python-client/labels/good%20first%20issue) can be in high demand!). Don't worry, these things happens, no one thinks less of you for trying!

## Style Guide for polywrap python client

Most of our "style" stuff is caught by the `black` and `pylint` linters, but we also recommend that contributors use f-strings for formatted strings:

### String Formatting

Python provides many different ways to format the string (you can read about them [here](https://realpython.com/python-formatted-output/)) and we use f-string formatting in our tool.

> Note: f-strings are only supported in python 3.6+.

- **Example:** Formatting string using f-string

```python
#Program prints a string containing name and age of person
name = "John Doe"
age = 23
print(f"Name of the person is {name} and his age is {age}")

#Output
# "Name of the person is John Doe and his age is 23"
```

Note that the string started with the `f` followed by the string. Values are always added in the curly braces. Also we don't need to convert age into string. (we may have used `str(age)` before using it in the string) f-strings are useful as they provide many cool features. You can read more about features and the good practices to use f-strings [here](https://realpython.com/python-f-strings/#f-strings-a-new-and-improved-way-to-format-strings-in-python).

## Making documentation

The documentation for Polywrap python client can be found in the `docs/` directory (with the exception of the README.md file, which is stored in the root directory).

Like many other Python-based projects, Polywrap python client uses Sphinx and
ReadTheDocs to format and display documentation. If you're doing more than minor typo
fixes, you may want to install the relevant tools to build the docs.  There's a
`pyproject.toml` file available in the `docs/` directory you can use to install
sphinx and related tools:

```bash
cd docs/
poetry install
```

Once those are installed, you can build the documentation using `build.sh`:

```bash
./build.sh
```

That will build the HTML rendering of the documentation and store it in the
`build` directory.   You can then use your web browser to go to that
directory and see what it looks like.

Note that you don't need to commit anything in the `build` directory.  Only the `.md` and `.rst` files should be checked in to the repository.

If you don't already have an editor that understands Markdown (`.md`) and
RestructuredText (.`rst`) files, you may want to try out Visual Studio Code, which is free and has a nice Markdown editor with a preview.

You can also use the `./clean.sh` script to clean the source tree of any files
that are generated by the docgen process.

By using `./docgen.sh` script, you can generate the documentation for the
project.  This script will generate the documentation in the `source` directory.

> NOTE: The use of `./clean.sh` and `./docgen.sh` is only recommended if you know what you're doing. 
> If you're just trying to build the docs after some changes you have made then use `./build.sh` instead.

## Where should I start?

Many beginners get stuck trying to figure out how to start.  You're not alone!

Here's three things we recommend:

- Try something marked as a "[good first issue](https://github.com/polywrap/python-client/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22)" We try to mark issues that might be easier for beginners.
- Suggest fixes for documentation.  If you try some instruction and it doesn't work, or you notice a typo, those are always easy first commits!  One place we're a bit weak is instructions for Windows users.
- Add new tests. We're always happy to have new tests, especially for things that are currently untested.  If you're not sure how to write a test, check out the existing tests for examples.
- Add new features.  If you have an idea for a new feature, feel free to suggest it!  We're happy to help you figure out how to implement it.

If you get stuck or find something that you think should work but doesn't, ask for help in an issue or stop by [the discord](https://discord.polywrap.io) to ask questions.

Note that our "good first issue" bugs are in high demand during the October due to the Hacktoberfest.  It's totally fine to comment on an issue and say you're interested in working on it, but if you don't actually have any pull request with a tentative fix up within a week or so, someone else may pick it up and finish it. If you want to spend more time thinking, the new tests (especially ones no one has asked for) might be a good place for a relaxed first commit.

### Claiming an issue

- You do not need to have an issue assigned to you before you work on it.  To "claim" an issue either make a linked pull request or comment on the issue saying you'll be working on it.  
- If someone else has already commented or opened a pull request, assume it is claimed and find another issue to work on.  
- If it's been more than 1 week without progress, you can ask in a comment if the claimant is still working on it before claiming it yourself (give them at least 3 days to respond before assuming they have moved on).

The reason we do it this way is to free up time for our maintainers to do more code review rather than having them handling issue assignment.  This is especially important to help us function during busy times of year when we take in a large number of new contributors such as Hacktoberfest (October).

# Resources

- [Polywrap Documentation](https://docs.polywrap.io)
- [Python Client Documentation](https://polywrap-client.rtfd.io)
- [Client Readiness](https://github.com/polywrap/client-readiness)
- [Discover Wrappers](https://wrapscan.io)
- [Polywrap Discord](https://discord.polywrap.io)
