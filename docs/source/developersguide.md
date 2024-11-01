# Developer's guide

## Install python package in a virtual environment

```bash
git clone git@github.com:boileaum/mdslicer.git  # clone the repository
cd mdslicer  # go to the project root directory
python3 -m virtualenv .venv  # create a virtual environment
pip install -e .  # install the package in editable mode
```

Note: in editable mode (`-e` option), the package is installed in a way that it is still possible to edit the source code and have the changes take effect immediately.

## Run the unitary tests

### Install the development dependencies

```bash
pip install -e ".[test]"
```

### Run the tests

Run the tests from the projet root directory using the `-s`:

```bash
pytest -sv
```

See [.gitlab-ci.yml](https://github.com/boileaum/mdslicer/blob/main/.gitlab-ci.yml) for more details.

## Build the documentation

### Install the documentation dependencies

```bash
pip install -e ".[doc]"
```

### Build and serve the documentation locally

```bash
sphinx-autobuild docs/source/ docs/_build/html  --watch src/mdslicer
```

Go to <http://localhost:8000> and see the changes in `docs/source/` directory take effect immediately.
