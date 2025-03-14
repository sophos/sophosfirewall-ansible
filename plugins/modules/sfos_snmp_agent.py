#!/usr/bin/python

# Copyright 2024 Sophos Ltd.  All rights reserved.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: sfos_snmp_agent

short_description: Manage SNMP Agent (System > Administration > SNMP)

version_added: "1.1.0"

description: Manage SNMP Agent (System > Administration > SNMP) on Sophos Firewall

extends_documentation_fragment:
  - sophos.sophos_firewall.fragments.base

options:
    enabled: 
        description: Enable (true) or disable (false) threat feeds
        type: bool
        required: false
    name:
        description: Identifying name of firewall
        type: str
        required: false
    description:
        description: Description assigned to SNMP agent
        type: str
        required: false
    location:
        description: SNMP location
        type: str
        required: false
    contact_person:
        description: SNMP contact
        type: str
        required: false
    state:
        description:
            - Use C(query) to retrieve or C(updated) to modify
        choices: [updated, query]
        type: str
        required: true

author:
    - Matt Mullen (@mamullen13316)
"""

EXAMPLES = r"""
- name: Update SNMP agent configuration
  sophos.sophos_firewall.sfos_snmp_agent:
    enabled: true
    name: testfirewall
    description: Firewall used for automation testing
    location: AWS
    contact_person: Network Operations
    state: updated

- name: Query SNMP settings
  sophos.sophos_firewall.sfos_snmp_agent:
    state: query
"""

RETURN = r"""
api_response:
    description: Serialized object containing the API response.
    type: dict
    returned: always

"""
import io
import contextlib

output_buffer = io.StringIO()

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


def get_snmp_agent(connection, module, result):
    """Get current SNMP agent settings from Sophos Firewall

    Args:
        connection (Connection): Ansible Connection object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: Results of lookup
    """
    try:
        resp = connection.invoke_sdk("get_tag", module_args={"xml_tag": "SNMPAgentConfiguration"})
    except Exception as error:
        module.fail_json("An unexpected error occurred: {0}".format(error), **result)

    if resp["success"] and not resp["exists"]:
        return {"exists": False, "api_response": resp["response"]}

    if not resp["success"]:
        module.fail_json(msg="An error occurred: {0}".format(resp["response"]))

    return {"exists": True, "api_response": resp["response"]}


def update_snmp_agent(connection, module, result):
    """Update SNMP agent configuration on Sophos Firewall

    Args:
        connection (Connection): Ansible Connection object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: API response
    """
    update_params = {}
    if module.params.get("enabled") is True:
        update_params["Configuration"] = "Enable"
    elif module.params.get("enabled") is False:
        update_params["Configuration"] = "Disable"

    if module.params.get("description"):
        update_params["Description"] = module.params.get("description")

    if module.params.get("name"):
        update_params["Name"] = module.params.get("name")

    if module.params.get("location"):
        update_params["Location"] = module.params.get("location")

    if module.params.get("contact_person"):
        update_params["ContactPerson"] = module.params.get("contact_person")

    try:
        with contextlib.redirect_stdout(output_buffer):
            resp = connection.invoke_sdk("update", module_args={
                "xml_tag": "SNMPAgentConfiguration", 
                "update_params": update_params,
                "debug": True
                }
            )
    except Exception as error:
        module.fail_json("An unexpected error occurred: {0}".format(error), **result)

    if not resp["success"]:
        module.fail_json(msg="An error occurred: {0}".format(resp["response"]))

    return resp["response"]


def eval_changed(module, exist_settings):
    """Evaluate the provided arguments against existing settings.

    Args:
        module (AnsibleModule): AnsibleModule object
        exist_settings (dict): Response from the call to get_admin_settings()

    Returns:
        bool: Return true if any settings are different, otherwise return false
    """
    exist_settings = exist_settings["api_response"]["Response"]["SNMPAgentConfiguration"]

    if module.params.get("enabled"):
        status = "Enable"
    else:
        status = "Disable"

    if not status == exist_settings["Configuration"] or (
        module.params.get("location") and not module.params.get("location") == exist_settings["Location"] or
        module.params.get("name") and not module.params.get("name") == exist_settings["Name"] or
        module.params.get("description") and not module.params.get("description") == exist_settings["Description"] or
        module.params.get("contact_person") and not module.params.get("contact_person") == exist_settings["ContactPerson"]
        ):
        return True

    return False


def main():
    """Code executed at run time."""
    argument_spec = {
        "enabled": {"type": "bool", "required": False},
        "name": {"type": "str", "required": False},
        "description": {"type": "str", "required": False},
        "location": {"type": "str", "required": False},
        "contact_person": {"type": "str", "required": False},
        "state": {"type": "str", "required": True, "choices": ["updated", "query"]},
    }

    required_if = [
        (
            "enabled",
            True,
            [
                "name",
                "location",
                "contact_person"
            ],
            False,
        ),
    ]

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

    exist_settings = get_snmp_agent(connection, module, result)
    result["api_response"] = exist_settings["api_response"]

    if state == "query":
        module.exit_json(**result)

    if module.check_mode:
        result["check_mode"] = True
        module.exit_json(**result)

    elif state == "updated":
        if eval_changed(module, exist_settings):
            api_response = update_snmp_agent(connection, module, result)

            if api_response:
                result["api_response"] = api_response
                if (
                    api_response["Response"]["SNMPAgentConfiguration"]["Status"]["#text"]
                    == "Configuration applied successfully."
                ):
                    result["changed"] = True

    module.exit_json(**result)


if __name__ == "__main__":
    main()
