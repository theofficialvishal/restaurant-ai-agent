import pytest
from backend.graph.state import RestaurantState
from backend.graph.nodes import respond_retry, terminate_session, take_order
from backend.graph.edges import route_after_validation
from backend.graph.workflow import create_restaurant_graph
from backend.app.menu import menu_repo
from langgraph.graph import END


@pytest.fixture(autouse=True)
def reset_menu():
    menu_repo.reset()


def test_respond_retry_node():
    state: RestaurantState = {
        "session_id": "test-retry-1",
        "current_input": "Who is Elon Musk?",
        "intent": "OFF_TOPIC",
        "validation_error": "off_topic",
        "invalid_attempts": 0,
    }
    result = respond_retry(state)
    assert result["invalid_attempts"] == 1
    assert result["workflow_status"] == "RETRY"
    assert result["is_terminal"] is False
    assert "2 attempt(s) remaining" in result["assistant_response"]


def test_terminate_session_node():
    state: RestaurantState = {
        "session_id": "test-term-1",
        "current_input": "Write some Python code",
        "intent": "OFF_TOPIC",
        "invalid_attempts": 2,
    }
    result = terminate_session(state)
    assert result["invalid_attempts"] == 3
    assert result["is_terminal"] is True
    assert result["workflow_status"] == "TERMINATED"
    assert "conclude this session" in result["assistant_response"]


def test_take_order_node():
    # Butter Chicken has 5 available
    state: RestaurantState = {
        "session_id": "test-order-1",
        "current_input": "I want 2 Butter Chicken",
        "intent": "ORDER",
        "validated_item_id": "butter-chicken",
        "validated_item_name": "Butter Chicken",
        "parsed_quantity": 2,
        "unit_price": 350.0,
        "invalid_attempts": 1,
        "order_items": [],
    }
    result = take_order(state)
    assert result["workflow_status"] == "ORDER_PLACED"
    assert result["invalid_attempts"] == 0
    assert len(result["order_items"]) == 1
    item = result["order_items"][0]
    assert item["dish_id"] == "butter-chicken"
    assert item["quantity"] == 2
    assert item["unit_price"] == 350.0
    assert item["item_total"] == 700.0

    # Verify inventory was decremented in menu_repo
    menu_item = menu_repo.get_by_id("butter-chicken")
    assert menu_item.available_qty == 3


def test_conditional_edge_routing():
    # Valid order -> take_order
    valid_order_state: RestaurantState = {
        "is_valid": True,
        "intent": "ORDER",
        "invalid_attempts": 0,
    }
    assert route_after_validation(valid_order_state) == "take_order"

    # Valid greeting / inquiry -> END
    greeting_state: RestaurantState = {
        "is_valid": True,
        "intent": "GREETING",
        "invalid_attempts": 0,
    }
    assert route_after_validation(greeting_state) == END

    # 1st invalid attempt (current_attempts = 0) -> respond_retry
    invalid_1_state: RestaurantState = {
        "is_valid": False,
        "intent": "OFF_TOPIC",
        "invalid_attempts": 0,
    }
    assert route_after_validation(invalid_1_state) == "respond_retry"

    # 2nd invalid attempt (current_attempts = 1) -> respond_retry
    invalid_2_state: RestaurantState = {
        "is_valid": False,
        "intent": "OFF_TOPIC",
        "invalid_attempts": 1,
    }
    assert route_after_validation(invalid_2_state) == "respond_retry"

    # 3rd invalid attempt (current_attempts = 2) -> terminate_session
    invalid_3_state: RestaurantState = {
        "is_valid": False,
        "intent": "OFF_TOPIC",
        "invalid_attempts": 2,
    }
    assert route_after_validation(invalid_3_state) == "terminate_session"

    # Session already terminated -> END
    terminated_state: RestaurantState = {
        "is_terminal": True,
        "invalid_attempts": 3,
    }
    assert route_after_validation(terminated_state) == END


def test_graph_valid_order_reaches_take_order():
    graph = create_restaurant_graph()

    state: RestaurantState = {
        "session_id": "sess-happy-1",
        "current_input": "Please give me 2 plates of Paneer Tikka",
        "invalid_attempts": 0,
        "order_items": [],
        "messages": [],
    }

    final_state = graph.invoke(state)

    assert final_state["is_valid"] is True
    assert final_state["workflow_status"] in ["ORDER_PLACED", "COMPLETED"]
    assert len(final_state["order_items"]) == 1
    assert final_state["order_items"][0]["dish_name"] == "Paneer Tikka"
    assert final_state["order_items"][0]["quantity"] == 2
    assert final_state["order_items"][0]["item_total"] == 500.0

    # Verify inventory was decremented from 8 to 6
    paneer = menu_repo.get_by_id("paneer-tikka")
    assert paneer.available_qty == 6


def test_graph_three_strike_termination_and_fourth_attempt():
    graph = create_restaurant_graph()

    # Turn 1: Invalid input #1
    state_1: RestaurantState = {
        "session_id": "sess-fail-1",
        "current_input": "What is the capital of France?",
        "invalid_attempts": 0,
        "order_items": [],
        "messages": [],
    }
    res_1 = graph.invoke(state_1)
    assert res_1["is_valid"] is False
    assert res_1["invalid_attempts"] == 1
    assert res_1["workflow_status"] == "RETRY"
    assert res_1["is_terminal"] is False
    assert "2 attempt(s) remaining" in res_1["assistant_response"]

    # Turn 2: Invalid input #2 (unknown dish)
    state_2 = dict(res_1)
    state_2["current_input"] = "I want 2 plates of Sushi"
    res_2 = graph.invoke(state_2)
    assert res_2["is_valid"] is False
    assert res_2["invalid_attempts"] == 2
    assert res_2["workflow_status"] == "RETRY"
    assert res_2["is_terminal"] is False
    assert "1 attempt(s) remaining" in res_2["assistant_response"]

    # Turn 3: Invalid input #3 (3rd strike -> Terminate!)
    state_3 = dict(res_2)
    state_3["current_input"] = "Tell me a funny joke"
    res_3 = graph.invoke(state_3)
    assert res_3["is_valid"] is False
    assert res_3["invalid_attempts"] == 3
    assert res_3["workflow_status"] == "TERMINATED"
    assert res_3["is_terminal"] is True
    assert "conclude this session" in res_3["assistant_response"]

    # Turn 4: User attempts to order on a terminated session
    state_4 = dict(res_3)
    state_4["current_input"] = "I want 2 Butter Chicken"
    res_4 = graph.invoke(state_4)
    assert res_4["is_terminal"] is True
    assert res_4["workflow_status"] == "TERMINATED"
    assert len(res_4.get("order_items", [])) == 0
    # Stock should remain untouched
    bc = menu_repo.get_by_id("butter-chicken")
    assert bc.available_qty == 5


def test_graph_multi_item_order_across_turns():
    graph = create_restaurant_graph()

    # Turn 1: 1 Biryani
    turn1: RestaurantState = {
        "session_id": "multi-order",
        "current_input": "I want 1 Hyderabadi Biryani",
        "invalid_attempts": 0,
        "order_items": [],
    }
    res1 = graph.invoke(turn1)
    assert res1["workflow_status"] in ["ORDER_PLACED", "COMPLETED"]
    assert len(res1["order_items"]) == 1

    # Turn 2: 2 Garlic Naan
    turn2 = dict(res1)
    turn2["current_input"] = "Add 2 Garlic Naan as well"
    res2 = graph.invoke(turn2)
    assert res2["workflow_status"] in ["ORDER_PLACED", "COMPLETED"]
    assert len(res2["order_items"]) == 2
    assert res2["order_items"][0]["dish_name"] == "Hyderabadi Biryani"
    assert res2["order_items"][1]["dish_name"] == "Garlic Naan"
    assert res2["order_items"][1]["quantity"] == 2

    # Verify inventory decrements
    biryani = menu_repo.get_by_id("hyderabadi-biryani")
    naan = menu_repo.get_by_id("garlic-naan")
    assert biryani.available_qty == 9  # 10 - 1
    assert naan.available_qty == 18    # 20 - 2
