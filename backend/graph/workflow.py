from langgraph.graph import StateGraph, START, END
from backend.graph.state import RestaurantState
from backend.graph.nodes import (
    validate_input,
    respond_retry,
    terminate_session,
    take_order,
    cook_order,
    handle_cooking_failure,
    serve_order,
    handle_serving_failure,
    generate_bill,
)
from backend.graph.edges import (
    route_after_validation,
    route_after_take_order,
    route_after_cooking,
    route_after_serving,
)


def create_restaurant_graph():
    """
    Construct and compile the full LangGraph workflow for Desi Dhaba AI Restaurant.
    
    Workflow Topology:
    START
      ↓
    validate_input
      ├── Invalid (<3) ──> respond_retry ──> END
      ├── Invalid (>=3) ─> terminate_session ──> END
      ├── Greeting / Inquiry ──> END
      └── Valid Order
            ↓
        take_order
            ├── Stock/Validation Issue ──> END
            └── Order Placed
                  ↓
              cook_order <────────────────────────┐
                  ├── Failed                      │ (re-cook)
                  │     ↓                         │
                  │   handle_cooking_failure ──> END (re-select)
                  │
                  └── Success
                        ↓
                    serve_order
                        ├── Failed
                        │     ↓
                        │   handle_serving_failure ────┘
                        │
                        └── Success
                              ↓
                          generate_bill ──> END
    """
    builder = StateGraph(RestaurantState)

    # 1. Add All Workflow Nodes
    builder.add_node("validate_input", validate_input)
    builder.add_node("respond_retry", respond_retry)
    builder.add_node("terminate_session", terminate_session)
    builder.add_node("take_order", take_order)
    builder.add_node("cook_order", cook_order)
    builder.add_node("handle_cooking_failure", handle_cooking_failure)
    builder.add_node("serve_order", serve_order)
    builder.add_node("handle_serving_failure", handle_serving_failure)
    builder.add_node("generate_bill", generate_bill)

    # 2. Add Entry Edge
    builder.add_edge(START, "validate_input")

    # 3. Add Conditional Routing from validate_input
    builder.add_conditional_edges(
        "validate_input",
        route_after_validation,
        {
            "take_order": "take_order",
            "cook_order": "cook_order",
            "generate_bill": "generate_bill",
            "respond_retry": "respond_retry",
            "terminate_session": "terminate_session",
            END: END,
        },
    )

    # 4. Routing from take_order into Kitchen Cooking
    builder.add_conditional_edges(
        "take_order",
        route_after_take_order,
        {
            "cook_order": "cook_order",
            END: END,
        },
    )

    # 5. Routing from cook_order: Success -> serve_order, Failed -> handle_cooking_failure
    builder.add_conditional_edges(
        "cook_order",
        route_after_cooking,
        {
            "serve_order": "serve_order",
            "handle_cooking_failure": "handle_cooking_failure",
        },
    )

    # 6. Cooking Failure ends turn for user to re-select dish
    builder.add_edge("handle_cooking_failure", END)

    # 7. Routing from serve_order: Success -> generate_bill, Failed -> handle_serving_failure
    builder.add_conditional_edges(
        "serve_order",
        route_after_serving,
        {
            "generate_bill": "generate_bill",
            "handle_serving_failure": "handle_serving_failure",
            END: END,
        },
    )

    # 8. Serving Failure loops back to cook_order (re-cooking cycle)
    builder.add_edge("handle_serving_failure", "cook_order")

    # 9. Terminal / Turn Completion Edges
    builder.add_edge("generate_bill", END)
    builder.add_edge("respond_retry", END)
    builder.add_edge("terminate_session", END)

    return builder.compile()


# Default compiled graph instance for reuse
restaurant_graph = create_restaurant_graph()

