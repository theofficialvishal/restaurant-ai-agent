---
name: finish-feature
description: Safely finalize a completed feature by validating the Git state, committing the intended changes, and pushing the current feature branch.
argument-hint: "Commit message (e.g. add login and logout functionality)"
allowed-tools: Bash(git:*)
---

# finish-feature Skill

You are responsible for safely finalizing a completed feature branch.

Your job is to:
1. verify that the work is on a feature/non-protected branch,
2. inspect the working tree,
3. stage the intended changes,
4. create a commit using the user's message,
5. push the current branch to its configured remote,
6. report the result.

Do not merge branches, create pull requests, or switch branches.

Do not assume a particular project, language, framework, package manager, or Git hosting provider.

---

# Step 1 — Validate Commit Message

Read `$ARGUMENTS` as the commit message.

If no commit message is supplied:

STOP.

Ask the user for a commit message.

Do not invent one.

---

# Step 2 — Verify Current Branch

Run:

```bash
git branch --show-current
```

Store the current branch name.

If the current branch is a protected/default branch such as:
- `main`
- `master`

STOP.

Tell the user:

> Never commit feature work directly to the protected/default branch. Switch to the intended feature branch first.

Do not switch branches automatically.

If the repository uses a different protected branch name, respect the project's documented Git workflow when that information is available. Do not guess a branch name that is not supported by the project context.

---

# Step 3 — Inspect Working Tree

Run:

```bash
git status
```

Review the result before staging anything.

If there are no modified, staged, or untracked files:

STOP.

Tell the user:

> There are no changes to commit.

Do not create an empty commit.

Before staging, identify whether there are clearly unrelated changes that should not be included.

Never silently discard or overwrite user changes.

---

# Step 4 — Stage Changes

Stage the intended completed feature changes.

Prefer:

```bash
git add .
```

only when the working tree is clearly scoped to the feature and there are no unrelated changes.

If unrelated changes are present or the scope is ambiguous:
- STOP rather than staging everything blindly.
- Tell the user which situation needs clarification.

Do not use destructive Git commands such as `git reset --hard`, `git clean`, checkout/discard commands, or anything else that can remove user work.

---

# Step 5 — Verify Staged Changes

Run:

```bash
git status
git diff --cached
```

Inspect the staged diff.

Confirm that:
- the intended feature changes are staged,
- unrelated or sensitive files were not accidentally staged,
- no obvious secrets or credentials are being committed,
- the staged changes match the completed feature scope.

If the staged content is clearly unsafe or unrelated:

STOP and report the issue.

Do not automatically rewrite or discard the user's changes.

---

# Step 6 — Commit

Create the commit using the exact user-supplied message:

```bash
git commit -m "$ARGUMENTS"
```

If the commit fails:
- STOP.
- Report the actual Git error.
- Do not pretend the commit succeeded.
- Do not automatically bypass hooks, signing requirements, or repository policies.

---

# Step 7 — Push

Determine the current branch again:

```bash
git branch --show-current
```

Push it to its configured `origin` remote:

```bash
git push origin <current_branch>
```

Do not use force push.

If the branch has no upstream or the push requires an unusual configuration:
- report the actual Git error,
- do not invent remote configuration,
- do not force-push.

If the push fails, clearly distinguish:
- commit succeeded
- push failed

Do not claim the feature was successfully pushed unless Git confirms success.

---

# Step 8 — Final Report

If both commit and push succeed, print:

```text
Current branch: <current_branch>
Commit message: <commit_message>
Status: Successfully committed and pushed to origin.
```

If commit succeeds but push fails, report that exact state and include the Git error.

If an earlier validation stops the workflow, report why it stopped.

Do not:
- merge branches,
- create pull requests,
- switch branches,
- delete branches,
- force-push,
- modify application/source files,
- discard user changes.

The feature branch is ready for the next repository workflow step once the push succeeds.
