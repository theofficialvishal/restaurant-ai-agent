from typing import TypedDict, List, Dict, Optional, Any


class RestaurantState(TypedDict, total=False):
    session_id: str
    messages: List[Dict[str, str]]
    current_input: str
    intent: str  # "ORDER", "INQUIRY", "OFF_TOPIC", "GREETING"
    parsed_items: List[Dict[str, Any]]
    validated_items: List[Dict[str, Any]]
    is_valid: bool
    validation_error: Optional[str]
    invalid_attempts: int
    order_items: List[Dict[str, Any]]
    workflow_status: str  # "IDLE", "VALIDATING", "ORDER_PLACED", "COOKING", "SERVING", "COMPLETED", "TERMINATED"
    cooking_status: str  # "PENDING", "COOKING", "SUCCESS", "FAILED"
    serving_status: str  # "PENDING", "SERVING", "SUCCESS", "FAILED"
    failure_reason: Optional[str]
    bill: Optional[Dict[str, Any]]
    assistant_response: str
    is_terminal: bool
    force_cooking_fail: bool
    force_serving_fail: bool
    simulate_random_failures: bool
    serving_retries: int

