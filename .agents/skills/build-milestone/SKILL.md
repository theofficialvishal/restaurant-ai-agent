---
name: build-milestone
description: Build one clearly defined project milestone using the project's approved roadmap, overall specification, implementation plan, GEMINI.md, existing codebase, and the appropriate specialized agent(s).
argument-hint: "Milestone number or name (e.g. 01 or 'Todo Backend')"
allowed-tools: Read, Write, Glob, Grep, Bash
---

# Build Milestone Skill

## Purpose

Build one clearly defined project milestone using the project's approved roadmap, overall specification, implementation plan, `GEMINI.md`, existing codebase, and the appropriate specialized agent(s).

This is an orchestration skill. It does not hardcode a specific technology stack, framework, project structure, or frontend/backend order.

The goal is to keep small and medium projects practical while allowing specialized AI agents to handle different areas of the system.

## Core Principle

Use milestone-based implementation instead of forcing a full Spec -> Plan -> Build cycle for every small feature.

Expected project-level workflow:

initialize-project
-> GEMINI.md
-> create-project-roadmap
-> Overall Specification
-> Overall Implementation Plan
-> build-milestone
-> Manual Testing
-> build-milestone
-> ...
-> finish-feature

A milestone may contain backend work, frontend work, infrastructure work, integration work, or a combination.

## Inputs

Before starting, read and use:

1. GEMINI.md
2. The project roadmap
3. The approved overall specification
4. The approved overall implementation plan
5. Existing relevant source code
6. Relevant project documentation
7. Relevant specialized skills
8. Relevant specialized agents

Do not assume information that is not available in these sources.

## Invocation

Typical usage:

/build-milestone 01

or:

/build-milestone "Todo Backend"

If the milestone cannot be uniquely identified, ask the user to specify which milestone to build.

# Workflow

## Step 1 - Identify the Milestone

Read the roadmap and identify the requested milestone.

Determine:

- Milestone name
- Goal
- Scope
- Prerequisites
- Expected outcome
- Dependencies on previous milestones
- Frontend work
- Backend work
- Database work
- Infrastructure work
- Integration work
- Testing expectations

Do not expand the milestone beyond its approved scope without user approval.

## Step 2 - Inspect Current Project State

Before assigning work:

- Inspect the existing project structure.
- Check which previous milestones are already complete.
- Check existing implementation patterns.
- Check relevant APIs, models, components, services, utilities, and configuration.
- Check whether required dependencies are already installed.
- Reuse existing patterns where appropriate.

Never recreate existing functionality unnecessarily.

## Step 3 - Determine Required Specializations

Analyze the milestone and determine which specialized agents are actually needed.

Possible areas include:

- Backend
- Frontend
- Database
- Infrastructure
- Integration
- Other project-specific specialization agents

Do not invoke an agent simply because it exists.

Only use agents whose specialization is relevant to the milestone.

# Agent Execution Rules

## Backend Specialist

Use the backend specialist when the milestone contains backend/API/server-side work.

Typical responsibilities:

- Server implementation
- API routes
- Controllers/handlers
- Business logic
- Validation
- Authentication/authorization where applicable
- Backend error handling
- Database interaction from the backend
- Backend tests when explicitly included in the milestone

The backend specialist must follow:

- GEMINI.md
- approved specification
- approved implementation plan
- existing backend conventions

## Frontend Specialist

Use the frontend specialist when the milestone contains frontend/UI work.

Typical responsibilities:

- Pages
- Components
- State management
- API integration
- Forms
- Loading/error/empty states
- Responsive behavior
- Accessibility
- Frontend tests when explicitly included in the milestone

For frontend/UI work, the frontend specialist must automatically read and follow:

.agents/skills/frontend-design/SKILL.md

when that skill exists.

The frontend specialist must use the project's documented design system and approved visual reference rather than inventing an unrelated visual direction.

# Execution Order

Do not blindly assume Backend -> Frontend.

Determine the dependency order from the milestone.

### If frontend depends on a new backend contract

Backend Specialist
-> Verify API/contract
-> Frontend Specialist
-> Integration Check

### If backend and frontend are independent

They may be developed independently, but for learning projects prefer sequential execution unless parallel execution provides a clear benefit.

### If the milestone is frontend-only

Frontend Specialist
-> Milestone Verification

### If the milestone is backend-only

Backend Specialist
-> Milestone Verification

### If the milestone is infrastructure-only

Use the appropriate infrastructure specialization if available.

### If the milestone is integration-focused

Use the specialists required by the existing architecture and verify the complete flow after implementation.

# Important: Do Not Over-Parallelize

For beginner or learning projects, prefer sequential specialist execution when one area depends on another.

The purpose is not maximum agent parallelism.

The purpose is:

- Correct implementation
- Clear ownership
- Understandable development flow
- Reusable specialization
- Minimal unnecessary context/token usage

# Before Calling a Specialist

Give the specialist only the context it needs.

At minimum provide:

- Milestone scope
- Relevant requirements from the specification
- Relevant implementation steps from the plan
- Relevant GEMINI.md rules
- Relevant existing code/files
- Dependencies or contracts produced by previous specialists
- Expected completion criteria

Do not unnecessarily dump the entire repository or unrelated specifications/plans into the specialist's context.

# Specialist Responsibilities

Each specialist should:

1. Read the provided project context.
2. Inspect relevant existing code.
3. Implement only the assigned milestone scope.
4. Follow existing project conventions.
5. Reuse existing utilities/components/patterns where appropriate.
6. Avoid unrelated refactoring.
7. Avoid introducing unnecessary dependencies.
8. Keep the implementation consistent with the approved architecture.
9. Validate its own work before reporting completion.
10. Clearly report:
   - What was implemented
   - Files created/changed
   - Important decisions
   - Tests/checks performed
   - Any blockers or remaining work

A specialist must not silently change major architecture decisions.

If the approved specification or plan appears inconsistent with the existing project, stop and surface the conflict instead of making a major architectural decision silently.

# Frontend Design Integration

When frontend work is involved:

Frontend Specialist
-> frontend-design skill
-> Implementation

The frontend implementation must consider:

- GEMINI.md UI/design conventions
- Approved visual reference
- Design tokens
- Existing components
- Responsive requirements
- Accessibility requirements
- Feature-specific UI requirements

The visual reference is a direction, not a literal image-copying instruction.

# Milestone Boundaries

A milestone must not silently become a new project phase.

Do not add unrelated:

- Features
- Authentication systems
- Infrastructure
- Refactors
- Libraries
- Design changes
- Architecture changes

unless they are required by the approved milestone or necessary to make the milestone function correctly.

If an additional change is genuinely required, explain why before expanding scope when the decision is significant.

# Verification After Specialists

After all required specialists complete their work:

1. Inspect the resulting changes.
2. Check that the milestone's expected outcome is achievable.
3. Check that specialists did not modify unrelated areas.
4. Check relevant API contracts and integration points.
5. Run available project checks/tests when appropriate.
6. Confirm no obvious build/runtime errors remain.

This is a lightweight milestone verification step.

It does not require the separate verify-feature or audit-feature workflow.

# Manual Testing

After build-milestone completes, the user should manually test the milestone when practical.

Provide a concise manual testing checklist based on the milestone.

Example:

Milestone Manual Test

[ ] Start application
[ ] Open Todo page
[ ] Create a Todo
[ ] Verify it appears in the list
[ ] Mark Todo complete
[ ] Refresh page
[ ] Verify persisted state
[ ] Delete Todo

Do not create a separate testing ceremony for trivial milestones unless the project specifically requires it.

# Completion Criteria

A milestone is complete only when:

- Its approved scope is implemented.
- Relevant specialists report completion.
- Relevant checks/tests pass or known failures are documented.
- No required dependency remains unfinished.
- The expected outcome from the roadmap is satisfied.
- The implementation remains consistent with GEMINI.md.
- No unrelated feature work was silently added.

# Failure Handling

If a specialist encounters a blocker:

1. Do not blindly continue dependent work.
2. Determine whether the blocker is local and can be safely fixed within the milestone.
3. If it can be fixed safely, fix it and continue.
4. If it requires a major architecture/specification change, stop and report the issue to the user.
5. Do not invent requirements to unblock the implementation.

If a previous milestone is incomplete, report the dependency instead of pretending it is complete.

# Output

At the end, provide a concise milestone report:

## Milestone Complete

Milestone:
<name>

Status:
Completed / Partially Completed / Blocked

Specialists Used:
- Backend Specialist
- Frontend Specialist
- ...

Implemented:
- ...
- ...

Files Changed:
- ...
- ...

Validation:
- ...
- ...

Manual Testing:
- ...

Remaining:
- ...

Keep the report concise. Detailed implementation belongs in the codebase and project documentation.

# What This Skill Must NOT Do

- Do not create a separate spec for every small task.
- Do not create a separate plan for every small task.
- Do not require manual approval after every specialist.
- Do not invoke every available agent.
- Do not hardcode React, Node.js, MongoDB, or any other technology.
- Do not force backend-before-frontend when dependencies do not require it.
- Do not introduce microservices or other complexity without project requirements.
- Do not replace the approved architecture with a new architecture.
- Do not perform unrelated refactoring.
- Do not commit or push code automatically unless the user explicitly asks for it or invokes the dedicated finishing workflow.

# Relationship With Other Skills

### initialize-project

Defines the project foundation and generates the project-specific GEMINI.md.

### create-project-roadmap

Defines milestones and their dependency/order.

### Overall Specification

Defines what the project/milestones should do.

### Overall Implementation Plan

Defines how the approved project should be implemented.

### build-milestone

Orchestrates implementation of one milestone using the appropriate specialists.

### frontend-design

Provides specialized frontend/UI design implementation guidance.

### finish-feature

Handles the final Git commit/push workflow after the user considers the work complete.

# Guiding Principle

Keep the process proportional to the project.

For a small project:

Roadmap
-> Overall Spec
-> Overall Plan
-> Milestone 01 -> Specialist(s)
-> Milestone 02 -> Specialist(s)
-> Milestone 03 -> Specialist(s)
-> Manual Testing
-> Finish

For a larger project, individual milestones may be broken down further when the complexity genuinely requires it.

The workflow should reduce unnecessary documentation and context overhead while preserving clear requirements, specialization, and controlled implementation.
