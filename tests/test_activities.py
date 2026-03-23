"""
Tests for GET /activities endpoint using AAA (Arrange-Act-Assert) pattern
"""
import pytest


class TestGetActivities:
    """Test suite for retrieving activities list"""

    def test_get_activities_success(self, client):
        """
        Arrange: Test client is ready
        Act: Make GET request to /activities
        Assert: Response is successful with expected status code
        """
        # Arrange
        # (client fixture is already set up)

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200

    def test_get_activities_returns_dict(self, client):
        """
        Arrange: Test client is ready
        Act: Make GET request to /activities
        Assert: Response body is a dictionary
        """
        # Arrange
        # (client fixture is already set up)

        # Act
        response = client.get("/activities")
        data = response.json()

        # Assert
        assert isinstance(data, dict)

    def test_get_activities_contains_expected_activities(self, client):
        """
        Arrange: Test client is ready
        Act: Make GET request to /activities
        Assert: Response contains expected activity names
        """
        # Arrange
        expected_activities = ["Chess Club", "Programming Class", "Gym Class"]

        # Act
        response = client.get("/activities")
        data = response.json()

        # Assert
        for activity in expected_activities:
            assert activity in data

    def test_get_activities_activity_has_required_fields(self, client):
        """
        Arrange: Test client is ready
        Act: Make GET request to /activities
        Assert: Each activity has required fields
        """
        # Arrange
        required_fields = ["description", "schedule", "max_participants", "participants"]

        # Act
        response = client.get("/activities")
        data = response.json()

        # Assert
        for activity_name, activity_data in data.items():
            for field in required_fields:
                assert field in activity_data, f"{activity_name} missing field: {field}"

    def test_get_activities_participants_is_list(self, client):
        """
        Arrange: Test client is ready
        Act: Make GET request to /activities
        Assert: Participants field is a list
        """
        # Arrange
        # (client fixture is already set up)

        # Act
        response = client.get("/activities")
        data = response.json()

        # Assert
        for activity_name, activity_data in data.items():
            assert isinstance(
                activity_data["participants"], list
            ), f"{activity_name} participants should be a list"
