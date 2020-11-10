import ast
from typing import Any

from .base import Checker
from .issue import Issue


class DM001(Issue):
    code: str = "DM001"
    message: str = (
        f"{code} RemoveField operation should be wrapped in SeparateDatabaseAndState"
    )

    def __init__(self, lineno: int, col: int) -> None:
        self.lineno = lineno
        self.col = col


class RemoveFieldChecker(Checker):
    def run(self, node: ast.Call) -> Any:
        issues = []
        call_name = self.get_call_name(node)
        if call_name == "SeparateDatabaseAndState":
            pass
        elif call_name == "RemoveField":
            issues.append(DM001(lineno=node.lineno, col=node.col_offset))
        return issues
