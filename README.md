# flake8-django-migrations

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

* Step 1: remove the field from the model and code. For foreign key fields, the foreign key constraint should also be dropped.
* Step 2: remove the column from the database.

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

