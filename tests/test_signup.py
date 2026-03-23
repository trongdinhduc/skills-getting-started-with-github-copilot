"""
Tests for POST /activities/{activity_name}/signup endpoint using AAA pattern
"""
import pytest
from src.app import activities


class TestSignup:
    """Test suite for student activity signup"""

    def test_signup_success(self, client, new_student_email):
        """
        Arrange: Prepare test data with a new student and valid activity
        Act: Make POST request to signup endpoint
        Assert: Response indicates success and student is added to participants
        """
        # Arrange
        activity_name = "Chess Club"
        email = new_student_email

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )

        # Assert
        assert response.status_code == 200
        assert "Signed up" in response.json()["message"]
        assert email in activities[activity_name]["participants"]

    def test_signup_adds_participant_to_list(self, client, new_student_email):
        """
        Arrange: Count initial participants for an activity
        Act: Make POST request to signup a new student
        Assert: Participants count increases by one
        """
        # Arrange
        activity_name = "Programming Class"
        email = new_student_email
        initial_count = len(activities[activity_name]["participants"])

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )

        # Assert
        assert response.status_code == 200
        assert len(activities[activity_name]["participants"]) == initial_count + 1

    def test_signup_invalid_activity(self, client, new_student_email):
        """
        Arrange: Prepare test data with non-existent activity
        Act: Make POST request to signup for invalid activity
        Assert: Response indicates 404 error
        """
        # Arrange
        activity_name = "Nonexistent Club"
        email = new_student_email

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )

        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]

    def test_signup_duplicate_email(self, client):
        """
        Arrange: Select an activity with an existing participant
        Act: Try to signup the same participant twice
        Assert: Response indicates 400 error (already registered)
        """
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already registered
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )

        # Assert
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]

    def test_signup_returns_message(self, client, new_student_email):
        """
        Arrange: Prepare test data for signup
        Act: Make POST request
        Assert: Response contains formatted message
        """
        # Arrange
        activity_name = "Gym Class"
        email = new_student_email

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )

        # Assert
        data = response.json()
        assert "message" in data
        assert email in data["message"]
        assert activity_name in data["message"]

    def test_signup_multiple_students_same_activity(self, client, sample_email, new_student_email):
        """
        Arrange: Prepare two different emails for signup
        Act: Sign up both students for the same activity
        Assert: Both are added to participants list
        """
        # Arrange
        activity_name = "Art Studio"
        email1 = sample_email
        email2 = new_student_email

        # Act
        response1 = client.post(f"/activities/{activity_name}/signup?email={email1}")
        response2 = client.post(f"/activities/{activity_name}/signup?email={email2}")

        # Assert
        assert response1.status_code == 200
        assert response2.status_code == 200
        assert email1 in activities[activity_name]["participants"]
        assert email2 in activities[activity_name]["participants"]
