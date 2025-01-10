"""Tests for `flake8_django_migrations` package."""

import ast
from textwrap import dedent

from flake8_django_migrations import Plugin


def _results(s: str) -> set[str]:
    tree = ast.parse(dedent(s))
    plugin = Plugin(tree)
    return {f"{line}:{col} {msg}" for line, col, msg, _ in plugin.run()}


def test_trivial_case():
    assert _results("") == set()


def test_plugin_version():
    assert isinstance(Plugin.version, str)
    assert "." in Plugin.version


def test_plugin_name():
    assert isinstance(Plugin.name, str)


def test_unsafe_drop_column():
    input_code = """
    class Migration(migrations.Migration):
        operations = [
            migrations.RemoveField(
                model_name="order",
                name="total",
            ),
        ]
    """
    assert _results(input_code) == {
        "4:8 DM001 RemoveField operation should be wrapped in SeparateDatabaseAndState",
    }


def test_safe_remove_field():
    input_code = """
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
    """

    assert _results(input_code) == set()
