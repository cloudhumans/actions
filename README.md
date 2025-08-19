# CloudHumans GitHub Actions

Reusable composite actions collected in one repository. Each action lives in its own folder and is consumed via a tag (e.g. `@v1`).

## Repository Layout
```
app-version/         # APP_VERSION computation + optional template var expansion
.github/workflows/   # CI tests for the actions
```

Every action folder contains:
`action.yml` · `README.md` · optional helper scripts.

## Actions
| Action | Purpose |
|--------|---------|
| app-version | Build a version string from a file/override + commit metadata; can env‑substitute templates. |

## Quick Use
```yaml
- uses: cloudhumans/actions/app-version@v1
  with:
    version_file: version
    format: "{base}-{sha7}"
```

## Development
1. Implement / update action.
2. Add or adjust tests in `.github/workflows`.
3. PR & merge.
4. Tag (or move major tag): `git tag v1 && git push origin v1 --force` (only when updating the major line).

## Versioning Policy
Semantic when practical. Breaking change ⇒ new major tag (`v2`). Keep major tag pointing to latest stable.

## Guidelines
Small, dependency‑light, fast (<1m CI). Fail fast with clear `::error` messages. Document inputs/outputs succinctly.

## Roadmap (short list)
- Docker build/publish
- Manifest validation
- Automatic semver bump

## Contributing
PRs / issues welcome. State motivation + impact.

## Language
English only across docs, code, and commits.

---
CloudHumans Engineering