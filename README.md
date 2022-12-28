# xbox-wireless

A python module for using a bluetooth xbox controller from a mac.

## Installing

You can install this package by running the following command.

```
pip install xbox-wireless
```

## Updating

If you want to update to the latest version, just update the python module with the
following command.

```
pip install xbox-wireless -U
```

## Pipenv

If you prefer to use pipenv for testing, run the following command to setup your pip
environment.

```
pipenv install --pre "-e . [dev]"
```

## How to Contribute

Install the latest packages.  Best practice would be do this within a virtualenv.

```
pip install --upgrade pip setuptools wheel
pip install -e ".[dev]"
```

Before committing run `pytest`.  Some formatting changes can be automatically corrected
by running `black`.
