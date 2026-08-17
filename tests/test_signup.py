"""
Tests for the POST /activities/{activity_name}/signup endpoint
"""
import pytest


class TestSignupForActivity:
    """Test suite for signing up students for activities"""
    
    def test_signup_successful(self, client):
        """
        Arrange: Prepare activity name and new email
        Act: POST signup request for new participant
        Assert: Response is 200 and participant is added
        """
        # Arrange
        activity_name = "Chess Club"
        new_email = "newstudent@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": new_email}
        )
        
        # Assert
        assert response.status_code == 200
        assert "Signed up" in response.json()["message"]
    
    def test_signup_adds_participant_to_activity(self, client):
        """
        Arrange: Prepare activity name and new email
        Act: Sign up new participant and fetch activities
        Assert: New participant appears in activity's participant list
        """
        # Arrange
        activity_name = "Chess Club"
        new_email = "alice@mergington.edu"
        
        # Act
        client.post(f"/activities/{activity_name}/signup", params={"email": new_email})
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        assert new_email in activities[activity_name]["participants"]
    
    def test_signup_duplicate_email_returns_400(self, client):
        """
        Arrange: Use email already signed up (michael@mergington.edu for Chess Club)
        Act: POST signup request with duplicate email
        Assert: Response is 400 with appropriate error message
        """
        # Arrange
        activity_name = "Chess Club"
        existing_email = "michael@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": existing_email}
        )
        
        # Assert
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]
    
    def test_signup_nonexistent_activity_returns_404(self, client):
        """
        Arrange: Use non-existent activity name
        Act: POST signup request to non-existent activity
        Assert: Response is 404 with Activity not found message
        """
        # Arrange
        activity_name = "Nonexistent Club"
        email = "student@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]
    
    def test_signup_response_contains_message(self, client):
        """
        Arrange: Prepare valid signup request
        Act: Sign up and get response
        Assert: Response contains success message with email and activity name
        """
        # Arrange
        activity_name = "Programming Class"
        email = "bob@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        data = response.json()
        
        # Assert
        assert "message" in data
        assert email in data["message"]
        assert activity_name in data["message"]
    
    def test_signup_multiple_participants_sequential(self, client):
        """
        Arrange: Prepare multiple new emails for same activity
        Act: Sign up multiple participants sequentially
        Assert: All participants are added successfully
        """
        # Arrange
        activity_name = "Basketball"
        emails = ["participant1@mergington.edu", "participant2@mergington.edu"]
        
        # Act
        for email in emails:
            response = client.post(
                f"/activities/{activity_name}/signup",
                params={"email": email}
            )
            assert response.status_code == 200
        
        # Get updated activities
        response = client.get("/activities")
        participants = response.json()[activity_name]["participants"]
        
        # Assert
        for email in emails:
            assert email in participants
    
    def test_signup_increments_participant_count(self, client):
        """
        Arrange: Get initial participant count
        Act: Sign up new participant
        Assert: Participant count increased by 1
        """
        # Arrange
        activity_name = "Tennis Club"
        new_email = "newplayer@mergington.edu"
        initial_response = client.get("/activities")
        initial_count = len(initial_response.json()[activity_name]["participants"])
        
        # Act
        client.post(f"/activities/{activity_name}/signup", params={"email": new_email})
        updated_response = client.get("/activities")
        updated_count = len(updated_response.json()[activity_name]["participants"])
        
        # Assert
        assert updated_count == initial_count + 1
