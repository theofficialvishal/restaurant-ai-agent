import pytest
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.menu import menu_repo
from backend.app.store import session_store


@pytest.fixture(autouse=True)
def setup_teardown():
    menu_repo.reset()
    session_store.clear_all()


client = TestClient(app)


def test_get_menu_endpoint():
    response = client.get("/api/menu")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert len(data["items"]) == 6
    # Check first item is Butter Chicken
    names = [i["name"] for i in data["items"]]
    assert "Butter Chicken" in names
    assert "Paneer Tikka" in names


def test_chat_endpoint_valid_order():
    # Place valid order
    payload = {
        "message": "I want 1 Butter Chicken",
        "force_cooking_fail": False,
        "force_serving_fail": False,
    }
    response = client.post("/api/chat", json=payload)
    assert response.status_code == 200
    data = response.json()

    assert data["session_id"] is not None
    assert data["workflow_status"] == "COMPLETED"
    assert data["cooking_status"] == "SUCCESS"
    assert data["serving_status"] == "SUCCESS"
    assert len(data["current_order"]) == 1
    assert data["current_order"][0]["dish_name"] == "Butter Chicken"
    assert data["bill"] is not None
    assert data["bill"]["grand_total"] == 367.50

    # Verify inventory was decremented in menu
    menu_res = client.get("/api/menu")
    bc = [i for i in menu_res.json()["items"] if i["id"] == "butter-chicken"][0]
    assert bc["available_qty"] == 4


def test_chat_endpoint_multi_turn():
    # Turn 1: Order Biryani
    res1 = client.post("/api/chat", json={"message": "I want 1 Hyderabadi Biryani"})
    assert res1.status_code == 200
    data1 = res1.json()
    sid = data1["session_id"]
    assert len(data1["current_order"]) == 1

    # Turn 2: Order Garlic Naan using same session_id
    res2 = client.post("/api/chat", json={"session_id": sid, "message": "Add 2 Garlic Naan"})
    assert res2.status_code == 200
    data2 = res2.json()
    assert data2["session_id"] == sid
    assert len(data2["current_order"]) == 2
    # Grand total should reflect both
    # 220 + 120 = 340 + 5% GST (17.0) = 357.0
    assert data2["bill"]["grand_total"] == 357.0


def test_chat_endpoint_cooking_failure_and_recovery():
    # Turn 1: Force cooking failure
    res1 = client.post("/api/chat", json={"message": "I want 2 Dal Makhani", "force_cooking_fail": True})
    assert res1.status_code == 200
    data1 = res1.json()
    assert data1["cooking_status"] == "FAILED"
    assert data1["workflow_status"] == "RESELECT_DISH"
    assert len(data1["current_order"]) == 0
    assert "kitchen issue" in data1["assistant_message"]

    # Dal Makhani inventory should remain 6
    dal = [i for i in client.get("/api/menu").json()["items"] if i["id"] == "dal-makhani"][0]
    assert dal["available_qty"] == 6

    # Turn 2: Re-select dish
    res2 = client.post("/api/chat", json={"session_id": data1["session_id"], "message": "Give me 1 Paneer Tikka"})
    assert res2.status_code == 200
    data2 = res2.json()
    assert data2["workflow_status"] == "COMPLETED"
    assert len(data2["current_order"]) == 1
    assert data2["current_order"][0]["dish_name"] == "Paneer Tikka"


def test_chat_endpoint_serving_failure_recovery_loop():
    # Force serving failure -> should recover in same turn and complete
    res = client.post("/api/chat", json={"message": "I want 2 Garlic Naan", "force_serving_fail": True})
    assert res.status_code == 200
    data = res.json()
    assert data["serving_retries"] == 1
    assert data["workflow_status"] == "COMPLETED"
    assert data["bill"] is not None
    assert data["bill"]["subtotal"] == 120.0


def test_reset_endpoint():
    # Start session with an order
    res1 = client.post("/api/chat", json={"message": "I want 1 Butter Chicken"})
    sid = res1.json()["session_id"]

    # Call reset
    res2 = client.post("/api/reset", json={"session_id": sid})
    assert res2.status_code == 200
    data2 = res2.json()
    assert data2["status"] == "reset_successful"
    assert data2["session_id"] != sid  # Fresh session ID returned
