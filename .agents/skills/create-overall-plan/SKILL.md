---
name: create-overall-plan
description: Create one complete, project-level implementation plan from the approved project specification and roadmap.
argument-hint: "Overall spec path or roadmap path"
allowed-tools: Read, Write, Glob, Grep, Bash
---

# Overall Implementation Plan Skill

## Purpose

Create one complete, project-level implementation plan from the approved project specification and roadmap.

This skill is designed for small and medium projects where creating a separate plan for every small feature would create unnecessary ceremony.

The plan defines **how the approved product will be implemented across milestones**.

It does not replace the specification and must not invent new product requirements.

## When to Use

Use this skill after:

```text
initialize-project
        ↓
GEMINI.md
        ↓
create-project-roadmap
        ↓
create-overall-spec
        ↓
Manual Spec Review
        ↓
create-overall-plan
```

After the plan is manually approved, implementation begins through:

```text
build-milestone
```

## Inputs

Before creating the plan, read:

1. `GEMINI.md`
2. Approved project roadmap
3. Approved overall specification
4. Existing project structure/codebase, if applicable
5. Existing relevant documentation
6. Approved design reference, if applicable

The approved specification is the primary source for product behavior.

The roadmap is the source of truth for milestone order.

Do not invent requirements.

## Core Principle

The plan answers:

> How will we implement the approved requirements?

It should translate the specification into practical engineering work without becoming a second specification.

## Output

Create:

```text
.agents/plans/project-plan.md
```

## Plan Structure

# Project Implementation Plan

## 1. Implementation Strategy

Describe the overall implementation approach and important sequencing decisions.

Keep it concise.

## 2. Architecture Implementation

Explain how the approved architecture will be implemented.

Cover only relevant areas such as:

- Frontend
- Backend
- Database
- API boundaries
- Authentication
- State management
- Infrastructure
- External services

Do not introduce architecture that was not approved.

## 3. Project Structure

Describe the intended project structure.

Use logical folders/modules rather than listing every file that might exist.

Example:

```text
client/
server/
src/
components/
routes/
models/
services/
```

Exact file paths should be included when they materially help implementation.

## 4. Dependency / Package Plan

List required dependencies by area:

| Package | Area | Purpose | Type | Milestone |
|---|---|---|---|---|
| ... | ... | ... | runtime/dev | ... |

Rules:

- Reuse existing dependencies.
- Avoid unnecessary packages.
- Distinguish runtime and development dependencies.
- Do not add packages simply because they are popular.
- Verify compatibility when version information matters.

## 5. Milestone Implementation Plan

Follow the approved roadmap exactly.

For every milestone include:

### Milestone <number> — <name>

**Goal**

What this milestone implements.

**Prerequisites**

Which earlier milestone(s) must be complete.

**Backend**

- Required server/API work
- Relevant modules
- Business logic
- Validation

**Frontend**

- Required pages/components
- State/UI work
- API integration

**Database**

- Models/schema/indexes/migrations as applicable

**Infrastructure**

- Configuration/deployment/container work when applicable

**Integration**

- Contracts and connections between areas

**Specialists**

Identify the specialization(s) likely required:

- Backend Specialist
- Frontend Specialist
- Other project-specific specialist

Do not force every milestone to use every specialist.

**Implementation Order**

Show dependencies, for example:

```text
Backend API
    ↓
API contract verification
    ↓
Frontend integration
```

**Validation**

List checks that should be performed after implementation.

**Expected Outcome**

Describe what should work when the milestone is complete.

## 6. Cross-Milestone Dependencies

Show important dependencies between milestones.

Example:

```text
Database model
    ↓
Backend API
    ↓
Frontend API integration
    ↓
End-to-end user flow
```

This section should clarify why the roadmap order exists.

## 7. Testing Strategy

Define a lightweight testing approach appropriate to the project.

Include relevant levels:

- Unit tests
- Integration tests
- API tests
- Component tests
- E2E tests
- Manual testing

Do not create an unnecessarily heavy testing framework for a small learning project.

Every milestone should have an appropriate validation checkpoint.

## 8. Design Implementation Strategy

For frontend projects, define how the approved design direction will be implemented.

Reference:

- `GEMINI.md`
- approved visual reference
- design tokens
- reusable components
- responsive behavior
- accessibility

Do not redesign the product during planning.

## 9. Environment and Configuration

Define required environment/configuration values without exposing secrets.

Example:

```text
MONGODB_URI=<environment variable>
API_BASE_URL=<environment variable>
```

Never place real credentials in the plan.

## 10. Risk and Dependency Notes

Document only meaningful implementation risks, such as:

- External API dependency
- Authentication complexity
- Data migration
- Browser compatibility
- Integration dependency

Do not over-document trivial risks.

## 11. Milestone Completion Criteria

Define what must be true before moving to the next milestone.

Keep criteria observable and concise.

## Plan Rules

### 1. Respect the Specification

Every implementation task should trace back to an approved requirement or a necessary technical dependency.

### 2. Do Not Invent Product Scope

If the plan requires a product behavior that is missing from the specification:

- identify the gap
- do not silently invent the requirement

### 3. Do Not Over-Plan

The plan should be detailed enough for an AI specialist to implement the work, but not so detailed that it duplicates source code.

Avoid giant code blocks.

### 4. Use Existing Patterns

For an existing project:

- inspect current code
- reuse established conventions
- avoid unnecessary rewrites

### 5. Keep Milestones Independently Buildable

Each milestone should have a clear boundary and expected outcome.

The build-milestone skill will execute one milestone at a time.

### 6. Preserve Architecture

Do not silently introduce:

- New services
- New frameworks
- New databases
- New infrastructure
- Major architectural patterns

unless already approved or required to satisfy an approved requirement.

### 7. Specialist-Friendly

The plan must make it easy for a milestone orchestrator to delegate work.

Clearly distinguish:

```text
Backend work
Frontend work
Database work
Infrastructure work
Integration work
```

so the appropriate specialist can be selected.

## Manual Review Gate

After generating the plan:

1. Save the plan.
2. Summarize the implementation strategy.
3. Highlight major dependencies or decisions.
4. Stop.

The user must manually review and approve the plan before any milestone is built.

Do not automatically invoke `build-milestone`.

## Output

Return a concise summary:

```text
## Overall Implementation Plan Created

File:
.agents/plans/project-plan.md

Covered:
- Architecture implementation
- Project structure
- Dependencies
- Milestone implementation steps
- Specialist assignments
- Integration order
- Testing strategy
- Design implementation
- Configuration
- Completion criteria

Manual Review Required:
Yes

Next Step:
After approval, run:

/build-milestone <milestone-number>
```

## Relationship With Other Skills

```text
initialize-project
        ↓
GEMINI.md
        ↓
create-project-roadmap
        ↓
create-overall-spec
        ↓
create-overall-plan
        ↓
build-milestone
        ↓
Manual Testing
        ↓
finish-feature
```

The specification defines **what**.

The plan defines **how**.

The build-milestone skill decides **which specialist(s) execute each milestone and in what dependency order**.

Specialist agents perform the actual implementation.
