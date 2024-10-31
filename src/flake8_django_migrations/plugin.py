from __future__ import annotations

import ast
import importlib.metadata as importlib_metadata
from collections.abc import Generator
from typing import Any, ClassVar

from .checkers.base import Checker
from .checkers.issue import Issue
from .checkers.remove_field import RemoveFieldChecker


class Visitor(ast.NodeVisitor):
    """Custom AST visitor."""

    checkers: ClassVar[list[Checker]] = [RemoveFieldChecker()]

    def __init__(self) -> None:
        self.issues: list[Issue] = []

    def visit_Call(self, node: ast.Call) -> Any:
        """Called when visiting a function called."""
        for checker in self.checkers:
            issues = checker.run(node)
            if issues:
                self.issues.extend(issues)


class Plugin:
    """Declare the flake8 plugin."""

    name = "flake8_django_migrations"
    version = importlib_metadata.version(name)

    def __init__(self, tree: ast.AST):
        self._tree = tree

    def run(self) -> Generator[tuple[int, int, str, type[Any]], None, None]:
        """Plugin entry point."""
        visitor = Visitor()
        visitor.visit(self._tree)

        for issue in visitor.issues:
            yield issue.lineno, issue.col, issue.message, type(self)
