#!/usr/bin/python

# Copyright 2024 Sophos Ltd.  All rights reserved.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: sfos_ips

short_description: Manage IPS protection (Protect > Intrusion Protection > IPS policies)

version_added: "1.2.0"

description: Manage IPS protection (Protect > Intrusion Protection > IPS policies) on Sophos Firewall

extends_documentation_fragment:
  - sophos.sophos_firewall.fragments.base

options:
    enabled: 
        description: Enable (true) or disable (false) IPS protection
        type: bool
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
- name: Enable IPS protection
  sophos.sophos_firewall.sfos_ips:
    username: "{{ username }}"
    password: "{{ password }}"
    hostname: "{{ inventory_hostname }}"
    port: 4444
    verify: false
    enabled: true
    state: updated
  delegate_to: localhost

- name: Query IPS protection settings
  sophos.sophos_firewall.sfos_ips:
    username: "{{ username }}"
    password: "{{ password }}"
    hostname: "{{ inventory_hostname }}"
    port: 4444
    verify: false
    state: query
  delegate_to: localhost
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


def get_ips(fw_obj, module, result):
    """Get current ips protection setting from Sophos Firewall

    Args:
        fw_obj (SophosFirewall): SophosFirewall object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: Results of lookup
    """
    try:
        resp = fw_obj.get_tag("IPSSwitch")
    except SophosFirewallZeroRecords as error:
        return {"exists": False, "api_response": str(error)}
    except SophosFirewallAuthFailure as error:
        module.fail_json(msg="Authentication error: {0}".format(error), **result)
    except SophosFirewallAPIError as error:
        module.fail_json(msg="API Error: {0}".format(error), **result)
    except RequestException as error:
        module.fail_json(msg="Error communicating to API: {0}".format(error), **result)

    return {"exists": True, "api_response": resp}


def update_ips(fw_obj, module, result):
    """Update admin settings on Sophos Firewall

    Args:
        fw_obj (SophosFirewall): SophosFirewall object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: API response
    """
    update_params = {}
    if module.params.get("enabled"):
        update_params["Status"] = "Enable"
    else:
        update_params["Status"] = "Disable"

    try:
        with contextlib.redirect_stdout(output_buffer):
            resp = fw_obj.update(xml_tag="IPSSwitch", update_params=update_params, debug=True)
    except SophosFirewallAuthFailure as error:
        module.fail_json(msg="Authentication error: {0}".format(error), **result)
    except SophosFirewallAPIError as error:
        module.fail_json(
            msg="API Error: {0},{1}".format(error, output_buffer.getvalue()), **result
        )
    except RequestException as error:
        module.fail_json(msg="Error communicating to API: {0}".format(error), **result)
    return resp


def eval_changed(module, exist_settings):
    """Evaluate the provided arguments against existing settings.

    Args:
        module (AnsibleModule): AnsibleModule object
        exist_settings (dict): Response from the call to get_admin_settings()

    Returns:
        bool: Return true if any settings are different, otherwise return false
    """
    exist_settings = exist_settings["api_response"]["Response"]["IPSSwitch"]

    if module.params.get("enabled"):
        status = "Enable"
    else:
        status = "Disable"

    if not status == exist_settings["Status"]:
        return True

    return False


def main():
    """Code executed at run time."""
    argument_spec = {
        "username": {"required": True},
        "password": {"required": True, "no_log": True},
        "hostname": {"required": True},
        "port": {"type": "int", "default": 4444},
        "verify": {"type": "bool", "default": True},
        "enabled": {"type": "bool", "required": False},
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
    ]

    module = AnsibleModule(
        argument_spec=argument_spec, required_if=required_if, supports_check_mode=True
    )

    if not PREREQ_MET["result"]:
        module.fail_json(msg=missing_required_lib(PREREQ_MET["missing_module"]))

    fw = SophosFirewall(
        username=module.params.get("username"),
        password=module.params.get("password"),
        hostname=module.params.get("hostname"),
        port=module.params.get("port"),
        verify=module.params.get("verify"),
    )

    result = {"changed": False, "check_mode": False}

    state = module.params.get("state")

    exist_settings = get_ips(fw, module, result)
    result["api_response"] = exist_settings["api_response"]

    if state == "query":
        module.exit_json(**result)

    if module.check_mode:
        result["check_mode"] = True
        module.exit_json(**result)

    elif state == "updated":
        if eval_changed(module, exist_settings):
            api_response = update_ips(fw, module, result)

            if api_response:
                result["api_response"] = api_response
                if (
                    api_response["Response"]["IPSSwitch"]["Status"]["#text"]
                    == "Configuration applied successfully."
                ):
                    result["changed"] = True

    module.exit_json(**result)


if __name__ == "__main__":
    main()
