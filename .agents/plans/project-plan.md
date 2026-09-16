# Desi Dhaba AI Restaurant — Overall Implementation Plan

## 1. Implementation Strategy

The project adopts an incremental, test-first, decoupled implementation approach across 6 milestones:

1. **Foundations First:** Establish clean monorepo boundaries (`frontend/` and `backend/`) with working dev servers and baseline health check before writing AI or complex UI code.
2. **Deterministic Agent Core:** Implement LangGraph logic in pure, modular Python (`backend/graph/`) with in-memory state. Develop and test the graph iteratively:
   - First: State schema and extraction/validation node.
   - Second: Cyclic edges, retry limits (3 strikes), and order confirmation.
   - Third: Simulated cooking and serving failure/recovery loops and bill calculation.
3. **Dedicated UI Scaffolding:** Build the React + Tailwind frontend shell independently with mock state matching the approved Desi Dhaba visual identity (`design/Desi Dhaba.png`).
4. **Full-Stack Assembly:** Wire the React chat, menu, status tracker, and bill components to FastAPI endpoints via HTTP JSON and verify end-to-end user journeys.

---

## 2. Architecture Implementation

### Frontend (React + Tailwind CSS)
- **Framework:** React 18+ initialized with Vite for rapid development and hot reload.
- **Styling:** Tailwind CSS with custom theme colors configured in `tailwind.config.js` (deep charcoal background, warm saffron orange accents, cream typography).
- **Icons:** `lucide-react` for clean, lightweight restaurant and conversational icons.
- **Client State:** Local React state (`useState`, `useEffect`) tracking `sessionId`, `chatMessages`, `menuItems`, `workflowStatus`, and `activeBill`.
- **API Client:** Simple native `fetch` or `axios` module (`src/services/api.js`) communicating with FastAPI.

### Backend & API (FastAPI)
- **Framework:** FastAPI with Uvicorn ASGI server.
- **Routing:** Thin controllers in `backend/app/routes/` delegating state updates and orchestration to the graph service.
- **CORS:** FastAPI CORS middleware enabled for local React development (`http://localhost:5173`).
- **Data Validation:** Strict Pydantic models for all API request bodies and JSON responses.

### LangGraph Workflow (Backend Orchestration)
- **State Schema:** `RestaurantState` defined with `typing.TypedDict`, holding conversation history, parsed order entities, attempt counters, and status flags.
- **LLM Integration:** Google Gemini via `langchain-google-genai` (e.g., `gemini-1.5-flash` or configurable model) utilizing structured output extraction.
- **Node Separation:** Individual small node functions in `backend/graph/nodes.py`:
  - `validate_input`: Extracts dish/quantity and checks against menu stock.
  - `respond_retry`: Increments invalid attempts and informs the user.
  - `terminate_session`: Terminal node reached after 3 invalid attempts.
  - `take_order`: Confirms order and reserves menu inventory.
  - `cook_order`: Simulates kitchen preparation (with failure branch).
  - `serve_order`: Simulates table delivery (with failure branch).
  - `generate_bill`: Calculates item totals, 5% GST, and final receipt.
- **Graph Assembly:** Compiled `StateGraph` in `backend/graph/workflow.py` with explicit conditional edges guarded by state counters.

### Data & State Management
- **In-Memory Store:** Ephemeral Python dictionary in `backend/app/store.py` holding `session_id -> {state, graph_instance}`.
- **Menu Truth:** Authoritative in-memory dictionary in `backend/app/menu.py` with thread-safe stock decrementing.

---

## 3. Project Structure

```text
Restaurant AI Agent/
├── .agents/
│   ├── plans/
│   │   └── project-plan.md
│   ├── roadmap/
│   │   └── project-roadmap.md
│   └── specs/
│       └── project-spec.md
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py            # FastAPI entry point & CORS
│   │   ├── config.py          # Settings & environment variables
│   │   ├── menu.py            # Authoritative menu data & inventory
│   │   ├── store.py           # In-memory session state repository
│   │   └── schemas.py         # Pydantic request/response schemas
│   ├── graph/
│   │   ├── __init__.py
│   │   ├── state.py           # RestaurantState TypedDict
│   │   ├── nodes.py           # Individual graph node functions
│   │   ├── edges.py           # Conditional edge routing logic
│   │   └── workflow.py        # Graph assembly & compile logic
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_menu.py       # Menu validation unit tests
│   │   ├── test_validation.py # Input validation & retry unit tests
│   │   └── test_workflow.py   # Full graph end-to-end tests
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   ├── postcss.config.js
│   └── src/
│       ├── main.jsx
│       ├── App.jsx
│       ├── index.css
│       ├── components/
│       │   ├── Header.jsx         # Dhaba branding & Reset CTA
│       │   ├── MenuSidebar.jsx    # Dish cards with live stock badges
│       │   ├── ChatTimeline.jsx   # Message bubbles & typing loader
│       │   ├── ChatComposer.jsx   # Input box & send action
│       │   ├── OrderStatus.jsx    # Visual kitchen stepper
│       │   └── BillModal.jsx      # Itemized receipt & totals
│       └── services/
│           └── api.js             # API request wrappers
├── design/
│   └── Desi Dhaba.png             # Approved UI reference image
├── GEMINI.md                      # Project rules & design guidelines
└── README.md
```

---

## 4. Dependency / Package Plan

### Backend Dependencies (`backend/requirements.txt`)

| Package | Area | Purpose | Type | Milestone |
|---|---|---|---|---|
| `fastapi` | Backend | API server framework | Runtime | Milestone 01 |
| `uvicorn[standard]` | Backend | ASGI production web server | Runtime | Milestone 01 |
| `pydantic` | Backend | Request/response data validation | Runtime | Milestone 01 |
| `python-dotenv` | Backend | Load environment variables from `.env` | Runtime | Milestone 01 |
| `langgraph` | Backend | Agent state graph & workflow engine | Runtime | Milestone 02 |
| `langchain-google-genai` | Backend | Gemini LLM wrapper & embeddings | Runtime | Milestone 02 |
| `langchain-core` | Backend | Core message abstractions & runnable interfaces | Runtime | Milestone 02 |
| `pytest` | Backend | Unit and integration test runner | Dev | Milestone 02 |
| `httpx` | Backend | FastAPI test client transport | Dev | Milestone 01 |

### Frontend Dependencies (`frontend/package.json`)

| Package | Area | Purpose | Type | Milestone |
|---|---|---|---|---|
| `react` | Frontend | Core UI library | Runtime | Milestone 01 |
| `react-dom` | Frontend | DOM rendering for React | Runtime | Milestone 01 |
| `lucide-react` | Frontend | Consistent UI icons | Runtime | Milestone 05 |
| `vite` | Frontend | Build tool & dev server | Dev | Milestone 01 |
| `@vitejs/plugin-react` | Frontend | React JSX plugin for Vite | Dev | Milestone 01 |
| `tailwindcss` | Frontend | Utility-first styling framework | Dev | Milestone 01 |
| `postcss` | Frontend | CSS preprocessor for Tailwind | Dev | Milestone 01 |
| `autoprefixer` | Frontend | CSS vendor prefixer | Dev | Milestone 01 |

---

## 5. Milestone Implementation Plan

### Milestone 01 — Project Foundation & Basic API

**Goal:** Establish the monorepo workspace, setup FastAPI backend with a `/health` endpoint, configure the Vite + React frontend with Tailwind CSS, and verify local development runtime.

**Prerequisites:** None.

**Backend:**
- Create `backend/requirements.txt` and install dependencies.
- Create `backend/app/config.py` with environment configuration.
- Create `backend/app/main.py` with FastAPI instance, CORS middleware, and `GET /api/health`.
- Create `backend/.env.example`.

**Frontend:**
- Initialize Vite React project in `frontend/`.
- Configure `tailwind.config.js` with Dhaba brand colors (`charcoal`, `saffron`, `cream`).
- Create basic `App.jsx` showing "Desi Dhaba AI Restaurant" connection test card.

**Database / Storage:** None.

**Infrastructure:** None (local development server).

**Integration:** Frontend makes a test fetch to `http://localhost:8000/api/health` and displays backend status.

**Specialists:**
- Backend Specialist (FastAPI scaffolding)
- Frontend Specialist (Vite + Tailwind scaffolding)

**Implementation Order:**
```text
Backend FastAPI Scaffolding
    ↓
Backend Health Check Verification
    ↓
Frontend Vite + Tailwind Scaffolding
    ↓
Frontend-to-Backend Health Ping Verification
```

**Validation:**
- `curl http://localhost:8000/api/health` returns `{"status": "healthy"}`.
- `npm run build` in `frontend/` succeeds without errors.
- Running frontend renders themed welcome screen and confirms backend connection.

**Expected Outcome:** Running FastAPI server and React dev environment communicating cleanly over HTTP.

---

### Milestone 02 — LangGraph Core: State & Validation

**Goal:** Build the restaurant menu repository, define the `RestaurantState` schema, and implement the `validate_input` node with Gemini entity extraction and deterministic inventory checking.

**Prerequisites:** Milestone 01.

**Backend:**
- Create `backend/app/menu.py` with the 6 authentic Indian dishes, prices, categories, and stock numbers.
- Create `backend/graph/state.py` defining the `RestaurantState` schema (messages, current_input, parsed_dish, parsed_quantity, is_valid, invalid_attempts).
- Create `backend/graph/nodes.py` with `validate_input` node:
  - Uses Gemini (`langchain-google-genai`) with structured output to parse dish name, quantity, and customer intent.
  - Matches parsed dish against `backend/app/menu.py`.
  - Validates requested quantity against `available_qty`.
  - Sets `is_valid = True/False` and populates `validation_error` deterministically.
- Create `backend/tests/test_validation.py` covering valid dish requests, unknown dishes, and stock overflow.

**Frontend:** None.

**Database / Storage:** In-memory menu dictionary.

**Infrastructure:** Configured `GEMINI_API_KEY` in `backend/.env`.

**Integration:** Expose `GET /api/menu` endpoint returning active menu and stock.

**Specialists:**
- Backend Specialist (LangGraph, Gemini integration, Menu model)

**Implementation Order:**
```text
Authoritative Menu Data Model
    ↓
RestaurantState Schema Definition
    ↓
Gemini Extraction & Menu Validation Node
    ↓
Pytest Test Suite for Input Validation
```

**Validation:**
- Unit tests verify "2 Butter Chicken" parses correctly and validates against 5 available stock.
- Unit tests verify "10 Butter Chicken" fails quantity validation.
- Unit tests verify "Pasta" fails dish name validation.

**Expected Outcome:** Input validation is 100% deterministic and testable through pytest.

---

### Milestone 03 — Workflow Edges: Retries & Take Order

**Goal:** Implement conditional branching in LangGraph for handling retries, bounding invalid attempts to a maximum of 3 before session termination, and adding the `take_order` node.

**Prerequisites:** Milestone 02.

**Backend:**
- Create `backend/graph/nodes.py`:
  - `respond_retry`: Increments `invalid_attempts`, generates courteous refusal/clarification response.
  - `terminate_session`: Final polite refusal message, sets `is_terminal = True`.
  - `take_order`: Decrements menu inventory, records confirmed item into `order_items`, updates `workflow_status = "ORDER_PLACED"`.
- Create `backend/graph/edges.py`:
  - `route_after_validation`:
    - If `is_valid == True` -> route to `take_order`.
    - If `is_valid == False` and `invalid_attempts < 3` -> route to `respond_retry`.
    - If `is_valid == False` and `invalid_attempts >= 3` -> route to `terminate_session`.
- Assemble first executable loop in `backend/graph/workflow.py`.
- Create unit tests in `backend/tests/test_retries.py` asserting that 4 consecutive invalid inputs terminate the graph, while a valid input reaches `take_order`.

**Frontend:** None.

**Database / Storage:** In-memory state holding retry count and inventory.

**Infrastructure:** None.

**Specialists:**
- Backend Specialist (LangGraph conditional routing, State mutation)

**Implementation Order:**
```text
Retry & Termination Nodes
    ↓
take_order Node & Inventory Decrement
    ↓
Conditional Routing Edges
    ↓
Pytest Suite for 3-Strike Boundary & Order Placement
```

**Validation:**
- Automated test verifies `invalid_attempts` increments on invalid input.
- Automated test confirms graph exits to `END` on 3rd invalid attempt.
- Automated test verifies `take_order` reduces stock from 5 to 3 when 2 plates are ordered.

**Expected Outcome:** LangGraph reliably handles bad input, enforces the 3-attempt safety guard, and takes valid orders.

---

### Milestone 04 — Simulated Failures: Cooking & Serving

**Goal:** Complete the full restaurant workflow by implementing `cook_order`, `serve_order`, and `generate_bill` nodes, along with backward recovery edges for simulated kitchen and serving failures.

**Prerequisites:** Milestone 03.

**Backend:**
- Implement `backend/graph/nodes.py`:
  - `cook_order`: Simulates kitchen cooking. Checks `force_cooking_fail` flag or random simulation (default 15%). Sets `cooking_status = "SUCCESS"` or `"FAILED"`.
  - `handle_cooking_failure`: Returns friendly cooking apology message and resets item selection.
  - `serve_order`: Simulates table delivery. Checks `force_serving_fail` flag or random simulation (default 15%). Sets `serving_status = "SUCCESS"` or `"FAILED"`.
  - `handle_serving_failure`: Returns serving mishap apology message and routes back to cooking.
  - `generate_bill`: Calculates item totals, 5% GST, and builds `BillSummary`. Updates `workflow_status = "COMPLETED"`.
- Implement `backend/graph/edges.py`:
  - `route_after_cooking`:
    - If `cooking_status == "SUCCESS"` -> route to `serve_order`.
    - If `cooking_status == "FAILED"` -> route to `handle_cooking_failure` -> `take_order` (re-select dish).
  - `route_after_serving`:
    - If `serving_status == "SUCCESS"` -> route to `generate_bill` -> `END`.
    - If `serving_status == "FAILED"` -> route to `handle_serving_failure` -> `cook_order` (re-cook).
- Add tests in `backend/tests/test_workflow.py` forcing failure flags to verify backward graph loops.

**Frontend:** None.

**Database / Storage:** In-memory bill calculation.

**Infrastructure:** None.

**Specialists:**
- Backend Specialist (LangGraph cyclic graph loops, Failure recovery)

**Implementation Order:**
```text
cook_order & serve_order Nodes
    ↓
Failure Handling & Recovery Nodes
    ↓
generate_bill Calculation Node
    ↓
Cyclic Edge Routing
    ↓
Pytest Suite for Failure Simulation and Backward Recovery
```

**Validation:**
- Running workflow with `force_cooking_fail=True` correctly loops back to dish selection.
- Running workflow with `force_serving_fail=True` correctly loops back to cooking.
- Happy path workflow produces complete bill with 5% tax and grand total.

**Expected Outcome:** Full backend LangGraph workflow is complete, resilient, and verified by tests.

---

### Milestone 05 — Frontend Foundation: Chat & Menu UI

**Goal:** Build the complete Desi Dhaba visual interface in React + Tailwind CSS according to the approved visual guidelines (`design/Desi Dhaba.png`).

**Prerequisites:** Milestone 01.

**Backend:** None (Milestone 05 focuses on frontend components using mock data).

**Frontend:**
- `src/components/Header.jsx`: Dhaba branding, tagline, session reset button.
- `src/components/MenuSidebar.jsx`: Scannable dish cards displaying image, price (₹), spice level badge, and real-time inventory count ("X left" / "Sold Out").
- `src/components/ChatTimeline.jsx`: Message history displaying chef avatar for assistant, user bubbles, and animated typing indicator.
- `src/components/ChatComposer.jsx`: Bottom input composer with send button and quick-order chips (e.g. "Order 2 Butter Chicken").
- `src/components/OrderStatus.jsx`: Live stage tracker (Order Placed ➔ Validated ➔ Cooking ➔ Serving ➔ Billed).
- `src/components/BillModal.jsx`: Itemized receipt card showing dishes, quantities, 5% GST, grand total, and "Order Again" action.
- Responsive layout with desktop-first two-column layout (Menu panel on left, Chat & Order status on right).

**Database / Storage:** None.

**Infrastructure:** None.

**Specialists:**
- Frontend Specialist (UI design, Tailwind styling, Component architecture)

**Implementation Order:**
```text
Dhaba Color Tokens & Typography Setup
    ↓
Header & Layout Scaffolding
    ↓
Menu Sidebar Component
    ↓
Chat Timeline & Composer Component
    ↓
Order Status Stepper & Bill Modal
```

**Validation:**
- Visual inspection against `design/Desi Dhaba.png`.
- Layout responds gracefully on desktop and mobile viewports.
- Interactive states (hover, typing, modal toggle) feel polished and responsive.

**Expected Outcome:** A production-quality, visually authentic Desi Dhaba interface ready for backend API connection.

---

### Milestone 06 — Full Stack Integration

**Goal:** Connect the React frontend to the FastAPI + LangGraph backend, implementing real-time chat ordering, live status updates, inventory synchronization, failure recovery notifications, and bill presentation.

**Prerequisites:** Milestone 04 and Milestone 05.

**Backend:**
- Create `POST /api/chat`: Accepts `session_id`, `message`, and optional test flags (`force_cooking_fail`, `force_serving_fail`). Dispatches message to compiled LangGraph, persists state in `store.py`, and returns assistant reply and updated state.
- Create `POST /api/reset`: Clears session state and returns fresh session ID.
- Update `GET /api/menu` to reflect real-time decremented quantities.

**Frontend:**
- Create `src/services/api.js` with calls to `/api/menu`, `/api/chat`, and `/api/reset`.
- Wire `App.jsx` state to API responses:
  - Initial load fetches live menu.
  - Sending message triggers loading spinner, appends assistant response, updates `OrderStatus` stepper.
  - When status reaches `COMPLETED`, display `BillModal`.
  - When status reaches `TERMINATED`, lock composer and offer reset button.
  - Clicking "Add to Chat" from menu card pre-fills composer.
  - Clicking "New Order" triggers `/api/reset` and cleans UI.

**Database / Storage:** In-memory session store.

**Infrastructure:** None.

**Specialists:**
- Full-Stack Integrator / Backend & Frontend Specialists

**Implementation Order:**
```text
FastAPI Chat & Reset Endpoints
    ↓
Frontend API Service Integration
    ↓
Chat & Order Status State Wiring
    ↓
Bill Display & Session Reset Wiring
    ↓
End-to-End User Testing & Verification
```

**Validation:**
- End-to-end test 1: Place valid order -> See cooking stepper -> See serving stepper -> Receive itemized bill.
- End-to-end test 2: Order out-of-stock item -> Receive polite refusal without state corruption.
- End-to-end test 3: Send 3 off-topic messages -> Verify session locks gracefully.
- End-to-end test 4: Trigger kitchen failure -> Observe retry loop and customer message.

**Expected Outcome:** A fully functional, resilient, end-to-end Desi Dhaba AI Restaurant application.

---

## 6. Cross-Milestone Dependencies

```text
[Milestone 01: Scaffolding & Health API]
       │
       ├───► [Milestone 02: LangGraph Core & Validation]
       │            │
       │            ▼
       │     [Milestone 03: Edges, Retries & Take Order]
       │            │
       │            ▼
       │     [Milestone 04: Cooking, Serving & Bill] ───┐
       │                                                │
       └───► [Milestone 05: Frontend UI Shell]          │
                    │                                   │
                    ▼                                   ▼
             [Milestone 06: Full Stack Integration & E2E]
```

### Dependency Logic
- **Milestone 01** provides the baseline environments so both backend and frontend can be developed in parallel or in sequence.
- **Milestones 02 ➔ 03 ➔ 04** construct the LangGraph workflow incrementally, ensuring state schema, branching, and cyclic recovery are robustly tested before connecting to the UI.
- **Milestone 05** produces the frontend interface without blocking on backend completion.
- **Milestone 06** merges both tracks into the finished product.

---

## 7. Testing Strategy

### 1. Backend Unit Tests (`pytest`)
- Run with: `pytest backend/tests`
- Fast, deterministic tests that mock LLM calls where appropriate to verify:
  - Menu data lookup and inventory validation.
  - Retry counter incrementation and 3-strike graph termination.
  - Failure flags routing properly backward in the state graph.
  - Math precision in 5% GST and grand total calculations.

### 2. API Contract Tests
- Test FastAPI routes using `httpx.AsyncClient` or `TestClient`:
  - `GET /api/health` returns `200 OK`.
  - `GET /api/menu` returns valid schema with 6 dishes.
  - `POST /api/chat` returns expected JSON structure.

### 3. Frontend Component & Visual Verification
- Verify build integrity with `npm run build`.
- Manual verification in browser of:
  - Dhaba color scheme, responsive sidebar, message scroll behavior.
  - Order status animations and modal popups.

### 4. End-to-End Acceptance Verification
- Execute the 5 core acceptance scenarios documented in `project-spec.md` directly via the browser UI.

---

## 8. Design Implementation Strategy

### Dhaba Design Tokens
- **Background:** `bg-[#121214]` (page base) and `bg-[#1c1c20]` (card surfaces).
- **Borders:** `border-[#2e2e34]` for soft, low-contrast separation.
- **Primary Accent:** Warm saffron orange (`#f97316` / `#ea580c`) for buttons, active tabs, and badges.
- **Typography:** Clean sans-serif (`Inter` or system sans-serif) with warm off-white (`#fafaf9`) text for headers and body, and warm muted gray (`#a1a1aa`) for subtitles.

### Component Design Principles
- **Menu Cards:** Large rounded corners (`rounded-2xl`), subtle hover zoom/shadow, prominent price badge, clear quantity chip.
- **Chat Timeline:** Dhaba chef avatar with saffron turban icon; clear bubble distinction between user and assistant.
- **Order Stepper:** Visual step indicator with saffron progress fill, pulsating dots for active state, and amber/red badge during a retry recovery.
- **Bill Modal:** Clean receipt aesthetic with dotted dividers, item breakdown, tax subtotal, and highlighted grand total.

---

## 9. Environment and Configuration

### Backend Environment Variables (`backend/.env`)
```bash
# Server Port
PORT=8000

# Google Gemini API Key for LangGraph extraction
GEMINI_API_KEY=your_gemini_api_key_here

# LLM Model Name
LLM_MODEL=gemini-1.5-flash

# Allowed CORS Origins
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

### Frontend Environment Variables (`frontend/.env`)
```bash
# Backend API Base URL
VITE_API_URL=http://localhost:8000
```

> [!IMPORTANT]
> Real API keys must never be committed to source control. `.env.example` will be provided for reference.

---

## 10. Risk and Dependency Notes

1. **LLM Structured Output Reliability:**
   - *Risk:* Gemini might return non-standard formatting if free-form prompt is used.
   - *Mitigation:* Use Pydantic schema binding with `with_structured_output` or strict JSON schemas to guarantee parseable entities.
2. **Infinite LangGraph Loops:**
   - *Risk:* Failure loops could bounce indefinitely between cooking and serving.
   - *Mitigation:* Cap recovery attempts in `RestaurantState` (e.g., max 2 kitchen retries) before falling back to a clean terminal state.
3. **In-Memory Concurrency & Persistence:**
   - *Risk:* In-memory inventory shared across sessions could run out during multi-session testing.
   - *Mitigation:* Keep inventory isolated per session ID or provide a one-click "Reset All" button in development.

---

## 11. Milestone Completion Criteria

- [ ] **Milestone 01 Complete:** FastAPI `/api/health` responds 200, React frontend builds and displays themed dashboard connected to API.
- [ ] **Milestone 02 Complete:** Menu repository created, `RestaurantState` defined, `validate_input` correctly parses dishes and inventory with passing pytest tests.
- [ ] **Milestone 03 Complete:** Conditional retry edges route bad inputs to retry, terminates on 3rd invalid attempt, and routes valid inputs to `take_order`.
- [ ] **Milestone 04 Complete:** `cook_order`, `serve_order`, failure recovery loops, and `generate_bill` nodes are fully functional and covered by unit tests.
- [ ] **Milestone 05 Complete:** Complete UI shell matching `design/Desi Dhaba.png` rendered in React with responsive menu, chat, status tracker, and bill card.
- [ ] **Milestone 06 Complete:** React UI and FastAPI + LangGraph backend communicate seamlessly; all 5 end-to-end acceptance scenarios pass.
