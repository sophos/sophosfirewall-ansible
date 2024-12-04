# Ansible Collection - sophos.sophos_firewall
This collection provides modules for working with Sophos Firewall running SFOS 18.0+. The modules leverage the [sophosfirewall-python](https://sophosfirewall-python.readthedocs.io) SDK to perform operations on the firewall using the embedded [XML API](https://docs.sophos.com/nsg/sophos-firewall/21.0/API/index.html).
  
For installation and usage details, please see the [Documentation](https://sophosfirewall-ansible.readthedocs.io)


## Contributing
This is an open source project and we welcome contributions from the community. To get started, fork this repository and perform development in the fork. The following guidelines should be followed:
  
- This project uses [Semantic Versioning](https://semver.org)
- When adding new modules, increment the `MINOR` version
- When making bug fixes, increment the `PATCH` version
- When adding new modules, configure the `version_added` field in the module to the new version

### Releasing
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


### Tests
When adding a new module, integration tests should be written and stored under the `tests/integration` directory. Each module should have a directory in the `targets` folder, and a `main.yml` file implementing the test cases. Tests can be run against a physical or virtual Sophos Firewall appliance. To run these tests against your own firewall, a file `integration_config.yml` must be created in the `tests` directory. An file `integration.yml.template` file is provided as an example. The variables in the example file should be replaced with the actual values, and the file renamed to `integration.yml`.  Once these steps are complete, tests for a specific module can be run using `ansible-test integration [module_name]`:
  
```bash
ansible-test integration sfos_syslog -v
```




