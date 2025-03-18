### Releasing
The following guidelines should be followed:
  
- This project uses [Semantic Versioning](https://semver.org). The format is `MAJOR.MINOR.PATCH`.
- When adding new modules, increment the `MINOR` version
- When making bug fixes, increment the `PATCH` version
- When adding new modules, configure the `version_added` field in the DOCUMENTATION section of the module to the new version
- Update the `version` field in `galaxy.yml` to the new version
- Update the `version` field in `pyproject.toml` to the new version
- In the `changelogs/fragments` directory, add a file named `x.y.z.yaml` where x.y.z indicates the version
- The file should have at a minimum, a `release_summary` field for example:
```yaml
release_summary: |
  This release introduces new modules for working with the X feature on Sophos Firewall
```
If only bug fixes are in the release:
```yaml
bugfixes:
  - docker_container - wait for removal of container if docker API returns early
    (https://github.com/ansible/ansible/issues/65811).
```
- Run `antsibull-changelog` to update the change log
```bash
antsibull-changelog release --version x.y.z -v
```
> The fragment file will be deleted and the `changelogs/changelog.yaml` will be updated. The Actions workflow
will take care of updating the change log in the documentation.
- Merge a PR
- Check out the `main` branch and do a `git pull` to incorporate changes merged in the PR
- Create and push a new tag
```bash
git tag vx.y.z
git push --tags
```
> This will cause the Actions workflow to build the collection and upload it to Ansible galaxy. When complete, it should be possible to update clients using the `--force` flag:  `ansible-galaxy collection install sophos.sophos_firewall --force`
