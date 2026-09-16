import pytest
from backend.graph.state import RestaurantState
from backend.graph.nodes import (
    cook_order,
    handle_cooking_failure,
    serve_order,
    handle_serving_failure,
    generate_bill,
)
from backend.graph.edges import (
    route_after_take_order,
    route_after_cooking,
    route_after_serving,
)
from backend.graph.workflow import create_restaurant_graph
from backend.app.menu import menu_repo


@pytest.fixture(autouse=True)
def reset_menu():
    menu_repo.reset()


# --- Unit Tests for Milestone 04 Nodes ---

def test_cook_order_success():
    state: RestaurantState = {
        "session_id": "test-cook-success",
        "validated_item_name": "Butter Chicken",
        "force_cooking_fail": False,
        "order_items": [{"dish_name": "Butter Chicken", "dish_id": "butter-chicken", "quantity": 1, "unit_price": 350.0, "item_total": 350.0}],
    }
    result = cook_order(state)
    assert result["cooking_status"] == "SUCCESS"
    assert result["workflow_status"] == "COOKING"
    assert result["failure_reason"] is None
    assert "chef is preparing" in result["assistant_response"]


def test_cook_order_forced_failure():
    state: RestaurantState = {
        "session_id": "test-cook-fail",
        "validated_item_name": "Dal Makhani",
        "force_cooking_fail": True,
    }
    result = cook_order(state)
    assert result["cooking_status"] == "FAILED"
    assert result["workflow_status"] == "COOKING_FAILED"
    assert result["failure_reason"] is not None


def test_handle_cooking_failure_restores_inventory():
    # Reserve 2 Dal Makhani first
    menu_repo.reserve_stock("dal-makhani", 2)
    assert menu_repo.get_by_id("dal-makhani").available_qty == 4

    state: RestaurantState = {
        "session_id": "test-cook-recovery",
        "validated_item_id": "dal-makhani",
        "validated_item_name": "Dal Makhani",
        "parsed_quantity": 2,
        "cooking_status": "FAILED",
        "order_items": [
            {"dish_id": "dal-makhani", "dish_name": "Dal Makhani", "quantity": 2, "unit_price": 180.0, "item_total": 360.0}
        ],
    }

    result = handle_cooking_failure(state)

    # 1. Stock restored
    assert menu_repo.get_by_id("dal-makhani").available_qty == 6
    # 2. Failed dish removed from order_items
    assert len(result["order_items"]) == 0
    # 3. Status reset to allow re-selection
    assert result["workflow_status"] == "RESELECT_DISH"
    assert result["is_valid"] is False
    assert result["validated_item_id"] is None
    assert "kitchen issue" in result["assistant_response"]


def test_serve_order_success():
    state: RestaurantState = {
        "session_id": "test-serve-success",
        "validated_item_name": "Paneer Tikka",
        "force_serving_fail": False,
    }
    result = serve_order(state)
    assert result["serving_status"] == "SUCCESS"
    assert result["workflow_status"] == "SERVING"
    assert result["failure_reason"] is None
    assert "served fresh and hot" in result["assistant_response"]


def test_serve_order_forced_failure():
    state: RestaurantState = {
        "session_id": "test-serve-fail",
        "validated_item_name": "Paneer Tikka",
        "force_serving_fail": True,
    }
    result = serve_order(state)
    assert result["serving_status"] == "FAILED"
    assert result["workflow_status"] == "SERVING_FAILED"
    assert result["failure_reason"] is not None


def test_handle_serving_failure_increments_and_resets():
    state: RestaurantState = {
        "session_id": "test-serve-recovery",
        "validated_item_name": "Hyderabadi Biryani",
        "serving_status": "FAILED",
        "force_serving_fail": True,
        "serving_retries": 0,
    }
    result = handle_serving_failure(state)
    assert result["serving_retries"] == 1
    assert result["force_serving_fail"] is False  # Reset to ensure retry recovers
    assert result["workflow_status"] == "RE_COOKING"
    assert result["cooking_status"] == "COOKING"
    assert result["serving_status"] == "PENDING"
    assert "slight slip while serving" in result["assistant_response"]


def test_generate_bill_calculation():
    state: RestaurantState = {
        "session_id": "test-bill",
        "order_items": [
            {"dish_id": "butter-chicken", "dish_name": "Butter Chicken", "unit_price": 350.0, "quantity": 2, "item_total": 700.0},
            {"dish_id": "garlic-naan", "dish_name": "Garlic Naan", "unit_price": 60.0, "quantity": 2, "item_total": 120.0},
        ],
    }
    result = generate_bill(state)
    assert result["workflow_status"] == "COMPLETED"
    assert result["bill"] is not None

    bill = result["bill"]
    # Subtotal: 700 + 120 = 820.0
    assert bill["subtotal"] == 820.0
    # Tax: 5% of 820 = 41.0
    assert bill["tax"] == 41.0
    # Grand Total: 820 + 41 = 861.0
    assert bill["grand_total"] == 861.0

    assert "Subtotal: ₹820.00" in result["assistant_response"]
    assert "GST (5%): ₹41.00" in result["assistant_response"]
    assert "Grand Total: ₹861.00" in result["assistant_response"]


# --- Conditional Routing Edges Tests ---

def test_milestone4_conditional_edges():
    # route_after_take_order
    assert route_after_take_order({"workflow_status": "ORDER_PLACED"}) == "cook_order"
    assert route_after_take_order({"workflow_status": "RETRY"}) == "__end__"

    # route_after_cooking
    assert route_after_cooking({"cooking_status": "SUCCESS"}) == "serve_order"
    assert route_after_cooking({"cooking_status": "FAILED"}) == "handle_cooking_failure"

    # route_after_serving
    assert route_after_serving({"serving_status": "SUCCESS"}) == "generate_bill"
    assert route_after_serving({"serving_status": "FAILED"}) == "handle_serving_failure"


# --- Full Workflow End-to-End Tests ---

def test_full_workflow_happy_path():
    """Scenario 1: Valid single dish order flows through cook, serve, and bill generation."""
    graph = create_restaurant_graph()

    state: RestaurantState = {
        "session_id": "happy-path-sess",
        "current_input": "I want 1 Butter Chicken",
        "force_cooking_fail": False,
        "force_serving_fail": False,
        "order_items": [],
        "invalid_attempts": 0,
    }

    final_state = graph.invoke(state)

    assert final_state["is_valid"] is True
    assert final_state["workflow_status"] == "COMPLETED"
    assert final_state["cooking_status"] == "SUCCESS"
    assert final_state["serving_status"] == "SUCCESS"
    assert final_state["bill"] is not None

    bill = final_state["bill"]
    assert bill["subtotal"] == 350.0
    assert bill["tax"] == 17.50
    assert bill["grand_total"] == 367.50

    # Stock was decremented from 5 to 4
    assert menu_repo.get_by_id("butter-chicken").available_qty == 4


def test_full_workflow_cooking_failure_recovery():
    """Scenario 4: Cooking fails, restores stock, asks user to re-select, then next turn completes."""
    graph = create_restaurant_graph()

    # Turn 1: Cooking Failure
    turn1_state: RestaurantState = {
        "session_id": "cook-fail-sess",
        "current_input": "Please bring 2 Dal Makhani",
        "force_cooking_fail": True,
        "order_items": [],
        "invalid_attempts": 0,
    }

    turn1_res = graph.invoke(turn1_state)

    # Asserts on cooking failure handling
    assert turn1_res["cooking_status"] == "FAILED"
    assert turn1_res["workflow_status"] == "RESELECT_DISH"
    assert len(turn1_res["order_items"]) == 0
    assert "kitchen issue" in turn1_res["assistant_response"]
    # Dal Makhani inventory should be fully restored back to 6
    assert menu_repo.get_by_id("dal-makhani").available_qty == 6

    # Turn 2: User selects alternative dish (Paneer Tikka)
    turn2_state = dict(turn1_res)
    turn2_state["current_input"] = "Give me 1 Paneer Tikka instead"
    turn2_state["force_cooking_fail"] = False
    turn2_state["force_serving_fail"] = False

    turn2_res = graph.invoke(turn2_state)

    assert turn2_res["is_valid"] is True
    assert turn2_res["cooking_status"] == "SUCCESS"
    assert turn2_res["serving_status"] == "SUCCESS"
    assert turn2_res["workflow_status"] == "COMPLETED"
    assert turn2_res["bill"]["subtotal"] == 250.0
    assert turn2_res["bill"]["tax"] == 12.50
    assert turn2_res["bill"]["grand_total"] == 262.50
    # Paneer Tikka stock decremented from 8 to 7
    assert menu_repo.get_by_id("paneer-tikka").available_qty == 7


def test_full_workflow_serving_failure_cyclic_recovery():
    """Scenario 5: Serving fails, graph loops back to cook_order, re-cooks and serves successfully."""
    graph = create_restaurant_graph()

    state: RestaurantState = {
        "session_id": "serve-fail-sess",
        "current_input": "I want 2 plates of Garlic Naan",
        "force_cooking_fail": False,
        "force_serving_fail": True,  # Will trigger handle_serving_failure and loop to cook_order
        "order_items": [],
        "invalid_attempts": 0,
    }

    final_state = graph.invoke(state)

    # Verify recovery loop occurred and concluded at generate_bill
    assert final_state["serving_retries"] == 1
    assert final_state["cooking_status"] == "SUCCESS"
    assert final_state["serving_status"] == "SUCCESS"
    assert final_state["workflow_status"] == "COMPLETED"
    assert final_state["bill"] is not None

    bill = final_state["bill"]
    # 2 x Garlic Naan @ 60 = 120.0
    assert bill["subtotal"] == 120.0
    assert bill["tax"] == 6.0
    assert bill["grand_total"] == 126.0

    # Stock should only be decremented once (20 -> 18)
    assert menu_repo.get_by_id("garlic-naan").available_qty == 18
    assert "slip while serving" in final_state["assistant_response"] or "prepared fresh" in final_state["assistant_response"]
