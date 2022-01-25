import ast
import sys
from typing import Any, Generator, List, Tuple, Type

from .checkers.issue import Issue
from .checkers.remove_field import RemoveFieldChecker

if sys.version_info < (3, 8):  # pragma: no cover (<PY38)
    # Third party
    import importlib_metadata
else:  # pragma: no cover (PY38+)
    # Core Library
    import importlib.metadata as importlib_metadata


class Visitor(ast.NodeVisitor):
    checkers = [RemoveFieldChecker()]

    def __init__(self) -> None:
        self.issues: List[Issue] = []

    def visit_Call(self, node: ast.Call) -> Any:
        for checker in self.checkers:
            issues = checker.run(node)
            if issues:
                self.issues.extend(issues)


class Plugin:
    name = "flake8_django_migrations"
    version = importlib_metadata.version(name)

    def __init__(self, tree: ast.AST):
        self._tree = tree

    def run(self) -> Generator[Tuple[int, int, str, Type[Any]], None, None]:
        visitor = Visitor()
        visitor.visit(self._tree)

        for issue in visitor.issues:
            yield issue.lineno, issue.col, issue.message, type(self)
