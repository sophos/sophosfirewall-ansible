### Releasing

Releases are driven by the `version` field in `galaxy.yml`. When a merge to `main`
lands a version that has no matching `vX.Y.Z` tag, the
[release workflow](.github/workflows/release.yaml) tags the merge commit, builds
the collection, creates a GitHub release and publishes to Ansible Galaxy. Every
other merge to `main` is a no-op.

#### The normal path

From a feature branch, run the `/release-prep` command in Claude Code:

```
/release-prep           # infer the version from the commits
/release-prep 2.6.0     # or set it explicitly
```

It will:

1. Read `main..HEAD` and classify each commit into changelog sections
2. Propose a version - MINOR if the release adds a module or a `minor_changes`
   entry, PATCH if it is only bugfixes (MAJOR is never inferred; pass it
   explicitly)
3. Bump `version` in both `galaxy.yml` and `pyproject.toml`
4. Check `version_added` on any new module matches the new version
5. Write `changelogs/fragments/x.y.z.yaml` and lint it
6. Run `antsibull-changelog release --version x.y.z`
7. **Pause** for you to review the generated `CHANGELOG.md` diff
8. Commit, then **pause** again before pushing and opening the PR

Merging the PR does the rest. Nothing is published until that merge - and a
Galaxy publish cannot be undone, so the changelog review in step 7 is the point
at which to catch mistakes.

#### Versioning

This project uses [Semantic Versioning](https://semver.org). The format is
`MAJOR.MINOR.PATCH`.

- New modules increment the `MINOR` version
- Bug fixes increment the `PATCH` version
- New modules need `version_added` set in the `DOCUMENTATION` section to the
  release they first ship in

#### Prerequisites

`antsibull-changelog` comes in as a dependency of `antsibull-docs`:

```bash
poetry install --with dev
```

#### Doing it by hand

If you need to run the process manually:

- Update `version` in `galaxy.yml` **and** `pyproject.toml` - the release
  workflow fails the build if the two disagree
- Add `changelogs/fragments/x.y.z.yaml` with at least a `release_summary`:

```yaml
release_summary: |
  This release introduces new modules for working with the X feature on Sophos Firewall
```

If only bug fixes are in the release:

```yaml
bugfixes:
  - Fixed an issue in sfos_admin_settings with the key HTTPSPort (should have been HTTPSport) causing module failures
```

> New modules do not go in the fragment - `antsibull-changelog` discovers them
from the plugin cache and generates the "New Modules" section itself.

- Run `antsibull-changelog` to update the changelog:

```bash
antsibull-changelog release --version x.y.z -v
```

> The fragment file is consumed and `changelogs/changelog.yaml` and
`CHANGELOG.md` are regenerated. Do not hand-edit those two files; the fragment
is the input of record.

- Merge a PR. The workflow takes it from there.

Once the workflow finishes, clients can update with the `--force` flag:
`ansible-galaxy collection install sophos.sophos_firewall --force`

#### Re-running a release

The workflow keys off tag existence, so it is safe to re-run. If a publish fails
partway, delete the `vX.Y.Z` tag and re-run the workflow from the Actions tab
via `workflow_dispatch`. If the version was already accepted by Galaxy, it
cannot be republished - bump the PATCH version and release again.
