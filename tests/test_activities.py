"""
Tests for the GET /activities endpoint
"""
import pytest


class TestGetActivities:
    """Test suite for retrieving all activities"""
    
    def test_get_all_activities_returns_success(self, client):
        """
        Arrange: TestClient is ready
        Act: Make GET request to /activities
        Assert: Response status is 200
        """
        # Arrange
        # client fixture provides TestClient
        
        # Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200
    
    def test_get_all_activities_returns_all_activities(self, client):
        """
        Arrange: Activities are loaded in the fixture
        Act: Make GET request to /activities
        Assert: Response contains all 9 activities
        """
        # Arrange
        expected_activities = [
            "Chess Club",
            "Programming Class",
            "Gym Class",
            "Basketball",
            "Tennis Club",
            "Art Studio",
            "Theater Club",
            "Debate Team",
            "Science Club"
        ]
        
        # Act
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        assert len(activities) == 9
        for activity_name in expected_activities:
            assert activity_name in activities
    
    def test_activity_has_required_fields(self, client):
        """
        Arrange: Call endpoint to get activities
        Act: Get activities and check one activity's structure
        Assert: Each activity has required fields (description, schedule, max_participants, participants)
        """
        # Arrange
        required_fields = ["description", "schedule", "max_participants", "participants"]
        
        # Act
        response = client.get("/activities")
        activities = response.json()
        chess_club = activities["Chess Club"]
        
        # Assert
        for field in required_fields:
            assert field in chess_club
    
    def test_participants_is_list(self, client):
        """
        Arrange: Get activities response
        Act: Retrieve an activity and check participants type
        Assert: Participants is a list
        """
        # Arrange
        # client fixture is ready
        
        # Act
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        for activity_name, activity_data in activities.items():
            assert isinstance(activity_data["participants"], list), \
                f"Participants for {activity_name} should be a list"
    
    def test_initial_participants_count(self, client):
        """
        Arrange: Get activities response
        Act: Check initial participant counts
        Assert: Participants match expected initial values
        """
        # Arrange
        expected_counts = {
            "Chess Club": 2,
            "Programming Class": 2,
            "Gym Class": 2,
            "Basketball": 1,
            "Tennis Club": 1,
            "Art Studio": 2,
            "Theater Club": 1,
            "Debate Team": 2,
            "Science Club": 1
        }
        
        # Act
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        for activity_name, expected_count in expected_counts.items():
            actual_count = len(activities[activity_name]["participants"])
            assert actual_count == expected_count, \
                f"{activity_name} should have {expected_count} participants, got {actual_count}"
