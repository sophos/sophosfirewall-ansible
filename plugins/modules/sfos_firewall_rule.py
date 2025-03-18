#!/usr/bin/python

# Copyright 2024 Sophos Ltd.  All rights reserved.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: sfos_firewall_rule

short_description: Manage Firewall Rules (Protect > Rules & policies)

version_added: "1.0.0"

description: Creates, updates or removes firewall rules (Protect > Rules & policies) on Sophos Firewall

extends_documentation_fragment:
  - sophos.sophos_firewall.fragments.base

options:
    name:
        description: Name of the firewall rule to create, update, or delete
        required: true
        type: str
    status:
        description: Enabled or Disabled state of the rule
        choices: ["enable", "disable"]
        type: str
        required: false
    position:
        description: Indicates where the rule should be inserted.
        choices: ["top", "bottom", "after", "before"]
        type: str
        required: false
        default: bottom
    after_rulename:
        description:
            - Name of the rule to insert this rule after.
        required: false
        type: str
    before_rulename:
        description:
            - Name of the rule to insert this rule before.
        required: false
        type: str
    action:
        description:
            - The rule action.
        choices: ["accept", "drop", "reject"]
        required: true
        type: str
    log:
        description:
            - Enable or disable logging.
        choices: ["enable", "disable"]
        required: true
        type: str
    description:
        description:
            - Rule description.
        required: true
        type: str
    src_zones:
        description:
            - Source zone(s).
        required: true
        type: list
        elements: str
    dst_zones:
        description:
            - Destination zone(s).
        required: true
        type: list
        elements: str
    src_networks:
        description:
            - Source network(s). 
        required: true
        type: list
        elements: str
    dst_networks:
        description:
            - Destination network(s).
        type: list
        elements: str
    service_list:
        description:
            - Name of service(s).
        type: list
        elements: str
    state:
        description:
            - Use C(query) to retrieve, C(present) to create, C(absent) to remove, or C(updated) to modify
        choices: [present, absent, updated, query]
        type: str
        required: true

author:
    - Matt Mullen (@mamullen13316)
"""

EXAMPLES = r"""
- name: Create Firewall Rule
  sophos.sophos_firewall.sfos_firewall_rule:
    name: TEST RULE 100
    after_rulename: TEST RULE 99
    action: accept
    description: Test rule created by Ansible
    log: enable
    status: enable
    position: bottom
    src_zones:
      - LAN
    dst_zones:
      - WAN
    src_networks:
      - SRCNET1
      - SRCNET2
    dst_networks:
      - DSTNET1
      - DSTNET2
    service_list:
      - HTTPS
      - SSH
    state: present
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


def get_firewallrule(connection, module, result):
    """Get firewall rule from Sophos Firewall

    Args:
        connection (Connection): Ansible Connection object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: Results of lookup
    """
    try:
        resp = connection.invoke_sdk("get_rule", module_args={"name":module.params.get("name")})
    except Exception as error:
        module.fail_json("An unexpected error occurred: {0}".format(error), **result)

    if resp["success"] and not resp["exists"]:
        return {"exists": False, "api_response": resp["response"]}

    if not resp["success"]:
        module.fail_json(msg="An error occurred: {0}".format(resp["response"]))

    return {"exists": True, "api_response": resp["response"]}

def create_firewallrule(connection, module, result):
    """Create a firewall rule on Sophos Firewall.

    Args:
        connection (Connection): Ansible Connection object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: API response
    """
    src_zones = module.params.get("src_zones")
    if src_zones:
        if "any" in [item.lower() for item in src_zones]:
            src_zones = []
    dst_zones = module.params.get("dst_zones")
    if dst_zones:
        if "any" in [item.lower() for item in dst_zones]:
            dst_zones = []
    src_networks = module.params.get("src_networks")
    if src_networks:
        if "any" in [item.lower() for item in src_networks]:
            src_networks = []
    dst_networks = module.params.get("dst_networks")
    if dst_networks:
        if "any" in [item.lower() for item in dst_networks]:
            dst_networks = []
    service_list = module.params.get("service_list")
    if service_list:
        if "any" in [item.lower() for item in service_list]:
            service_list = []

    rule_params = {
        "rulename": module.params.get("name"),
        "status": module.params.get("status").capitalize()
        if module.params.get("status")
        else None,
        "position": module.params.get("position").capitalize()
        if module.params.get("position")
        else None,
        "after_rulename": module.params.get("after_rulename"),
        "before_rulename": module.params.get("before_rulename"),
        "action": module.params.get("action").capitalize()
        if module.params.get("action")
        else None,
        "log": module.params.get("log").capitalize()
        if module.params.get("log")
        else None,
        "description": module.params.get("description"),
        "src_zones": src_zones,
        "dst_zones": dst_zones,
        "src_networks": src_networks,
        "dst_networks": dst_networks,
        "service_list": service_list,
    }

    try:
        resp = connection.invoke_sdk("create_rule", module_args={"rule_params":rule_params})
    except Exception as error:
        module.fail_json("An unexpected error occurred: {0}".format(error), **result)

    if not resp["success"]:
        module.fail_json(msg="An error occurred: {0}".format(resp["response"]))

    return resp["response"]


def remove_firewallrule(connection, module, result):
    """Remove a firewall rule from Sophos Firewall.

    Args:
        connection (Connection): Ansible Connection object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: API response
    """
    try:
        resp = connection.invoke_sdk("remove", module_args={"xml_tag": "FirewallRule", "name": module.params.get("name")})
    except Exception as error:
        module.fail_json("An unexpected error occurred: {0}".format(error), **result)

    if not resp["success"]:
        module.fail_json(msg="An error occurred: {0}".format(resp["response"]))

    return resp["response"]


def update_firewallrule(connection, module, result):
    """Update an existing firewall rule on Sophos Firewall

    Args:
        connection (Connection): Ansible Connection object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: API response
    """
    rule_params = {
        "rulename": module.params.get("name"),
        "status": module.params.get("status").capitalize()
        if module.params.get("status")
        else None,
        "position": module.params.get("position"),
        "after_rulename": module.params.get("after_rulename"),
        "before_rulename": module.params.get("before_rulename"),
        "action": module.params.get("action").capitalize()
        if module.params.get("action")
        else None,
        "log": module.params.get("log").capitalize()
        if module.params.get("log")
        else None,
        "description": module.params.get("description"),
        "src_zones": module.params.get("src_zones"),
        "dst_zones": module.params.get("dst_zones"),
        "src_networks": module.params.get("src_networks"),
        "dst_networks": module.params.get("dst_networks"),
        "service_list": module.params.get("service_list"),
    }
    try:
        resp = connection.invoke_sdk("update_rule", module_args={
            "name": module.params.get("name"), "rule_params": rule_params
            }
        )
    except Exception as error:
        module.fail_json("An unexpected error occurred: {0}".format(error), **result)

    if not resp["success"]:
        module.fail_json(msg="An error occurred: {0}".format(resp["response"]))

    return resp["response"]


def main():
    """Code executed at run time."""
    argument_spec = {
        "name": {"required": True},
        "status": {"choices": ["enable", "disable"]},
        "position": {
            "choices": ["top", "bottom", "after", "before"],
            "default": "bottom",
        },
        "after_rulename": {"type": "str"},
        "before_rulename": {"type": "str"},
        "action": {"choices": ["accept", "drop", "reject"]},
        "description": {"type": "str"},
        "log": {"choices": ["enable", "disable"]},
        "src_zones": {"type": "list", "elements": "str"},
        "dst_zones": {"type": "list", "elements": "str"},
        "src_networks": {"type": "list", "elements": "str"},
        "dst_networks": {"type": "list", "elements": "str"},
        "service_list": {"type": "list", "elements": "str"},
        "state": {
            "required": True,
            "choices": ["present", "absent", "updated", "query"],
        },
    }

    required_if = [
        ("position", "after", ("after_rulename",), True),
        ("position", "before", ("before_rulename",), True),
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

    exist_check = get_firewallrule(connection, module, result)
    result["api_response"] = exist_check["api_response"]

    if state == "query":
        module.exit_json(**result)

    if module.check_mode:
        result["check_mode"] = True
        module.exit_json(**result)

    if state == "present" and not exist_check["exists"]:
        api_response = create_firewallrule(connection, module, result)
        if (
            api_response["Response"]["FirewallRule"]["Status"]["#text"]
            == "Configuration applied successfully."
        ):
            result["changed"] = True
            result["api_response"] = api_response

    elif state == "present" and exist_check["exists"]:
        result["changed"] = False

    elif state == "absent" and exist_check["exists"]:
        api_response = remove_firewallrule(connection, module, result)
        if (
            api_response["Response"]["FirewallRule"]["Status"]["#text"]
            == "Configuration applied successfully."
        ):
            result["changed"] = True
        result["api_response"] = api_response

    elif state == "absent" and not exist_check["exists"]:
        result["changed"] = False

    elif state == "updated" and exist_check["exists"]:
        api_response = update_firewallrule(connection, module, result)

        if api_response:
            if (
                api_response["Response"]["FirewallRule"]["Status"]["#text"]
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
