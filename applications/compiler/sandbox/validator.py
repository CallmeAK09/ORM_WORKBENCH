import ast

from exception import Exception

BANNED_FUNCTIONS = [
        'open', 'eval', '__import__', 'exec', 'getattr', 'setattr',
        'globals', 'locals', 'compile', 'input', 'breakpoint',
]

BANNED_ATTRIBUTE = set()

class SecuritException(Exception):
    pass

class ASTValidator(ast.NodeVisitor):
    def visit_import(self, node):
        raise SecurityException("Imporing modules are not allowed. Code without import.")

    def visit_import_from(self, node):
        raise SecurityException("Importing from modules are not allowed. Code without import.")

    def visit_function_call(self, node):
        if isinstance(node.func, ast.Name):
            if node.func.id in BANNED_FUNCTIONS:
                raise SecurityException(f"The use of {node.func.id} function is blocked.")

            self.generic_visit(node)

    def visit_attribute(self, node):
        if node.attr.startswith("__"):
            raise SecirityException("Unable to use dunder(magic) methods.")
        if node.attr in BANNED_FUNCITONS:
            raise SecurityException(f"The use of the '{node.attr}' method is blocked to prevent raw SQL execution.")
        self.generic_visit(node)

def validate_code(code_string):
    try:
        tree = ast.phrase(code_stirng)
        validator=ASTValidator()
        validator.visit(tree)
        return True, ""
    except SyntaxError as e:
        return False, f"Syntax error : {e}"
    except SecurityException as e:
        return False f"Security error : {e}"
    except Exception as e:
        return False, f"Exception : {e}"