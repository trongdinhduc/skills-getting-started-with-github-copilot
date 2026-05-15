"""
Tests for the signup endpoint using AAA (Arrange-Act-Assert) pattern
"""


def test_signup_success(client, reset_activities):
    """Test successful signup for an activity"""
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup?email={email}"
    )
    
    # Assert
    assert response.status_code == 200
    assert email in response.json()["message"]
    
    # Verify participant was added
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert email in activities[activity_name]["participants"]


def test_signup_duplicate_fails(client, reset_activities):
    """Test that duplicate signup fails"""
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Already registered
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup?email={email}"
    )
    
    # Assert
    assert response.status_code == 400
    assert "already" in response.json()["detail"].lower()


def test_signup_nonexistent_activity_fails(client, reset_activities):
    """Test that signup for non-existent activity fails"""
    # Arrange
    activity_name = "NonExistent Club"
    email = "student@mergington.edu"
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup?email={email}"
    )
    
    # Assert
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_signup_increases_participant_count(client, reset_activities):
    """Test that signup increases the participant count"""
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    
    # Get initial count
    initial_response = client.get("/activities")
    initial_count = len(initial_response.json()[activity_name]["participants"])
    
    # Act
    client.post(f"/activities/{activity_name}/signup?email={email}")
    
    # Assert
    updated_response = client.get("/activities")
    updated_count = len(updated_response.json()[activity_name]["participants"])
    assert updated_count == initial_count + 1
