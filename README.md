# flake8-django-migrations

<p align="center">
  <a href="https://github.com/browniebroke/flake8-django-migrations/actions?query=workflow%3ACI">
    <img alt="CI Status" src="https://img.shields.io/github/workflow/status/browniebroke/flake8-django-migrations/CI?label=CI&logo=github&style=flat-square">
  </a>
  <a href="https://codecov.io/gh/browniebroke/flake8-django-migrations">
    <img src="https://img.shields.io/codecov/c/github/browniebroke/flake8-django-migrations.svg?logo=codecov&style=flat-square" alt="Test coverage percentage">
  </a>
</p>
<p align="center">
  <a href="https://python-poetry.org/">
    <img src="https://img.shields.io/badge/packaging-poetry-299bd7?style=flat-square&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAASCAYAAABrXO8xAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAJJSURBVHgBfZLPa1NBEMe/s7tNXoxW1KJQKaUHkXhQvHgW6UHQQ09CBS/6V3hKc/AP8CqCrUcpmop3Cx48eDB4yEECjVQrlZb80CRN8t6OM/teagVxYZi38+Yz853dJbzoMV3MM8cJUcLMSUKIE8AzQ2PieZzFxEJOHMOgMQQ+dUgSAckNXhapU/NMhDSWLs1B24A8sO1xrN4NECkcAC9ASkiIJc6k5TRiUDPhnyMMdhKc+Zx19l6SgyeW76BEONY9exVQMzKExGKwwPsCzza7KGSSWRWEQhyEaDXp6ZHEr416ygbiKYOd7TEWvvcQIeusHYMJGhTwF9y7sGnSwaWyFAiyoxzqW0PM/RjghPxF2pWReAowTEXnDh0xgcLs8l2YQmOrj3N7ByiqEoH0cARs4u78WgAVkoEDIDoOi3AkcLOHU60RIg5wC4ZuTC7FaHKQm8Hq1fQuSOBvX/sodmNJSB5geaF5CPIkUeecdMxieoRO5jz9bheL6/tXjrwCyX/UYBUcjCaWHljx1xiX6z9xEjkYAzbGVnB8pvLmyXm9ep+W8CmsSHQQY77Zx1zboxAV0w7ybMhQmfqdmmw3nEp1I0Z+FGO6M8LZdoyZnuzzBdjISicKRnpxzI9fPb+0oYXsNdyi+d3h9bm9MWYHFtPeIZfLwzmFDKy1ai3p+PDls1Llz4yyFpferxjnyjJDSEy9CaCx5m2cJPerq6Xm34eTrZt3PqxYO1XOwDYZrFlH1fWnpU38Y9HRze3lj0vOujZcXKuuXm3jP+s3KbZVra7y2EAAAAAASUVORK5CYII=" alt="Poetry">
  </a>
  <a href="https://github.com/ambv/black">
    <img src="https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square" alt="black">
  </a>
  <a href="https://github.com/pre-commit/pre-commit">
    <img src="https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white&style=flat-square" alt="pre-commit">
  </a>
</p>
<p align="center">
  <a href="https://pypi.org/project/flake8-django-migrations/">
    <img src="https://img.shields.io/pypi/v/flake8-django-migrations.svg?logo=python&amp;logoColor=fff&amp;style=flat-square" alt="PyPi Status">
  </a>
  <img src="https://img.shields.io/pypi/pyversions/flake8-django-migrations.svg?style=flat-square" alt="pyversions">
  <img src="https://img.shields.io/pypi/l/flake8-django-migrations.svg?style=flat-square" alt="license">
</p>

Flake8 plugin to lint for backwards incompatible database migrations.

## Installation

Install using `pip` (or your favourite package manager):

```sh
pip install flake8-django-migrations
```

## Usage

This plugin should be used automatically when running flake8:

```sh
flake8
```

## Checks

This is the list of checks currently implemented by this plugin.

### DM001

`RemoveField` operation should be wrapped in `SeparateDatabaseAndState`.

Such an operation should be run in two separate steps, using `SeparateDatabaseAndState`, otherwise it is not backwards compatible.

- Step 1: remove the field from the model and code. For foreign key fields, the foreign key constraint should also be dropped.
- Step 2: remove the column from the database.

#### Bad

```python
class Migration(migrations.Migration):
    operations = [
        migrations.RemoveField(
            model_name="order",
            name="total",
        ),
    ]
```

#### Good

```python
class Migration(migrations.Migration):
    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.RemoveField(
                    model_name="order",
                    name="total",
                ),
            ],
        ),
    ]
```
