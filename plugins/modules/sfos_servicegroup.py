#!/usr/bin/python

# Copyright 2024 Sophos Ltd.  All rights reserved.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: sfos_servicegroup

short_description: Manage Service Group (System > Hosts and services > Service Group) 

version_added: "1.0.0"

description: Creates, updates or removes a Service Group (System > Hosts and services > Service Group) on Sophos Firewall

extends_documentation_fragment:
  - sophos.sophos_firewall.fragments.base

options:
    name:
        description: Name of the Service Group object to create, update, or delete
        required: true
        type: str
    description:
        description:
            - Description to be included on the Service Group object.
        required: false
        type: str
    service_list:
        description:
            - List of Service objects to be included in the Servicegroup
        type: list
        required: false
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
- name: Retrieve Service Group
  sophos.sophos_firewall.sfos_servicegroup:
    name: TESTSERVICEGROUP
    state: query

- name: Create Service Group
  sophos.sophos_firewall.sfos_servicegroup:
    name: TESTSERVICEGROUP
    description: Test Service Group
    service_list:
      - HTTP
      - HTTPS
    state: present

- name: Add Services to Service Group
  sophos.sophos_firewall.sfos_servicegroup:
    name: TESTSERVICEGROUP
    description: Test Host Group
    service_list:
      - TESTSERVICE3
      - TESTSERVICE4
    action: add
    state: updated
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


def get_servicegroup(connection, module, result):
    """Get Service Group from Sophos Firewall

    Args:
        connection (Connection): Ansible Connection object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: Results of lookup
    """
    try:
        resp = connection.invoke_sdk("get_service_group", module_args={"name": module.params.get("name")})
    except Exception as error:
        module.fail_json("An unexpected error occurred: {0}".format(error), **result)

    if resp["success"] and not resp["exists"]:
        return {"exists": False, "api_response": resp["response"]}

    if not resp["success"]:
        module.fail_json(msg="An error occurred: {0}".format(resp["response"]))

    return {"exists": True, "api_response": resp["response"]}


def create_servicegroup(connection, module, result):
    """Create an Service Group on Sophos Firewall

    Args:
        connection (Connection): Ansible Connection object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: API response
    """
    try:
        resp = connection.invoke_sdk("create_service_group", module_args={
            "name": module.params.get("name"),
            "description": module.params.get("description"),
            "service_list": module.params.get("service_list"),
            }
        )
    except Exception as error:
        module.fail_json("An unexpected error occurred: {0}".format(error), **result)

    if not resp["success"]:
        module.fail_json(msg="An error occurred: {0}".format(resp["response"]))

    return resp["response"]



def remove_servicegroup(connection, module, result):
    """Remove an Service Group from Sophos Firewall

    Args:
        connection (Connection): Ansible Connection object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: API response
    """
    try:
        resp = connection.invoke_sdk("remove", module_args={"xml_tag": "ServiceGroup", "name": module.params.get("name")})
    except Exception as error:
        module.fail_json("An unexpected error occurred: {0}".format(error), **result)

    if not resp["success"]:
        module.fail_json(msg="An error occurred: {0}".format(resp["response"]))

    return resp["response"]

def update_servicegroup(connection, module, result):
    """Update an existing Service Group on Sophos Firewall

    Args:
        connection (Connection): Ansible Connection object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: API response
    """
    try:
        resp = connection.invoke_sdk("update_service_group", module_args={
            "name": module.params.get("name"),
            "service_list": module.params.get("service_list"),
            "description": module.params.get("description"),
            "action": module.params.get("action"),
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
        "description": {"type": "str", "default": None},
        "service_list": {"type": "list", "default": [], "elements": "str"},
        "action": {
            "type": "str",
            "choices": ["add", "remove", "replace"],
            "default": None,
        },
        "state": {
            "required": True,
            "choices": ["present", "absent", "updated", "query"],
        },
    }
    required_if = [
        ("state", "present", ("service_list",), True),
        ("state", "updated", ("action",), True),
    ]

    module = AnsibleModule(
        argument_spec=argument_spec, required_if=required_if, supports_check_mode=True
    )

    if not PREREQ_MET["result"]:
        module.fail_json(msg=missing_required_lib(PREREQ_MET["missing_module"]))

    result = {"changed": False, "check_mode": False}

    try:
        connection = Connection(module._socket_path)
    except AssertionError as e:
        module.fail_json(msg="Connection error: Ensure you are targeting a remote host and not using 'delegate_to: localhost'.")

    if not hasattr(connection, "httpapi"):
        module.fail_json(msg="HTTPAPI plugin is not initialized. Ensure the connection is set to 'httpapi'.")

    state = module.params.get("state")
    exist_check = get_servicegroup(connection, module, result)
    result["api_response"] = exist_check["api_response"]

    if state == "query":
        module.exit_json(**result)

    if module.check_mode:
        result["check_mode"] = True
        module.exit_json(**result)

    if state == "present" and not exist_check["exists"]:
        api_response = create_servicegroup(connection, module, result)
        if (
            api_response["Response"]["ServiceGroup"]["Status"]["#text"]
            == "Configuration applied successfully."
        ):
            result["changed"] = True
            result["api_response"] = api_response

    elif state == "present" and exist_check["exists"]:
        result["changed"] = False

    elif state == "absent" and exist_check["exists"]:
        api_response = remove_servicegroup(connection, module, result)
        if (
            api_response["Response"]["ServiceGroup"]["Status"]["#text"]
            == "Configuration applied successfully."
        ):
            result["changed"] = True
        result["api_response"] = api_response

    elif state == "absent" and not exist_check["exists"]:
        result["changed"] = False

    elif state == "updated" and exist_check["exists"]:
        if sorted(
            exist_check["api_response"]["Response"]["ServiceGroup"]["ServiceList"][
                "Service"
            ]
        ) != sorted(module.params.get("service_list")):
            api_response = update_servicegroup(connection, module, result)
            if (
                api_response["Response"]["ServiceGroup"]["Status"]["#text"]
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
