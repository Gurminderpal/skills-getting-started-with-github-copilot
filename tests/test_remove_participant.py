"""
Tests for the DELETE /activities/{activity_name}/participants/{email} endpoint
"""
import pytest


class TestRemoveParticipant:
    """Test suite for removing participants from activities"""
    
    def test_remove_participant_successful(self, client):
        """
        Arrange: Prepare existing participant to remove
        Act: DELETE request to remove participant
        Assert: Response is 200 with success message
        """
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"
        
        # Act
        response = client.delete(f"/activities/{activity_name}/participants/{email}")
        
        # Assert
        assert response.status_code == 200
        assert "message" in response.json()
        assert email in response.json()["message"]
    
    def test_remove_participant_removes_from_list(self, client):
        """
        Arrange: Get initial participants list
        Act: Remove a participant and fetch activities
        Assert: Participant is no longer in the list
        """
        # Arrange
        activity_name = "Art Studio"
        email = "sara@mergington.edu"
        
        # Act
        client.delete(f"/activities/{activity_name}/participants/{email}")
        response = client.get("/activities")
        participants = response.json()[activity_name]["participants"]
        
        # Assert
        assert email not in participants
    
    def test_remove_nonexistent_participant_returns_400(self, client):
        """
        Arrange: Use email not signed up for activity
        Act: DELETE request to remove non-existent participant
        Assert: Response is 400 with appropriate error message
        """
        # Arrange
        activity_name = "Chess Club"
        email = "notregistered@mergington.edu"
        
        # Act
        response = client.delete(f"/activities/{activity_name}/participants/{email}")
        
        # Assert
        assert response.status_code == 400
        assert "not signed up" in response.json()["detail"]
    
    def test_remove_from_nonexistent_activity_returns_404(self, client):
        """
        Arrange: Use non-existent activity name
        Act: DELETE request from non-existent activity
        Assert: Response is 404 with Activity not found message
        """
        # Arrange
        activity_name = "Nonexistent Club"
        email = "student@mergington.edu"
        
        # Act
        response = client.delete(f"/activities/{activity_name}/participants/{email}")
        
        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]
    
    def test_remove_participant_decrements_count(self, client):
        """
        Arrange: Get initial participant count
        Act: Remove a participant
        Assert: Participant count decreased by 1
        """
        # Arrange
        activity_name = "Debate Team"
        email = "ryan@mergington.edu"
        initial_response = client.get("/activities")
        initial_count = len(initial_response.json()[activity_name]["participants"])
        
        # Act
        client.delete(f"/activities/{activity_name}/participants/{email}")
        updated_response = client.get("/activities")
        updated_count = len(updated_response.json()[activity_name]["participants"])
        
        # Assert
        assert updated_count == initial_count - 1
    
    def test_remove_multiple_participants_sequential(self, client):
        """
        Arrange: Prepare existing participants to remove
        Act: Remove multiple participants sequentially
        Assert: All participants are removed successfully
        """
        # Arrange
        activity_name = "Programming Class"
        emails = ["emma@mergington.edu", "sophia@mergington.edu"]
        
        # Act
        for email in emails:
            response = client.delete(f"/activities/{activity_name}/participants/{email}")
            assert response.status_code == 200
        
        # Get updated activities
        response = client.get("/activities")
        participants = response.json()[activity_name]["participants"]
        
        # Assert
        for email in emails:
            assert email not in participants
    
    def test_remove_then_readd_participant(self, client):
        """
        Arrange: Prepare participant to remove and re-add
        Act: Remove participant, then sign them up again
        Assert: Participant can be added back successfully
        """
        # Arrange
        activity_name = "Gym Class"
        email = "john@mergington.edu"
        
        # Act - Remove
        remove_response = client.delete(f"/activities/{activity_name}/participants/{email}")
        
        # Assert removal was successful
        assert remove_response.status_code == 200
        
        # Act - Re-add
        signup_response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert signup was successful
        assert signup_response.status_code == 200
        
        # Verify participant is in list
        get_response = client.get("/activities")
        participants = get_response.json()[activity_name]["participants"]
        assert email in participants
    
    def test_remove_response_message_format(self, client):
        """
        Arrange: Prepare valid removal request
        Act: Remove participant and check response
        Assert: Response message contains email and activity name
        """
        # Arrange
        activity_name = "Science Club"
        email = "noah@mergington.edu"
        
        # Act
        response = client.delete(f"/activities/{activity_name}/participants/{email}")
        data = response.json()
        
        # Assert
        assert "message" in data
        assert email in data["message"]
        assert activity_name in data["message"]
        assert "Removed" in data["message"]
