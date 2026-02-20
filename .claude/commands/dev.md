# Automated Development Pipeline

You are an AI development agent. The user gives you a requirement — you build it, test it, review it, and deliver a PR. The ONLY manual step is the user approving your review.

## Flow

```
AUTOMATIC: Context → Plan → Implement → Test → Self-Review
MANUAL:    User reviews and approves
AUTOMATIC: Commit → Push → Create PR
STOP:      PR sits on GitHub for team review and merge
```

## Pipeline

### Stage 1: CONTEXT (Automatic)

Understand the project before writing any code.

**Step 1 — Detect Language:**

Check for these files:

| File Found | Language | Test Runner | Linter |
|------------|----------|-------------|--------|
| `package.json` | JavaScript/TypeScript | jest / vitest / mocha | eslint |
| `tsconfig.json` | TypeScript | jest / vitest | eslint |
| `pyproject.toml` / `requirements.txt` | Python | pytest | ruff / flake8 |
| `pom.xml` | Java (Maven) | JUnit / TestNG | checkstyle / spotbugs |
| `build.gradle` | Java/Kotlin (Gradle) | JUnit | checkstyle |
| `go.mod` | Go | go test | golangci-lint |
| `*.csproj` / `*.sln` | C# (.NET) | xUnit / NUnit / MSTest | roslyn |
| `Cargo.toml` | Rust | cargo test | clippy |

**Step 2 — Read Project:**

- Read `CLAUDE.md` for project-specific rules and architecture
- Read `CONTRIBUTING.md` if it exists
- Read the main entry point file
- Read existing test files to understand testing patterns
- Read package/dependency files for available libraries
- Run `git log --oneline -10` to understand recent work
- Run `git branch -a` to see branch structure
- Detect the default branch (main or master)

**Step 3 — Read Existing Code:**

- If project has < 30 source files: read ALL of them
- If larger: read the top 10 most-imported/referenced files
- Understand: naming conventions, import style, error handling patterns, logging approach
- Understand: directory structure, module organization, API patterns

**Step 4 — Print Context Summary:**

```
=== PROJECT CONTEXT ===
Language:    <detected>
Framework:   <detected>
Structure:   <file count, directory layout>
Patterns:    <naming, imports, error handling>
Tests:       <framework, test directory, existing test count>
Default branch: <main/master>
===
```

### Stage 2: PLAN (Automatic)

**Step 1 — Break down the requirement:**

- What components are needed (models, services, routes, tests, etc.)
- Which existing files to modify vs new files to create
- What dependencies are needed (if any)
- What patterns to follow (from Stage 1 context)

**Step 2 — Print the plan:**

```
=== IMPLEMENTATION PLAN ===

REQUIREMENT: <what the user asked for>
APPROACH:    <technical approach>

FILES TO CREATE:
  1. <path> — <purpose>
  2. <path> — <purpose>

FILES TO MODIFY:
  1. <path> — <what changes>

NEW DEPENDENCIES: <list or "None">

TESTS PLANNED:
  - Unit: <what will be tested>
  - Integration: <what will be tested, or "N/A">
  - Edge cases: <what will be tested>

PATTERNS FOLLOWED:
  - <patterns from project context>
===
```

**Do NOT wait for approval here. Proceed to Stage 3 immediately.**

### Stage 3: IMPLEMENT (Automatic)

Write production-ready code following the project's patterns.

**Rules:**

- Follow naming conventions detected in Stage 1
- Follow import style detected in Stage 1
- Follow error handling patterns detected in Stage 1
- Follow directory structure detected in Stage 1
- Type annotations on ALL function signatures
- Documentation on ALL public functions (docstring / JSDoc / Javadoc / GoDoc)
- No hardcoded values (use env vars or config)
- No print / console.log / System.out (use proper logging)
- No commented-out code
- No TODO/FIXME without ticket references
- Specific exception types, never generic Exception/Error
- Never silently swallow errors (no empty catch blocks)
- Timeouts on all external calls
- Input validation on all external boundaries

**If new dependencies are needed:**

- Python: add to `requirements.txt` or `pyproject.toml`, run `pip install`
- JS/TS: run `npm install <package>`
- Java: add to `pom.xml` or `build.gradle`
- Go: run `go get <package>`
- C#: run `dotnet add package <package>`

### Stage 4: TEST (Automatic — Scenario-Driven)

Tests must prove that **the user's requirement works correctly**. Every test traces back to a specific behavior from the requirement.

**Step 1 — Extract test scenarios FROM the requirement:**

Go back to the user's original requirement. Break it into concrete, testable scenarios.

Example — Requirement: "Add a REST API for managing todos"

```
SCENARIOS DERIVED:
  1. Create a todo with a title → returns 201 + the created todo
  2. List all todos → returns all created todos
  3. Get a single todo by ID → returns the correct todo
  4. Update a todo title → persists the change
  5. Mark a todo as completed → updates the completed flag
  6. Delete a todo → removed, GET returns 404
  7. Create without title → rejected with 422
  8. Get non-existent ID → returns 404
  9. Create with extremely long title → rejected or truncated
  10. Concurrent creates → no data loss or corruption
```

Each scenario = one or more test functions. Every test MUST map to a user behavior.

**Step 2 — Write tests at the appropriate level:**

Choose test levels intelligently based on what was built:

```
What did you build?          → Which test levels apply?
─────────────────────          ──────────────────────────
A utility function           → Unit tests only
A service with business logic → Unit + error/edge cases
An API endpoint              → Unit + integration + security
A data pipeline              → Unit + integration + data validation
A UI component               → Unit + snapshot + accessibility
A full feature (API + DB)    → Unit + integration + security + regression
A bug fix                    → Regression test (proves bug is fixed)
```

**Level 1: Unit Tests** (always — for every new function)

Test individual functions in isolation. Use realistic data from the scenario.

```python
# GOOD — tests the ACTUAL scenario
def test_create_todo_returns_todo_with_id():
    todo = create_todo(title="Buy groceries")
    assert todo.id is not None
    assert todo.title == "Buy groceries"
    assert todo.completed is False

# BAD — generic, proves nothing about the requirement
def test_create_todo():
    result = create_todo(title="test")
    assert result is not None
```

**Level 2: Integration Tests** (when components talk to each other)

Only if the requirement involves multiple components working together.

```python
# Tests the ACTUAL user workflow: create → retrieve → verify
def test_create_and_retrieve_todo(client):
    # Create
    response = client.post("/api/todos", json={"title": "Buy groceries"})
    assert response.status_code == 201
    todo_id = response.json()["id"]

    # Retrieve and verify
    response = client.get(f"/api/todos/{todo_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Buy groceries"
```

**Level 3: Error and Edge Case Tests** (always — for every scenario)

For EACH scenario, ask: "What goes wrong?"

```python
# From scenario 7: "Create without title → rejected"
def test_create_todo_without_title_returns_422(client):
    response = client.post("/api/todos", json={})
    assert response.status_code == 422
    assert "title" in response.json()["detail"][0]["loc"]

# From scenario 8: "Get non-existent → 404"
def test_get_nonexistent_todo_returns_404(client):
    response = client.get("/api/todos/99999")
    assert response.status_code == 404

# Edge: empty string title
def test_create_todo_empty_title_rejected(client):
    response = client.post("/api/todos", json={"title": ""})
    assert response.status_code == 422

# Edge: extremely long title
def test_create_todo_very_long_title(client):
    response = client.post("/api/todos", json={"title": "a" * 10000})
    assert response.status_code in [201, 422]  # either accepts or rejects, doesn't crash

# Edge: special characters
def test_create_todo_unicode_title(client):
    response = client.post("/api/todos", json={"title": "Buy café ☕ naïve résumé"})
    assert response.status_code == 201
    assert response.json()["title"] == "Buy café ☕ naïve résumé"
```

**Level 4: Security Tests** (when handling user input or auth)

Only generate these if the requirement involves:
- User input (APIs, forms, file uploads)
- Authentication or authorization
- Data that could contain injection

```python
# SQL injection attempt
def test_search_todos_sql_injection(client):
    response = client.get("/api/todos?q='; DROP TABLE todos; --")
    assert response.status_code == 200  # doesn't crash, returns empty or safe results

# XSS attempt
def test_create_todo_xss_sanitized(client):
    response = client.post("/api/todos", json={"title": "<script>alert('xss')</script>"})
    assert "<script>" not in response.json().get("title", "")

# Auth bypass
def test_access_without_token_returns_401(client):
    response = client.get("/api/todos", headers={})  # no auth
    assert response.status_code == 401

# Other user's data
def test_cannot_access_other_users_todo(client, user_a_token, user_b_todo_id):
    response = client.get(f"/api/todos/{user_b_todo_id}", headers={"Authorization": user_a_token})
    assert response.status_code == 403
```

**Level 5: Regression Tests** (when modifying existing code)

Only if modifying an existing codebase (not greenfield).

```bash
# Run ALL existing tests BEFORE writing new code (baseline)
# Run ALL existing tests AFTER changes
# If any existing test fails after your changes → it's a regression → fix it
```

- Count existing tests before: X passed
- Count existing tests after: X passed (must be same or more)
- If existing test fails: fix the root cause, not the test

**Level 6: Data Validation Tests** (when storing/transforming data)

Only if the requirement involves data persistence or transformation.

```python
# Data round-trip: create → store → retrieve → compare
def test_todo_data_integrity(client, db):
    client.post("/api/todos", json={"title": "Buy groceries", "priority": 3})

    # Verify in DB directly
    todo = db.query(Todo).first()
    assert todo.title == "Buy groceries"
    assert todo.priority == 3

    # Verify via API
    response = client.get(f"/api/todos/{todo.id}")
    assert response.json()["title"] == "Buy groceries"
    assert response.json()["priority"] == 3
```

**Step 3 — Run ALL tests:**

```bash
# Run existing project tests first (regression check)
# Then run new tests

# Python
python -m pytest tests/ -v --tb=short --cov=. --cov-report=term-missing

# JS/TS
npm test -- --coverage

# Java
mvn test

# Go
go test ./... -v -cover

# C#
dotnet test --verbosity normal --collect:"XPlat Code Coverage"
```

**Step 4 — Verify and report:**

- If any test fails: fix the code (not the test), re-run
- If all pass: proceed to Stage 5
- Target: 80%+ coverage on new code

Print test results mapped back to the requirement:

```
=== TEST RESULTS ===

REQUIREMENT: "Add a REST API for managing todos"

SCENARIOS TESTED:
  [PASS] Create todo with title → 201 returned
  [PASS] List all todos → correct count
  [PASS] Get by ID → correct data
  [PASS] Update title → change persisted
  [PASS] Delete → removed, GET returns 404
  [PASS] Create without title → 422 rejected
  [PASS] Get non-existent → 404
  [PASS] SQL injection → safe
  [PASS] XSS in title → sanitized
  [PASS] Unicode characters → preserved
  [PASS] Data round-trip → no data loss

SUMMARY:
  Unit:        8 tests — PASS
  Integration: 5 tests — PASS
  Edge/Error:  6 tests — PASS
  Security:    3 tests — PASS
  Regression:  12 existing tests — PASS (0 regressions)
  Data:        2 tests — PASS
  Total:       36 passed, 0 failed
  Coverage:    92%
===
```

### Stage 5: SELF-REVIEW (Automatic)

Run the same checks as `/review` against your own code. Act as a senior engineer reviewing a PR.

**Re-read EVERY file you created or modified. Check:**

| Category | What to Check |
|----------|--------------|
| Architecture | Files in correct directories? Separation of concerns? |
| Hardcoded Values | Any URLs, ports, timeouts, secrets hardcoded? |
| Dead Code | Unused imports? Unused variables? Unreachable code? |
| Over-Engineering | Unnecessary abstractions? Pointless wrappers? |
| Comments | Excessive? Obvious? Commented-out code? |
| Print Statements | Any print/console.log/System.out left? |
| Error Handling | Empty catches? Generic exceptions? Silent failures? |
| Test Quality | Weak assertions? Missing error cases? Missing edge cases? |
| Type Safety | Missing type hints? Using `any`? Nullable not handled? |
| Security | Secrets in code? PII in logs? Injection risks? |
| Logging | Using proper logger? Correct levels? Context included? |

**For each issue found: fix it immediately.**

**After fixing, generate the review report:**

```
=== SELF-REVIEW ===

FILES CREATED: <count>
  <path> (<lines> lines) — <purpose>

FILES MODIFIED: <count>
  <path> — <what changed>

TESTS: <passed>/<total> passed | Coverage: <X>%

REVIEW:
  | Category         | Status | Details |
  |------------------|--------|---------|
  | Architecture     | PASS   |         |
  | Hardcoded Values | PASS   |         |
  | Dead Code        | PASS   |         |
  | Over-Engineering | PASS   |         |
  | Print Statements | PASS   |         |
  | Error Handling   | PASS   |         |
  | Test Quality     | PASS   |         |
  | Type Safety      | PASS   |         |
  | Security         | PASS   |         |
  | Logging          | PASS   |         |

IMPROVEMENTS APPLIED: <count>
  1. <what was fixed>
  2. <what was fixed>

=== READY FOR YOUR REVIEW ===
```

### ---- STOP HERE — WAIT FOR USER APPROVAL ----

This is the ONLY manual step. Print:

```
Everything above is what I built and reviewed.
Please review the code and the self-review report.

Reply:
  "approve" — I will commit, push, and create a PR for team review
  "changes" — tell me what to change, I will fix and re-review
```

**Wait for user response.**

- If user says "approve" or "yes" or "looks good" → proceed to Stage 6
- If user gives feedback → apply changes, re-run Stage 4 + 5, ask again

### Stage 6: DELIVER (Automatic — runs after user approval)

**Step 1 — Create branch:**

```bash
# Detect default branch
DEFAULT_BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "main")
git checkout -b ai/<short-description>
```

**Step 2 — Stage and commit:**

Stage specific files (never `git add -A`):

```bash
git add <file1> <file2> <file3> ...

git commit -m "$(cat <<'EOF'
feat: <description of what was built>

- <bullet point 1>
- <bullet point 2>
- <bullet point 3>

Co-Authored-By: Claude Code <noreply@anthropic.com>
EOF
)"
```

Use the correct commit type:
- `feat:` for new features
- `fix:` for bug fixes
- `refactor:` for refactoring
- `test:` for test-only changes
- `docs:` for documentation-only changes

**Step 3 — Push:**

```bash
git push -u origin ai/<short-description>
```

**Step 4 — Create PR:**

```bash
gh pr create --title "<type>: <description>" --body "$(cat <<'EOF'
## Summary
<what was built and why — 2-3 bullet points>

## Changes
<list of files changed with one-line descriptions>

## Tests
- Tests: <passed>/<total> passed
- Coverage: <X>% on new code
- Test types: unit, integration, edge cases

## Self-Review
All 10 quality checks passed. See details in commit.

Generated with **Claude Code**
EOF
)"
```

**Step 5 — Print completion:**

```
=== PR CREATED ===

Requirement: <what was asked>
Branch:      ai/<description>
PR:          <PR URL>
Status:      OPEN — ready for team review

Files delivered:
  <path> (<lines> lines) — <purpose>
  <path> (<lines> lines) — <purpose>

Tests: <passed>/<total> | Coverage: <X>%
Self-Review: All checks passed

Next: Team reviews the PR on GitHub and merges to main.
===
```

**IMPORTANT: Do NOT merge the PR. Do NOT run `gh pr merge`. The PR stays open for the team to review and merge on GitHub.**

## Summary of What's Automatic vs Manual

```
AUTOMATIC    Stage 1: Read project context
AUTOMATIC    Stage 2: Plan implementation
AUTOMATIC    Stage 3: Write code
AUTOMATIC    Stage 4: Write and run tests
AUTOMATIC    Stage 5: Self-review and fix issues
--------------------------------------------
MANUAL       User reviews and says "approve"
--------------------------------------------
AUTOMATIC    Stage 6: Commit
AUTOMATIC           Push
AUTOMATIC           Create PR
STOP         PR sits on GitHub for team review and merge
```

## Reference Documents

- `CLAUDE.md` — Project-specific rules (read first)
- `.claude/agents/code-writer.md` — Code writing patterns
- `.claude/agents/code-reviewer.md` — Review standards
- `.claude/commands/review.md` — Review checklist details
