"""
Tests for the DELETE /activities/{activity_name}/signup endpoint using the AAA pattern.
"""

import pytest


class TestUnregisterFromActivity:
    """Test suite for the DELETE /activities/{activity_name}/signup endpoint."""
    
    def test_unregister_success(self, client, reset_activities):
        """
        TEST: Unregister - Success Case
        
        Arrange: Reset activities, select registered participant
        Act: Delete signup request for registered student
        Assert: Response status is 200, participant removed from activity
        """
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already registered
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        data = response.json()
        
        # Assert
        assert response.status_code == 200
        assert "Unregistered" in data["message"]
        
        # Verify participant was actually removed
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert email not in activities[activity_name]["participants"]
    
    def test_unregister_nonexistent_participant_returns_error(self, client, reset_activities):
        """
        TEST: Unregister - Non-existent Participant Returns Error
        
        Arrange: Reset activities, use email not registered
        Act: Delete signup request for non-registered student
        Assert: Response status is 400 with appropriate error message
        """
        # Arrange
        activity_name = "Chess Club"
        email = "notregistered@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        data = response.json()
        
        # Assert
        assert response.status_code == 400
        assert "not registered" in data["detail"].lower()
    
    def test_unregister_nonexistent_activity_returns_404(self, client, reset_activities):
        """
        TEST: Unregister - Nonexistent Activity Returns 404
        
        Arrange: Reset activities, use invalid activity name
        Act: Delete signup request for non-existent activity
        Assert: Response status is 404 with appropriate error message
        """
        # Arrange
        activity_name = "Nonexistent Activity"
        email = "student@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        data = response.json()
        
        # Assert
        assert response.status_code == 404
        assert "not found" in data["detail"].lower()
    
    def test_unregister_participant_count_decreases(self, client, reset_activities):
        """
        TEST: Unregister - Participant Count Decreases
        
        Arrange: Reset activities, get initial count
        Act: Delete signup request for registered participant
        Assert: Participant count decreased by 1
        """
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"
        
        initial_response = client.get("/activities")
        initial_count = len(initial_response.json()[activity_name]["participants"])
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        
        final_response = client.get("/activities")
        final_count = len(final_response.json()[activity_name]["participants"])
        assert final_count == initial_count - 1
    
    def test_unregister_removes_only_that_participant(self, client, reset_activities):
        """
        TEST: Unregister - Removes Only That Participant
        
        Arrange: Reset activities with multiple participants
        Act: Delete signup for one participant
        Assert: Other participants remain in activity
        """
        # Arrange
        activity_name = "Chess Club"
        email_to_remove = "michael@mergington.edu"
        email_to_keep = "daniel@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email_to_remove}
        )
        
        # Assert
        assert response.status_code == 200
        
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert email_to_remove not in activities[activity_name]["participants"]
        assert email_to_keep in activities[activity_name]["participants"]
    
    def test_unregister_then_signup_same_participant(self, client, reset_activities):
        """
        TEST: Unregister - Can Re-signup After Unregister
        
        Arrange: Reset activities, select registered participant
        Act: Delete signup, then post signup
        Assert: Participant can be added back
        """
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"
        
        # Act - Unregister
        delete_response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert unregister succeeded
        assert delete_response.status_code == 200
        
        # Act - Sign up again
        signup_response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert signup succeeded
        assert signup_response.status_code == 200
        
        # Verify participant is registered again
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert email in activities[activity_name]["participants"]
