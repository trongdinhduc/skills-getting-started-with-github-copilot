import pytest
from copy import deepcopy
from starlette.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def original_activities():
    """Store the original activities state"""
    return deepcopy(activities)


@pytest.fixture
def client(original_activities):
    """Provide a TestClient and reset activities before each test"""
    # Reset activities to original state
    activities.clear()
    activities.update(deepcopy(original_activities))
    
    # Return TestClient
    return TestClient(app)


@pytest.fixture
def sample_email():
    """Provide a sample email for testing"""
    return "test.student@mergington.edu"


@pytest.fixture
def new_student_email():
    """Provide a different sample email for testing"""
    return "new.student@mergington.edu"
