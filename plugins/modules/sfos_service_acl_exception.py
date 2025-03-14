#!/usr/bin/python

# Copyright 2024 Sophos Ltd.  All rights reserved.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: sfos_service_acl_exception

short_description: Manage Local Service Exception ACL Rules (System > Administration > Device Access)

version_added: "1.0.0"

description: Creates, updates or removes an Local Service Exception Rule (System > Administration > Device Access) on Sophos Firewall

extends_documentation_fragment:
  - sophos.sophos_firewall.fragments.base

options:
    name:
        description: Name of the Local service ACL exception rule to create, update, or delete
        required: true
        type: str
    description:
        description: Description of the Local service ACL exception rule.
        required: false
        type: str
    position:
        description: Position of the rule (Top or Bottom).
        required: false
        type: str
        choices: [top, bottom]
        default: bottom
    source_zone:
        description:
            - Source zone of the Local service ACL exception rule.
        required: false
        type: str
    source_list:
        description:
            - Source Network(s) or Host(s).
        type: list
        required: false
        elements: str
    dest_list:
        description:
            - Destination Host(s).
        type: list
        required: false
        elements: str
    service_list:
        description:
            - Service(s).
        type: list
        required: false
        elements: str
    action:
        description:
            - Accept or Drop. 
        type: str
        choices: [accept, drop]
        required: false
    update_action:
        description:
            - Indicate whether entries specified for source_list, dest_list, or service_list should be added or removed from, or replaced when updating.
        type: str
        choices: [add, remove, replace]
        default: add
        required: false
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
- name: Retrieve Local service ACL exception rule
  sophos.sophos_firewall.sfos_service_acl_exception:
    name: TESTACLRULE
    state: query

- name: Create Local service ACL exception rule
  sophos.sophos_firewall.sfos_service_acl_exception:
    name: TESTACLRULE
    description: Test ACL Rule
    position: bottom
    source_zone: LAN
    source_list:
      - TESTHOST1
      - TESTHOST2
    dest_list:
      - TESTHOST3
    service_list:
      - HTTP
      - HTTPS
    action: drop
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


def get_acl_rule(connection, module, result):
    """Get Local service ACL exception rule from Sophos Firewall

    Args:
        connection (Connection): Ansible Connection object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: Results of lookup
    """
    try:
        resp = connection.invoke_sdk("get_acl_rule", module_args={"name": module.params.get("name")})
    except Exception as error:
        module.fail_json("An unexpected error occurred: {0}".format(error), **result)

    if resp["success"] and not resp["exists"]:
        return {"exists": False, "api_response": resp["response"]}

    if not resp["success"]:
        module.fail_json(msg="An error occurred: {0}".format(resp["response"]))

    return {"exists": True, "api_response": resp["response"]}


def create_acl_rule(connection, module, result):
    """Create an Local service ACL exception rule on Sophos Firewall

    Args:
        connection (Connection): Ansible Connection object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: API response
    """
    try:
        resp = connection.invoke_sdk("create_acl_rule", module_args={
            "name": module.params.get("name"),
            "description": module.params.get("description"),
            "position": module.params.get("position"),
            "source_zone": module.params.get("source_zone"),
            "source_list": module.params.get("source_list"),
            "dest_list": module.params.get("dest_list"),
            "service_list": module.params.get("service_list"),
            "action": module.params.get("action"),
            }
        )
    except Exception as error:
        module.fail_json("An unexpected error occurred: {0}".format(error), **result)

    if not resp["success"]:
        module.fail_json(msg="An error occurred: {0}".format(resp["response"]))

    return resp["response"]


def remove_acl_rule(connection, module, result):
    """Remove an Local service ACL exception rule from Sophos Firewall

    Args:
        connection (Connection): Ansible Connection object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: API response
    """
    try:
        resp = connection.invoke_sdk("remove", module_args={
            "xml_tag": "LocalServiceACL", "name": module.params.get("name"), "key": "RuleName"
            }
        )
    except Exception as error:
        module.fail_json("An unexpected error occurred: {0}".format(error), **result)

    if not resp["success"]:
        module.fail_json(msg="An error occurred: {0}".format(resp["response"]))

    return resp["response"]


def update_acl_rule(connection, module, result):
    """Update an existing Local service ACL exception rule on Sophos Firewall

    Args:
        connection (Connection): Ansible Connection object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: API response
    """
    try:
        resp = connection.invoke_sdk("update_acl_rule", module_args={
            "name": module.params.get("name"),
            "description": module.params.get("description"),
            "source_zone": module.params.get("source_zone"),
            "source_list": module.params.get("source_list"),
            "dest_list": module.params.get("dest_list"),
            "service_list": module.params.get("service_list"),
            "action": module.params.get("action"),
            "update_action": module.params.get("update_action"),
            }
        )
    except Exception as error:
        module.fail_json("An unexpected error occurred: {0}".format(error), **result)

    if not resp["success"]:
        module.fail_json(msg="An error occurred: {0}".format(resp["response"]))

    return resp["response"]


def eval_list(list1, list2, condition):
    """Evaluate whether contents of list1 exist in list2, or contents of list1 do not exist in list2.

    Args:
        list1 (list): List of strings
        list2 (list): List of strings
        condition (str): If set to 'positive', will return true if any elements in list1 are in list2.
        If set to 'negative', will return true if any elements in list1 are NOT in list2.
    """
    for item in list1:
        if condition == "positive":
            if item in list2:
                return True
        if condition == "negative":
            if item not in list2:
                return True
    return False


def main():
    """Code executed at run time."""
    argument_spec = {
        "name": {"required": True},
        "description": {"type": "str", "default": None},
        "position": {"type": "str", "default": "bottom"},
        "source_zone": {"type": "str"},
        "source_list": {"type": "list", "default": [], "elements": "str"},
        "dest_list": {"type": "list", "default": [], "elements": "str"},
        "service_list": {"type": "list", "default": [], "elements": "str"},
        "action": {"type": "str", "choices": ["accept", "drop"], "default": None},
        "update_action": {
            "type": "str",
            "choices": ["add", "remove", "replace"],
            "default": "add",
        },
        "state": {
            "required": True,
            "choices": ["present", "absent", "updated", "query"],
        },
    }
    required_if = [("state", "updated", ("update_action",), True)]

    module = AnsibleModule(
        argument_spec=argument_spec, required_if=required_if, supports_check_mode=True
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

    exist_check = get_acl_rule(connection, module, result)
    result["api_response"] = exist_check["api_response"]

    if state == "query":
        module.exit_json(**result)

    if module.check_mode:
        result["check_mode"] = True
        module.exit_json(**result)

    if state == "present" and not exist_check["exists"]:
        api_response = create_acl_rule(connection, module, result)
        if (
            api_response["Response"]["LocalServiceACL"]["Status"]["#text"]
            == "Configuration applied successfully."
        ):
            result["changed"] = True
            result["api_response"] = api_response

    elif state == "present" and exist_check["exists"]:
        result["changed"] = False

    elif state == "absent" and exist_check["exists"]:
        api_response = remove_acl_rule(connection, module, result)
        if (
            api_response["Response"]["LocalServiceACL"]["Status"]["#text"]
            == "Configuration applied successfully."
        ):
            result["changed"] = True
        result["api_response"] = api_response

    elif state == "absent" and not exist_check["exists"]:
        result["changed"] = False

    elif state == "updated" and exist_check["exists"]:
        new_source_list = sorted(module.params.get("source_list"))
        if new_source_list:
            new_source_list = sorted(new_source_list)
        exist_source_list = exist_check["api_response"]["Response"]["LocalServiceACL"][
            "Hosts"
        ]["Host"]
        if isinstance(exist_source_list, str):
            exist_source_list = [exist_source_list]
        else:
            exist_source_list = sorted(exist_source_list)

        new_dest_list = sorted(module.params.get("dest_list"))
        if new_dest_list:
            new_dest_list = sorted(new_dest_list)
        if "DstHost" in exist_check["api_response"]["Response"]["LocalServiceACL"]["Hosts"]:
            exist_dest_list = exist_check["api_response"]["Response"]["LocalServiceACL"]["Hosts"]["DstHost"]
        else:
            exist_dest_list = []
        if isinstance(exist_dest_list, str):
            exist_dest_list = [exist_dest_list]
        else:
            exist_dest_list = sorted(exist_dest_list)

        new_service_list = module.params.get("service_list")
        if new_service_list:
            new_service_list = sorted(new_service_list)
        exist_service_list = exist_check["api_response"]["Response"]["LocalServiceACL"][
            "Services"
        ]["Service"]
        if isinstance(exist_service_list, str):
            exist_service_list = [exist_service_list]
        else:
            exist_service_list = sorted(exist_service_list)

        exist_description = exist_check["api_response"]["Response"]["LocalServiceACL"][
            "Description"
        ]
        exist_source_zone = exist_check["api_response"]["Response"]["LocalServiceACL"][
            "SourceZone"
        ]
        exist_action = exist_check["api_response"]["Response"]["LocalServiceACL"][
            "Action"
        ]

        if (
            (
                module.params.get("description")
                and exist_description != module.params.get("description")
            )
            or (
                module.params.get("source_zone")
                and exist_source_zone != module.params.get("source_zone")
            )
            or (
                module.params.get("action")
                and exist_action != module.params.get("action")
            )
            or (
                new_source_list
                and module.params.get("update_action") == "add"
                and eval_list(new_source_list, exist_source_list, "negative")
            )
            or (
                new_dest_list
                and module.params.get("update_action") == "add"
                and eval_list(new_dest_list, exist_dest_list, "negative")
            )
            or (
                new_service_list
                and module.params.get("update_action") == "add"
                and eval_list(new_service_list, exist_service_list, "negative")
            )
            or (
                new_source_list
                and module.params.get("update_action") == "remove"
                and eval_list(new_source_list, exist_source_list, "positive")
            )
            or (
                new_dest_list
                and module.params.get("update_action") == "remove"
                and eval_list(new_dest_list, exist_dest_list, "positive")
            )
            or (
                new_service_list
                and module.params.get("update_action") == "remove"
                and eval_list(new_service_list, exist_service_list, "positive")
            )
            or (
                new_source_list
                and module.params.get("update_action") == "replace"
                and new_source_list != exist_source_list
            )
            or (
                new_dest_list
                and module.params.get("update_action") == "replace"
                and new_dest_list != exist_dest_list
            )
            or (
                new_service_list
                and module.params.get("update_action") == "replace"
                and new_service_list != exist_service_list
            )
        ):
            api_response = update_acl_rule(connection, module, result)
            if (
                api_response["Response"]["LocalServiceACL"]["Status"]["#text"]
                == "Configuration applied successfully."
            ):
                result["changed"] = True
            result["api_response"] = api_response

    elif state == "updated" and not exist_check["exists"]:
        result["changed"] = False
        module.fail_json(exist_check["api_response"], **result)

    module.exit_json(**result)


if __name__ == "__main__":
    main()
