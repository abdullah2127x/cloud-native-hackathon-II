---
name: python-test-generator
description: Comprehensive Python test generation with pytest framework. Generate unit tests, integration tests, parametrized tests, and fixture-based tests for Python code. Handles various Python code types including modules, classes, functions, web applications, and APIs.
---

# Python Test Generator

Generate comprehensive Python tests using the pytest framework for any Python codebase.

## What This Skill Does

This skill generates pytest-based tests for Python code including:
- Unit tests for functions and methods
- Integration tests for multiple components
- Parametrized tests for multiple input scenarios
- Fixture-based tests for setup/teardown
- Exception and error condition tests
- Test coverage considerations

## What This Skill Does NOT Do

- Run the tests (use pytest command separately)
- Install pytest or manage dependencies
- Debug failing tests
- Generate tests for non-Python code

## Before Implementation

Gather context to ensure successful implementation:

| Source | Gather |
|--------|--------|
| **Codebase** | Python project structure, existing test patterns, imports, dependencies |
| **Conversation** | User's specific testing requirements, target functions/classes to test |
| **Skill References** | Pytest patterns from `references/` (fixtures, parametrization, best practices) |
| **User Guidelines** | Project-specific testing conventions, team standards |

Ensure all required context is gathered before implementing.

## Test Generation Process

### Step 1: Analyze Target Code
- Identify functions, methods, and classes to test
- Determine input parameters and expected return types
- Identify potential edge cases and error conditions
- Note any dependencies that may need mocking

### Step 2: Determine Test Types Needed
- Unit tests: Test individual functions/methods in isolation
- Integration tests: Test interactions between components
- Parametrized tests: Test with multiple input combinations
- Exception tests: Test error handling and edge cases

### Step 3: Generate Test Structure
- Create appropriate test file names (test_*.py or *_test.py)
- Set up fixtures for common test data/setup
- Write test functions with descriptive names
- Follow AAA pattern (Arrange, Act, Assert)

### Step 4: Apply Best Practices
- Use descriptive test names that explain expected behavior
- Keep tests independent and isolated
- Test both positive and negative cases
- Include appropriate assertions

## Pytest Best Practices

### Naming Conventions
- Test files: `test_*.py` or `*_test.py`
- Test functions: `test_*` (e.g., `test_calculate_sum`, `test_invalid_input_raises_error`)
- Test classes: `Test*` (e.g., `TestClassProcessor`)

### Test Structure (AAA Pattern)
```python
def test_function_behavior():
    # Arrange - Set up test data
    input_data = "test_value"
    expected_result = "expected_value"

    # Act - Execute the function
    result = function_to_test(input_data)

    # Assert - Verify the result
    assert result == expected_result
```

### Using Fixtures
```python
import pytest

@pytest.fixture
def sample_data():
    return {"key": "value", "number": 42}

def test_with_fixture(sample_data):
    assert sample_data["number"] == 42
```

### Parametrized Tests
```python
@pytest.mark.parametrize("input,expected", [
    (2, 4),
    (3, 9),
    (4, 16),
])
def test_square_function(input, expected):
    assert square(input) == expected
```

### Testing Exceptions
```python
def test_invalid_input_raises_error():
    with pytest.raises(ValueError):
        function_with_validation("invalid_input")
```

### Mocking Dependencies
```python
from unittest.mock import Mock
import pytest

def test_function_with_external_dependency():
    mock_dependency = Mock()
    mock_dependency.get_data.return_value = "test_data"

    result = function_using_dependency(mock_dependency)

    assert result == "expected_result"
    mock_dependency.get_data.assert_called_once()
```

## Test Coverage Considerations

When generating tests, ensure coverage of:
- Normal operation cases
- Edge cases (empty inputs, boundary values)
- Error conditions
- Exception handling
- Multiple code paths (if/else branches)

## Common Test Scenarios

### For Functions
- Test with valid inputs and expected outputs
- Test with edge cases (empty strings, zero values, None)
- Test error conditions and exception handling
- Test performance with large inputs if applicable

### For Classes
- Test initialization and constructor parameters
- Test all public methods
- Test state changes
- Test interactions between methods
- Test error conditions in methods

### For Web Applications (Flask/Django)
- Test route responses
- Test HTTP methods (GET, POST, PUT, DELETE)
- Test request data handling
- Test response formatting
- Test error handling for invalid requests

## Generated Test Template

Based on the target Python code, this skill will generate tests following this structure:

```python
import pytest
from path.to.module import function_to_test, ClassToTest

class TestFunctionToTest:
    """Test cases for function_to_test."""

    def test_normal_operation(self):
        """Test function with normal inputs."""
        # Implementation based on target function

    def test_edge_cases(self):
        """Test function with edge case inputs."""
        # Implementation based on target function

    def test_error_conditions(self):
        """Test function error handling."""
        # Implementation based on target function

class TestClassToTest:
    """Test cases for ClassToTest."""

    @pytest.fixture
    def sample_instance(self):
        """Create a sample instance for testing."""
        return ClassToTest()

    def test_initialization(self, sample_instance):
        """Test class initialization."""
        # Implementation based on class
```