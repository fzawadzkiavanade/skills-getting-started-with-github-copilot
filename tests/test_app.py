from urllib.parse import quote

from fastapi.testclient import TestClient

from src.app import app, activities

client = TestClient(app)


def test_get_activities():
    res = client.get("/activities")
    assert res.status_code == 200
    data = res.json()
    assert "Chess Club" in data


def test_signup_and_unregister_flow():
    activity = "Chess Club"
    encoded = quote(activity, safe="")
    email = "test.user@example.com"

    # Ensure clean state
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    # Sign up
    res = client.post(f"/activities/{encoded}/signup?email={email}")
    assert res.status_code == 200
    assert email in activities[activity]["participants"]

    # Duplicate signup should fail
    res_dup = client.post(f"/activities/{encoded}/signup?email={email}")
    assert res_dup.status_code == 400

    # Unregister
    res_unreg = client.delete(f"/activities/{encoded}/participants?email={email}")
    assert res_unreg.status_code == 200
    assert email not in activities[activity]["participants"]
