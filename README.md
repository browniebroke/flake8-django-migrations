# flake8-django-migrations

<p align="center">
  <a href="https://github.com/browniebroke/flake8-django-migrations/actions/workflows/ci.yml?query=branch%3Amain">
    <img alt="CI Status" src="https://img.shields.io/github/actions/workflow/status/browniebroke/flake8-django-migrations/ci.yml?branch=main&label=CI&logo=github&style=flat-square">
  </a>
  <a href="https://codecov.io/gh/browniebroke/flake8-django-migrations">
    <img src="https://img.shields.io/codecov/c/github/browniebroke/flake8-django-migrations.svg?logo=codecov&style=flat-square" alt="Test coverage percentage">
  </a>
</p>
<p align="center">
  <a href="https://github.com/astral-sh/uv">
    <img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json" alt="uv">
  </a>
  <a href="https://github.com/astral-sh/ruff">
    <img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json" alt="Ruff">
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

---

**Source Code**: <a href="https://github.com/browniebroke/flake8-django-migrations" target="_blank">https://github.com/browniebroke/flake8-django-migrations</a>

---

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
