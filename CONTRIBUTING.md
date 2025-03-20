# Contributing
To begin developing a new module, or implementing a bug fix, the first step is to fork this repository. On the Github website, click the Fork button and create a fork in your Github organization or personal account. You only need to copy the `main` branch.

Once the fork is created, clone the fork to your local system. Then create a branch using a name of your choice. For new modules or feature updates, create a branch prefixed with `feature_xxx`. For bugfixes, use the prefix `bugfix_xxx`. Check out the branch and begin development. 

## Module Development
All modules use a similar approach and structure, so the easiest way to maintain consistency is to copy one of the existing modules, rename it, and then modify it to implement the new module functionality. All modules are located in the `plugins/modules` directory. Required modifications include:
- Update the DOCUMENTATION section with the necessary arguments for the new module
- Update the DOCUMENTATION section examples
- Update the GET, CREATE, UPDATE, and REMOVE functions (more details below)
- Update the `eval_changed` method which checks the current configuration against the provided arguments and ensures changes are only made if necessary (this is what drives module idempotence)
- Update the `argument_spec` with the required arguments
- Update logic as necessary to run the required GET, CREATE, UPDATE, or REMOVE functions based on the provided `state` argument

### The `state` Argument
Modules should have a `state` argument with one or more of the following as valid choices:
- present: create an object if not already present
- updated: update an existing object or setting
- absent: remove an existing object
- query: query an existing object or setting

Some features will have all four, such as `sfos_ip_host` for example. In some cases, a module might be modifying settings that cannot be created or removed, and in that case would only have a `updated` and `query` choices implemented. 

### GET, CREATE, UPDATE and REMOVE Functions
Modules will have at a minimum, a GET and UPDATE function. Similar to the `state` argument, some modules may be updating firewall settings that cannot be added or removed, so they may not have a CREATE or REMOVE function. 

When working with these functions, as of version 2.0.0 they are using the HTTPAPI module `invoke_sdk` method to utilize the XML API of Sophos firewall. This method utilizes the [Python SDK](https://sophosfirewall-python.readthedocs.io) to make calls against the API. 

> When REST API becomes available in Sophos Firewall, we will implement the `send_request` method and modules will be updated to use that instead of `invoke_sdk`.  Then any new modules will use `send_request` instead of `invoke_sdk`, and the existing modules will also be updated to use `send_request`. Eventually, use of the SDK and XML API will be deprecated. This documentation will be updated with the implementation details once REST API becomes available.  

The `invoke_sdk` method takes as arguments the SDK method name to be called, and a `method_args` argument, which can be specified as a dictionary containing the SDK method arguments. For example, to call the SDK method `get_ip_host` to find a host named `testhost`, the following code could be used:
 
```python
resp = connection.invoke_sdk("get_ip_host", module_args={"name": "testhost"})
```
> The `connection` is an `ansible.module_utils.connection.Connection` object, which is instantiated in the main section of the module.

In some cases, there may not be a specific SDK method for a particular feature. In this case, you can use the SDK `submit_xml` method. The `submit_xml` method takes as arguments a template which should include the XML payload to configure a particular feature. The template supports Jinja2 syntax, and can also take a dictionary containing variables to be inserted into the template when rendered. This can be accomplished by including variables in the template using the format `{{ var }}`, and then passing in the variables using the `template_vars` argument. An example of this can be seen in the [sfos_ipsec_connection](https://github.com/sophos/sophosfirewall-ansible/blob/httpapi/plugins/modules/sfos_ipsec_connection.py) Ansible module: 

```python
payload = """
    <Get>
        <VPNIPSecConnection>
           <Configuration>
           <Filter>
                <key name="Name" 
                criteria="=">{{ name }}</key>
            </Filter>
          </Configuration>
        </VPNIPSecConnection>
    </Get>
"""
    try:
        resp = connection.invoke_sdk("submit_xml", module_args={
            "template_data": payload,
            "set_operation":None,
            "template_vars": {"name": module.params.get("name")},
            }
        )

    except Exception as error:
        module.fail_json("An unexpected error occurred: {0}".format(error), **result)

```
> For the above example, a GET is being performed and therefore the `set_operation` argument is set to None. When implementing create functions it should be set to `add`, which is the default. For update or remove functions, `set_operation` should be set to `update` or `remove`. 

### Eval_Changed Method
The purpose of the `eval_changed()` method is to compare the existing settings of a feature to the arguments provided, and return a True result if something is different. Otherwise, if nothing is different, it should return False. This function is to ensure that the module is idempotent; it won't make a change if the intended configuration is already implemented.

It takes as input the `exist_settings` dictionary, which is the result of the GET function being called in the beginning of the `main()` function. 

> In some cases, `eval_changed()` can't compare the argument with the configuration because the value in the configuration is encrypted. This would be the case for passwords or encryption keys. In this case, if one of these arguments is specified in the task, the `eval_changed()` should return True.

### Tests
Each module is required to have a manual test case built in the `tests/manual` directory, as well as a more comprehensive set of test cases in the `tests/integration` directory. The manual tests are intended to be run using the `ansible-playbook` command, whereas the integration tests use the `ansible-test` command for execution. Both are intended to be run against an actual physical or virtual Sophos Firewall appliance.

The easiest way to create the integration tests is to copy one of the existing folders in `/tests/integration/targets` directory, and then modify the `tasks/main.yml` file in the new directory with the test tasks for your module. The integration tests run through the GET, CREATE, UPDATE, and REMOVE functions, as well as test for error conditions or expected results when trying to update settings that are already in the desired state. 

The integration tests can be executed using the `ansible-test` command:
```bash
ansible-test integration sfos_ip_host -vv
```
A file `integration_config.yml` must be placed in the `tests/integration` folder containing the connection details for the Sophos Firewall that the tests will be run against. This file will need to be created, as it is not checked into the Github repository. An example `integration_config.yml.template` is provided in the repo. 

Below is an example `integration_config.yml` file:

```yaml
ansible_user: my_api_user
ansible_host: testfirewall.lab.sophos.net
ansible_password: supersecretpassword
ansible_httpapi_validate_certs: false
ansible_httpapi_port: 4444
ansible_connection: ansible.netcommon.httpapi
ansible_network_os: sophos.sophos_firewall.sfos
```

###  Main Function
The changes needed to the `main()` section of code should be minimal:
- Update the arguments in the `argument_spec` dictionary
- Implement any argument requirements such as `required_if`, `mutually_exclusive` etc. See the Ansible [documentation](https://docs.ansible.com/ansible/latest/dev_guide/developing_program_flow_modules.html#dependencies-between-module-options) for details.
- Update the calls to the correct GET, CREATE, UPDATE, and REMOVE functions

## Dev Environment Setup
- Create the folder structure `~/collections/ansible_collections/sophos/sophos_firewall` and then clone this project inside the `sophos_firewall` folder. Then set the `ANSIBLE_COLLECTIONS_PATH` environment variable to `~/collections`. This will allow the `ansible-playbook` command to see your code changes automatically without having to reinstall the collection.

```bash
mkdir -p ~/collections/ansible_collections/sophos/sophos_firewall
cd ~/collections/ansible_collections/sophos/sophos_firewall
git clone https://github.com/sophos/sophosfirewall-ansible.git .
export ANSIBLE_COLLECTIONS_PATH=~/collections
```
  
> Once the `ANSIBLE_COLLECTIONS_PATH` environment variable is set, DO NOT run `ansible-galaxy collection install sophos.sophos_firewall --force`, as this will overwrite the `~/collections/ansible_collections/sophos/sophos_firewall` directory with the contents of the package from Ansible Galaxy. In other words, it will overwrite your work! 
  
- If not already installed, install [Poetry](https://python-poetry.org) using `pip install poetry`
- Create a Python virtual environment, activate it, and then use Poetry to install dependencies
  
```
python -m venv ~/sophosfirewall-ansible
source ~/sophosfirewall-ansible/bin/activate
poetry install
```
  
Once it is complete, you should see the `sophosfirewall-ansible` module at the top of the `ansible-galaxy collection list` output. 
  
```
ansible-galaxy collection list

Collection                               Version
---------------------------------------- -------
sophos.sophos_firewall                   2.0.0
```
  
To test if your system is able to find the modules, run the command `ansible-doc -t module sophos.sophos_firewall.sfos_ip_host`. If all is working properly, this should display a text version of the module documentation. 

## Preparing for release
Create a Pull Request against the `main` branch. The maintainers will review the PR, and run the included tests. If changes are needed, they will be requested in the PR review comments. When the review is complete, the PR will be merged and the CI/CD pipeline will publish a new version of the collection to Ansible Galaxy.