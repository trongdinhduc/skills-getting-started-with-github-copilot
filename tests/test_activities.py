"""
Tests for the activities endpoints using AAA (Arrange-Act-Assert) pattern
"""


def test_get_activities(client):
    """Test retrieving all activities"""
    # Arrange
    expected_activities = ["Chess Club", "Programming Class", "Gym Class"]
    
    # Act
    response = client.get("/activities")
    
    # Assert
    assert response.status_code == 200
    activities = response.json()
    for activity_name in expected_activities:
        assert activity_name in activities


def test_get_activities_structure(client):
    """Test that activities have required fields"""
    # Arrange
    required_fields = ["description", "schedule", "max_participants", "participants"]
    
    # Act
    response = client.get("/activities")
    activities = response.json()
    
    # Assert
    for activity_name, activity_data in activities.items():
        for field in required_fields:
            assert field in activity_data, f"Missing field '{field}' in {activity_name}"


def test_root_redirect(client):
    """Test that root path redirects to index.html"""
    # Arrange
    expected_redirect = "/static/index.html"
    
    # Act
    response = client.get("/", follow_redirects=False)
    
    # Assert
    assert response.status_code == 307
    assert expected_redirect in response.headers["location"]
