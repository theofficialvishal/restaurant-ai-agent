from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    session_id: Optional[str] = Field(
        default=None,
        description="Session identifier. If omitted or empty, a new session is initialized."
    )
    message: str = Field(
        ...,
        min_length=1,
        description="User's natural language message or order request."
    )
    force_cooking_fail: Optional[bool] = Field(
        default=False,
        description="Dev/test flag to simulate a kitchen cooking failure loop."
    )
    force_serving_fail: Optional[bool] = Field(
        default=False,
        description="Dev/test flag to simulate a table serving mishap recovery loop."
    )


class ChatResponse(BaseModel):
    session_id: str
    assistant_message: str
    workflow_status: str
    invalid_attempts: int
    current_order: List[Dict[str, Any]]
    bill: Optional[Dict[str, Any]] = None
    is_terminal: bool = False
    cooking_status: Optional[str] = None
    serving_status: Optional[str] = None
    serving_retries: int = 0
    messages: List[Dict[str, str]] = []


class ResetRequest(BaseModel):
    session_id: Optional[str] = Field(
        default=None,
        description="The session ID to reset. If not provided, initializes a fresh session."
    )


class ResetResponse(BaseModel):
    status: str = "reset_successful"
    session_id: str
    message: str = "Session reset successfully. Namaste!"
