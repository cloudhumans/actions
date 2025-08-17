# app-version Action

A lightweight composite action to compute an APP_VERSION string for builds and deployments.

It combines:
- A base version read from a file (default: `version`) or provided via override
- A short (7 or 8 chars) or full Git SHA
- Date / datetime placeholders
- A customizable format template
- (Optional) Post-processing of template files by expanding `$VAR` / `${VAR}` environment variables (mini envsubst)

## Why
Centralizing version logic avoids duplicating shell snippets across repositories. The output can be used to:
- Tag Docker images
- Annotate artifacts
- Label deployments

## Inputs
| Name | Default | Required | Description |
|------|---------|----------|-------------|
| version_file | `version` | No | File containing the base version string (ignored if `base_override` provided). |
| format | `{base}-{sha7}` | No | Template placeholders: `{base} {sha7} {sha8} {sha} {date} {datetime}` |
| fail_if_missing | `true` | No | Fail when file missing and no override. |
| export_env | `true` | No | Export `APP_VERSION` to `$GITHUB_ENV`. |
| trim | `true` | No | Trim whitespace/newlines around base version. |
| base_override | (empty) | No | Overrides reading from file entirely. |
| fallback_base | `0.0.0` | No | Used if file missing AND `fail_if_missing=false` AND no override. |
| write_summary | `true` | No | Append markdown summary (table) to job summary. |
| process_templates | `false` | No | Run env substitution in files after computing version. |
| templates_glob | `deploy/**/*.yaml` | No | Glob used if `process_templates=true`. |

## Placeholders
| Placeholder | Meaning |
|------------|---------|
| `{base}` | Base version |
| `{sha7}` | First 7 chars of commit SHA |
| `{sha8}` | First 8 chars of commit SHA |
| `{sha}` | Full commit SHA |
| `{date}` | UTC date `YYYYMMDD` |
| `{datetime}` | UTC timestamp `YYYYMMDDHHMMSS` |

## Outputs
| Output | Description |
|--------|-------------|
| app_version | Final computed version |
| base_version | Base (pre-template) version |
| short_sha | 7-char SHA |
| short_sha8 | 8-char SHA |
| format_used | Template actually applied |

## Basic Usage
```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Compute version
        id: version
        uses: cloudhumans/actions/app-version@v1
        with:
          version_file: version
          format: "{base}-{sha7}"
          export_env: true
          write_summary: true
      - name: Show
        run: |
          echo "APP_VERSION env=$APP_VERSION"
          echo "APP_VERSION out=${{ steps.version.outputs.app_version }}"
```

## Custom Format
```yaml
with:
  format: "{base}-{date}-{sha7}"
```

## Missing File (Tolerant)
```yaml
with:
  version_file: version
  fail_if_missing: false
  fallback_base: "0.0.0"
  format: "{base}-{sha7}"
```

## Override Only
```yaml
with:
  base_override: "1.5.2"
  format: "{base}-{datetime}"
```

## Replacing Manual Step
Instead of:
```yaml
- run: |
    APP_VERSION_FILE=$(cat version)
    export APP_VERSION="${APP_VERSION_FILE}-$(echo ${{ github.sha }} | cut -c1-7)"
    echo "APP_VERSION=$APP_VERSION" >> $GITHUB_ENV
```
Use:
```yaml
- name: Compute APP_VERSION
  id: version
  uses: cloudhumans/actions/app-version@v1
  with:
    version_file: version
    format: "{base}-{sha7}"
    export_env: true
    write_summary: true
    process_templates: true
    templates_glob: "deploy/**/*.yaml"
```

## Template Processing
When `process_templates=true`, the script scans the glob and replaces:
| Pattern | Replaced With |
|---------|---------------|
| `$VAR` | Value or empty if unset |
| `${VAR}` | Value or empty if unset |

Typically this expands `APP_VERSION` inside deployment manifests.

## Notes
- Fails if final `APP_VERSION` empty.
- Trims whitespace when `trim=true`.
- Unset env vars become empty strings in template processing.

## Roadmap
- Optional semver enforcement
- Git tag creation (opt-in)
- Prefix injection
- CI contract JSON schema

## Release
Tag a version (e.g. `v1`) and consumers pin to it: `cloudhumans/actions/app-version@v1`.

---
Contributions welcome.
