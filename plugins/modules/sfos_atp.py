#!/usr/bin/python

# Copyright 2024 Sophos Ltd.  All rights reserved.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: sfos_atp

short_description: Manage Active Threat Protection (Protect > Active threat response > Sophos X-Ops threat feeds)

version_added: "1.0.0"

description: Manage Active Threat Protection (Protect > Active threat response > Sophos X-Ops threat feeds) on Sophos Firewall

extends_documentation_fragment:
  - sophos.sophos_firewall.fragments.base

options:
    enabled: 
        description: Enable (true) or disable (false) threat feeds
        type: bool
        required: false
    inspect_content:
        description: Configure inspection of only untrusted or both trusted and untrusted content
        type: str
        choices: ["all", "untrusted"]
    logging_policy:
        description: Configure logging policy
        type: str
        choices: ["Log only", "Log and Drop"]
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
- name: Update advanced threat protection settings
  sophos.sophos_firewall.sfos_atp:
    enabled: true
    inspect_content: untrusted
    logging_policy: Log and Drop
    state: updated
  vars:
    ansible_command_timeout: 90

- name: Query advanced threat protection settings
  sophos.sophos_firewall.sfos_atp:
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


def get_atp(connection, module, result):
    """Get current malware protection setting from Sophos Firewall

    Args:
        connection (Connection): Ansible Connection object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: Results of lookup
    """
    try:
        resp = connection.invoke_sdk("get_tag", module_args={"xml_tag": "ATP"})
    except Exception as error:
        module.fail_json("An unexpected error occurred: {0}".format(error), **result)

    if resp["success"] and not resp["exists"]:
        return {"exists": False, "api_response": resp["response"]}

    if not resp["success"]:
        module.fail_json(msg="An error occurred: {0}".format(resp["response"]))

    return {"exists": True, "api_response": resp["response"]}



def update_atp(connection, module, result):
    """Update admin settings on Sophos Firewall

    Args:
        connection (Connection): Ansible Connection object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: API response
    """
    update_params = {}
    if module.params.get("enabled"):
        update_params["ThreatProtectionStatus"] = "Enable"
    else:
        update_params["ThreatProtectionStatus"] = "Disable"

    if module.params.get("inspect_content"):
        update_params["InspectContent"] = module.params.get("inspect_content")

    if module.params.get("log_policy"):
        update_params["Policy"] = module.params.get("log_policy")

    try:
        with contextlib.redirect_stdout(output_buffer):
            resp = connection.invoke_sdk("update", module_args={"xml_tag": "ATP", "update_params": update_params, "timeout": 90, "debug": True})
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
    exist_settings = exist_settings["api_response"]["Response"]["ATP"]

    if module.params.get("enabled"):
        status = "Enable"
    else:
        status = "Disable"

    if not (status == exist_settings["ThreatProtectionStatus"]) or (
        not module.params.get("inspect_content") == exist_settings["InspectContent"]
    ):
        return True

    if module.params.get("enabled") and exist_settings.get("Policy"):
        if not module.params.get("log_policy") == exist_settings["Policy"]:
            return True

    if module.params.get("enabled") and not exist_settings.get("Policy"):
        return True

    return False


def main():
    """Code executed at run time."""
    argument_spec = {
        "enabled": {"type": "bool", "required": False},
        "inspect_content": {"type": "str", "choices": ["all", "untrusted"]},
        "log_policy": {"type": "str", "choices": ["Log Only", "Log and Drop"]},
        "state": {"type": "str", "required": True, "choices": ["updated", "query"]},
    }

    required_if = [
        (
            "state",
            "updated",
            [
                "enabled",
            ],
            False,
        ),
        (
            "enabled",
            True,
            [
                "log_policy",
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

    exist_settings = get_atp(connection, module, result)
    result["api_response"] = exist_settings["api_response"]

    if state == "query":
        module.exit_json(**result)

    if module.check_mode:
        result["check_mode"] = True
        module.exit_json(**result)

    elif state == "updated":
        if eval_changed(module, exist_settings):
            api_response = update_atp(connection, module, result)

            if api_response:
                result["api_response"] = api_response
                if (
                    api_response["Response"]["ATP"]["Status"]["#text"]
                    == "Configuration applied successfully."
                ):
                    result["changed"] = True

    module.exit_json(**result)


if __name__ == "__main__":
    main()
