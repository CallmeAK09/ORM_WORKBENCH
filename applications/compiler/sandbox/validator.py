import ast


BANNED_FUNCTIONS = [
        'open', 'eval', '__import__', 'exec', 'getattr', 'setattr',
        'globals', 'locals', 'compile', 'input', 'breakpoint',
]

BANNED_ATTRIBUTE = set()

class SecurityException(Exception):
    pass

class ASTValidator(ast.NodeVisitor):
    def visit_Import(self, node):
        raise SecurityException("Imporing modules are not allowed. Code without import.")

    def visit_ImportFrom(self, node):
        raise SecurityException("Importing from modules are not allowed. Code without import.")

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            if node.func.id in BANNED_FUNCTIONS:
                raise SecurityException(f"The use of {node.func.id} function is blocked.")

            self.generic_visit(node)

    def visit_Attribute(self, node):
        if node.attr.startswith("__"):
            raise SecurityException("Unable to use dunder(magic) methods.")
        if node.attr in BANNED_FUNCTIONS:
            raise SecurityException(f"The use of the '{node.attr}' method is blocked to prevent raw SQL execution.")
        self.generic_visit(node)

def validate_code(code_string):
    try:
        tree = ast.parse(code_string)
        validator=ASTValidator()
        validator.visit(tree)
        return True, ""
    except SyntaxError as e:
        return False, f"Syntax error : {e}"
    except SecurityException as e:
        return False, f"Security error : {e}"
    except Exception as e:
        return False, f"Exception : {e}"


def format_validation_error(e):
    """
    To format ValidationError into a human readable string.
    Also handle field specific errors and __all__ errors like UniqueConstraint.
    """
    error_msg = "Validation Error : \n"
    if hasattr(e, 'message_dict'):
        for field, error in e.message_dict.items():
            field_display = "Constraint/General" if field == "__all__" else field
            error_msg += f"- {field_display}: {', '.join(error)}\n"
    else:
        error_msg += f"- {str(e)}"

    return error_msg