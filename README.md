# Ansible Collection - sophos.sophos_firewall
This collection provides modules for working with Sophos Firewall running SFOS 18.0+. The modules leverage the [sophosfirewall-python](https://sophosfirewall-python.readthedocs.io) SDK to perform operations on the firewall using the embedded [XML API](https://docs.sophos.com/nsg/sophos-firewall/21.0/API/index.html).
  
For installation and usage details, please see the [Documentation](https://sophosfirewall-ansible.readthedocs.io)


## Contributing
This is an open source project and we welcome contributions from the community. To get started, fork this repository and perform development in the fork. The following guidelines should be followed:
  
- This project uses [Semantic Versioning](https://semver.org)
- When adding new modules, increment the `MINOR` version
- When making bug fixes, increment the `PATCH` version
- When adding new modules, configure the `version_added` field to the new version the module will be added to
- Update the `version` field in `galaxy.yml` to the new version
- In the `changelogs/fragments` directory, add a file named `x.y.z.yaml` where x.y.z indicates the version
- The file should have at a minimum, a `release_summary` field for example:
```yaml
release_summary: |
  This release introduces new modules for working with the X feature on Sophos Firewall
```
- Github Actions will take care of updating the documentation and changelog automatically upon PR merge

### Tests
When adding a new module, integration tests should be written and stored under the `tests/integration` directory. Each module should have a directory in the `targets` folder, and a `main.yml` file implementing the test cases. Tests can be run against a physical or virtual Sophos Firewall appliance. To run these tests against your own firewall, a file `integration_config.yml` must be created in the `tests` directory. An file `integration.yml.template` file is provided as an example. The variables in the example file should be replaced with the actual values, and the file renamed to `integration.yml`.  Once these steps are complete, tests for a specific module can be run using `ansible-test integration [module_name]`:
  
```bash
ansible-test integration sfos_syslog -v
```




