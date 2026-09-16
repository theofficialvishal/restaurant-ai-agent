import uuid
from typing import Dict, Optional
from backend.graph.state import RestaurantState


class SessionStore:
    """In-memory session state repository keyed by session_id."""

    def __init__(self):
        self._sessions: Dict[str, RestaurantState] = {}

    def get_or_create(self, session_id: Optional[str] = None) -> tuple[str, RestaurantState]:
        """Retrieve existing session state or initialize a fresh one."""
        sid = session_id or str(uuid.uuid4())
        if sid not in self._sessions:
            self._sessions[sid] = {
                "session_id": sid,
                "messages": [],
                "current_input": "",
                "intent": "GREETING",
                "parsed_dish": None,
                "parsed_quantity": 1,
                "validated_item_id": None,
                "validated_item_name": None,
                "unit_price": 0.0,
                "is_valid": False,
                "validation_error": None,
                "invalid_attempts": 0,
                "order_items": [],
                "workflow_status": "IDLE",
                "cooking_status": "PENDING",
                "serving_status": "PENDING",
                "failure_reason": None,
                "bill": None,
                "assistant_response": "Namaste! Welcome to Desi Dhaba. What delicious Indian dish would you like to enjoy today?",
                "is_terminal": False,
                "force_cooking_fail": False,
                "force_serving_fail": False,
                "simulate_random_failures": False,
                "serving_retries": 0,
            }
        return sid, self._sessions[sid]

    def get(self, session_id: str) -> Optional[RestaurantState]:
        """Get state for an existing session."""
        return self._sessions.get(session_id)

    def save(self, session_id: str, state: RestaurantState) -> None:
        """Persist updated state into memory."""
        self._sessions[session_id] = state

    def reset(self, session_id: str) -> str:
        """Clear a specific session and return a fresh session ID."""
        if session_id in self._sessions:
            del self._sessions[session_id]
        new_sid = str(uuid.uuid4())
        _, state = self.get_or_create(new_sid)
        return new_sid

    def clear_all(self) -> None:
        """Clear all active sessions (useful for tests)."""
        self._sessions.clear()


# Global singleton instance
session_store = SessionStore()
