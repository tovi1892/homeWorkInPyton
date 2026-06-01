import ast
from typing import Any


class AnalyzerCode(ast.NodeVisitor):
    def __init__(self):
        self.functions_info = []
        self.assigned_variables=set()
        self.used_variables = set()
    def visit_FunctionDef(self, node):
       func_name = node.name
       has_docstring = ast.get_docstring(node) is not None
       start_line = node.lineno
       end_line = getattr(node, 'end_lineno', start_line)
       function_length = end_line - start_line + 1
       self.functions_info.append({
           "name": func_name,
           "length": function_length,
           "has_docstring": has_docstring
       })
       self.generic_visit(node)

    def visit_Assign(self, node):
        for target in node.targets:
            if isinstance(target, ast.Name):
                self.assigned_variables.add(target.id)
        self.generic_visit(node)

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Load):
            self.used_variables.add(node.id)
        self.generic_visit(node)

def analyze_file_length(file_content: str) -> int:
    lines = file_content.splitlines()
    return len(lines)
def analyze_code_quality(file_content: str) -> dict[str, str] | dict[str, int | list[Any]]:
    try:
        tree = ast.parse(file_content)
    except SyntaxError as e:
        return {"error": f"Invalid Python code: {e}"}
    analyzer = AnalyzerCode()
    analyzer.visit(tree)
    total_lines = analyze_file_length(file_content)
    alerts=[]
    for func in analyzer.functions_info:
        if func["length"] > 20:
            alerts.append(f"Warning: Function '{func['name']}' is too long ({func['length']} lines). Max is 20.")
        if not func["has_docstring"]:
            alerts.append(f"Warning: Function '{func['name']}' is missing a docstring.")
    if total_lines > 200:
        alerts.append(f"Warning: File is too long ({total_lines} lines). Max is 200.")
    unused_vars = analyzer.assigned_variables - analyzer.used_variables
    for var in unused_vars:
        alerts.append(f"Warning: Variable '{var}' is assigned but never used.")
    return {
        "total_lines": total_lines,
        "functions": analyzer.functions_info,
        "alerts": alerts
    }
if __name__ == "__main__":
    test_code = """def my_short_function():
    print("Hello")

def my_long_and_undocumented_function():
    y = 2
    x = 1
    yt = 2
    
    return x + y
"""

    result = analyze_code_quality(test_code)
    print(result["alerts"])