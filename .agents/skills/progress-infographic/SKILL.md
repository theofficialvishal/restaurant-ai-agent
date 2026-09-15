---
name: progress-infographic
description: Convert a project progress-tracker Markdown file into a single-file HTML progress infographic for quickly understanding project status.
argument-hint: "Path to the progress tracker Markdown file"
allowed-tools: Read, Write, Glob
---

# progress-infographic Skill

You are a technical information designer.

Your job is to convert a project's **progress-tracker Markdown file** into a polished, single-file HTML infographic that shows the current project status at a glance.

This is an **optional visualization skill**.

It does not create, maintain, or modify the progress tracker itself. It only visualizes the information already present in the supplied Markdown file.

Do not assume a particular project, language, framework, database, workflow, repository structure, or development methodology.

---

# Input

User input:

$ARGUMENTS

The argument must identify the Markdown file containing the project's current progress/status.

The source may contain information such as:
- current phase
- current goal
- completed work
- work in progress
- next tasks
- open questions
- architecture/design decisions
- blockers
- notes
- milestones
- workflow stages
- test/review status
- other project-status information

Only visualize information that actually exists in the source.

---

# Step 1 — Locate the Progress Tracker

Extract the file path from `$ARGUMENTS`.

Run:

```text
Glob <path>
```

If the file does not exist:

- STOP.
- Tell the user the path could not be found.
- Ask them to confirm the correct path.
- Do NOT guess another file or path.

---

# Step 2 — Read the Source

Read the full Markdown file.

Treat the progress tracker as the **single source of truth** for the infographic.

Extract only information explicitly present in the source.

Identify whichever structures actually exist:

### 1. Current Status
Examples:
- current phase
- current goal
- current feature
- current status
- latest update

### 2. Completion Information
Examples:
- completed items
- completed milestones
- finished workflow stages
- explicitly reported completion percentage

### 3. In-Progress Information
Examples:
- active tasks
- current implementation
- work being reviewed
- partially completed milestones

### 4. Next Up
Examples:
- next tasks
- upcoming milestones
- planned work
- pending actions

### 5. Blockers / Open Questions
Examples:
- blockers
- unresolved questions
- dependencies
- decisions awaiting confirmation

### 6. Decisions / Notes
Examples:
- architecture decisions
- important project decisions
- session notes
- constraints
- important observations

### 7. Workflow / Timeline
If the source contains an actual ordered workflow or timeline, visualize it in that order.

Only create a timeline when the source provides a meaningful order.

### 8. Other Useful Status Information
If meaningful information does not fit the categories above, place it in an appropriate simple section.

If a category is absent, omit it.

Do not invent sections just to make the infographic look complete.

---

# Step 3 — Progress Calculation Rules

Progress must be based only on actual source data.

### If the source explicitly provides a percentage

Use that exact percentage.

### If the source provides clearly countable status items

A completion percentage may be calculated only when:
- the total set of items is clearly defined,
- completed items are clearly identifiable,
- the calculation is meaningful for that set.

If calculated, label it clearly as a **derived value**.

Example:

```text
Progress: 6 / 8 completed
Derived completion: 75%
```

### If progress cannot be calculated reliably

Do not invent a percentage.

Instead show factual status such as:

```text
Completed: 6
In Progress: 1
Pending: 1
```

### Never invent

Never invent:
- percentages
- counts
- dates
- deadlines
- milestones
- completion states
- velocity
- trends
- estimated completion dates
- health scores
- "on track" status
- blockers
- priorities

A visual progress bar, donut, chart, or status badge must represent real source information.

---

# Step 4 — Design Pass

Design the infographic around the actual information in the progress tracker.

Use:
- a deliberate visual hierarchy
- a small, cohesive color system
- clear status distinctions
- responsive layout
- restrained visual decoration

The primary purpose is to answer quickly:

> "Where is the project right now, what is done, what is happening, and what comes next?"

Useful visual elements may include:
- status cards
- progress bars
- completion rings
- workflow timelines
- milestone cards
- blocker cards
- next-task cards
- decision lists

Only use a visual element when the source contains data that supports it.

Do not add charts merely for decoration.

If there are explicit status categories such as completed / in progress / pending / blocked, visually distinguish them.

If there is no meaningful numerical data, prefer status cards and lists over fake charts.

Do not use a generic dashboard template that obscures the actual project information.

---

# Step 5 — Build the HTML

Create exactly one self-contained HTML file.

Requirements:

- Inline `<style>` CSS.
- No external JavaScript dependencies.
- Optional external web fonts are allowed.
- Responsive down to mobile width.
- Semantic HTML with headings, lists, sections, and tables where useful.
- Accessible contrast.
- Visible keyboard focus states if interactive elements exist.
- One scrollable page.
- Fast to scan.
- Concise labels.
- Do not copy large Markdown paragraphs verbatim.
- Preserve the meaning and status of the source.
- Keep important blockers and unresolved items visible.
- Do not hide incomplete work behind overly positive visuals.

The HTML should remain understandable even if the styling fails.

---

# Step 6 — Existing Output Protection

Determine the output slug from the progress tracker's identity/title.

Convert it to lowercase kebab-case.

The default output path is:

```text
.agents/infographics/<slug>-progress.html
```

Before saving, run:

```text
Glob .agents/infographics/<slug>-progress.html
```

If the file already exists:

- STOP.
- Do NOT overwrite it.
- Ask:

> "A progress infographic for '<slug>' already exists. Overwrite it?"

Only overwrite after explicit user confirmation.

---

# Step 7 — Save

Create `.agents/infographics/` if it does not already exist.

Save only to:

```text
.agents/infographics/<slug>-progress.html
```

Do not save the infographic anywhere else.

If saving fails:

- STOP.
- Report the actual error.

---

# Step 8 — Final Report

Print ONLY:

```text
Source: <original progress tracker path>
Infographic: .agents/infographics/<slug>-progress.html
```

Then tell the user:

> Open the HTML file in a browser to view the project progress infographic.

---

# Important Principles

- This skill is optional.
- It does not maintain the progress tracker.
- It does not change project status.
- It does not determine what should be completed next.
- It visualizes the supplied progress information only.
- The progress tracker is the source of truth.
- Never invent project status or metrics.
- Never claim a project is "on track" unless the source explicitly supports that conclusion.
- Never create a fake completion percentage.
- Never create a fake trend from a single snapshot.
- Never turn plans into completed work.
- Never turn "in progress" into "completed".
- Preserve blockers and open questions accurately.
