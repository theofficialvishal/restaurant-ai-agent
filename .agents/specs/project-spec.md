# Desi Dhaba AI Restaurant — Overall Project Specification

## 1. Project Overview

### Product Purpose
**Desi Dhaba AI Restaurant** is a full-stack, conversational restaurant ordering web application. It showcases an autonomous yet tightly governed AI ordering assistant that guides customers through choosing Indian dishes, validates orders against real-time menu availability, processes orders through realistic kitchen workflows (taking order, cooking, and serving with simulated real-world failures), and generates an itemized bill.

The primary engineering goal is to master **LangGraph stateful workflows**, demonstrating that LLM agents can be constrained to deterministic state machines and retry loops rather than acting as unconstrained chatbots.

### Target Users
- **Restaurant Customers:** Dining patrons who interact with the Desi Dhaba AI assistant using natural language to browse the menu, place orders, observe live preparation status, and receive a bill.
- **Developers / Learners:** Engineers evaluating LangGraph patterns, cyclic graphs, deterministic validation guardrails, state persistence, and full-stack integration with FastAPI and React.

### Primary Problem Being Solved
Standard LLM chat wrappers suffer from hallucinations, failure to enforce strict business rules (such as inventory, price calculation, and strict transition states), and inability to handle operational failures cleanly. Desi Dhaba solves this by wrapping an LLM intent extractor inside an explicit LangGraph state machine where restaurant rules, inventory decrementing, failure routing, and bill calculation remain strictly deterministic.

### High-Level Product Scope
- Curated Indian dhaba menu with real-time stock and pricing.
- Conversational chat interface backed by Gemini via LangGraph.
- Natural language intent extraction for dishes and quantities.
- Deterministic inventory & quantity validation.
- Bounded retry loops (maximum 3 invalid or off-topic attempts before polite termination).
- Realistic kitchen simulation (`take_order` → `cook_order` → `serve_order` → `generate_bill`).
- Controlled failure simulations (cooking failure routing back to dish selection; serving failure routing back to kitchen cooking).
- Live order status tracking in the UI.
- Final itemized receipt with tax breakdown and order reset.

---

## 2. Product Goals

1. **Deterministic Guardrails:** Ensure 100% of price calculations, dish validation, and inventory checks are handled by backend business logic, never trusted to raw LLM output.
2. **Predictable State Transitions:** Model the entire restaurant lifecycle as an explicit LangGraph `StateGraph` with well-defined entry, intermediate, retry, and terminal states.
3. **Resilient Failure Recovery:** Gracefully handle operational failures (cooking burnt/spilled, serving drops) and user errors (unknown dish, out of stock, off-topic chat) via cyclic graph loops.
4. **Cohesive Premium Dhaba UX:** Deliver a rich, warm, conversational UI reflecting authentic Indian hospitality using dark charcoal surfaces, saffron accents, and live workflow visualization.
5. **Seamless Full-Stack Bridge:** Connect a synchronous React HTTP frontend to an asynchronous or stateful FastAPI + LangGraph backend cleanly.

---

## 3. User Roles

The initial learning version requires only one user role:
- **Customer (Guest User):** Interacts with the AI assistant, selects items, tracks order preparation, and views the generated bill. No authentication or login is required.

---

## 4. Functional Requirements

### 4.1 Menu Management & Presentation
- **Capability:** Display a curated list of authentic Indian dishes with names, descriptions, prices (INR ₹), categories, spice levels, and available inventory.
- **User Interaction:** Customer views dish cards in a dedicated menu panel with live availability indicators.
- **Preconditions:** Server initializes mock in-memory inventory upon startup.
- **Expected Behavior:** Dishes display remaining stock (e.g., "5 left"). When stock drops to 0, item displays "Sold Out".
- **Initial Menu Items:**
  - *Butter Chicken* (Curry, ₹350, 5 available)
  - *Paneer Tikka* (Starter, ₹250, 8 available)
  - *Hyderabadi Biryani* (Rice, ₹220, 10 available)
  - *Dal Makhani* (Curry, ₹180, 6 available)
  - *Garlic Naan* (Bread, ₹60, 20 available)
  - *Gulab Jamun (2 pcs)* (Dessert, ₹90, 12 available)

### 4.2 Conversational Ordering & Intent Extraction
- **Capability:** Interpret natural language customer messages to extract intended dish names and quantities.
- **User Interaction:** Customer types requests like *"Get me 2 Butter Chicken and one Garlic Naan"* or *"Kya Paneer Tikka milega?"*.
- **Expected Behavior:** LangGraph uses Gemini with structured output (or schema extraction) to parse:
  - `dish_name` (normalized string or matched candidate)
  - `quantity` (positive integer)
  - `intent` (ORDER, INQUIRY, OFF_TOPIC, CANCEL)
- **Edge Cases:**
  - Ambiguous dish names (e.g., "Chicken") prompt a clarifying question.
  - Non-numeric or missing quantities default to 1 with confirmation.

### 4.3 Deterministic Order Validation
- **Capability:** Validate extracted items against authoritative menu inventory before sending to the kitchen.
- **Preconditions:** Extracted order item passed to `validate_input` node.
- **Success Behavior:** If dish exists and `requested_quantity <= available_quantity`, mark item as valid and transition to `take_order`.
- **Failure Behavior:**
  - *Unknown Dish:* Return courteous notification that the item is not on the Desi Dhaba menu, suggest popular dishes.
  - *Out of Stock / Insufficient Quantity:* Inform customer of remaining quantity (e.g., *"Only 2 plates of Dal Makhani are available"*), request adjusted quantity.

### 4.4 Off-Topic and Invalid Attempt Bounding
- **Capability:** Guard the assistant against off-topic rambling, jailbreaks, or repeated invalid ordering attempts.
- **Rules:**
  - Assistant politely declines questions unrelated to Desi Dhaba food ordering (e.g., coding, general trivia, weather).
  - Each invalid order attempt or off-topic message increments `invalid_attempts` in state.
  - If `invalid_attempts < 3`: Provide polite guidance, restate the purpose, and invite an order.
  - If `invalid_attempts >= 3`: Issue a polite closing statement (e.g., *"We can only assist with dining orders at this time. We must conclude this session. Namaste!"*) and transition graph to `END`. Further input is blocked until the conversation is restarted.

### 4.5 Order Fulfillment Workflow (LangGraph State Machine)
- **Workflow Topology:**
  ```text
  START
    ↓
  validate_input
    ├── Invalid (attempts < 3) ──> respond_retry ──> WAIT_FOR_USER
    ├── Invalid (attempts >= 3) ─> terminate_session ──> END
    └── Valid
          ↓
      take_order (reserve inventory, add to active order)
          ↓
      cook_order (kitchen preparation)
          ├── Failure ───────────> handle_cooking_failure ──> take_order (re-select dish)
          └── Success
                ↓
            serve_order (table delivery)
                ├── Failure ─────> handle_serving_failure ──> cook_order (re-cook)
                └── Success
                      ↓
                  generate_bill (calculate taxes, totals, display summary)
                      ↓
                     END
  ```

### 4.6 Simulated Cooking Failure & Recovery
- **Capability:** Simulate realistic kitchen mishaps (e.g., dish burnt, ingredients spoiled).
- **Behavior:** In testing/simulation mode, a configurable probability (or deterministic test flag) triggers a cooking failure.
- **Routing:** State records failure reason, informs customer warmly (e.g., *"Our chef encountered an issue preparing your dish. Let's pick a fresh dish for you!"*), and routes the customer back to dish selection without billing for the failed dish.

### 4.7 Simulated Serving Failure & Recovery
- **Capability:** Simulate table service mishaps (e.g., waiter dropped tray, wrong garnish).
- **Routing:** State records serving failure, notifies customer (e.g., *"Apologies! The tray had a slip. Our kitchen is rushing a fresh hot preparation right away!"*), and loops back to `cook_order`. Inventory is not double-charged.

### 4.8 Bill Generation & Summary
- **Capability:** Calculate the final payable bill once serving succeeds.
- **Calculations:**
  - `Item Total = Price * Quantity`
  - `Subtotal = Sum of Item Totals`
  - `GST (5% Restaurant tax) = Subtotal * 0.05`
  - `Grand Total = Subtotal + GST`
- **Presentation:** Formatted summary showing item names, unit prices, quantities, subtotal, GST, and grand total in INR (₹).

---

## 5. User Flows

### Flow 1: Standard Ordering Journey (Happy Path)
```text
User enters app
    ↓
Greets assistant / asks for menu
    ↓
Assistant welcomes user: "Namaste! Welcome to Desi Dhaba..."
    ↓
User: "I want 2 Butter Chicken and 2 Garlic Naan"
    ↓
Validation Node checks stock: Butter Chicken (5 avail >= 2), Garlic Naan (20 avail >= 2)
    ↓
Order Taken -> Inventory decremented
    ↓
Kitchen Cooking -> State: "Cooking your rich Butter Chicken..."
    ↓
Table Serving -> State: "Served hot with fresh butter!"
    ↓
Bill Generated -> Assistant displays final receipt with ₹ total
    ↓
UI displays "Start New Order" button
```

### Flow 2: Out of Stock / Quantity Exceeded Flow
```text
User: "Give me 10 Butter Chicken"
    ↓
Validation Node detects requested (10) > available (5)
    ↓
State increments invalid_attempts (or handles soft quantity correction)
    ↓
Assistant: "We only have 5 Butter Chicken left today! Would you like 5 plates or something else?"
    ↓
User replies with valid quantity or alternative
```

### Flow 3: Off-Topic / 3-Strike Termination Flow
```text
User: "Write me a Python script to scrape Google" (Attempt 1)
    ↓
Assistant: "Sorry, I can only help with restaurant orders. What dish would you like?"
    ↓
User: "Tell me the weather in Mumbai" (Attempt 2)
    ↓
Assistant: "I specialize only in Desi Dhaba orders. Please pick a dish from our menu."
    ↓
User: "Who won the 2022 World Cup?" (Attempt 3)
    ↓
Assistant: "We cannot fulfill non-restaurant requests. Ending this session. Namaste!"
    ↓
Graph reaches END; composer is disabled in UI with 'Start New Order' CTA
```

### Flow 4: Kitchen Cooking Failure Recovery
```text
Order Taken (e.g., Dal Makhani)
    ↓
cook_order node triggers simulated failure (e.g., 20% random or test flag)
    ↓
State updates: cooking_status = "FAILED", reason = "Kitchen issue: Over-simmered"
    ↓
Assistant: "We ran into an issue in the kitchen preparing your Dal Makhani. Please select another dish!"
    ↓
Graph loops back to take_order / dish selection
```

### Flow 5: Serving Failure Recovery
```text
Cooking Success (e.g., Paneer Tikka)
    ↓
serve_order node triggers simulated failure (e.g., dropped platter)
    ↓
State updates: serving_status = "FAILED"
    ↓
Assistant: "Oops! We had a slip while serving. Don't worry, chef is preparing a fresh batch right now!"
    ↓
Graph loops back to cook_order (re-cooking, no re-selection needed)
    ↓
cook_order succeeds -> serve_order succeeds -> Bill generated
```

---

## 6. Data Requirements

### 6.1 Entities & Schemas

#### MenuItem
```python
class MenuItem:
    id: str
    name: str
    category: str       # "Curry", "Starter", "Rice", "Bread", "Dessert"
    price: float        # Price in INR
    available_qty: int  # Current remaining stock
    description: str
    spice_level: str    # "Mild", "Medium", "Spicy"
```

#### OrderItem
```python
class OrderItem:
    dish_id: str
    dish_name: str
    unit_price: float
    quantity: int
    item_total: float
```

#### BillSummary
```python
class BillSummary:
    items: list[OrderItem]
    subtotal: float
    tax: float          # 5% GST
    grand_total: float
    generated_at: str
```

#### GraphState (LangGraph State Schema)
```python
class RestaurantState(TypedDict):
    session_id: str
    messages: list[dict]            # Chat history (role, content)
    current_input: str              # Latest user utterance
    parsed_dish: Optional[str]      # Dish extracted by LLM
    parsed_quantity: Optional[int]  # Quantity extracted by LLM
    validation_error: Optional[str] # Error description if invalid
    is_valid: bool                  # Result of deterministic validation
    invalid_attempts: int           # Counter for 3-strike rule
    order_items: list[OrderItem]    # Active confirmed items
    workflow_status: str            # "IDLE", "VALIDATING", "COOKING", "SERVING", "COMPLETED", "TERMINATED"
    cooking_status: str             # "PENDING", "COOKING", "SUCCESS", "FAILED"
    serving_status: str             # "PENDING", "SERVING", "SUCCESS", "FAILED"
    failure_reason: Optional[str]   # Explanation of simulated failure
    bill: Optional[BillSummary]     # Final bill calculation
    is_terminal: bool               # Indicates if graph reached END
```

### 6.2 Persistence
- **Storage Strategy:** In-memory storage. State is stored by `session_id` on the FastAPI server instance during runtime.
- **Reset Mechanism:** User can click "New Order" or refresh to reset state.

---

## 7. API & System Behavior

### 7.1 Endpoints

#### 1. `GET /api/health`
- **Purpose:** Health check for server and LLM configuration.
- **Response:** `{"status": "healthy", "model": "gemini-..."}`

#### 2. `GET /api/menu`
- **Purpose:** Retrieve the active menu and live available quantities.
- **Response:**
  ```json
  {
    "items": [
      {
        "id": "butter-chicken",
        "name": "Butter Chicken",
        "category": "Curry",
        "price": 350.0,
        "available_qty": 5,
        "description": "Tender chicken in rich creamy tomato and butter gravy.",
        "spice_level": "Medium"
      }
    ]
  }
  ```

#### 3. `POST /api/chat`
- **Purpose:** Submit customer message, execute graph step, and return updated workflow state.
- **Request Body:**
  ```json
  {
    "session_id": "string",
    "message": "string",
    "force_cooking_fail": false,
    "force_serving_fail": false
  }
  ```
- **Response Body:**
  ```json
  {
    "session_id": "string",
    "assistant_message": "string",
    "workflow_status": "COOKING",
    "invalid_attempts": 0,
    "current_order": [...],
    "bill": null,
    "is_terminal": false
  }
  ```

#### 4. `POST /api/reset`
- **Purpose:** Clear session state and re-initialize conversation.
- **Request:** `{"session_id": "string"}`
- **Response:** `{"status": "reset_successful", "session_id": "string"}`

---

## 8. Frontend & UI Requirements

### 8.1 Visual Identity & Styling
- **Theme:** Modern, authentic Indian dhaba aesthetic aligned with `design/Desi Dhaba.png` and `GEMINI.md`.
- **Color Palette:**
  - Background: Deep Charcoal (`#121214` / `#18181b`)
  - Surface Cards: Rich Dark Grey (`#202024` / `#27272a`) with subtle low-contrast borders (`#3f3f46`)
  - Accent: Warm Saffron / Amber Orange (`#f97316` / `#ea580c`)
  - Accent Hover: Brighter Warm Orange (`#fb923c`)
  - Text Primary: Cream / Off-White (`#fafaf9`)
  - Text Muted: Warm Gray (`#a1a1aa`)
  - Status Success: Emerald Green (`#10b981`)
  - Status Warning / Failure: Crimson / Amber (`#ef4444` / `#f59e0b`)

### 8.2 Layout & Screens
1. **Header & Branding:**
   - Restaurant logo / Dhaba icon with "Desi Dhaba AI" branding.
   - Live server connection indicator.
   - "New Order" reset button.
2. **Interactive Menu Drawer / Sidebar:**
   - Visual food cards with price badges, tags, and dynamic "X left" badges.
   - Quick "Add to Chat" click action to pre-fill prompt.
3. **Conversational Ordering Hub (Main Panel):**
   - Message timeline with distinctive Dhaba Chef avatar and user bubbles.
   - Live inline status chip indicating current workflow stage.
   - Sticky chat input composer with submit button, placeholder suggestions.
4. **Order Status Stepper:**
   - Visual progress bar tracking:
     1. Order Received ➔ 2. Validated ➔ 3. Kitchen Cooking ➔ 4. Serving ➔ 5. Billed
   - Animated cooking / serving spinners with friendly status messages.
   - Visual retry indicator when a simulated failure loops back.
5. **Bill & Receipt Card / Modal:**
   - Itemized table with quantities, prices, taxes, and grand total.
   - Print / Finish Order CTA.

---

## 9. Security Requirements

- **API Input Validation:** All API requests validated through Pydantic schemas.
- **Prompt Injection Defense:** Strict separation between extracted structured entities and execution nodes. User message cannot override workflow state transitions.
- **API Key Protection:** LLM provider keys stored in `.env` and loaded via backend environment variables; never exposed to frontend code or bundle.
- **Sanitized Errors:** Internal server errors or LangGraph exceptions are converted into clean user-facing friendly messages.

---

## 10. Non-Functional Requirements

- **Latency & Responsiveness:** Fast local response times; LLM calls must show clear typing/cooking indicators so the user is never left without feedback.
- **Deterministic Testability:** LangGraph transitions must be fully testable with mock LLM outputs and controllable failure toggles (`force_cooking_fail`, `force_serving_fail`).
- **Code Maintainability:** Strict modular separation:
  - `backend/app/` for FastAPI endpoints and server models.
  - `backend/graph/` for LangGraph state, nodes, and conditional edges.
  - `frontend/src/components/` for modular React UI components.
- **Reliability:** The graph must NEVER enter an infinite loop. Guard edges with bounded counters (`invalid_attempts <= 3`).

---

## 11. Acceptance Criteria

### Scenario 1: Valid Single-Dish Order
- **Given** an active session and 5 available Butter Chicken,
- **When** the user says *"I want 1 Butter Chicken"*,
- **Then** the input is validated, inventory drops to 4, order moves through cooking and serving, and a bill for ₹350 + ₹17.50 GST (Total ₹367.50) is returned.

### Scenario 2: Out-of-Stock Rejection
- **Given** an active session with 5 available Butter Chicken,
- **When** the user requests 8 plates,
- **Then** the assistant informs the user that only 5 are available, inventory is not decremented, and the order is not placed in the kitchen.

### Scenario 3: Bounded Invalid / Off-Topic Attempts
- **Given** an active session with `invalid_attempts = 0`,
- **When** the user inputs 3 consecutive non-restaurant or invalid prompts,
- **Then** the first two receive polite refusal guidance with incremented counters, and the third prompt outputs a polite closing message, sets `is_terminal = True`, and ends the session.

### Scenario 4: Simulated Cooking Failure Recovery
- **Given** a valid order placed and `force_cooking_fail = True`,
- **When** the order reaches `cook_order`,
- **Then** cooking fails, customer receives an apology asking to pick another dish, and state routes back to dish selection without generating a bill.

### Scenario 5: Simulated Serving Failure Recovery
- **Given** a valid order cooking successfully and `force_serving_fail = True`,
- **When** the order reaches `serve_order`,
- **Then** serving fails, customer is informed of a service mishap, and the graph routes back to `cook_order` to re-prepare the dish without double-charging.

---

## 12. Milestone Mapping

This specification directly maps to the approved 6-session project roadmap:

| Roadmap Session | Specification Coverage |
|---|---|
| **01 — Project Foundation & Basic API** | Backend FastAPI scaffolding, `/api/health`, React + Tailwind setup, monorepo structure. |
| **02 — LangGraph Core: State & Validation** | Menu data schema, `RestaurantState`, `validate_input` node, Gemini extraction. |
| **03 — Workflow Edges: Retries & Take Order** | Conditional routing, 3-attempt bounding, `take_order` node, inventory reservation. |
| **04 — Simulated Failures: Cooking & Serving** | `cook_order`, `serve_order`, failure routing loops, `generate_bill` calculation. |
| **05 — Frontend Foundation: Chat & Menu UI** | React components: Menu sidebar, Chat timeline, Order status stepper, Receipt card. |
| **06 — Full Stack Integration** | Connecting React to FastAPI endpoints, session lifecycle, end-to-end testing. |

---

## 13. Out of Scope

- Real payment gateway integration (Stripe, Razorpay, UPI).
- Persistent external database (PostgreSQL, MongoDB, Redis) — in-memory is sufficient for learning.
- User registration, login, and profile history.
- Real-time kitchen staff hardware integration (KDS screens, thermal printers).
- Multi-table dining room management.

---

## 14. Assumptions and Open Questions

### Approved Decisions
- **Frameworks:** React (Vite) + Tailwind CSS on Frontend; FastAPI + LangGraph on Backend.
- **LLM:** Google Gemini via `langchain-google-genai`.
- **State Scope:** Ephemeral in-memory sessions keyed by `session_id`.
- **Currency:** Indian Rupee (INR ₹) with 5% standard restaurant GST calculation.
- **Simulations:** Controlled random failure rates (default 15-20%) with manual override flags for deterministic automated testing.

### Open Questions & Future Considerations
- Should multi-item ordering in a single utterance (e.g. "1 Biryani and 2 Naan") be handled in Session 02 or extended in Session 03? *(Planned: Basic entity extraction starts with single primary dish in Session 02, supports list of items by Session 03).*
