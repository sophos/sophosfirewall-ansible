#!/usr/bin/python

# Copyright 2024 Sophos Ltd.  All rights reserved.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: sfos_urlgroup

short_description: Manage URL Groups on Sophos Firewall

version_added: "2.2.0"

description: Creates, updates or removes URL Groups from Sophos Firewall

extends_documentation_fragment:
  - sophos.sophos_firewall.fragments.base

options:
  name:
    description: Name of the URL Group to create, update, or delete
    required: true
    type: str
  domain_list:
    description:
      - List of domains to be included in the URL Group.
    type: list
    elements: str
  state:
    description:
      - Use C(present) to create, C(absent) to remove, C(update) to modify, or C(query) to get information
    choices: [present, absent, update, query]
    type: str
    required: true
  action:
    description:
      - Action to perform when updating a URL Group.
      - Required when I(state=update).
    type: str
    choices:
      - add
      - remove
      - replace

author:
    - Sophos
"""

EXAMPLES = r"""
- name: Get all URL groups
  sophos.sophos_firewall.sfos_urlgroup:
    state: query

- name: Get specific URL group
  sophos.sophos_firewall.sfos_urlgroup:
    state: query
    name: "Marketing_Websites"

- name: Create a URL group
  sophos.sophos_firewall.sfos_urlgroup:
    state: present
    name: "Marketing_Websites"
    domain_list:
      - example.com
      - example.org

- name: Add domains to existing URL group
  sophos.sophos_firewall.sfos_urlgroup:
    state: update
    name: "Marketing_Websites"
    domain_list:
      - example.net
      - example.io
    action: add

- name: Remove domains from URL group
  sophos.sophos_firewall.sfos_urlgroup:
    state: update
    name: "Marketing_Websites"
    domain_list:
      - example.net
    action: remove

- name: Replace all domains in URL group
  sophos.sophos_firewall.sfos_urlgroup:
    state: update
    name: "Marketing_Websites"
    domain_list:
      - new-example.com
      - new-example.org
    action: replace

- name: Delete URL group
  sophos.sophos_firewall.sfos_urlgroup:
    state: absent
    name: "Marketing_Websites"
"""

RETURN = r"""
api_response:
    description: Serialized object containing the API response.
    type: dict
    returned: always
"""

try:
    from sophosfirewall_python.firewallapi import (
        SophosFirewall,
        SophosFirewallZeroRecords,
        SophosFirewallAuthFailure,
        SophosFirewallAPIError,
    )
    from requests.exceptions import RequestException

    PREREQ_MET = {"result": True}
except ImportError as errMsg:
    PREREQ_MET = {"result": False, "missing_module": errMsg.name}

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.basic import missing_required_lib
from ansible.module_utils.connection import Connection

def get_urlgroup(connection, module, result, name=None):
    """Get URL Group from Sophos Firewall

    Args:
        connection (Connection): Ansible Connection object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console
        name (str, optional): Name of URL group to query. Defaults to None.

    Returns:
        dict: Results of lookup with exists flag and API response
    """
    try:
        if name:
            resp = connection.invoke_sdk("get_urlgroup", module_args={"name": name})
        else:
            resp = connection.invoke_sdk("get_urlgroup", module_args={})
    except Exception as error:
        module.fail_json("An unexpected error occurred: {0}".format(error), **result)

    # Handle case where name is specified but not found
    if name and resp["success"] and not resp["exists"]:
        return {"exists": False, "api_response": resp["response"]}
    
    # Handle errors from API
    if not resp["success"]:
        module.fail_json(msg="An error occurred: {0}".format(resp["response"]))

    # Return successful response
    return {"exists": True, "api_response": resp["response"]}


def make_request(connection, request_method, module, result, **kwargs):
    """Make request to Sophos Firewall API

    Args:
        connection (Connection): HTTPAPI Connection object
        request_method (str): API method to call
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console
        **kwargs: Additional parameters for the API call

    Returns:
        dict: API response
    """
    try:
        resp = connection.invoke_sdk(request_method, module_args=kwargs)
    except Exception as error:
        module.fail_json("An unexpected error occurred: {0}".format(error), **result)
    
    if not resp["success"]:
        module.fail_json(msg="An error occurred: {0}".format(resp["response"]))

    return resp["response"]


def create_urlgroup(connection, module, result, name, domain_list):
    """Create a URL Group on Sophos Firewall

    Args:
        connection (Connection): HTTPAPI Connection object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console
        name (str): Name of URL group
        domain_list (list): List of domains to include in the URL group

    Returns:
        dict: API response
    """
    kwargs = dict(name=name, domain_list=domain_list)
    return make_request(connection, "create_urlgroup", module, result, **kwargs)


def update_urlgroup(connection, module, result, name, domain_list, action):
    """Update a URL Group on Sophos Firewall

    Args:
        connection (Connection): HTTPAPI Connection object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console
        name (str): Name of URL group
        domain_list (list): List of domains for the update operation
        action (str): Action to perform (add, remove, replace)

    Returns:
        dict: API response
    """
    kwargs = dict(name=name, domain_list=domain_list, action=action)
    return make_request(connection, "update_urlgroup", module, result, **kwargs)


def remove_urlgroup(connection, module, result, name):
    """Remove a URL Group from Sophos Firewall

    Args:
        connection (Connection): HTTPAPI Connection object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console
        name (str): Name of URL group to remove

    Returns:
        dict: API response
    """
    kwargs = dict(xml_tag="WebFilterURLGroup", name=name)
    return make_request(connection, "remove", module, result, **kwargs)


def main():
    argument_spec = dict(
        name=dict(type='str', required=False),
        state=dict(type='str', required=True, choices=['query', 'present', 'update', 'absent']),
        domain_list=dict(type='list', elements='str'),
        action=dict(type='str', choices=['add', 'remove', 'replace'])
    )

    required_if = [
        ['state', 'present', ['name', 'domain_list']],
        ['state', 'update', ['name', 'domain_list', 'action']],
        ['state', 'absent', ['name']],
    ]

    module = AnsibleModule(
        argument_spec=argument_spec,
        required_if=required_if,
        supports_check_mode=True
    )

    if not PREREQ_MET["result"]:
        module.fail_json(msg=missing_required_lib(PREREQ_MET["missing_module"]))

    result = {"changed": False, "check_mode": False}
    
    connection = Connection(module._socket_path)
    
    state = module.params.get('state')
    name = module.params.get('name')
    domain_list = module.params.get('domain_list')
    action = module.params.get('action')
    
    if state == 'query':
        if name:
            exist_check = get_urlgroup(connection, module, result, name)
            result["api_response"] = exist_check["api_response"]
        else:
            # Get all URL groups
            try:
                resp = connection.invoke_sdk("get_urlgroup", module_args={})
                result["api_response"] = resp["response"]
            except Exception as error:  # pylint: disable=broad-except
                module.fail_json(msg="An error occurred retrieving URL groups: {0}".format(error), **result)
    
    elif state == 'present':
        # Check if URL group already exists
        exist_check = get_urlgroup(connection, module, result, name)
        
        if not exist_check["exists"]:
            # URL group doesn't exist, create it
            if not module.check_mode:
                api_response = create_urlgroup(connection, module, result, name, domain_list)
                result["api_response"] = api_response
                result["changed"] = True
            else:
                result["check_mode"] = True
                result["changed"] = True
        else:
            # URL group exists, check if it needs updating
            try:
                # Get the latest data directly from the API to ensure we have current state
                get_resp = connection.invoke_sdk("get_urlgroup", module_args={"name": name})
                
                if not get_resp["success"] or not get_resp["exists"]:
                    module.fail_json(msg=f"Failed to retrieve URL group {name} for comparison")
                
                response_data = get_resp["response"]
                webfilter_group = response_data.get("Response", {}).get("WebFilterURLGroup", {})
                
                # Handle both "URLlist" and "URLList" keys (API might use either)
                url_list = webfilter_group.get("URLlist", webfilter_group.get("URLList", {}))
                
                # Extract current domains, handling different API response structures
                if not url_list:
                    current_domains = []
                else:
                    current_domains = url_list.get("URL", [])
                    
                    # Handle case where there's only one domain (returned as string, not list)
                    if not isinstance(current_domains, list):
                        current_domains = [current_domains]
                    
                    # Handle case where empty strings might be returned
                    current_domains = [domain for domain in current_domains if domain]
                
                # Normalize domain lists for proper comparison
                sorted_current = sorted([str(d).strip() for d in current_domains if d])
                sorted_desired = sorted([str(d).strip() for d in domain_list if d])
                
                # Debug information to help troubleshoot domain comparison
                module.debug(f"Current domains: {sorted_current}")
                module.debug(f"Desired domains: {sorted_desired}")
                
                # Compare current and desired domains
                if sorted_current != sorted_desired:
                    if not module.check_mode:
                        api_response = update_urlgroup(connection, module, result, name, domain_list, 'replace')
                        result["api_response"] = api_response
                        result["changed"] = True
                    else:
                        result["check_mode"] = True
                        result["changed"] = True
                else:
                    # No changes needed, URL group exists with the same domains
                    result["api_response"] = response_data
                    result["changed"] = False
            except Exception as error:
                module.fail_json(msg=f"Error comparing URL group domains: {error}", **result)
    
    elif state == 'update':
        # Check if URL group exists
        exist_check = get_urlgroup(connection, module, result, name)
        
        if not exist_check["exists"]:
            module.fail_json(msg="Cannot update non-existent URL group: {}".format(name))
        
        # Perform the update based on the action
        if not module.check_mode:
            api_response = update_urlgroup(connection, module, result, name, domain_list, action)
            result["api_response"] = api_response
            result["changed"] = True
        else:
            result["check_mode"] = True
            result["changed"] = True
    
    elif state == 'absent':
        # Check if URL group exists
        exist_check = get_urlgroup(connection, module, result, name)
        
        if exist_check["exists"]:
            if not module.check_mode:
                api_response = remove_urlgroup(connection, module, result, name)
                result["api_response"] = api_response
                result["changed"] = True
            else:
                result["check_mode"] = True
                result["changed"] = True
        else:
            result["api_response"] = exist_check["api_response"]
    
    module.exit_json(**result)


if __name__ == "__main__":
    main()
