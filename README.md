# Registry Ping

Community sample app for testing the LSM Studio **app registry** end to end: GitHub install,
catalog listing, **View Manifest**, updates via release tags, and Studio embedding.

Cloned from `apps_testing/TEST-debug-shell` with custom teal branding and a radar-style launcher
icon. Same file-tree + code-editor harness — enough UI to confirm the install path works.

## Publish to your own GitHub repo

1. Create a **public** repository (empty is fine).
2. Copy **this folder’s contents** to the repo root (not the `samples/registry_ping` wrapper path).
3. Commit and push.
4. Create a GitHub **release** with tag `v1.0.0` (must match `source_ref` in the catalog row).
5. Open an LSM Studio submission issue with the `app_submission` label — paste
   `catalog_submission.json` after filling in your URLs and publisher name.

See [docs/App_Registry_Submission.md](../../docs/App_Registry_Submission.md) in the monorepo.

## Local test before publishing

From the LSM Studio repo root (with the same venv Studio uses):

```cmd
venv\Scripts\python.exe samples\registry_ping\assets\generate_registry_ping_icon.py
venv\Scripts\python.exe samples\registry_ping\scripts\gui.py
```

To test **Install** without waiting for MMG catalog merge, add a row to a local copy of
`apps/app_catalog.json` (or `apps/app_catalog_debug.json`) using `catalog_submission.json` as a
template, set `source_url` to your repo, restart Studio, and use **Library → Install**.

## Layout

| Path | Purpose |
| --- | --- |
| `lsm_studio_manifest.json` | Studio discovery + embedding |
| `lsm_studio_branding.json` | Launcher card colors and icon |
| `catalog_submission.json` | Paste into GitHub `app_submission` issue |
| `scripts/gui.py` | Standalone entry |
| `scripts/ui/app.py` | `RegistryPingFrame` embeddable root |
| `help/index.html` | Optional `?` help on launcher tile |
| `data/` | Sample project files for the file tree |

## Version bumps

When you ship an update:

1. Bump `version` in `lsm_studio_manifest.json`.
2. Tag the repo (e.g. `v1.0.1`).
3. Ask MMG to update the catalog row (`version`, `source_ref`, `release_date`) or submit a new
   issue if this is your first listing.

Registry update detection compares catalog `version` / `source_ref` against the installed copy.
