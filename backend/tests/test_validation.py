import pytest
from backend.graph.state import RestaurantState
from backend.graph.nodes import validate_input
from backend.app.menu import menu_repo


@pytest.fixture(autouse=True)
def reset_menu():
    menu_repo.reset()


def test_valid_single_dish():
    state: RestaurantState = {
        "session_id": "test-1",
        "current_input": "I want 2 Butter Chicken please",
        "invalid_attempts": 0,
    }
    result = validate_input(state)
    assert result["is_valid"] is True
    assert result["intent"] == "ORDER"
    assert result["validated_item_id"] == "butter-chicken"
    assert result["parsed_quantity"] == 2
    assert result["unit_price"] == 350.0
    assert result["validation_error"] is None
    assert "validated" in result["assistant_response"]


def test_exceeded_quantity():
    # Butter Chicken only has 5 available
    state: RestaurantState = {
        "session_id": "test-2",
        "current_input": "Give me 8 Butter Chicken",
        "invalid_attempts": 0,
    }
    result = validate_input(state)
    assert result["is_valid"] is False
    assert "only have 5" in result["assistant_response"]
    assert result["validation_error"] is not None


def test_unknown_dish():
    state: RestaurantState = {
        "session_id": "test-3",
        "current_input": "Can I order 2 plates of Margherita Pizza",
        "invalid_attempts": 0,
    }
    result = validate_input(state)
    assert result["is_valid"] is False
    assert "not on our Desi Dhaba menu" in result["assistant_response"]
    assert result["validation_error"] is not None


def test_off_topic_message():
    state: RestaurantState = {
        "session_id": "test-4",
        "current_input": "What is the weather in Delhi today?",
        "invalid_attempts": 0,
    }
    result = validate_input(state)
    assert result["is_valid"] is False
    assert result["intent"] == "OFF_TOPIC"
    assert "restaurant dining" in result["assistant_response"]


def test_greeting_message():
    state: RestaurantState = {
        "session_id": "test-5",
        "current_input": "Namaste!",
        "invalid_attempts": 0,
    }
    result = validate_input(state)
    assert result["is_valid"] is True
    assert result["intent"] == "GREETING"
    assert "Namaste" in result["assistant_response"]


def test_menu_inquiry():
    state: RestaurantState = {
        "session_id": "test-6",
        "current_input": "What do you have on the menu?",
        "invalid_attempts": 0,
    }
    result = validate_input(state)
    assert result["is_valid"] is True
    assert result["intent"] == "INQUIRY"
    assert "Butter Chicken" in result["assistant_response"]


def test_langgraph_compilation_and_execution():
    from langgraph.graph import StateGraph, START, END

    builder = StateGraph(RestaurantState)
    builder.add_node("validate_input", validate_input)
    builder.add_edge(START, "validate_input")
    builder.add_edge("validate_input", END)
    compiled_graph = builder.compile()

    initial_state: RestaurantState = {
        "session_id": "test-graph-1",
        "current_input": "I want 1 plate of Paneer Tikka",
        "invalid_attempts": 0,
    }
    final_state = compiled_graph.invoke(initial_state)

    assert final_state["is_valid"] is True
    assert final_state["validated_item_id"] == "paneer-tikka"
    assert final_state["unit_price"] == 250.0
    assert final_state["parsed_quantity"] == 1

