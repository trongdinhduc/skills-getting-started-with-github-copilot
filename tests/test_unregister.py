"""
Tests for the unregister endpoint using AAA (Arrange-Act-Assert) pattern
"""


def test_unregister_success(client, reset_activities):
    """Test successful unregister from an activity"""
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Already registered
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/unregister?email={email}"
    )
    
    # Assert
    assert response.status_code == 200
    assert email in response.json()["message"]
    
    # Verify participant was removed
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert email not in activities[activity_name]["participants"]


def test_unregister_not_registered_fails(client, reset_activities):
    """Test that unregister for non-registered student fails"""
    # Arrange
    activity_name = "Chess Club"
    email = "notregistered@mergington.edu"
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/unregister?email={email}"
    )
    
    # Assert
    assert response.status_code == 400
    assert "not registered" in response.json()["detail"].lower()


def test_unregister_nonexistent_activity_fails(client, reset_activities):
    """Test that unregister from non-existent activity fails"""
    # Arrange
    activity_name = "NonExistent Club"
    email = "student@mergington.edu"
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/unregister?email={email}"
    )
    
    # Assert
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_unregister_decreases_participant_count(client, reset_activities):
    """Test that unregister decreases the participant count"""
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    
    # Get initial count
    initial_response = client.get("/activities")
    initial_count = len(initial_response.json()[activity_name]["participants"])
    
    # Act
    client.post(f"/activities/{activity_name}/unregister?email={email}")
    
    # Assert
    updated_response = client.get("/activities")
    updated_count = len(updated_response.json()[activity_name]["participants"])
    assert updated_count == initial_count - 1
