import ast


class Checker:
    """Base class for the plugin."""

    @staticmethod
    def get_call_name(node: ast.Call):
        """Return call name for the given node."""
        if isinstance(node.func, ast.Attribute):
            return node.func.attr
        elif isinstance(node.func, ast.Name):
            return node.func.id

    def run(self, node: ast.expr):
        """Entry point to be implemented in subclasses."""
        raise NotImplementedError()
