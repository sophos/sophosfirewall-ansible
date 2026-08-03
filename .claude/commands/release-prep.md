---
description: Prepare a release - bump versions, generate the changelog fragment, run antsibull-changelog, and open the PR
argument-hint: "[x.y.z] (omit to infer the version from the commits)"
allowed-tools: Bash(git:*), Bash(gh:*), Bash(antsibull-changelog:*), Bash(poetry:*), Bash(grep:*), Bash(ls:*), Bash(cd:*), Read, Edit, Write, Grep, Glob
---

Prepare a release of the `sophos.sophos_firewall` collection.

Requested version: `$1` (may be empty - infer it in step 3 if so)

Work through the steps in order. **Halt and report** on any failed precondition
rather than working around it. There are two stop points where you wait for the
user: step 8 (review the changelog) and step 10 (confirm the push).

## 1. Establish the working directory

All paths below are relative to the collection root - the directory holding
`galaxy.yml`. Get it with `git rev-parse --show-toplevel`. If the current
directory is not a git repository, use
`collections/ansible_collections/sophos/sophos_firewall` relative to the
project root.

## 2. Check preconditions

Halt if any of these fail:

- **Not on `main`.** This flow needs a feature branch to open a PR from. Report
  the current branch and stop.
- **`main..HEAD` has commits.** If `git log --no-merges main..HEAD` is empty
  there is nothing to release.
- **Working tree is clean.** `git status --porcelain` must be empty, so the
  diff you show in step 8 contains only release changes.
- **`main` is up to date.** Run `git fetch origin main` and check that
  `main..origin/main` is empty. If `origin/main` has moved ahead, tell the user
  to rebase first - otherwise the commit range and the version bump may both be
  computed against a stale base.
- **`antsibull-changelog` is available.** Try `antsibull-changelog --version`,
  then `poetry run antsibull-changelog --version`. Use whichever works for
  steps 6 and 7. If neither works, stop and tell the user to run
  `poetry install --with dev` (it arrives as a dependency of `antsibull-docs`).

## 3. Determine the version

Read the current version from `galaxy.yml`.

**If `$1` was supplied**, validate it: valid `MAJOR.MINOR.PATCH` semver,
strictly greater than the current version, and no existing `vX.Y.Z` tag either
locally or on the remote (`git ls-remote --tags origin`). Halt on any failure.

**If `$1` was empty**, classify the commits first (step 4), then derive the
bump from that classification:

- any new module, or any `minor_changes` entry -> bump **MINOR**, reset PATCH to 0
- only `bugfixes` entries -> bump **PATCH**
- anything you would classify as `breaking_changes` -> **do not guess.** Stop
  and tell the user this looks like a MAJOR release and they should re-run with
  an explicit version.

## 4. Read and classify the commits

Run `git log --no-merges main..HEAD` and `git diff --name-status main..HEAD`.

Map each commit to a changelog section, using `changelogs/config.yaml` for the
available sections:

- Fixes to existing module behaviour -> `bugfixes`
- New options or capabilities on an existing module -> `minor_changes`
- A new file under `plugins/modules/` -> a new module. **Do not write these into
  the fragment** - `antsibull-changelog` discovers them from the plugin cache
  and generates the "New Modules" section itself.
- Test-only, CI-only, or docs-only commits -> omit, or put under `trivial`

Commit messages here are written as descriptions of the problem, not of the fix.
Rewrite them into the house style, which is past-tense and names the module:

> `snmp_agent Configuration key changed to EnableAgent`
> -> `Fixed an issue in sfos_snmp_agent where the Configuration key is now renamed to EnableAgent`

Use bare module names (`sfos_snmp_agent`), not FQCNs - match the existing
entries in `changelogs/changelog.yaml`. One entry per user-visible change, not
one per commit; squash multiple commits that fix the same thing.

## 5. Bump the version and check `version_added`

- Update `version:` in `galaxy.yml`
- Update `version` under `[tool.poetry]` in `pyproject.toml`

Both must end up identical - the release workflow fails the build if they
disagree.

For any **new** module in this range, check that `version_added:` in its
`DOCUMENTATION` block matches the new version, and fix it if not. This value is
baked into the published docs and cannot be corrected after release without a
new one.

## 6. Write the fragment

Write `changelogs/fragments/<version>.yaml`. Halt if that file already exists -
it means a release for this version was started and not finished.

Always include `release_summary`. Match the tone of the existing summaries:

```yaml
release_summary: |
  This release introduces new modules for working with certificate authorities
  and notification email settings on Sophos Firewall.
```

```yaml
release_summary: |
  This release implements bug fixes for working with Sophos Firewall running
  SFOS version 22.0 and later versions.
bugfixes:
  - Fixed an issue in sfos_admin_settings with the key HTTPSPort (should have been HTTPSport) causing module failures
```

Then run `antsibull-changelog lint`. If it fails, fix the fragment and re-run;
do not proceed with a fragment that does not lint.

## 7. Release the changelog

```
antsibull-changelog release --version <version> -v
```

This consumes the fragment file and rewrites `CHANGELOG.md` and
`changelogs/changelog.yaml`. Note that `keep_fragments: false`, so the fragment
is deleted - that is expected.

## 8. STOP - review

Show the user:

- the version and how it was chosen (inferred with reasoning, or supplied)
- a summary of the commits and how each was classified
- the `CHANGELOG.md` diff (`git diff CHANGELOG.md`)
- the version bumps

Then wait.

**If the user wants wording changes**, reset the generated output before
editing - the fragment no longer exists, so it must be recreated:

```
git checkout -- CHANGELOG.md changelogs/changelog.yaml
```

Then go back to step 6 with the revised wording. Do not hand-edit
`CHANGELOG.md` or `changelogs/changelog.yaml` directly; they are generated
files and the fragment is the input of record.

## 9. Commit

Stage only release files: `galaxy.yml`, `pyproject.toml`, `CHANGELOG.md`,
`changelogs/changelog.yaml`, and any `version_added` fix from step 5. Commit as:

```
release: v<version>
```

## 10. STOP - confirm, then push and open the PR

Ask the user to confirm before pushing, since this pushes a branch and opens a
PR that notifies reviewers.

On confirmation:

```
git push -u origin HEAD
gh pr create --base main --title "release: v<version>" --body "<body>"
```

Build the PR body from the `release_summary` you wrote plus the changelog
entries - do not ask the user to retype a description they have already
written. Report the PR URL.

Then remind the user of what happens next: merging the PR triggers
`.github/workflows/release.yaml`, which tags `v<version>` on the merge commit,
builds the collection, creates the GitHub release and publishes to Ansible
Galaxy. Nothing is published until the merge, and a Galaxy publish cannot be
undone.
