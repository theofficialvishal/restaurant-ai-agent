# Desi Dhaba AI Restaurant — Project Roadmap

## Project Goal

A conversational AI restaurant ordering application built to learn the basics of LangGraph, state management, and conditional agent workflows.

## Approved Architecture

```text
React Frontend (Chat & Menu UI)
       ↓ (HTTP JSON)
FastAPI Backend
       ↓
LangGraph Workflow (State Machine)
 ┌──────────────────────────────────────────────┐
 │ State: Messages, Order, Cart, WorkflowStatus │
 │ Nodes: Validate, Cook, Serve, Bill           │
 │ Edges: Conditional Retries, Success, Fail    │
 └──────────────────────────────────────────────┘
```

## Learning Goals

- Master LangGraph basics (State, Nodes, Edges, Conditional Routing).
- Understand how to embed an LLM agent inside a deterministic, rule-based workflow.
- Build cyclic graph loops (e.g., retries on failure or invalid input).

## Build Strategy

**1 Session = 1 Feature or Clearly Bounded Milestone**
The project will be built by starting with the infrastructure, moving to the core backend LangGraph logic, creating the frontend shell, and finally integrating them into a complete full-stack application.

---

## Session Roadmap

### 01 — Project Foundation & Basic API
**Goal:** Initialize the React frontend and FastAPI backend, establishing the development environment.
**Why now:** We need a working environment and an API boundary before we can build the graph or UI.
**Prerequisites:** None.
**Frontend:** React scaffolding (Vite/Create React App), Tailwind CSS setup.
**Backend:** FastAPI setup, basic `/health` endpoint.
**Database:** None.
**Infrastructure:** None.
**Packages:** `fastapi`, `uvicorn` / `react`, `tailwindcss`.
**Testing:** Ensure both dev servers start and the API responds.
**Learning:** Monorepo/Full-stack project structure.
**Expected outcome:** A running React app and a running FastAPI server.

---

### 02 — LangGraph Core: State & Validation
**Goal:** Define the graph state and the first LLM node to understand user input and validate it against a hardcoded menu.
**Why now:** The state schema is the foundation of LangGraph. Validation is the first step of the workflow.
**Prerequisites:** Session 01.
**Frontend:** None.
**Backend:** Initialize LangGraph `StateGraph`, define the State `TypedDict`, create the menu data, and add the `validate_input` node using Gemini.
**Database:** In-memory mock menu data.
**Packages:** `langgraph`, `langchain-google-genai`, `pydantic`.
**Testing:** Unit test the graph with a valid and invalid dish name via a simple Python script/test.
**Learning:** LangGraph State schema, Node definition, Tool binding/Prompting for specific outputs.
**Expected outcome:** The graph can take a text input, identify the dish/quantity, and check if it exists in the menu.

---

### 03 — Workflow Edges: Retries & Take Order
**Goal:** Implement conditional edges for handling invalid inputs (max 3 retries) and the `take_order` success path.
**Why now:** We must handle the output of the validation node before moving to cooking.
**Prerequisites:** Session 02.
**Backend:** Add conditional routing. If invalid, increment a retry counter in state. If retries > 3, route to END. If valid, route to `take_order` node.
**Testing:** Test the graph loop with 4 invalid inputs to ensure it terminates. Test 1 valid input to ensure it reaches `take_order`.
**Learning:** Conditional edges, cyclic loops, state mutation (counters).
**Expected outcome:** A resilient input loop that protects the system from infinite LLM hallucinations.

---

### 04 — Simulated Failures: Cooking & Serving
**Goal:** Complete the restaurant workflow by adding `cook_order`, `serve_order`, and `generate_bill` nodes.
**Why now:** The order is validated and taken; now it must be processed realistically.
**Prerequisites:** Session 03.
**Backend:** Implement nodes that simulate success/failure (e.g., using `random.choice`). Route cooking failures back to `take_order` (re-select dish). Route serving failures back to `cook_order`. 
**Testing:** Force failures in tests to ensure the graph properly loops backward and recovers.
**Learning:** Complex cyclic routing, simulating real-world service unreliability within an agent.
**Expected outcome:** The entire LangGraph backend workflow is complete and testable via terminal/API.

---

### 05 — Frontend Foundation: Chat & Menu UI
**Goal:** Build the Desi Dhaba visual interface using React and Tailwind.
**Why now:** The backend workflow is solid; now we need the UI to visualize it.
**Prerequisites:** Session 01.
**Frontend:** Implement the Chat UI (user/assistant bubbles), the static Menu sidebar, and an Order Status component.
**Design:** Dark charcoal background, warm saffron accents, high-quality typography.
**Packages:** `lucide-react` (icons).
**Testing:** Manually verify UI responsiveness and layout.
**Expected outcome:** A polished, static frontend ready to be wired up.

---

### 06 — Full Stack Integration
**Goal:** Connect the React frontend to the LangGraph API.
**Why now:** Both sides are complete; this is the final assembly.
**Prerequisites:** Session 04 and Session 05.
**Frontend:** Add API calls to send messages to the backend. Update local state based on API responses (chat history, order status, bill).
**Backend:** Create a FastAPI POST endpoint that accepts chat messages, invokes the compiled LangGraph, and returns the updated state and assistant response.
**Packages:** `axios` or native `fetch`.
**Testing:** End-to-end manual test: order a dish, see it cook, serve, and receive a bill in the UI.
**Learning:** Bridging asynchronous agent workflows with synchronous HTTP UI updates.
**Expected outcome:** A fully functional Desi Dhaba AI Restaurant application.

---

## Package / Dependency Inventory

| Package | Workspace | Purpose | Type | Introduced |
|---|---|---|---|---|
| `fastapi` | Backend | API framework | Runtime | Session 01 |
| `uvicorn` | Backend | ASGI server | Runtime | Session 01 |
| `react`, `react-dom` | Frontend | UI framework | Runtime | Session 01 |
| `tailwindcss` | Frontend | Styling | Dev | Session 01 |
| `langgraph` | Backend | Agent workflow orchestration | Runtime | Session 02 |
| `langchain-google-genai` | Backend | LLM integration (Gemini) | Runtime | Session 02 |
| `pydantic` | Backend | Data validation / schemas | Runtime | Session 02 |
| `lucide-react` | Frontend | UI Icons | Runtime | Session 05 |

## Infrastructure Progression

- **Session 01 - 06:** Everything runs locally in-memory. The FastAPI server holds the graph in memory. Once the server stops, state is cleared. No external DB or Redis is introduced to keep the focus strictly on LangGraph.

## Authentication Progression

- Authentication is explicitly omitted from this learning phase to maintain focus on agent orchestration.

## Frontend Progression

- **Session 01:** Scaffolding only.
- **Session 05:** Full static UI implemented (Chat, Menu, Status).
- **Session 06:** State dynamically driven by the backend API.

## Completion Criteria

The project is considered complete when:
- The React UI successfully loads and communicates with the FastAPI backend.
- A user can order an item from the menu via natural language.
- The LangGraph agent correctly routes the state through taking, cooking, and serving the order.
- The system correctly terminates the conversation after 3 invalid attempts.
- Simulated failures properly route the workflow backwards to recover.
- The user is presented with a final bill summary.
