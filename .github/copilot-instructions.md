# GitHub Copilot Project Instructions

You are an AI coding assistant working in this project. Follow these rules for ALL code you write and review.

## When Asked to Build Something (Development)

Follow this pipeline automatically:

1. **CONTEXT** — Open and read the file `CLAUDE.md` at the project root (it contains project-specific rules). Detect language, scan project structure, read existing code patterns
2. **PLAN** — Break down the requirement, list files to create/modify, identify test scenarios
3. **IMPLEMENT** — Write production-ready code following project patterns (see Code Quality below)
4. **TEST** — Write scenario-driven tests (see Testing below), run them, fix failures
5. **SELF-REVIEW** — Re-read all code, check for issues (see Review Checklist below), fix them
6. **PRESENT** — Show the user what you built, test results, review report. Wait for approval.
7. **DELIVER** — After approval: create branch `ai/<description>`, commit, push, create PR. Do NOT merge.

## When Asked to Review Code

Check the git diff and run through the Review Checklist below. Output a structured report with APPROVE / REQUEST_CHANGES / COMMENT decision.

## Code Quality Standards

- Type annotations on ALL function signatures
- Documentation on ALL public functions
- No hardcoded values (URLs, ports, timeouts, secrets) — use env vars or config
- No print/console.log/System.out — use proper logging
- No commented-out code — delete it, git has history
- No TODO/FIXME without ticket references
- Specific exception types, never generic Exception/Error
- Never silently swallow errors (no empty catch blocks)
- Timeouts on all external calls
- Input validation on all external boundaries
- Follow existing project patterns (open and read `CLAUDE.md` for project-specific conventions)

## Testing — Scenario-Driven

Tests must prove the requirement works. Every test traces back to a user behavior.

**Choose levels based on what was built:**
- Utility function → Unit tests only
- Service with logic → Unit + error/edge cases
- API endpoint → Unit + integration + security
- Full feature (API + DB) → Unit + integration + security + regression
- Bug fix → Regression test (proves bug is fixed)

**Test rules:**
- Use STRONG assertions (test specific values, not just existence)
- BAD: `assert result is not None` / `expect(result).toBeTruthy()`
- GOOD: `assert result["status"] == "success"` / `expect(result.status).toBe("success")`
- Test error cases (invalid input, service failure, timeout)
- Test edge cases (empty input, boundary values, unicode, very long strings)
- Test security if handling user input (injection, XSS, auth bypass)
- Run existing tests after changes to catch regressions

## Review Checklist (AI Slop Detection)

When reviewing code (yours or the user's), check for:

| Check | Flag if Found |
|-------|--------------|
| Dead code / unused imports | REQUEST_CHANGES |
| Over-engineering / unnecessary abstractions | COMMENT |
| Excessive comments that repeat code | COMMENT |
| Defensive over-validation (checking impossible conditions) | COMMENT |
| Verbose / redundant code | COMMENT |
| Print/console.log/System.out statements | REQUEST_CHANGES |
| Backwards compatibility hacks (_vars, re-exports) | REQUEST_CHANGES |
| Empty catch blocks / silently swallowed errors | REQUEST_CHANGES |
| Secrets or API keys in code | REQUEST_CHANGES |
| Sensitive files committed (.env, credentials) | REQUEST_CHANGES |
| No tests for new code | REQUEST_CHANGES |
| Tests with only weak assertions | REQUEST_CHANGES |
| Missing error/edge case tests | COMMENT |
| Hardcoded configuration values | REQUEST_CHANGES |
| Business logic in wrong layer | REQUEST_CHANGES |

## Decision Matrix

- All checks pass → APPROVE
- 1-2 warnings, no critical → COMMENT
- 3+ warnings or any critical → REQUEST_CHANGES
- Secrets in code → REQUEST_CHANGES (always)

## Git Conventions

- Branch: `ai/<description>` or `feature/<description>`
- Commits: Conventional Commits format (`feat:`, `fix:`, `refactor:`, `test:`, `docs:`)
- Always include: `Co-Authored-By: GitHub Copilot <noreply@github.com>`
- Never force push to main/master
- Never auto-merge PRs — create PR and stop

## Project-Specific Rules

Open and read the file `CLAUDE.md` at the project root. It contains project-specific architecture rules, naming conventions, testing commands, and team standards. Those rules override these defaults. If `CLAUDE.md` does not exist, auto-detect from the codebase.
