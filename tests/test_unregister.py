"""
Tests for DELETE /activities/{activity_name}/participants/{email} endpoint using AAA pattern
"""
import pytest
from src.app import activities


class TestUnregister:
    """Test suite for student activity unregistration"""

    def test_unregister_success(self, client):
        """
        Arrange: Select an activity with existing participant
        Act: Make DELETE request to unregister the participant
        Assert: Response indicates success and student is removed
        """
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already in participants

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants/{email}"
        )

        # Assert
        assert response.status_code == 200
        assert "Unregistered" in response.json()["message"]
        assert email not in activities[activity_name]["participants"]

    def test_unregister_removes_participant_from_list(self, client):
        """
        Arrange: Count initial participants for an activity
        Act: Make DELETE request to remove a participant
        Assert: Participants count decreases by one
        """
        # Arrange
        activity_name = "Programming Class"
        email = "emma@mergington.edu"  # Already in participants
        initial_count = len(activities[activity_name]["participants"])

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants/{email}"
        )

        # Assert
        assert response.status_code == 200
        assert len(activities[activity_name]["participants"]) == initial_count - 1

    def test_unregister_invalid_activity(self, client):
        """
        Arrange: Prepare test data with non-existent activity
        Act: Make DELETE request for non-existent activity
        Assert: Response indicates 404 error
        """
        # Arrange
        activity_name = "Nonexistent Club"
        email = "test@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants/{email}"
        )

        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]

    def test_unregister_not_registered_student(self, client):
        """
        Arrange: Select student not registered for activity
        Act: Make DELETE request to unregister non-existent participant
        Assert: Response indicates 400 error (not registered)
        """
        # Arrange
        activity_name = "Chess Club"
        email = "nonexistent@mergington.edu"  # Not in participants

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants/{email}"
        )

        # Assert
        assert response.status_code == 400
        assert "not registered" in response.json()["detail"]

    def test_unregister_returns_message(self, client):
        """
        Arrange: Select an activity with existing participant
        Act: Make DELETE request
        Assert: Response contains formatted message
        """
        # Arrange
        activity_name = "Gym Class"
        email = "john@mergington.edu"  # Already in participants

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants/{email}"
        )

        # Assert
        data = response.json()
        assert "message" in data
        assert email in data["message"]
        assert activity_name in data["message"]

    def test_unregister_then_cannot_unregister_again(self, client):
        """
        Arrange: Select an activity with existing participant
        Act: Unregister the same participant twice
        Assert: Second unregister returns 400 error
        """
        # Arrange
        activity_name = "Drama Club"
        email = "noah@mergington.edu"  # Already in participants

        # Act - First unregister (should succeed)
        response1 = client.delete(
            f"/activities/{activity_name}/participants/{email}"
        )

        # Act - Second unregister (should fail)
        response2 = client.delete(
            f"/activities/{activity_name}/participants/{email}"
        )

        # Assert
        assert response1.status_code == 200
        assert response2.status_code == 400
        assert "not registered" in response2.json()["detail"]

    def test_unregister_then_can_register_again(self, client):
        """
        Arrange: Select an activity with existing participant
        Act: Unregister the participant, then re-register
        Assert: Student can register after unregistering
        """
        # Arrange
        activity_name = "Debate Team"
        email = "grace@mergington.edu"

        # Act - Unregister
        response1 = client.delete(
            f"/activities/{activity_name}/participants/{email}"
        )

        # Act - Re-register
        response2 = client.post(f"/activities/{activity_name}/signup?email={email}")

        # Assert
        assert response1.status_code == 200
        assert response2.status_code == 200
        assert email in activities[activity_name]["participants"]
