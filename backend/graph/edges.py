from typing import Literal
from langgraph.graph import END
from backend.graph.state import RestaurantState


def route_after_validation(
    state: RestaurantState,
) -> Literal["take_order", "respond_retry", "terminate_session", "__end__"]:
    """
    Conditional routing edge following input validation.
    
    Routes to:
    - '__end__' if session is already terminal or for non-ordering conversational intents (GREETING, INQUIRY).
    - 'take_order' if user intent is ORDER and the dish & quantity are valid.
    - 'terminate_session' if validation failed and invalid_attempts + 1 >= 3 (3rd strike boundary).
    - 'respond_retry' if validation failed and invalid_attempts + 1 < 3.
    """
    if state.get("is_terminal"):
        return END

    is_valid = state.get("is_valid", False)
    intent = state.get("intent")

    if is_valid:
        if intent == "ORDER":
            return "take_order"
        elif intent == "FINALIZE":
            return "cook_order"
        elif intent == "REQUEST_BILL":
            return "generate_bill"
        # Greetings, inquiries, or menu questions conclude turn without taking an order
        return END

    # Validation failed or off-topic: check retry threshold
    current_attempts = state.get("invalid_attempts", 0)
    if current_attempts + 1 >= 3:
        return "terminate_session"
    else:
        return "respond_retry"


def route_after_take_order(
    state: RestaurantState,
) -> Literal["cook_order", "__end__"]:
    """
    Conditional routing edge following take_order.
    If order was placed successfully, proceed to cook_order in the kitchen.
    Otherwise (e.g., unexpected stock issue), end turn for customer retry.
    """
    if state.get("workflow_status") == "AWAITING_CONFIRMATION":
        return END
    return END


def route_after_cooking(
    state: RestaurantState,
) -> Literal["handle_cooking_failure", "serve_order"]:
    """
    Conditional routing edge following cook_order.
    Routes to handle_cooking_failure if cooking failed.
    Otherwise routes to serve_order for table delivery.
    """
    if state.get("cooking_status") == "FAILED":
        return "handle_cooking_failure"
    return "serve_order"


def route_after_serving(
    state: RestaurantState,
) -> Literal["handle_serving_failure", "generate_bill"]:
    """
    Conditional routing edge following serve_order.
    Routes to handle_serving_failure if serving platter slipped.
    Otherwise routes to generate_bill to conclude with itemized receipt.
    """
    if state.get("serving_status") == "FAILED":
        return "handle_serving_failure"
    return END

