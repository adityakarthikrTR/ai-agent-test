# How to Use the `/review` Command

The `/review` command performs a comprehensive code review BEFORE you commit or create a PR. It catches issues early so you spend less time in PR review cycles.

## What It Checks

| Check | What It Catches |
|-------|----------------|
| Architecture Compliance | Wrong layer separation, hardcoded config, circular deps |
| AI Slop Detection | Dead code, over-engineering, verbose code, print statements, empty catches |
| Test Quality | Weak assertions, missing error/edge cases, no revert coverage |
| Security | Secrets in code, sensitive files, PII in logs |
| Best Practices | Missing types, missing docs, commented-out code |

## When to Use

Run `/review` BEFORE:

- Committing code
- Creating a PR
- Pushing to remote

## How to Use

### Step 1: Stage your changes

```bash
git add src/new-feature.py tests/test_new_feature.py
```

### Step 2: Run the review

In Claude Code (terminal or VS Code), type:

```
/review
```

Claude will:

1. Auto-detect your project language
2. Read the git diff
3. Read all changed files fully
4. Run 5 checks (architecture, slop, tests, security, questions)
5. Output a structured review report

### Step 3: Fix issues

If the review finds issues, fix them and run `/review` again.

### Step 4: Commit when approved

When the review outputs `APPROVE`, you're ready to commit.

## Understanding the Output

### Decision Types

| Decision | Meaning | What to Do |
|----------|---------|------------|
| **APPROVE** | All checks pass | Ready to commit and create PR |
| **REQUEST_CHANGES** | Critical or multiple issues found | Must fix before committing |
| **COMMENT** | Minor issues or suggestions | Fix recommended but not required |

### Issue Priorities

| Priority | Meaning | Required? |
|----------|---------|-----------|
| **Critical** | Security, missing tests, architecture violations | Yes — must fix |
| **Warnings** | Code quality, maintainability issues | Recommended |
| **Suggestions** | Style improvements, optimizations | Optional |

## Common Issues Detected

### 1. Weak Test Assertions

The review flags assertions that prove nothing:

| Language | BAD | GOOD |
|----------|-----|------|
| Python | `assert result is not None` | `assert result["status"] == "success"` |
| JS/TS | `expect(result).toBeTruthy()` | `expect(result.status).toBe("success")` |
| Java | `assertNotNull(result)` | `assertEquals("success", result.getStatus())` |
| Go | `if result == nil { t.Fatal() }` | `if result.Status != "success" { t.Errorf(...) }` |
| C# | `Assert.IsNotNull(result)` | `Assert.AreEqual("success", result.Status)` |

### 2. Dead Code and Unused Imports

```python
# FLAGGED: only Optional is used
from typing import Optional, List, Dict
```

```javascript
// FLAGGED: only map is used
import { map, filter, reduce } from 'lodash'
```

### 3. Print Statements

| Language | Flagged | Replace With |
|----------|---------|-------------|
| Python | `print()` | `logger.info()` |
| JS/TS | `console.log()` | `logger.info()` (winston/pino) |
| Java | `System.out.println()` | `log.info()` (SLF4J) |
| Go | `fmt.Println()` | `slog.Info()` |
| C# | `Console.WriteLine()` | `logger.LogInformation()` |

### 4. Empty Error Handling

```python
# FLAGGED
try:
    something()
except Exception:
    pass  # silently swallowed
```

```javascript
// FLAGGED
try {
    something()
} catch (e) {}  // empty catch
```

## Tips for Passing Review

### 1. Write strong test assertions

Test the actual VALUE, not just existence.

### 2. Test error cases

For every function, ask: "What happens when the input is wrong?"

### 3. Use proper logging

Replace all print/console.log with structured logging.

### 4. Delete dead code

Don't comment it out. Git has history. Delete it.

### 5. Keep functions focused

If a function does 3 things, split it into 3 functions.

## Workflow Integration

### Daily Development Flow

```bash
# 1. Create feature branch
git checkout -b feature/add-search

# 2. Write tests first (TDD)
# 3. Implement the feature
# 4. Stage changes
git add .

# 5. Run review BEFORE committing
/review

# 6. Fix any issues found
# 7. Run review again (should pass)
/review

# 8. Commit
git commit -m "feat: add search endpoint"

# 9. Push and create PR
git push -u origin feature/add-search
gh pr create --title "feat: add search endpoint" --body "..."
```

### Pre-PR Checklist

```bash
# 1. Run tests locally
npm test          # or pytest, mvn test, go test, dotnet test

# 2. Run /review
/review

# 3. Fix all critical issues

# 4. Push and create PR
git push
gh pr create
```

## Customization

To add project-specific review checks:

- Edit `CLAUDE.md` at the project root (add architecture rules, naming conventions, forbidden patterns)
- The `/review` command reads `CLAUDE.md` automatically and applies those rules

To change the severity of checks:

- Edit `.claude/commands/review.md` and modify the Decision Matrix section

## Related Files

| File | Purpose |
|------|---------|
| `.claude/commands/review.md` | The /review skill definition |
| `.claude/agents/code-writer.md` | Patterns for writing code |
| `.claude/agents/code-reviewer.md` | Standards for reviewing code |
| `CLAUDE.md` | Project-specific rules (you create this) |
| `CONTRIBUTING.md` | Team contribution guidelines |
