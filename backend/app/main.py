import os
from typing import Optional
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from backend.app.config import CORS_ORIGINS, LLM_MODEL
from backend.app.schemas import ChatRequest, ChatResponse, ResetRequest, ResetResponse
from backend.app.store import session_store
from backend.graph.workflow import restaurant_graph

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FRONTEND_DIST = os.path.join(BASE_DIR, "frontend", "dist")

app = FastAPI(
    title="Desi Dhaba AI Restaurant API",
    description="Conversational AI restaurant ordering API powered by LangGraph",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api")
async def root():
    return {
        "name": "Desi Dhaba AI Restaurant API",
        "status": "online",
        "documentation": "/docs",
        "health": "/api/health",
    }


@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "desi-dhaba-api",
        "version": "1.0.0",
        "llm_model": LLM_MODEL,
    }


@app.get("/api/menu")
async def get_menu():
    from backend.app.menu import menu_repo
    return {"items": [item.model_dump() for item in menu_repo.get_all()]}


@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Submit customer utterance to the LangGraph restaurant workflow,
    persist conversation state in session store, and return agent response.
    """
    # 1. Retrieve or create session state
    session_id, current_state = session_store.get_or_create(request.session_id)

    # 2. Update state with current user utterance and test flags
    state_to_run = dict(current_state)
    state_to_run["current_input"] = request.message
    state_to_run["force_cooking_fail"] = bool(request.force_cooking_fail)
    state_to_run["force_serving_fail"] = bool(request.force_serving_fail)

    # 3. Invoke LangGraph workflow
    updated_state = restaurant_graph.invoke(state_to_run)

    # 4. Save updated state back to session store
    session_store.save(session_id, updated_state)

    # 5. Formulate and return ChatResponse
    return ChatResponse(
        session_id=session_id,
        assistant_message=updated_state.get("assistant_response", ""),
        workflow_status=updated_state.get("workflow_status", "IDLE"),
        invalid_attempts=updated_state.get("invalid_attempts", 0),
        current_order=updated_state.get("order_items", []),
        bill=updated_state.get("bill"),
        is_terminal=updated_state.get("is_terminal", False),
        cooking_status=updated_state.get("cooking_status"),
        serving_status=updated_state.get("serving_status"),
        serving_retries=updated_state.get("serving_retries", 0),
        messages=updated_state.get("messages", []),
    )


@app.post("/api/reset", response_model=ResetResponse)
async def reset_endpoint(request: Optional[ResetRequest] = None):
    """
    Clear session state and return a fresh session ID.
    """
    import uuid
    sid = request.session_id if request and request.session_id else None
    if sid:
        new_sid = session_store.reset(sid)
    else:
        new_sid = str(uuid.uuid4())
        session_store.get_or_create(new_sid)

    return ResetResponse(
        status="reset_successful",
        session_id=new_sid,
        message="Session reset successfully. Namaste!",
    )




# Mount static assets (React Vite build outputs CSS/JS to dist/assets)
if os.path.exists(os.path.join(FRONTEND_DIST, "assets")):
    app.mount("/assets", StaticFiles(directory=os.path.join(FRONTEND_DIST, "assets")), name="assets")

# Catch-all route to serve the React application and other static files
@app.get("/{full_path:path}")
async def serve_react_app(full_path: str):
    # Don't intercept API routes
    if full_path.startswith("api/"):
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="API route not found")
        
    # Check if the requested path is a real file in the dist directory (e.g. favicon.ico, images)
    file_path = os.path.join(FRONTEND_DIST, full_path)
    if os.path.isfile(file_path):
        return FileResponse(file_path)
        
    # Otherwise, return index.html for client-side routing
    index_path = os.path.join(FRONTEND_DIST, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    
    # If frontend is not built, return a simple message
    return {"message": "Frontend not built yet. Please run 'npm run build' in the frontend directory."}


if __name__ == "__main__":
    import uvicorn
    from backend.app.config import PORT

    uvicorn.run("backend.app.main:app", host="0.0.0.0", port=PORT, reload=True)
