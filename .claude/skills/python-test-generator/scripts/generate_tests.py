#!/usr/bin/env python3
"""
Python Test Generator Script

This script analyzes Python code and generates corresponding pytest tests.
"""
import ast
import sys
import os
from pathlib import Path
from typing import List, Dict, Any


class PythonAnalyzer:
    """Analyzes Python code to extract functions, classes, and methods for testing."""

    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self.tree = None
        self.functions = []
        self.classes = []

    def analyze(self):
        """Analyze the Python file and extract functions and classes."""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                self.tree = ast.parse(content)
        except Exception as e:
            print(f"Error reading file {self.file_path}: {e}")
            return

        for node in ast.walk(self.tree):
            if isinstance(node, ast.FunctionDef):
                # Skip private functions and special methods unless they're important
                if not node.name.startswith('_') or node.name in ['__init__']:
                    self.functions.append({
                        'name': node.name,
                        'args': [arg.arg for arg in node.args.args if arg.arg != 'self'],
                        'line_no': node.lineno
                    })
            elif isinstance(node, ast.ClassDef):
                methods = []
                for item in node.body:
                    if isinstance(item, ast.FunctionDef):
                        if not item.name.startswith('_') or item.name in ['__init__']:
                            methods.append({
                                'name': item.name,
                                'args': [arg.arg for arg in item.args.args if arg.arg != 'self'],
                                'line_no': item.lineno
                            })
                self.classes.append({
                    'name': node.name,
                    'methods': methods
                })

    def get_import_path(self) -> str:
        """Generate the import path for the module."""
        # Remove .py extension and convert path to module format
        relative_path = self.file_path.relative_to(Path('.').resolve())
        module_path = str(relative_path.with_suffix('')).replace(os.sep, '.')
        return module_path


def generate_test_content(analyzer: PythonAnalyzer) -> str:
    """Generate test content based on the analyzed Python code."""
    module_path = analyzer.get_import_path()

    # Build import statements
    test_imports = f"import pytest\nfrom {module_path} import "

    # Add functions and classes to import
    all_imports = []
    for func in analyzer.functions:
        all_imports.append(func['name'])
    for cls in analyzer.classes:
        all_imports.append(cls['name'])

    if all_imports:
        test_imports += ", ".join(all_imports)

    test_content = f'{test_imports}\n\n'

    # Generate function tests
    for func in analyzer.functions:
        test_content += generate_function_test(func)
        test_content += "\n"

    # Generate class tests
    for cls in analyzer.classes:
        test_content += generate_class_tests(cls)
        test_content += "\n"

    return test_content


def generate_function_test(func: Dict[str, Any]) -> str:
    """Generate a test for a specific function."""
    test_name = f"test_{func['name']}"
    test_content = f"def {test_name}():\n"
    test_content += f'    """Test the {func["name"]} function."""\n'

    # Generate parameters for the test
    example_params = []
    for i, arg in enumerate(func['args']):
        if i == 0:
            example_params.append(f'param_{i+1}_value')
        else:
            example_params.append(f'param_{i+1}_value')

    params_str = ", ".join(example_params)

    # Add test content based on function name (with some heuristics)
    test_content += f"    # TODO: Add appropriate test values for {func['name']}\n"
    if example_params:
        test_content += f"    # result = {func['name']}({params_str})\n"
        test_content += f"    # assert result == expected_value\n"
    else:
        test_content += f"    # result = {func['name']}()\n"
        test_content += f"    # assert result == expected_value\n"

    test_content += f"    pass  # Implement test logic\n\n"
    return test_content


def generate_class_tests(cls: Dict[str, Any]) -> str:
    """Generate tests for a specific class."""
    test_content = f"class Test{cls['name']}:\n"
    test_content += f'    """Test cases for the {cls["name"]} class."""\n\n'

    # Add fixture for the class instance if there are methods
    if cls['methods']:
        test_content += f"    @pytest.fixture\n"
        test_content += f"    def {cls['name'].lower()}_instance(self):\n"
        test_content += f'        """Create a {cls["name"]} instance for testing."""\n'
        test_content += f"        return {cls['name']}()\n\n"

    # Generate tests for each method
    for method in cls['methods']:
        if method['name'] == '__init__':
            test_content += generate_init_test(cls['name'])
        else:
            test_content += generate_method_test(cls['name'], method)

        test_content += "\n"

    return test_content


def generate_init_test(class_name: str) -> str:
    """Generate a test for the __init__ method."""
    test_content = f"    def test_initialization(self):\n"
    test_content += f'        """Test {class_name} initialization."""\n'
    test_content += f"        # instance = {class_name}()\n"
    test_content += f"        # assert instance is not None\n"
    test_content += f"        pass  # Implement test logic\n\n"
    return test_content


def generate_method_test(class_name: str, method: Dict[str, Any]) -> str:
    """Generate a test for a specific method."""
    test_name = f"test_{method['name']}"
    test_content = f"    def {test_name}(self, {class_name.lower()}_instance):\n"
    test_content += f'        """Test the {method["name"]} method."""\n'

    # Generate parameters for the method test
    example_params = []
    for i, arg in enumerate(method['args']):
        if i == 0:
            example_params.append(f'param_{i+1}_value')
        else:
            example_params.append(f'param_{i+1}_value')

    params_str = ", ".join(example_params)

    # Add test content
    test_content += f"        # TODO: Add appropriate test values for {method['name']}\n"
    if example_params:
        test_content += f"        # result = {class_name.lower()}_instance.{method['name']}({params_str})\n"
        test_content += f"        # assert result == expected_value\n"
    else:
        test_content += f"        # result = {class_name.lower()}_instance.{method['name']}()\n"
        test_content += f"        # assert result == expected_value\n"

    test_content += f"        pass  # Implement test logic\n\n"
    return test_content


def main():
    if len(sys.argv) != 2:
        print("Usage: python generate_tests.py <path_to_python_file>")
        sys.exit(1)

    file_path = sys.argv[1]

    if not os.path.exists(file_path):
        print(f"File {file_path} does not exist.")
        sys.exit(1)

    if not file_path.endswith('.py'):
        print(f"{file_path} is not a Python file.")
        sys.exit(1)

    analyzer = PythonAnalyzer(file_path)
    analyzer.analyze()

    if not analyzer.functions and not analyzer.classes:
        print(f"No testable functions or classes found in {file_path}")
        sys.exit(0)

    test_content = generate_test_content(analyzer)

    # Generate test file name
    source_path = Path(file_path)
    test_dir = source_path.parent / "tests"
    test_dir.mkdir(exist_ok=True)

    # Create test file name with 'test_' prefix
    test_file_name = f"test_{source_path.name}"
    test_file_path = test_dir / test_file_name

    with open(test_file_path, 'w', encoding='utf-8') as test_file:
        test_file.write(test_content)

    print(f"Test file generated: {test_file_path}")
    print(f"Functions found: {len(analyzer.functions)}")
    print(f"Classes found: {len(analyzer.classes)}")


if __name__ == "__main__":
    main()