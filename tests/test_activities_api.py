from copy import deepcopy
from urllib.parse import quote

from fastapi.testclient import TestClient

from src import app as app_module

client = TestClient(app_module.app)

ORIGINAL_ACTIVITIES = deepcopy(app_module.activities)


def reset_activities():
    app_module.activities = deepcopy(ORIGINAL_ACTIVITIES)


def test_get_activities_returns_expected_data():
    reset_activities()

    response = client.get("/activities")

    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]
    assert "max_participants" in data["Chess Club"]


def test_signup_adds_student_to_activity():
    reset_activities()
    email = "newstudent@mergington.edu"
    activity_name = "Chess Club"

    response = client.post(
        f"/activities/{quote(activity_name)}/signup",
        params={"email": email},
    )

    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"
    assert email in app_module.activities[activity_name]["participants"]


def test_signup_rejects_duplicate_participant():
    reset_activities()
    email = "duplicate@mergington.edu"
    activity_name = "Programming Class"

    first_response = client.post(
        f"/activities/{quote(activity_name)}/signup",
        params={"email": email},
    )
    second_response = client.post(
        f"/activities/{quote(activity_name)}/signup",
        params={"email": email},
    )

    assert first_response.status_code == 200
    assert second_response.status_code == 400
    assert second_response.json()["detail"] == "Student is already signed up for this activity"


def test_unregister_removes_student_from_activity():
    reset_activities()
    email = "remove_me@mergington.edu"
    activity_name = "Chess Club"

    client.post(f"/activities/{quote(activity_name)}/signup", params={"email": email})
    response = client.delete(
        f"/activities/{quote(activity_name)}/unregister",
        params={"email": email},
    )

    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from {activity_name}"
    assert email not in app_module.activities[activity_name]["participants"]


def test_invalid_activity_returns_404():
    reset_activities()

    response = client.post(
        "/activities/NotARealClub/signup",
        params={"email": "someone@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
