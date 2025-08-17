# CloudHumans Reusable GitHub Actions

Monorepo containing reusable GitHub Actions for the CloudHumans organization. Each action lives in its own subdirectory at the repository root and is versioned via tags (`v1`, `v2`, etc.).

## Goal
Standardize repeated pipeline logic (versioning, template processing, etc.) to reduce boilerplate and the risk of divergence across repositories.

## Structure

```
actions/
  app-version/        # Action that generates APP_VERSION and (optionally) processes templates
  .github/workflows/  # Automated tests for the actions
  README.md           # This file
```

Each action directory contains:
- `action.yml` (composite action definition)
- `README.md` (action‑specific docs)
- Helper scripts (if any)

## Available Actions

| Action | Path | Description |
|--------|------|-------------|
| app-version | `app-version/` | Computes a version from file/override + commit metadata and optionally expands variables inside templates. |

## How to Use

Reference an action with `uses: cloudhumans/actions/<folder>@v1` after publishing the tag:

```yaml
- name: Compute version
  uses: cloudhumans/actions/app-version@v1
  with:
    version_file: version
    format: "{base}-{sha7}"
```

## Development Workflow

1. Add or edit an action in a new/existing directory.
2. Create / update tests under `.github/workflows/*` ensuring minimal coverage (happy path + edge cases).
3. Open a PR.
4. After merge: create/update the major tag (`git tag v1 && git push origin v1`).

## Versioning

Follow SemVer whenever possible. When introducing breaking changes, bump the major tag (`v2`). Keep the major tag pointing to the latest stable minor/patch.

## Best Practices
- Avoid unnecessary dependencies (prefer pure composite actions using simple bash/python).
- Clear, documented outputs.
- Fail fast with meaningful `::error` messages.
- Keep tests fast (< 1 min) for continuous feedback.

## Roadmap
- Standardized Docker build/publish action
- Manifest validation action
- Automatic semver bump action

## Contributing
PRs and issues are welcome. Clearly describe motivation and impact.

## Language Policy
All documentation, commit messages, code comments, identifiers, and future additions must be written in English only. This keeps the codebase consistent and maximizes tooling (e.g. Copilot) effectiveness.

---
CloudHumans Engineering