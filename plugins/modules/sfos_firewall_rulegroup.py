#!/usr/bin/python

# Copyright 2024 Sophos Ltd.  All rights reserved.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: sfos_firewall_rulegroup

short_description: Manage Firewall Rules (Protect > Rules & policies)

version_added: "1.4.0"

description: Creates, updates or removes firewall rule groups (Protect > Rules & policies) on Sophos Firewall

extends_documentation_fragment:
  - sophos.sophos_firewall.fragments.base

options:
    name:
        description: Name of the firewall rule group to create, update, or delete
        required: true
        type: str
    description:
        description: Rule group description
        type: str
        required: false
    policy_list:
        description: List of firewall rules to be added to the group
        type: list
        elements: str
        required: false
    source_zones:
        description:
            - Source zones for the rule group
        required: false
        type: list
        elements: str
    dest_zones:
        description:
            - Destination zones for the rule group
        required: false
        type: str
        elements: str
    policy_type:
        description:
            - Type of policy
        choices: ["User/network rule", "Network rule", "User rule", "WAF rule", "Any"]
        required: false
        type: str
        default: "Any"
    source_zone_action:
        description:
            - Indicate whether adding to, removing from, or replacing the list of source zones. Default is add.
        choices: ["add", "remove", "replace"]
        required: false
        type: str
        default: add
    dest_zone_action:
        description:
            - Indicate whether adding to, removing from, or replacing the list of destination zones. Default is add.
        choices: ["add", "remove", "replace"]
        required: false
        type: str
        default: add
    state:
        description:
            - Use C(query) to retrieve, C(present) to create, C(absent) to remove, or C(updated) to modify
        choices: [present, updated, query]
        type: str
        required: true

author:
    - Matt Mullen (@mamullen13316)
"""

EXAMPLES = r"""
- name: Create Firewall Rule Group
  sophos.sophos_firewall.sfos_firewall_rulegroup:
    name: TEST RULEGROUP
    description: Test rule group created by Ansible
    policy_list:
      - TEST RULE 1
      - TEST RULE 2
    policy_type: Any
    source_zones:
      - LAN
    dest_zones:
      - WAN
    state: present
  delegate_to: localhost
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


def get_firewallrulegroup(connection, module, result):
    """Get firewall rule group from Sophos Firewall

    Args:
        connection (Connection): Ansible Connection object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: Results of lookup
    """
    try:
        resp = connection.invoke_sdk("get_rulegroup", module_args={"name": module.params.get("name")})
    except Exception as error:
        module.fail_json("An unexpected error occurred: {0}".format(error), **result)

    if resp["success"] and not resp["exists"]:
        return {"exists": False, "api_response": resp["response"]}

    if not resp["success"]:
        module.fail_json(msg="An error occurred: {0}".format(resp["response"]))

    return {"exists": True, "api_response": resp["response"]}


def create_firewallrulegroup(connection, module, result):
    """Create a firewall rule group on Sophos Firewall.

    Args:
        connection (Connection): Ansible Connection object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: API response
    """
    params = dict(
        name=module.params.get("name"),
        description=module.params.get("description"),
        policy_list=module.params.get("policy_list"),
        source_zones=module.params.get("source_zones"),
        dest_zones=module.params.get("dest_zones"),
        policy_type=module.params.get("policy_type")
    )
    try:
        resp = connection.invoke_sdk("create_rulegroup", module_args=params)
    except Exception as error:
        module.fail_json("An unexpected error occurred: {0}".format(error), **result)

    if not resp["success"]:
        module.fail_json(msg="An error occurred: {0}".format(resp["response"]))

    return resp["response"]


def update_firewallrulegroup(connection, module, result):
    """Update an existing firewall rule group on Sophos Firewall

    Args:
        connection (Connection): Ansible Connection object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: API response
    """
    params = dict(
        name=module.params.get("name"),
        description=module.params.get("description"),
        policy_list=module.params.get("policy_list"),
        source_zones=module.params.get("source_zones"),
        dest_zones=module.params.get("dest_zones"),
        policy_type=module.params.get("policy_type"),
        source_zone_action=module.params.get("source_zone_action"),
        dest_zone_action=module.params.get("dest_zone_action")
    )

    try:
        resp = connection.invoke_sdk("update_rulegroup", module_args=params)
    except Exception as error:
        module.fail_json("An unexpected error occurred: {0}".format(error), **result)

    if not resp["success"]:
        module.fail_json(msg="An error occurred: {0}".format(resp["response"]))

    return resp["response"]


def main():
    """Code executed at run time."""
    argument_spec = {
        "name": {"type": "str", "required": True},
        "description": {"type": "str"},
        "policy_list": {"type": "list", "elements": "str"},
        "source_zones": {"type": "list", "elements": "str"},
        "dest_zones": {"type": "list", "elements": "str"},
        "policy_type": {"type": "str", "choices": ["User/network rule", "Network rule", "User rule", "WAF rule", "Any"]},
        "source_zone_action": {"type": "str", "choices": ["add", "remove", "replace"], "default": "add"},
        "dest_zone_action": {"type": "str", "choices": ["add", "remove", "replace"], "default": "add"},
        "state": {
            "required": True,
            "choices": ["present", "updated", "query"],
        },
    }

    required_if = [
        ("state", "present", ("policy_list", "source_zones", "dest_zones",), True),
    ]


    module = AnsibleModule(
        argument_spec=argument_spec,
        required_if=required_if,
        supports_check_mode=True,
    )

    if not PREREQ_MET["result"]:
        module.fail_json(msg=missing_required_lib(PREREQ_MET["missing_module"]))

    result = {"changed": False, "check_mode": False}

    state = module.params.get("state")

    try:
        connection = Connection(module._socket_path)
    except AssertionError as e:
        module.fail_json(msg="Connection error: Ensure you are targeting a remote host and not using 'delegate_to: localhost'.")

    if not hasattr(connection, "httpapi"):
        module.fail_json(msg="HTTPAPI plugin is not initialized. Ensure the connection is set to 'httpapi'.")

    exist_check = get_firewallrulegroup(connection, module, result)
    result["api_response"] = exist_check["api_response"]

    if state == "query":
        module.exit_json(**result)

    if module.check_mode:
        result["check_mode"] = True
        module.exit_json(**result)

    if state == "present" and not exist_check["exists"]:
        api_response = create_firewallrulegroup(connection, module, result)
        if (
            api_response["Response"]["FirewallRuleGroup"]["Status"]["#text"]
            == "Configuration applied successfully."
        ):
            result["changed"] = True
            result["api_response"] = api_response

    elif state == "present" and exist_check["exists"]:
        result["changed"] = False

    elif state == "updated" and exist_check["exists"]:
        api_response = update_firewallrulegroup(connection, module, result)

        if api_response:
            if (
                api_response["Response"]["FirewallRuleGroup"]["Status"]["#text"]
                == "Configuration applied successfully."
            ):
                result["changed"] = True
            result["api_response"] = api_response
        else:
            result["changed"] = False

    elif state == "updated" and not exist_check["exists"]:
        result["changed"] = False
        module.fail_json(exist_check["api_response"], **result)

    module.exit_json(**result)


if __name__ == "__main__":
    main()
