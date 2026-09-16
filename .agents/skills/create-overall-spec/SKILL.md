---
name: create-overall-spec
description: Create one complete, project-level specification after project initialization and roadmap approval.
argument-hint: "Project name, roadmap path, or requirements context"
allowed-tools: Read, Write, Glob, Grep, Bash
---

# Overall Specification Skill

## Purpose

Create one complete, project-level specification after project initialization and roadmap approval.

This skill is designed for small and medium projects where creating a separate specification for every small feature would add unnecessary documentation overhead.

The specification defines **what the product must do and how it should behave**. It does not define the detailed implementation steps.

## When to Use

Use this skill after:

```text
initialize-project
        ↓
GEMINI.md
        ↓
create-project-roadmap
        ↓
Approved Roadmap
        ↓
create-overall-spec
```

The output becomes the single high-level specification used by the implementation plan and milestone builders.

For large or highly complex projects, individual feature specifications may still be appropriate when the project genuinely requires them.

## Inputs

Before creating the specification, read:

1. `GEMINI.md`
2. Approved project roadmap
3. Existing project requirements/documentation
4. Approved design reference information, if applicable
5. Existing codebase, if this is an existing project

Do not invent requirements.

If important requirements are ambiguous and materially affect the product, ask the user before finalizing them.

## Core Principle

Separate:

### Product Requirements

What the application must provide to users.

### Learning Goals

Technologies or concepts the user wants to practice.

Learning goals should not automatically become product requirements.

If a learning goal affects architecture or implementation, document the resulting decision and its trade-off.

## Specification Structure

Create:

```text
.agents/specs/project-spec.md
```

Use this structure unless the project genuinely needs a different organization:

# Project Specification

## 1. Project Overview

Describe:

- Product purpose
- Target users
- Primary problem being solved
- High-level product scope

## 2. Product Goals

List the intended product outcomes.

## 3. User Roles

Define user types and permissions when applicable.

If there is only one user type, keep this section simple.

## 4. Functional Requirements

Describe the complete product functionality.

For each major capability define:

- Capability
- User interaction
- Expected behavior
- Preconditions
- Success behavior
- Failure behavior
- Important edge cases

Keep requirements implementation-independent unless an implementation detail is necessary to define observable behavior.

## 5. User Flows

Describe important end-to-end user journeys.

Example:

```text
User opens application
    ↓
Creates item
    ↓
Item appears in list
    ↓
User edits item
    ↓
Updated item is displayed
```

## 6. Data Requirements

Define:

- Entities
- Important fields
- Relationships
- Required/optional data
- Data validation requirements
- Persistence expectations

Do not prescribe database implementation details unless already established as a project constraint.

## 7. API / System Behavior

When the project has APIs or service boundaries, describe:

- Required operations
- Inputs
- Outputs
- Validation behavior
- Error behavior
- Authentication/authorization expectations
- Important API contracts

Do not turn this section into an implementation plan.

## 8. Frontend / UI Requirements

Define observable UI behavior:

- Required screens
- Components/features
- Navigation
- Forms
- Loading states
- Empty states
- Error states
- Success feedback
- Responsive behavior
- Accessibility expectations
- Theme behavior where applicable

Use the project's approved visual reference and `GEMINI.md` design conventions.

Do not reproduce the visual reference literally.

## 9. Security Requirements

Only include security requirements relevant to the project.

Examples:

- Authentication
- Authorization
- Input validation
- Sensitive data handling
- Secure cookies/tokens
- Rate limiting
- Access isolation

Do not invent security features solely because they are common.

## 10. Non-Functional Requirements

Include applicable requirements such as:

- Performance
- Reliability
- Accessibility
- Responsiveness
- Maintainability
- Observability

Keep this proportional to project size.

## 11. Acceptance Criteria

Define clear conditions that determine whether the product requirements are satisfied.

Acceptance criteria should be observable and testable.

Example:

```text
Given a valid Todo title,
When the user submits the form,
Then a new Todo is persisted and displayed.
```

## 12. Milestone Mapping

Map requirements to the approved roadmap milestones.

Example:

```text
Milestone 01 → Project foundation
Milestone 02 → Todo API
Milestone 03 → Frontend foundation
Milestone 04 → Todo UI
Milestone 05 → Full-stack integration
```

Do not create new milestones here.

The roadmap is the source of truth for milestone ordering.

## 13. Out of Scope

Explicitly list functionality that is intentionally not part of the current project.

This prevents scope creep during implementation.

## 14. Assumptions and Open Questions

Document:

- Explicit assumptions
- Decisions already approved
- Remaining questions

Do not silently convert an unresolved question into a requirement.

## Specification Rules

### 1. Requirements Before Implementation

The specification should answer:

> What should the system do?

It should not primarily answer:

> Which file should I edit?

File-level implementation details belong in the implementation plan.

### 2. Avoid Technology Duplication

Do not repeat the entire `GEMINI.md` tech stack in every requirement.

Reference established project decisions where appropriate.

### 3. Keep It Complete but Proportional

Cover the complete product scope, but do not create unnecessary enterprise documentation for a small application.

### 4. Preserve Approved Decisions

Do not silently change:

- Product scope
- Architecture
- Technology choices
- Design direction
- Authentication strategy
- Data ownership

If a change appears necessary, surface it to the user.

### 5. No Code Implementation

This skill creates requirements only.

Do not:

- Implement features
- Modify application source code
- Install dependencies
- Change architecture
- Commit or push changes

## Manual Review Gate

After generating the specification:

1. Save the specification.
2. Summarize the major requirements.
3. Identify important assumptions/open questions.
4. Stop.

The user must manually review and approve the specification before the overall implementation plan is created.

## Output

Return a concise summary:

```text
## Overall Specification Created

File:
.agents/specs/project-spec.md

Covered:
- Product requirements
- User flows
- Data requirements
- API behavior
- UI behavior
- Security requirements
- Acceptance criteria
- Milestone mapping
- Out-of-scope items

Manual Review Required:
Yes

Next Step:
After approval, run the overall plan skill.
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
```

The roadmap defines **when/what milestone**.

The specification defines **what the product must do**.

The plan defines **how it will be implemented**.

The build-milestone skill executes the approved plan using appropriate specialists.
