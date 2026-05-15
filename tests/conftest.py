import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def client():
    """Fixture providing TestClient for API testing"""
    return TestClient(app)


@pytest.fixture
def reset_activities():
    """Fixture to reset activities to a known state before and after each test"""
    from src import app as app_module
    import copy
    
    # Store original activities before the test
    original_activities = copy.deepcopy(app_module.activities)
    
    yield
    
    # Reset activities after test to original state
    app_module.activities.clear()
    app_module.activities.update(copy.deepcopy(original_activities))
