# Desi Dhaba AI Restaurant — Project Guide

> This file provides the project-wide context, architecture direction, UI/UX language,
> coding conventions, and AI-agent rules for the Desi Dhaba AI Restaurant repository.
>
> This project is built using a spec-driven development workflow:
>
> **Requirement → Spec → Plan → Build → Verify**
>
> The feature specification and implementation plan define feature-level details.
> This file defines stable project-wide rules and design direction.

---

## 1. Project Overview

**Desi Dhaba AI Restaurant** is a conversational AI restaurant ordering application.
A user interacts with an AI restaurant assistant, selects dishes and quantities from
an Indian menu, and moves through a realistic restaurant workflow.

### Purpose

The project is primarily a learning project for understanding **LangGraph and
stateful AI-agent workflows** through a realistic, user-facing application.

The application should demonstrate that an LLM agent can operate inside a controlled
workflow instead of behaving like a free-form chatbot.

### Target Users

- Restaurant customers interacting with the AI ordering assistant.
- Developers learning LangGraph, agent workflows, state management, and conditional
  graph execution.

### Core Capabilities

- Conversational restaurant ordering.
- Indian menu with dish, price, and available quantity.
- Order validation before an order enters the kitchen.
- `take_order → cook_order → serve_order → generate_bill` workflow.
- Conditional routing and retry loops using LangGraph.
- Maximum three invalid/off-topic ordering attempts before ending the conversation.
- Simulated cooking failures that can send the order back to dish selection.
- Simulated serving failures that can send the order back to cooking.
- Order status updates shown in the UI.
- Final bill/order summary.
- Polite handling of non-restaurant questions.

---

## 2. Tech Stack

Document the actual technologies used by the project. The initial project direction is:

- **Frontend Framework**: React
- **Styling**: Tailwind CSS
- **Backend Language / Runtime**: Python
- **Backend Framework**: FastAPI
- **AI Workflow Framework**: LangGraph
- **LLM**: Determined by the feature specification/configuration; never hard-code
  an LLM provider in project-wide architecture unless required.
- **Database**: Not required for the initial learning version. Use an appropriate
  persistent database only when a specification explicitly requires it.
- **Testing**: Pytest for backend/agent logic; frontend test tooling should be
  introduced only when required by the project plan.
- **Package Management**: Follow the package manager selected by the repository
  setup. Do not invent commands.
- **Other Important Technologies**:
  - LangChain/LangGraph ecosystem — AI workflow and state orchestration.
  - HTTP/JSON API — communication between React and Python backend.

> Only document technologies actually used by the implementation.
> If the repository changes technology, update this section after the decision is
> made through the project workflow.

---

## 3. Directory & Folder Structure

The exact repository structure is established during project initialization and must
remain synchronized with the implementation.

A preferred separation is:

```text
desi-dhaba-ai/
├── frontend/              # React application and UI
├── backend/               # Python application
│   ├── app/               # API and application modules
│   ├── graph/             # LangGraph workflow
│   ├── models/            # State/domain models
│   ├── services/          # Business/AI support services
│   └── tests/             # Backend and graph tests
├── specs/                 # Feature specifications
├── plans/                 # Implementation plans
├── docs/                  # Stable project documentation
├── .env.example           # Example environment configuration
├── GEMINI.md              # Project-wide AI/developer instructions
└── README.md              # Project setup and usage documentation
```

> This is a recommended logical structure, not permission to create every directory
> immediately. Follow the current repository and the active implementation plan.

### Important Directories

- `frontend/` — owns the customer-facing restaurant UI.
- `backend/` — owns API endpoints and server-side application logic.
- `backend/graph/` — owns LangGraph nodes, edges, routing, and graph state.
- `specs/` — owns feature requirements and acceptance criteria.
- `plans/` — owns step-by-step implementation plans.
- `docs/` — owns stable documentation that is not feature-specific.

---

## 4. Common Commands & Workflows

Commands must be taken from the actual repository configuration.

### Setup

Follow the setup instructions documented in `README.md`.

### Install Dependencies

Use the package manager configured by the repository.

### Development

Run the frontend and backend using the commands defined by the repository.

### Production Build

Use the actual frontend build command configured in the project.

### Run Tests

Backend/graph tests should be executable through the configured Python test command,
normally Pytest when Pytest is present.

### Lint / Format / Type Check

Use only tools that are actually configured in the repository.

> Do not invent commands. Verify them against repository configuration before using
> or documenting them.

---

## 5. Architecture & Design Patterns

The application is a **stateful workflow**, not simply an LLM chat wrapper.

### Frontend Boundary

React owns:

- Chat interface.
- Menu presentation.
- Order/cart presentation when implemented.
- Order status visualization.
- Bill/order summary.
- Loading, error, and empty states.
- User interaction and API communication.

The frontend must not contain the authoritative restaurant workflow logic.

### Backend/API Boundary

FastAPI owns:

- HTTP API endpoints.
- Request/response validation.
- Session/conversation handoff to the graph.
- Backend error handling.
- Communication between the UI and LangGraph.

### LangGraph Boundary

LangGraph owns the restaurant workflow and state transitions.

The graph should conceptually support:

```text
START
  ↓
Understand / Validate User Input
  ↓
Order Valid?
  ├── No → Increment Invalid Attempt → Retry or END
  │
  └── Yes
        ↓
    take_order
        ↓
    cook_order
        ├── Failure → Select Another Dish → take_order
        │
        └── Success
              ↓
          serve_order
              ├── Failure → cook_order
              │
              └── Success
                    ↓
              More Items?
                ├── Yes → take_order
                └── No → generate_bill → END
```

The exact graph topology is defined by the active specification and plan.

### Data Flow

```text
React UI
   ↓
FastAPI
   ↓
LangGraph
   ↓
Restaurant State + Menu/Services
   ↓
Response
   ↓
React UI
```

### Important Architectural Rules

- Keep restaurant business rules deterministic where possible.
- The LLM may interpret natural language, but it must not bypass workflow rules.
- Menu availability and quantity validation must be enforced by application logic.
- Graph routing must be explicit and testable.
- Nodes should have focused responsibilities.
- Do not hide major workflow transitions inside giant node functions.
- Keep graph state explicit.
- Avoid putting UI concerns inside LangGraph nodes.
- Avoid putting LangGraph/business logic inside React components.
- Do not introduce microservices for this learning project unless a specification
  explicitly requires them.
- Do not add Redis, Kafka, Docker orchestration, API gateways, or other infrastructure
  merely for complexity. Add them only when they serve a defined learning goal or
  requirement.

---

## 6. Data & Storage

### Menu Data

The initial menu represents Indian dishes and should contain at minimum:

- Dish name.
- Price.
- Available quantity.

Example conceptual data:

```text
Butter Chicken → ₹350 → 5 available
Paneer Tikka   → ₹250 → 8 available
Biryani        → ₹220 → 10 available
Dal Makhani    → ₹180 → 6 available
```

These values are examples for understanding the domain. The authoritative menu belongs
to the implementation/specification.

### Restaurant State

The graph state may contain information such as:

- Current user message.
- Selected dish/dishes.
- Requested quantity.
- Validity of the current request.
- Current order.
- Invalid/order attempt count.
- Cooking status.
- Serving status.
- Bill/total.
- Current workflow status.

The exact state schema is defined by the feature specification.

### External Services

LLM/provider configuration is external configuration and must never be committed
as a secret.

### Important Data Rules

- Never trust user-provided price or availability values.
- Validate dish names and quantities against authoritative menu data.
- Do not expose internal graph state unnecessarily to the client.
- Do not commit API keys or credentials.
- Keep domain data separate from presentation data.

---

## 7. Authentication & Authorization

Authentication is **not required for the initial learning version** unless a later
specification explicitly introduces accounts.

If authentication is later introduced:

- Keep authentication concerns separate from restaurant workflow logic.
- Never put credentials or tokens into source control.
- Define ownership and session rules in the relevant specification before implementation.

---

## 8. UI & Design Conventions

The UI should follow the visual direction established for the Desi Dhaba concept:
**modern, premium, warm, conversational, Indian-food-inspired, and easy to use.**

The generated UI reference is the visual direction for the project, not a pixel-perfect
implementation requirement. Recreate its design language rather than blindly copying
every element.

### Visual Language

The visual identity should feel like a modern premium Indian restaurant rather than
a generic AI chatbot.

Key characteristics:

- Dark, rich base surfaces.
- Warm orange/peach accent color.
- Cream/off-white text and surfaces where appropriate.
- High-quality Indian food imagery.
- Large rounded cards.
- Soft shadows and subtle borders.
- Strong visual hierarchy.
- Generous spacing.
- Friendly chef/restaurant assistant personality.
- Subtle animations rather than excessive motion.
- Premium but approachable appearance.

### Color Direction

Use design tokens/CSS variables instead of scattered hard-coded colors.

Recommended semantic roles:

| Role | Direction |
|---|---|
| Background | Deep charcoal / near-black |
| Surface | Slightly lighter charcoal |
| Primary Accent | Warm saffron/orange |
| Accent Hover | Slightly brighter warm orange |
| Primary Text | Warm white / cream |
| Secondary Text | Muted warm gray |
| Success | Soft green |
| Error | Soft red |
| Border | Subtle low-contrast neutral |

Exact color values may be selected during implementation, but the visual relationship
between these roles should remain consistent.

### Typography

Use a modern readable sans-serif for UI text.

Typography should have:

- Strong display typography for hero headings.
- Clear medium/semibold typography for dish names and prices.
- Comfortable body text for chat messages.
- Compact typography for metadata such as quantity and status.
- Good line-height and spacing.

Avoid excessive font families. Prefer one primary family plus an optional display
family only if it materially improves the restaurant identity.

### Core Screens

The UI should be designed around these experiences:

1. **Landing/Home**
   - Desi Dhaba branding.
   - Strong food-focused hero.
   - Short AI ordering explanation.
   - Primary “Start Ordering” CTA.
   - Visual indicators for AI ordering, authentic menu, real-time updates,
     and fast/friendly service.

2. **AI Ordering Chat**
   - Conversational assistant.
   - Clear user/assistant message distinction.
   - Restaurant/chef avatar.
   - Composer at the bottom.
   - Menu access without leaving the ordering flow.
   - Clear confirmation and error states.

3. **Menu**
   - Category/filter chips.
   - Food cards with image, name, price, availability.
   - Quantity controls.
   - Add/order action.
   - Visually clear “X left” availability indicator.

4. **Order Status**
   - Order received.
   - Cooking.
   - Serving.
   - Completed.
   - Friendly status messaging.
   - Failure/retry states should feel intentional rather than like application errors.

5. **Bill / Order Summary**
   - Ordered dishes.
   - Quantities.
   - Item totals.
   - Subtotal/tax when applicable.
   - Final total.
   - Order-again action.

### Layout Patterns

- Desktop-first polished experience with responsive mobile behavior.
- Use a centered max-width content container.
- Prefer card-based sections with consistent radius.
- Keep primary actions visually obvious.
- Use sticky/fixed chat composer where appropriate.
- Menu cards should remain scannable.
- Do not overcrowd the interface.
- Preserve consistent spacing between sections.

### Chat UX

The chat is the heart of the application.

Assistant responses should be visually calm and readable.

Examples of intended interaction style:

```text
Assistant:
Namaste! Welcome to Desi Dhaba.
What would you like to order today?

User:
I want 2 Butter Chicken.

Assistant:
Great choice! Butter Chicken is available.
2 plates will be added to your order.
```

For an unrelated question:

```text
Assistant:
Sorry, I can only help with restaurant orders here.
Please tell me which dish you'd like and the quantity.
```

Do not make refusal messages robotic or aggressive.

### Failure UX

Failures are intentionally part of the LangGraph learning experience.

Examples:

```text
Cooking:
“Sorry! We ran into a kitchen issue while preparing your dish.
Please choose another dish and we'll get it started.”
```

```text
Serving:
“Oops! Your dish couldn't be served successfully.
We're sending it back to the kitchen for another preparation.”
```

Failures should be represented as **workflow states**, not generic red error screens.

### Icons

Use a consistent icon library if one is introduced.

Icons should:

- Support the meaning of an action.
- Have consistent stroke weight.
- Not replace important text.
- Use accessible labels/tooltips where necessary.

### Accessibility

- Maintain readable contrast.
- All interactive controls must be keyboard accessible.
- Buttons must have meaningful labels.
- Images need appropriate alt text.
- Do not communicate status using color alone.
- Chat messages should remain readable with assistive technologies.
- Respect reduced-motion preferences where animations are implemented.

### Motion

Use subtle, purposeful animations:

- Message entrance.
- Button hover/press feedback.
- Order status transitions.
- Loading/cooking indicators.
- Cart quantity changes.

Avoid:

- Excessive bouncing.
- Constant decorative motion.
- Long blocking animations.
- Animation that makes ordering slower.

---

## 9. Coding Standards & Guidelines

### Python

- Follow standard Python conventions and clear naming.
- Prefer small, focused functions.
- Use type hints where practical.
- Keep LangGraph state explicit.
- Keep node functions focused on one workflow responsibility.
- Separate deterministic validation from LLM interpretation.
- Handle expected failures explicitly.
- Avoid broad exception swallowing.

### LangGraph

- Define state clearly.
- Keep nodes small and composable.
- Make conditional routing explicit.
- Use loops intentionally and guard them with counters/conditions.
- Ensure every possible branch has a defined destination.
- Define clear termination conditions.
- Do not create infinite graph loops.
- Keep retry counters in state when the retry limit is part of workflow behavior.
- Make graph behavior testable without depending entirely on an actual LLM response.

### FastAPI

- Keep API routes thin.
- Validate request/response data at the API boundary.
- Delegate business logic to services/graph modules.
- Return predictable response structures.
- Do not place large LangGraph workflows directly inside route handlers.

### React / Frontend

- Use functional components.
- Keep components focused.
- Avoid giant components containing the entire application.
- Separate API/state logic from presentation where practical.
- Prefer reusable UI components.
- Keep loading, success, empty, and failure states explicit.
- Do not duplicate menu/order data across components.
- Never make the frontend the source of truth for menu availability or pricing.

### Styling

- Prefer Tailwind utility classes and reusable design tokens.
- Avoid random one-off styling when an existing token/component can be reused.
- Maintain consistent spacing, radii, typography, and interaction states.
- Do not introduce a component library merely to avoid building a small reusable
  component.

### General Rules

- Keep modules/components/services focused on a clear responsibility.
- Reuse existing utilities, helpers, components, and patterns.
- Do not duplicate existing logic.
- Do not introduce unnecessary dependencies.
- Do not make unrelated changes.
- Preserve existing functionality unless a feature explicitly requires a change.
- Prefer the simplest architecture that satisfies the current specification.

---

## 10. Git Commit Conventions

Use concise conventional commit-style messages when the repository adopts Git commits.

Preferred structure:

```text
<scope>: <short description>
```

Examples:

```text
frontend: build restaurant chat UI
graph: add order validation workflow
graph: add cooking failure loop
backend: add order endpoint
ui: add order status component
test: cover invalid order retries
fix: prevent duplicate order submission
```

---

## 11. Testing Conventions

### Test Structure

Keep backend and graph tests close to the backend test structure established by the
repository.

### What Must Be Tested

At minimum, the workflow should eventually test:

- Valid dish + valid quantity.
- Unknown dish.
- Quantity greater than available quantity.
- Invalid/off-topic request.
- Three invalid/off-topic attempts ending the conversation.
- Successful `take_order`.
- Successful cooking.
- Cooking failure routing back to dish selection.
- Successful serving.
- Serving failure routing back to cooking.
- Multiple-item ordering.
- Bill calculation.
- Correct workflow termination.
- Protection against unintended infinite loops.

### Test Expectations

Graph behavior should be testable deterministically.

Random failure simulation should be controllable during tests rather than making tests
depend on unpredictable randomness.

---

## 12. Environment & Configuration

### Environment Variables

Only document variables that actually exist in the repository.

Typical categories may include:

| Variable | Purpose | Required |
|---|---|---|
| `LLM_API_KEY` | LLM provider authentication | Depends on provider |
| `LLM_MODEL` | Selected model configuration | Depends on implementation |

> Replace these examples with the exact variable names used by the implementation.
> Never put actual secrets in `GEMINI.md`.

### Configuration Rules

- Use environment variables for secrets and environment-specific configuration.
- Maintain `.env.example` without real credentials.
- Never commit API keys.
- Never print secrets in logs.
- Keep model/provider configuration separate from workflow logic.

---

## 13. Protected Files & Areas

Unless explicitly instructed:

- Do not modify feature specifications to make implementation easier.
- Do not modify completed plans retroactively without a clear reason.
- Do not delete tests to make a feature pass.
- Do not remove existing functionality unrelated to the current task.
- Do not overwrite environment files containing secrets.

If no repository-specific protected paths exist yet, preserve the existing structure
and follow the active plan.

---

## 14. Project Invariants

The codebase must never violate these rules:

1. **Menu truth lives on the backend**, not in the frontend.
2. **Price and availability must never be trusted from user input.**
3. **The LangGraph workflow must always have a defined termination path.**
4. **Invalid/off-topic order attempts must be bounded; the initial requirement is
   a maximum of three attempts.**
5. **Cooking and serving failures are workflow branches, not unhandled application
   errors.**
6. **The LLM must not bypass deterministic restaurant rules.**
7. **UI code must not own restaurant business logic.**
8. **Secrets must never be committed.**
9. **Do not introduce infrastructure complexity without a documented requirement.**
10. **Feature-level behavior must come from the active specification and plan.**

---

## 15. Current Project Status

### Current Phase

**Project initialization complete / Ready for specification**

### Current Focus

Building the Desi Dhaba AI Restaurant learning project using spec-driven development.

The intended workflow is:

```text
GEMINI.md
   ↓
Create Spec
   ↓
Create Plan
   ↓
Build
   ↓
Verify
```

The project architecture (React + FastAPI + LangGraph) has been approved. The primary goal is to learn LangGraph basics.
The next step is to create a feature specification for the initial scaffolding and core workflow.

### Known Limitations

- The initial version is a learning project, not a production restaurant platform.
- Cooking and serving failures are intentionally simulated.
- Authentication is not part of the initial core workflow unless explicitly added.
- Real payment processing is outside the initial scope.
- Real kitchen integration is outside the initial scope.

### Established Decisions

- **Architecture:** Full-stack (React + FastAPI) to visualize the agent workflow.
- **LLM Provider:** Gemini (configurable via environment variables).
- **Database:** In-memory state for initial learning, no external DB required yet.

### Important Open Questions

Feature specifications may decide:

- Whether conversation persistence is required beyond in-memory state.
- Whether streaming responses are required.
- Whether real-time transport is HTTP or WebSocket.
- Exact menu categories and dish inventory.

Do not make these decisions silently. Record them in the relevant specification or
plan.

---

## 16. Documentation & Source of Truth

Use the following priority when information conflicts:

1. Explicit user requirements for the current task.
2. This `GEMINI.md` file for project-wide conventions, architecture direction,
   and design language.
3. Existing implementation and tests.
4. Active feature specification.
5. Active implementation plan.
6. Other project documentation.
7. General assumptions.

When information is missing or ambiguous:

- Do not invent behavior.
- Inspect the existing code and documentation.
- If the answer still cannot be determined, state **"Not enough information."**
- Ask the user when clarification is required.

### Spec-Driven Development Rule

Do not jump directly from a vague requirement to implementation.

For meaningful features:

```text
Requirement
    ↓
Specification
    ↓
Implementation Plan
    ↓
Build
    ↓
Verification
```

The specification should describe **what and why**.

The plan should describe **how and in what order**.

Technology-specific implementation details belong primarily in the plan when they
are implementation decisions rather than stable project-wide constraints.

---

## 17. AI Development Rules

AI coding assistants working in this repository must:

- Read this `GEMINI.md` before making architectural or implementation decisions.
- Follow the documented project direction and existing repository structure.
- Reuse established project patterns before introducing new ones.
- Avoid speculative changes.
- Keep changes scoped to the requested feature.
- Read the active specification before implementing a feature.
- Read the active implementation plan before building a planned feature.
- Do not skip required workflow stages merely because the implementation appears simple.
- Validate changes using the project's documented commands.
- Update documentation when architecture, conventions, or stable project decisions change.
- Never expose or commit secrets.
- Never invent undocumented project behavior.
- Do not silently change the product workflow because an implementation is difficult.
- Prefer deterministic, testable logic for business rules.
- Keep LLM responsibilities narrow where deterministic code is more reliable.
- Treat LangGraph state transitions as explicit application behavior.
- Prevent unbounded retries and graph loops.
- Preserve the Desi Dhaba visual language when modifying the frontend.
- Do not replace the restaurant UI with a generic chatbot interface.
- Do not add unnecessary infrastructure solely to make the project appear more
  production-grade.
- When a requirement conflicts with this file, follow the source-of-truth priority
  defined above and document the resulting decision when appropriate.
