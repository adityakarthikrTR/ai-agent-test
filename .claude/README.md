# Claude Code Configuration

This directory contains agent specifications and commands for Claude Code integration. These files are **language-agnostic** and work with any project.

## Directory Structure

```
.claude/
├── agents/
│   ├── code-writer.md       # Patterns for writing new code
│   └── code-reviewer.md     # Standards for code review
├── commands/
│   ├── dev.md               # /dev command (fully automated pipeline)
│   └── review.md            # /review command (review only)
├── README.md                # This file
└── REVIEW_USAGE.md          # How to use /review and /dev
```

## Two Commands

| Command | What It Does | Code Writing | User Action |
|---------|-------------|-------------|-------------|
| `/dev` | Full pipeline: code + test + review + PR + merge | Automatic (Claude writes) | Review and say "approve" |
| `/review` | Review only: checks your code | Manual (you write) | Fix issues, commit, PR |

## How It Works

### Automatic Loading

Files in `.claude/agents/` are **automatically loaded** into Claude's system prompt when you start Claude Code in this project directory. Claude is always aware of your project's writing and review standards.

### The `/dev` Command (Fully Automated)

Type `/dev` and give a requirement. Claude automatically: reads project context, plans, writes code, writes tests, runs tests, self-reviews, fixes issues — then asks you to review. After you approve, Claude commits, pushes, creates a PR, and merges to main.

### The `/review` Command (Review Only)

Type `/review` after writing code yourself. Claude reviews your code against quality standards and outputs a structured report.

See [REVIEW_USAGE.md](REVIEW_USAGE.md) for the complete guide.

## How Files Relate

```
CLAUDE.md (Project-Specific Rules)
    |
    |  referenced by all:
    |
    ├──> code-writer.md
    |    How to WRITE code for this project.
    |    Covers: TDD, error handling, patterns, pre-commit checklist.
    |
    ├──> code-reviewer.md
    |    How to REVIEW code for this project.
    |    Covers: 5-step process, security, tests, quality, decision matrix.
    |
    ├──> commands/dev.md
    |    The /dev automated pipeline.
    |    ORCHESTRATES: context → plan → implement → test → review → PR → merge.
    |    Only stops for user approval.
    |
    └──> commands/review.md
         The /review manual command.
         ORCHESTRATES: detect language, gather diff, run 5 checks, output report.
```

**Key:** `CLAUDE.md` is the single customization point. The `.claude/` files are generic templates that defer project-specific rules to `CLAUDE.md`.

## Language Support

The `/review` command auto-detects the project language:

| Detection File | Language | Default Test Runner | Default Linter |
|---------------|----------|-------------------|---------------|
| `package.json` | JavaScript/TypeScript | jest / vitest | eslint |
| `pyproject.toml` / `requirements.txt` | Python | pytest | ruff |
| `pom.xml` | Java (Maven) | JUnit / TestNG | checkstyle |
| `build.gradle` | Java/Kotlin (Gradle) | JUnit | checkstyle |
| `go.mod` | Go | go test | golangci-lint |
| `*.csproj` / `*.sln` | C# (.NET) | xUnit / NUnit | roslyn |
| `Cargo.toml` | Rust | cargo test | clippy |

Override defaults by specifying the language and tools in `CLAUDE.md`.

## Customization

**DO customize:** `CLAUDE.md` at the project root (project-specific rules)

**DO NOT customize:** files in `.claude/` (these are generic templates)

If you need to change review behavior for ALL projects, update the template repo and re-copy.

If you need to change behavior for ONE project, add rules to that project's `CLAUDE.md`.

## Adopting This Template

```bash
# 1. Copy .claude/ directory into your repo
cp -r path/to/claude-review-template/.claude/ your-repo/.claude/

# 2. Copy the CLAUDE.md template and fill it in
cp path/to/claude-review-template/CLAUDE.md.template your-repo/CLAUDE.md
# Edit CLAUDE.md with your project's specific rules

# 3. Commit
cd your-repo
git add .claude/ CLAUDE.md
git commit -m "chore: add Claude Code review pipeline"

# 4. Start using /review
# Stage changes → run /review → fix issues → commit
```

## Updating

When the template repo is updated:

```bash
# Re-copy .claude/ files (your CLAUDE.md is NOT overwritten)
cp -r path/to/claude-review-template/.claude/ your-repo/.claude/
git add .claude/
git commit -m "chore: update Claude Code review template"
```
