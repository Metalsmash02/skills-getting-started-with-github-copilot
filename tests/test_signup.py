"""
Tests for the POST /activities/{activity_name}/signup endpoint using the AAA pattern.
"""

import pytest


class TestSignupForActivity:
    """Test suite for the POST /activities/{activity_name}/signup endpoint."""
    
    def test_signup_success(self, client, reset_activities):
        """
        TEST: Signup - Success Case
        
        Arrange: Reset activities, prepare new email
        Act: Post signup request with valid activity and email
        Assert: Response status is 200, participant added to activity
        """
        # Arrange
        activity_name = "Chess Club"
        email = "newstudent@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        data = response.json()
        
        # Assert
        assert response.status_code == 200
        assert "Signed up" in data["message"]
        assert email in data["message"]
        
        # Verify participant was actually added by making a GET request
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert email in activities[activity_name]["participants"]
    
    def test_signup_duplicate_returns_error(self, client, reset_activities):
        """
        TEST: Signup - Duplicate Signup Error
        
        Arrange: Reset activities, select participant already signed up
        Act: Post signup request for already-registered student
        Assert: Response status is 400 with appropriate error message
        """
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already registered
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        data = response.json()
        
        # Assert
        assert response.status_code == 400
        assert "already" in data["detail"].lower()
    
    def test_signup_nonexistent_activity_returns_404(self, client, reset_activities):
        """
        TEST: Signup - Nonexistent Activity Returns 404
        
        Arrange: Reset activities, use invalid activity name
        Act: Post signup request for non-existent activity
        Assert: Response status is 404 with appropriate error message
        """
        # Arrange
        activity_name = "Nonexistent Activity"
        email = "student@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        data = response.json()
        
        # Assert
        assert response.status_code == 404
        assert "not found" in data["detail"].lower()
    
    def test_signup_case_sensitive_activity_name(self, client, reset_activities):
        """
        TEST: Signup - Case Sensitive Activity Names
        
        Arrange: Reset activities, use lowercase activity name
        Act: Post signup request with wrong case
        Assert: Response status is 404 (activity names are case-sensitive)
        """
        # Arrange
        activity_name = "chess club"  # Wrong case
        email = "student@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404
    
    def test_signup_multiple_students_same_activity(self, client, reset_activities):
        """
        TEST: Signup - Multiple Different Students Can Join Same Activity
        
        Arrange: Reset activities, prepare two new emails
        Act: Post signup for two different students
        Assert: Both students are added to activity
        """
        # Arrange
        activity_name = "Chess Club"
        email1 = "student1@mergington.edu"
        email2 = "student2@mergington.edu"
        
        # Act
        response1 = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email1}
        )
        response2 = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email2}
        )
        
        # Assert
        assert response1.status_code == 200
        assert response2.status_code == 200
        
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert email1 in activities[activity_name]["participants"]
        assert email2 in activities[activity_name]["participants"]
    
    def test_signup_participant_count_increases(self, client, reset_activities):
        """
        TEST: Signup - Participant Count Increases
        
        Arrange: Reset activities, get initial count
        Act: Post signup request
        Assert: Participant count increased by 1
        """
        # Arrange
        activity_name = "Chess Club"
        email = "newstudent@mergington.edu"
        
        initial_response = client.get("/activities")
        initial_count = len(initial_response.json()[activity_name]["participants"])
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        
        final_response = client.get("/activities")
        final_count = len(final_response.json()[activity_name]["participants"])
        assert final_count == initial_count + 1
