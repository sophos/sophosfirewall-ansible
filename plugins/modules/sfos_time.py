#!/usr/bin/python

# Copyright 2024 Sophos Ltd.  All rights reserved.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: sfos_time

short_description: Manage Date and Time settings (System > Administration > Time)

version_added: "1.0.0"

description: Manage Date and Time settings (System > Administration > Time) on Sophos Firewall. 

extends_documentation_fragment:
  - sophos.sophos_firewall.fragments.base

options:
    timezone:
        description: 
          - "Timezone setting. WARNING: WILL CAUSE DEVICE REBOOT!"
        required: false
        type: str
    date:
        description: 
          - Date settings
        required: false
        type: dict
        suboptions:
            year:
                description:
                  - Year
                type: int
                required: false
            month:
                description: 
                  - Month
                type: int
                required: false
            day:
                description: 
                  - Day
                type: int
                required: false
    time:
        description: 
          - Time settings
        required: false
        type: dict
        suboptions:
            hour:
                description: 
                  - Hour
                type: int
                required: false
            minute:
                description: 
                  - Minute
                type: int
                required: false
            second:
                description: 
                  - Second
                type: int
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
- name: Update Time Settings
  sophos.sophos_firewall.sfos_time:e
    timezone: Europe/London
    date:
      year: 2024
      month: 9
      day: 26
    time:
      hour: 10
      minute: 28
      second: 59
    state: updated
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


def get_time_settings(connection, module, result):
    """Get current time settings from Sophos Firewall

    Args:
        connection (Connection): Ansible Connection object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: Results of lookup
    """
    try:
        resp = connection.invoke_sdk("get_tag", module_args={"xml_tag": "Time"})

    except Exception as error:
        module.fail_json("An unexpected error occurred: {0}".format(error), **result)

    if resp["success"] and not resp["exists"]:
        return {"exists": False, "api_response": resp["response"]}

    if not resp["success"]:
        module.fail_json(msg="An error occurred: {0}".format(resp["response"]))

    return {"exists": True, "api_response": resp["response"]}

def update_time_settings(connection, module, result):
    """Update Time settings on Sophos Firewall

    Args:
        connection (Connection): Ansible Connection object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: API response
    """
    update_params = connection.invoke_sdk("get_tag", module_args={"xml_tag": "Time"})["response"]["Response"]["Time"]

    date_settings = module.params.get("date", {})
    if date_settings:
        year = date_settings.get("year")
        if year:
            update_params["SetDateTime"]["Date"]["Year"] = year

        month = date_settings.get("month")
        if month:
            update_params["SetDateTime"]["Date"]["Month"] = month

        day = date_settings.get("day")
        if day:
            update_params["SetDateTime"]["Date"]["Day"] = day

    time_settings = module.params.get("time", {})
    if time_settings:
        hour = time_settings.get("hour")
        if hour:
            update_params["SetDateTime"]["Time"]["HH"] = hour

        minute = time_settings.get("minute")
        if minute:
            update_params["SetDateTime"]["Time"]["MM"] = minute

        second = time_settings.get("second")
        if second:
            update_params["SetDateTime"]["Time"]["SS"] = second

    if module.params.get("timezone"):
        update_params["TimeZone"] = module.params.get("timezone")

    try:
        resp = connection.invoke_sdk("update", module_args={"xml_tag":"Time", "update_params": update_params})

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
    exist_settings = exist_settings["api_response"]["Response"]["Time"]

    date_settings = module.params.get("date", {})
    if date_settings:
        year = str(module.params["date"].get("year"))
        month = str(module.params["date"].get("month"))
        day = str(module.params["date"].get("day"))

        if (
            year
            and not year == exist_settings["SetDateTime"]["Date"]["Year"]
            or month
            and not month == exist_settings["SetDateTime"]["Date"]["Month"]
            or day
            and not day == exist_settings["SetDateTime"]["Date"]["Day"]
        ):
            return True

    time_settings = module.params.get("time", {})
    if time_settings:
        hour = str(module.params["time"].get("hour"))
        minute = str(module.params["time"].get("minute"))
        second = str(module.params["time"].get("second"))

        if (
            hour
            and not hour == exist_settings["SetDateTime"]["Time"]["HH"]
            or minute
            and not minute == exist_settings["SetDateTime"]["Time"]["MM"]
            or second
            and not second == exist_settings["SetDateTime"]["Time"]["SS"]
        ):
            return True

    timezone = module.params.get("timezone")
    if timezone and not timezone == exist_settings["TimeZone"]:
        return True

    return False


def main():
    """Code executed at run time."""
    argument_spec = {
        "date": {
            "type": "dict",
            "required": False,
            "options": {
                "year": {"type": "int", "required": False},
                "month": {"type": "int", "required": False},
                "day": {"type": "int", "required": False},
            },
        },
        "time": {
            "type": "dict",
            "required": False,
            "options": {
                "hour": {"type": "int", "required": False},
                "minute": {"type": "int", "required": False},
                "second": {"type": "int", "required": False},
            },
        },
        "timezone": {"type": "str", "required": False},
        "state": {"type": "str", "required": True, "choices": ["updated", "query"]},
    }

    module = AnsibleModule(
        argument_spec=argument_spec,
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

    exist_settings = get_time_settings(connection, module, result)
    result["api_response"] = exist_settings["api_response"]

    if state == "query":
        module.exit_json(**result)

    if module.check_mode:
        result["check_mode"] = True
        module.exit_json(**result)

    elif state == "updated":
        if eval_changed(module, exist_settings):
            api_response = update_time_settings(connection, module, result)
            if api_response:
                if (
                    api_response["Response"]["Time"]["Status"]["#text"]
                    == "Configuration applied successfully."
                ):
                    result["changed"] = True
                result["api_response"] = api_response
            else:
                result["changed"] = False

    module.exit_json(**result)


if __name__ == "__main__":
    main()
