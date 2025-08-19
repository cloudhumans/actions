# CloudHumans Actions – AI Assistant Guide

Concise, repo-specific instructions for automated coding agents. Focus: fast, low‑dependency GitHub composite actions.

## Project Snapshot
- Mono-repo of reusable composite GitHub Actions. Each action is a folder with `action.yml` + helper scripts.
- Primary action today: `app-version` – computes `APP_VERSION` and optionally performs env var substitution in template files.
- Language: Python for helper script; shell inside workflows. All docs & code strictly English.

## Key Directories / Files
- `app-version/action.yml`: Defines inputs/outputs & runs steps (Python + shell). Keep modifications minimal & backward compatible.
- `app-version/process_templates.py`: Lightweight envsubst replacement. Patterns: `$VAR` or `${VAR}` replaced with value or empty string. Now logs per-file replacement counts and a final total.
- `deploy/sample.yaml`: Test fixture for template substitution.
- `.github/workflows/*.yml`: Acts as test suite (no separate unit test framework). Update/add jobs to extend coverage.
- Root `README.md` + `app-version/README.md`: Source of truth for public usage & inputs; update when changing behavior.

## Action Behavior (app-version)
1. Determine base version: `base_override` > file `version` (trim optional) > `fallback_base` when allowed.
2. Build placeholders: `{base} {sha7} {sha8} {sha} {date} {datetime} {run_number}`.
3. Format final `APP_VERSION`; export & write summary/table when configured.
4. If `templates_glob` non-empty: split on space/comma/semicolon, glob each, dedupe, then run `process_templates.py`.
5. Template processing blanks unset vars instead of leaving token text.

## Conventions & Constraints
- Keep runtime fast (<1 minute CI). Avoid heavy deps; pure stdlib preferred.
- Explicit, fail-fast messaging. For GitHub actions, prefer `::error ::warning` annotations if adding new validations.
- English only; avoid introducing non-English identifiers or comments.
- Backwards compatibility: do not silently rename inputs/outputs. Add new ones as optional.
- Logging: simple `print` acceptable; avoid noisy debug unless guarded by an opt-in flag.
- Replacement counts: per file line `Processed: <file> (replacements: N)` plus final `Total replacements across all files: X`.

## Commit Message Guidelines
Format: `<type><scope?>: <short imperative description>`
- type: an emoji or keyword indicating the nature of the change
- scope (optional): area of codebase in parentheses
- description: concise, imperative, under 50 chars, no trailing period

Rules:
- Use imperative mood; do not capitalize first word
- Keep subject < 50 chars; no trailing period
- Blank line between subject and body (if body used)
- Body (wrapped ~72 chars) explains what & why, not how
- Footer may reference issues (e.g. `Closes #45`, `Refs #67`)

Examples:
```
:sparkles: add user authentication module
:bug: fix crash on logout when token expires
:wrench: update database connection timeout setting
:zap: improve query performance for large datasets
```

## Making Changes
- When altering behavior surfaced to users (inputs, outputs, logging semantics), update both READMEs and add/modify a workflow job demonstrating it.
- Extend tests by cloning pattern in `test-app-version.yml`; each job isolates a scenario.
- Prefer adding assertions via shell with `set -euo pipefail` and explicit `grep` / pattern matches.

## Adding a New Action
1. Create folder `<name>/` with `action.yml`, `README.md`, optional scripts (bash/python minimal).
2. Follow style of `app-version` for documentation tables (Inputs/Outputs, examples).
3. Provide at least one workflow job exercising it.
4. Tag release (move major tag).

## Python Script Guidelines
- Must run under system Python 3.x without extra deps.
- Keep functions short & testable; reuse patterns from `process_templates.py` (regex precompiled at module level, helper functions underscore-prefixed).
- Provide deterministic output; avoid reliance on locale/timezone except UTC for timestamps.

## Testing Locally (quick examples)
- Run template processing: `python app-version/process_templates.py 'deploy/**/*.yaml'`
- Simulate action step: create `version` file then emulate placeholders via environment variables.

## Common Pitfalls (and expectations)
- Unset vars become empty (not an error). Tests assert blank lines where appropriate.
- Multiple glob patterns may overlap; duplicates must be processed once.
- Trimming base version default on; watch trailing spaces in `version` file.

## When Unsure
- Mirror existing patterns before inventing new structures.
- If adding feature flags, default them to current behavior to avoid breaking consumers.

## Output / Input Names (do not change silently)
- Outputs: `app_version`, `base_version`, `short_sha`, `short_sha8`, `format_used`, `full_sha`.
- Key inputs (subset): `version_file`, `format`, `fail_if_missing`, `export_env`, `trim`, `base_override`, `fallback_base`, `write_summary`, `templates_glob`.

---
Refine this guide if new actions or patterns are introduced; keep it brief and actionable.
