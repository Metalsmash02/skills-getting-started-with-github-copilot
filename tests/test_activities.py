"""
Tests for the GET /activities endpoint using the AAA (Arrange-Act-Assert) pattern.
"""

import pytest


class TestGetActivities:
    """Test suite for the GET /activities endpoint."""
    
    def test_get_activities_returns_all_activities(self, client, reset_activities):
        """
        TEST: Get Activities - Success Case
        
        Arrange: Reset activities to known state
        Act: Make GET request to /activities
        Assert: Response status is 200 and contains all expected activities
        """
        # Arrange: fixture handles reset_activities
        expected_activities = ["Chess Club", "Programming Class", "Gym Class"]
        
        # Act
        response = client.get("/activities")
        data = response.json()
        
        # Assert
        assert response.status_code == 200
        assert len(data) == 3
        for activity_name in expected_activities:
            assert activity_name in data
    
    def test_get_activities_returns_correct_structure(self, client, reset_activities):
        """
        TEST: Get Activities - Response Structure Validation
        
        Arrange: Reset activities to known state
        Act: Make GET request to /activities
        Assert: Each activity has required fields (description, schedule, max_participants, participants)
        """
        # Arrange: fixture handles reset_activities
        required_fields = {"description", "schedule", "max_participants", "participants"}
        
        # Act
        response = client.get("/activities")
        data = response.json()
        
        # Assert
        assert response.status_code == 200
        for activity_name, activity_details in data.items():
            assert isinstance(activity_details, dict)
            assert required_fields.issubset(set(activity_details.keys()))
            assert isinstance(activity_details["participants"], list)
            assert isinstance(activity_details["max_participants"], int)
    
    def test_get_activities_participants_are_persisted(self, client, reset_activities):
        """
        TEST: Get Activities - Participants are Persisted
        
        Arrange: Reset activities with known participants
        Act: Make GET request to /activities
        Assert: Initial participants from setup are returned
        """
        # Arrange: fixture handles reset_activities
        expected_participants = {
            "Chess Club": ["michael@mergington.edu", "daniel@mergington.edu"],
            "Programming Class": ["emma@mergington.edu", "sophia@mergington.edu"],
            "Gym Class": ["john@mergington.edu", "olivia@mergington.edu"]
        }
        
        # Act
        response = client.get("/activities")
        data = response.json()
        
        # Assert
        assert response.status_code == 200
        for activity_name, expected_list in expected_participants.items():
            assert data[activity_name]["participants"] == expected_list
