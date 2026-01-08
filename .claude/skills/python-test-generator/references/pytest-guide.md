# Pytest Reference Guide

## Core Pytest Concepts

### Fixtures
Fixtures are functions that provide data or setup for tests. They are used with the `@pytest.fixture` decorator and can be injected into test functions by including the fixture name as a parameter.

```python
import pytest

@pytest.fixture
def temporary_file(tmp_path):
    file_path = tmp_path / "test_file.txt"
    file_path.write_text("test content")
    return file_path

def test_file_content(temporary_file):
    assert temporary_file.read_text() == "test content"
```

### Parametrized Testing
Parametrized testing allows running the same test with multiple input sets:

```python
@pytest.mark.parametrize("input,expected", [
    (2, 4),
    (3, 9),
    (4, 16),
])
def test_square(input, expected):
    assert input ** 2 == expected
```

### Markers
Markers allow you to tag tests with metadata and run specific subsets:

```python
@pytest.mark.slow
def test_slow_operation():
    # This test will only run when explicitly requested
    pass

@pytest.mark.integration
def test_integration():
    # Integration test
    pass
```

## Pytest Command Line Options

- `pytest`: Run all tests
- `pytest test_file.py`: Run tests in a specific file
- `pytest test_file.py::test_function`: Run a specific test
- `pytest -k "test_name"`: Run tests matching a pattern
- `pytest -m "marker_name"`: Run tests with a specific marker
- `pytest --cov=module`: Run tests with coverage
- `pytest -x`: Stop after first failure
- `pytest --lf`: Run only the last failed tests

## Advanced Pytest Patterns

### Session-scoped Fixtures
```python
@pytest.fixture(scope="session")
def database_connection():
    # Setup once for the entire test session
    conn = create_connection()
    yield conn
    conn.close()
```

### Class-scoped Fixtures
```python
@pytest.fixture(scope="class")
def setup_class():
    # Setup once for all tests in the class
    return SomeClass()
```

### Conditional Fixtures
```python
@pytest.fixture
def conditional_fixture(request):
    if request.config.getoption("--integration"):
        return integration_setup()
    else:
        return mock_setup()
```

## Testing Different Python Code Types

### Testing Functions
```python
def add_numbers(a, b):
    return a + b

def test_add_numbers():
    assert add_numbers(2, 3) == 5
    assert add_numbers(-1, 1) == 0
    assert add_numbers(0, 0) == 0
```

### Testing Classes
```python
class Calculator:
    def __init__(self):
        self.history = []

    def add(self, a, b):
        result = a + b
        self.history.append(f"{a} + {b} = {result}")
        return result

@pytest.fixture
def calculator():
    return Calculator()

def test_calculator_add(calculator):
    result = calculator.add(2, 3)
    assert result == 5
    assert len(calculator.history) == 1
```

### Testing Async Code
```python
import pytest
import asyncio

async def async_add(a, b):
    await asyncio.sleep(0.1)  # Simulate async operation
    return a + b

@pytest.mark.asyncio
async def test_async_add():
    result = await async_add(2, 3)
    assert result == 5
```

### Testing with Mocks
```python
from unittest.mock import Mock, patch

def fetch_data_from_api(url):
    import requests
    response = requests.get(url)
    return response.json()

def test_fetch_data_from_api():
    with patch('requests.get') as mock_get:
        mock_response = Mock()
        mock_response.json.return_value = {"data": "test"}
        mock_get.return_value = mock_response

        result = fetch_data_from_api("http://example.com")

        assert result == {"data": "test"}
        mock_get.assert_called_once_with("http://example.com")
```

## Testing Web Applications

### Flask Testing
```python
import pytest
from myapp import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_page(client):
    rv = client.get('/')
    assert rv.status_code == 200
    assert b'Welcome' in rv.data
```

### Django Testing
```python
import pytest
from django.test import Client
from django.urls import reverse

@pytest.fixture
def api_client():
    return Client()

def test_api_endpoint(api_client):
    url = reverse('api-endpoint')
    response = api_client.get(url)
    assert response.status_code == 200
```

## Testing Data Processing
```python
def process_data(data_list):
    """Process a list of dictionaries and return filtered results."""
    return [item for item in data_list if item.get('active', False)]

def test_process_data():
    input_data = [
        {'id': 1, 'active': True},
        {'id': 2, 'active': False},
        {'id': 3, 'active': True},
    ]

    result = process_data(input_data)

    assert len(result) == 2
    assert result[0]['id'] == 1
    assert result[1]['id'] == 3
```

## Exception Testing
```python
def divide(a, b):
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return a / b

def test_divide_by_zero():
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)

def test_divide_by_zero_message():
    with pytest.raises(ZeroDivisionError, match="Cannot divide by zero"):
        divide(10, 0)
```

## Test Organization Best Practices

### Test File Organization
```
tests/
├── conftest.py              # Common fixtures
├── test_models.py           # Model tests
├── test_views.py            # View tests
├── test_utils.py            # Utility function tests
└── integration/
    ├── test_api.py          # API integration tests
    └── test_workflow.py     # Workflow tests
```

### conftest.py Example
```python
import pytest
import tempfile
import os

@pytest.fixture
def temp_file():
    """Create a temporary file for testing."""
    temp_dir = tempfile.mkdtemp()
    temp_path = os.path.join(temp_dir, "temp_file.txt")
    yield temp_path
    # Cleanup after test
    if os.path.exists(temp_path):
        os.remove(temp_path)
    os.rmdir(temp_dir)
```

## Pytest Plugins

### pytest-cov (Coverage)
```bash
pip install pytest-cov
pytest --cov=myproject --cov-report=html
```

### pytest-mock
```python
def test_with_mock(mocker):
    mocker.patch('myproject.module.function', return_value=42)
    result = myproject.module.function()
    assert result == 42
```

### pytest-bdd (Behavior Driven Development)
```gherkin
Feature: Calculator
  Scenario: Add two numbers
    Given I have a calculator
    When I add 2 and 3
    Then the result should be 5
```

## Performance Testing
```python
import time
import pytest

def test_performance():
    start_time = time.time()
    # Code to test performance
    result = expensive_operation()
    end_time = time.time()

    assert end_time - start_time < 1.0  # Should complete in under 1 second
```

## Testing Configuration and Environment
```python
import os
import pytest

@pytest.fixture
def temp_env_var():
    os.environ['TEST_VAR'] = 'test_value'
    yield
    # Cleanup
    if 'TEST_VAR' in os.environ:
        del os.environ['TEST_VAR']

def test_with_env_var(temp_env_var):
    assert os.environ['TEST_VAR'] == 'test_value'
```

## Common Pytest Assertions

```python
# Basic assertions
assert result == expected
assert result != unexpected
assert item in collection
assert item not in collection

# Boolean assertions
assert condition
assert not condition

# Exception assertions
with pytest.raises(ExceptionType):
    dangerous_operation()

# Float assertions (with tolerance)
assert 0.1 + 0.2 == pytest.approx(0.3)

# Exception with message
with pytest.raises(ValueError, match="expected message"):
    raise ValueError("expected message")
```

## Testing Strategies for Different Scenarios

### Unit Testing Strategy
- Test individual functions/methods in isolation
- Use mocks to replace external dependencies
- Focus on one specific behavior per test
- Aim for high code coverage

### Integration Testing Strategy
- Test how multiple components work together
- Use real dependencies when possible
- Test complete workflows
- Verify data flows between components

### End-to-End Testing Strategy
- Test complete user journeys
- Use real environments when possible
- Verify system behavior from start to finish
- Focus on critical user paths