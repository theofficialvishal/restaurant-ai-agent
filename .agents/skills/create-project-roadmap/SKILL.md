---
name: create-project-roadmap
description: Create a step-by-step project build roadmap that breaks an entire project into dependency-ordered implementation sessions, with one feature or milestone per session and a project-specific package/dependency plan.
argument-hint: "Project name, GEMINI.md path, requirements, or project context"
allowed-tools: Read, Write, Glob, Grep, Bash
---

# create-project-roadmap Skill

You are a project delivery-roadmap planner.

Your job is to transform an approved project foundation into a practical, dependency-ordered sequence for completing the entire project.

The roadmap must help the developer understand:

- What gets built first
- What gets built next
- Why that order makes sense
- What each session/feature delivers
- Which frontend, backend, database, infrastructure, authentication, testing, and deployment work belongs to each session
- Which npm/packages/dependencies are required for each stage
- Which packages are already installed versus newly required
- What must be completed before the next session can begin

The roadmap is a planning artifact. It does not implement the project.

This skill is universal and must not assume React, Node.js, MongoDB, npm, microservices, Redis, Docker, or any other specific technology.

---

# Core Principle

Use:

> 1 Session = 1 Feature or 1 Clearly Bounded Technical Milestone

A session should produce a meaningful, testable increment of the project.

Do not create a roadmap where one session contains an entire subsystem with many unrelated features.

Do not split tiny implementation details into separate sessions unless doing so materially improves learning or dependency management.

The roadmap should follow the natural way a real project is built:

```text
Foundation
    ↓
Data / Domain
    ↓
Backend capabilities
    ↓
Frontend capabilities
    ↓
Integration
    ↓
Authentication / Authorization
    ↓
Caching / Infrastructure
    ↓
Advanced capabilities
    ↓
Testing / Security / Quality
    ↓
Deployment / Production readiness
```

Adapt this sequence to the actual project.

---

# Step 1 — Read Project Context

Read the available project context:

1. `GEMINI.md`
2. Approved project architecture
3. Project requirements
4. Learning goals
5. Approved frontend design direction
6. Existing repository structure, if applicable
7. Existing package/dependency manifests
8. Existing specifications/plans, if applicable

If `GEMINI.md` is missing and the project context is insufficient, ask the user to initialize the project first or provide the required context.

Do not invent project architecture.

---

# Step 2 — Identify the Complete Scope

Create a scope inventory.

Consider applicable areas:

## Project Foundation

- Repository setup
- Frontend setup
- Backend setup
- Service structure
- Environment configuration
- Shared configuration
- Development scripts
- Docker/local infrastructure

## Database

- Database setup
- Connection
- Schema/models
- Indexes
- Migrations when applicable
- Seed data when applicable

## Backend

- Server/bootstrap
- Health checks
- API conventions
- Domain/service layer
- Validation
- Error handling
- CRUD/API features
- Service-to-service communication

## Frontend

- App shell
- Routing
- Design system/tokens
- Shared components
- Layout
- Feature UI
- Loading/error/empty states
- Responsive behavior
- Accessibility

## Authentication & Authorization

- Registration
- Login
- Logout
- JWT/session handling
- OAuth/Google authentication when applicable
- Authorization
- Resource ownership
- Protected routes
- Service authentication

## Infrastructure

- Redis
- Cache strategy
- Session management
- API Gateway
- Load Balancer
- Docker
- Docker Compose
- Networking
- Health checks
- Scaling
- Observability

Only include components that are actually part of the approved project.

If a technology exists primarily as a learning goal, identify it as such and explain where it will be practiced.

## Testing & Quality

- Unit tests
- Integration tests
- API tests
- Frontend tests
- End-to-end tests when appropriate
- Security review
- Quality review

## Deployment

- Production build
- Containerization
- Environment configuration
- Deployment
- Production verification
- Operational documentation

## AI / MCP

If applicable:

- MCP server setup
- MCP tools/resources
- AI integration
- Permissions/security
- Tool testing

---

# Step 3 — Build Dependency Graph

Before assigning session numbers, determine dependencies.

For each major capability ask:

- What must exist before this can be implemented?
- Does it depend on the database?
- Does it depend on authentication?
- Does it depend on another service?
- Does it depend on frontend components?
- Does it depend on Redis/infrastructure?
- Does it depend on another feature?
- Can it be tested independently?

Then order the sessions accordingly.

Example:

```text
01 Project Foundation
        ↓
02 Database Connection
        ↓
03 Todo Data Model
        ↓
04 Create Todo API
        ↓
05 Todo List API
        ↓
06 React App Shell
        ↓
07 Create Todo UI
        ↓
08 Todo List UI
        ↓
09 Frontend + Backend Integration
```

Do not blindly follow this example. Derive the actual dependency order from the project.

---

# Step 4 — Decide Session Boundaries

For every roadmap item define:

- Session number
- Feature/milestone name
- Goal
- Why it comes at this point
- Prerequisites
- Scope
- Expected outcome
- Main files/modules/services likely involved
- Testing expectation
- Packages/dependencies required
- Whether a new infrastructure component is introduced

Prefer feature-oriented sessions once the project foundation is ready.

Example:

```text
Session 07 — Create Todo

Goal:
Allow authenticated users to create a todo.

Prerequisites:
- Database
- Todo model
- Authentication
- POST API

Frontend:
- Todo form
- Validation
- Loading/error states

Backend:
- POST /todos
- Request validation
- Authorization
- Persistence

Packages:
- Already installed: ...
- New packages: ...

Outcome:
A user can create a todo from the UI and see the persisted result.
```

---

# Step 5 — Package & Dependency Plan

Create a project-specific dependency inventory.

For JavaScript/TypeScript projects, include applicable packages from:

- Frontend
- Backend
- Shared packages
- Testing
- Development tooling
- Infrastructure tooling

For each dependency document:

| Package | Workspace/Service | Purpose | Dependency Type | Introduced In |
|---|---|---|---|---|
| ... | ... | ... | runtime/dev | Session 01 |

Use the actual package manager from `GEMINI.md`.

Important rules:

- Do not add packages merely because they are popular.
- Prefer the smallest reasonable dependency set.
- Reuse packages already present when appropriate.
- Do not introduce two packages for the same responsibility without justification.
- Distinguish runtime dependencies from development dependencies.
- Distinguish global/system tools from project packages.
- Do not claim a package is required when the platform/framework already provides the capability.
- Consider compatibility between package versions and the approved runtime/framework.
- When current package/version information matters, verify it using authoritative/current sources rather than guessing.
- If a package decision is uncertain, mark it as a decision requiring review.

For non-JavaScript projects, document equivalent dependencies in the ecosystem's normal dependency format.

---

# Step 6 — Learning Progression

Because the roadmap may be used as a learning plan, explicitly identify what each session teaches.

Example:

```text
Session 01
Learning:
- Project structure
- Environment configuration

Session 02
Learning:
- Database connection
- Schema design

Session 03
Learning:
- REST API
- Controller/service separation

Session 04
Learning:
- React state
- API integration

Session 05
Learning:
- Redis cache-aside pattern
- TTL
- Cache invalidation
```

Do not turn the roadmap into a tutorial. Keep the explanation concise and practical.

The roadmap should make the overall project-building flow memorable.

---

# Step 7 — Testing Checkpoint for Every Session

Every session must define a verification checkpoint.

At minimum:

- What should work after this session?
- What should be tested?
- What should be manually verified?

The implementation workflow remains:

```text
Session
  ↓
/create-spec
  ↓
Manual Spec Review
  ↓
/create-plan
  ↓
Manual Plan Review
  ↓
/build
  ↓
/verify-feature
  ↓
/audit-feature
  ↓
/finish-feature
```

The roadmap should reference this workflow rather than replacing it.

Do not create a separate spec/plan/build process inside the roadmap skill.

---

# Step 8 — Handle Infrastructure Progression Carefully

Infrastructure should be introduced when it provides a meaningful learning or product milestone.

For example, if Redis is part of the approved architecture:

```text
First:
Database-backed feature works.

Then:
Redis introduced.

Then:
Cache strategy implemented.

Then:
Cache invalidation tested.

Then:
Failure fallback verified.
```

Do not add Redis before there is a meaningful operation to cache unless the learning goal specifically requires an earlier infrastructure session.

Similarly, for a load balancer:

```text
Single service instance
        ↓
Containerized service
        ↓
Multiple instances
        ↓
Load balancer
        ↓
Health checks
        ↓
Failure/scaling validation
```

For API Gateway:

```text
Individual service APIs
        ↓
Gateway introduced
        ↓
Routing
        ↓
Authentication boundary
        ↓
Rate limiting / policies when applicable
```

Adapt to the actual architecture.

---

# Step 9 — Authentication Progression

If authentication is part of the project, order it according to actual dependencies.

A common progression may be:

```text
User model
    ↓
Registration
    ↓
Password handling
    ↓
Login
    ↓
JWT/session issuance
    ↓
Protected API
    ↓
Frontend auth state
    ↓
Authorization / ownership
    ↓
Google OAuth
```

Do not force this exact sequence if the architecture requires another order.

If JWT and Google OAuth are included primarily for learning, explicitly identify the learning purpose.

---

# Step 10 — Frontend Progression

Use the approved visual foundation from `GEMINI.md`.

Do not create a separate frontend roadmap unless the project genuinely requires one.

The project roadmap should include frontend work alongside backend work.

For each frontend session, consider:

- Layout
- Components
- Design tokens
- Typography
- Responsive behavior
- Loading states
- Empty states
- Error states
- Accessibility
- Motion/animation
- Mobile behavior

The roadmap should identify when the core UI foundation is created versus when feature-specific UI is implemented.

---

# Step 11 — Produce the Roadmap Document

Create:

```text
.agents/
└── roadmap/
    └── project-roadmap.md
```

If the directory does not exist, create it.

Use this structure:

```md
# [Project Name] — Project Roadmap

## Project Goal

[Short description]

## Approved Architecture

[High-level architecture diagram]

## Learning Goals

- ...

## Build Strategy

1 Session = 1 Feature or Clearly Bounded Milestone

## Session Roadmap

### 01 — [Name]

**Goal:** ...

**Why now:** ...

**Prerequisites:** ...

**Frontend:** ...

**Backend:** ...

**Database:** ...

**Infrastructure:** ...

**Packages:** ...

**Testing:** ...

**Learning:** ...

**Expected outcome:** ...

---

### 02 — [Name]

...

## Package / Dependency Inventory

| Package | Workspace/Service | Purpose | Type | Introduced |
|---|---|---|---|---|

## Infrastructure Progression

[Short explanation]

## Authentication Progression

[Short explanation]

## Frontend Progression

[Short explanation]

## Completion Criteria

The project is considered complete when:

- ...
- ...
- ...
```

---

# Step 12 — Roadmap Quality Rules

The final roadmap must:

- Start from the approved architecture.
- Be dependency ordered.
- Be understandable without reading the entire codebase.
- Use one-session-one-feature/milestone progression.
- Include package/dependency information.
- Explain why major steps occur in that order.
- Include frontend and backend work together where they belong to one feature.
- Include testing checkpoints.
- Include infrastructure progression.
- Reflect explicit learning goals.
- Avoid unrelated work.
- Avoid premature optimization.
- Avoid unnecessary packages.
- Avoid unnecessary microservices.
- Avoid invented requirements.
- Avoid invented package requirements.
- Avoid invented package versions.
- Avoid invented infrastructure.
- Clearly identify assumptions and decisions requiring approval.

---

# Step 13 — Final Summary

After creating the roadmap, report:

## Roadmap Created

Path to the roadmap.

## Total Sessions

Give the actual number of roadmap sessions.

Do not invent or estimate the count.

## Major Learning Areas

List the major engineering concepts covered.

## Dependency Highlights

Mention important package/infrastructure introductions.

## First Session

State exactly what Session 01 will accomplish.

Do not start implementing Session 01 automatically.

---

# Important Rules

- This skill creates the project roadmap; it does not implement features.
- The roadmap is project-specific, while this skill itself is universal.
- One session should produce one meaningful, testable increment.
- Do not force every technology into the roadmap.
- Distinguish product requirements from learning goals.
- Major architectural decisions must already be approved before creating the roadmap.
- Do not silently change the approved architecture.
- Do not invent packages, package versions, commands, infrastructure, requirements, or implementation details.
- Verify current package information when current compatibility/version details matter.
- Prefer simple dependency graphs and clear learning progression.
- Keep package selection minimal and justified.
- Feature specifications remain the source of truth for feature requirements.
- Implementation plans remain the source of truth for exact implementation steps.
- `GEMINI.md` remains the source of truth for stable project-wide architecture, technology, design, and conventions.
- The roadmap describes the order in which the project will be built; it does not replace the existing spec-driven workflow.
