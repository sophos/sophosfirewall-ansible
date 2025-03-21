#!/usr/bin/python

# Copyright 2024 Sophos Ltd.  All rights reserved.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: sfos_user

short_description: Manage Users (Configure > Authentication > Users)

version_added: "1.0.0"

description: Creates, updates or removes Users (Configure > Authentication > Users) on Sophos Firewall

extends_documentation_fragment:
  - sophos.sophos_firewall.fragments.base

options:
    user:
        description: Username to create, update, or delete.
        required: true
        type: str
    name:
        description: User display name.
        type: str
        required: false
    description:
        description: User description.
        type: str
        required: false
    user_password:
        description:
            - User password.
        required: false
        type: str
    user_type:
        description:
            - Type of user (Administrator/User).
        choices: ["Administrator", "User"]
        required: false
        type: str
    profile:
        description:
            - Profile name.
        required: false
        type: str
    group:
        description:
            - Group name.
        required: false
        type: str
    email:
        description:
            - User email address.
        required: false
        type: str
    access_time_policy:
        description:
            - Access time policy name.
        required: false
        type: str
        default: Allowed all the time
    sslvpn_policy:
        description:
            - SSL VPN Policy name.
        required: false
        type: str
        default: No Policy Applied
    clientless_policy:
        description:
            - Clientless VPN policy. 
        required: false
        type: str
        default: No Policy Applied
    l2tp:
        description:
            - Enable/Disable l2tp.
        type: str
        choices: ["Enable", "Disable"]
        default: Disable
    pptp:
        description:
            - Enable/Disable pptp.
        type: str
        choices: ["Enable", "Disable"]
        default: Disable
    cisco:
        description:
            - Enable/Disable Cisco.
        type: str
        choices: ["Enable", "Disable"]
        default: Disable
    quarantine_digest:
        description:
            - Enable/Disable Quarantine Digest.
        type: str
        choices: ["Enable", "Disable"]
        default: Disable
    mac_binding:
        description:
            - Enable/Disable MAC binding.
        type: str
        choices: ["Enable", "Disable"]
        default: Disable
    login_restriction:
        description:
            - Login Restriction for user.
        type: str
        default: UserGroupNode
    isencryptcert:
        description:
            - Enable/Disable encrypted cert.
        type: str
        choices: ["Enable", "Disable"]
        default: Disable
    simultaneous_logins:
        description:
            - Enable/Disable simultaneous logins
        choices: ["Enable", "Disable"]
    surfingquota_policy:
        description:
            - Surfing quota policy name.
        type: str
        default: Unlimited Internet Access
    applianceaccess_schedule:
        description:
            - Name of appliance access schedule.
        type: str
        default: All The Time
    appliance_login_restriction:
        description:
            - Login restriction for appliance.
        type: str
        default: AnyNode
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
- name: Create User
  sophos.sophos_firewall.sfos_user:
    user: testuser
    name: Test User
    description: Testing user creation from Ansible
    user_password: Sup3rS3cr3tP@ssw0rd
    user_type: User
    group: Open Group
    email: test.user@sophos.com
    state: present
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


def get_user(connection, module, result):
    """Get user from Sophos Firewall

    Args:
        connection (Connection): Ansible Connection object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: Results of lookup
    """
    try:
        resp = connection.invoke_sdk("get_user", module_args={"username": module.params.get("user")})
    except Exception as error:
        module.fail_json("An unexpected error occurred: {0}".format(error), **result)

    if resp["success"] and not resp["exists"]:
        return {"exists": False, "api_response": resp["response"]}

    if not resp["success"]:
        module.fail_json(msg="An error occurred: {0}".format(resp["response"]))

    return {"exists": True, "api_response": resp["response"]}


def create_user(connection, module, result):
    """Create a user on Sophos Firewall.

    Args:
        connection (Connection): Ansible Connection object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: API response
    """
    user_params = {
        "user": module.params.get("user"),
        "name": module.params.get("name"),
        "description": module.params.get("description"),
        "user_password": module.params.get("user_password"),
        "user_type": module.params.get("user_type"),
        "profile": module.params.get("profile"),
        "group": module.params.get("group"),
        "email": module.params.get("email"),
        "access_time_policy": module.params.get("access_time_policy"),
        "sslvpn_policy": module.params.get("sslvpn_policy"),
        "clientless_policy ": module.params.get("clientless_policy"),
        "l2tp": module.params.get("l2tp"),
        "pptp": module.params.get("pptp"),
        "cisco": module.params.get("cisco"),
        "quarantine_digest": module.params.get("quarantine_digest"),
        "mac_binding": module.params.get("mac_binding"),
        "login_restriction": module.params.get("login_restriction"),
        "isencryptcert": module.params.get("isencryptcert"),
        "simultaneous_logins": module.params.get("simultaneous_logins"),
        "surfingquota_policy": module.params.get("surfingquota_policy"),
        "applianceaccess_schedule": module.params.get("applianceaccess_schedule"),
        "login_restriction": module.params.get("appliance_login_restriction")
        if module.params.get("user_type") == "Administrator"
        else module.params.get("login_restriction"),
    }

    try:
        with contextlib.redirect_stdout(output_buffer):
            resp = connection.invoke_sdk("create_user", module_args={"debug": True, **user_params})
    except Exception as error:
        module.fail_json("An unexpected error occurred: {0}".format(error), **result)

    if not resp["success"]:
        module.fail_json(msg="An error occurred: {0}".format(resp["response"]))

    return resp["response"]


def remove_user(connection, module, result):
    """Remove a user from Sophos Firewall.

    Args:
        connection (Connection): Ansible Connection object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: API response
    """
    try:
        resp = connection.invoke_sdk("remove", module_args={"xml_tag": "User", "name": module.params.get("user")})
    except Exception as error:
        module.fail_json("An unexpected error occurred: {0}".format(error), **result)

    if not resp["success"]:
        module.fail_json(msg="An error occurred: {0}".format(resp["response"]))

    return resp["response"]


def update_user(connection, module, result):
    """Update an existing user on Sophos Firewall

    Args:
        connection (Connection): Ansible Connection object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: API response
    """
    user_params = {
        "Username": module.params.get("user"),
        "Name": module.params.get("name"),
        "Description": module.params.get("description"),
        "Password": module.params.get("user_password"),
        "UserType": module.params.get("user_type"),
        "Profile": module.params.get("profile"),
        "Group": module.params.get("group"),
        "EmailList": {"EmailID": module.params.get("email")}
        if module.params.get("email")
        else None,
        "AccessTimePolicy": module.params.get("access_time_policy"),
        "SSLVPNPolicy": module.params.get("sslvpn_policy"),
        "ClientlessPolicy": module.params.get("clientless_policy"),
        "L2TP": module.params.get("l2tp"),
        "PPTP": module.params.get("pptp"),
        "CISCO": module.params.get("cisco"),
        "QuarantineDigest": module.params.get("quarantine_digest"),
        "MACBinding": module.params.get("mac_binding"),
        "LoginRestriction": module.params.get("login_restriction"),
        "IsEncryptCert": module.params.get("isencryptcert"),
        "SimultaneousLoginsGlobal": module.params.get("simultaneous_logins"),
        "SurfingQuotaPolicy": module.params.get("surfingquota_policy"),
        "ScheduleForApplianceAccess": module.params.get("applianceaccess_schedule"),
        "LoginRestrictionForAppliance": module.params.get(
            "appliance_login_restriction"
        ),
    }
    # Remove any keys with null values
    user_params = {key: value for key, value in user_params.items() if value}

    try:
        if module.params.get("user_password"):
            with contextlib.redirect_stdout(output_buffer):
                resp = connection.invoke_sdk("update_user_password", module_args={
                    "username": module.params.get("user"),
                    "new_password": module.params.get("user_password"),
                    "debug": True,
                    }
                )
                
        with contextlib.redirect_stdout(output_buffer):
            resp = connection.invoke_sdk("update", module_args={
                "xml_tag": "User",
                "update_params": user_params,
                "name": module.params.get("name"),
                "debug": True,
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
        "user": {"type": "str", "required": True},
        "name": {"type": "str"},
        "description": {"type": "str"},
        "user_password": {"type": "str", "no_log": True},
        "user_type": {"type": "str", "choices": ["Administrator", "User"]},
        "profile": {"type": "str"},
        "group": {"type": "str"},
        "email": {"type": "str"},
        "access_time_policy": {"type": "str", "default": "Allowed all the time"},
        "sslvpn_policy": {"type": "str", "default": "No Policy Applied"},
        "clientless_policy": {"type": "str", "default": "No Policy Applied"},
        "l2tp": {"type": "str", "choices": ["Enable", "Disable"], "default": "Disable"},
        "pptp": {"type": "str", "choices": ["Enable", "Disable"], "default": "Disable"},
        "cisco": {
            "type": "str",
            "choices": ["Enable", "Disable"],
            "default": "Disable",
        },
        "quarantine_digest": {
            "type": "str",
            "choices": ["Enable", "Disable"],
            "default": "Disable",
        },
        "mac_binding": {
            "type": "str",
            "choices": ["Enable", "Disable"],
            "default": "Disable",
        },
        "login_restriction": {"type": "str", "default": "UserGroupNode"},
        "isencryptcert": {
            "type": "str",
            "choices": ["Enable", "Disable"],
            "default": "Disable",
        },
        "simultaneous_logins": {"type": "str", "choices": ["Enable", "Disable"]},
        "surfingquota_policy": {"type": "str", "default": "Unlimited Internet Access"},
        "applianceaccess_schedule": {"type": "str", "default": "All The Time"},
        "appliance_login_restriction": {"type": "str", "default": "AnyNode"},
        "state": {
            "type": "str",
            "required": True,
            "choices": ["present", "absent", "updated", "query"],
        },
    }

    required_if = [
        ("state", "present", ["user_password", "user_type", "group", "email"], False),
        ("user_type", "Administrator", ["profile"], True),
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

    exist_check = get_user(connection, module, result)
    result["api_response"] = exist_check["api_response"]

    if state == "query":
        module.exit_json(**result)

    if module.check_mode:
        result["check_mode"] = True
        module.exit_json(**result)

    if state == "present" and not exist_check["exists"]:
        api_response = create_user(connection, module, result)
        if (
            api_response["Response"]["User"]["Status"]["#text"]
            == "Configuration applied successfully."
        ):
            result["changed"] = True
            result["api_response"] = api_response

    elif state == "present" and exist_check["exists"]:
        result["changed"] = False

    elif state == "absent" and exist_check["exists"]:
        api_response = remove_user(connection, module, result)
        if (
            api_response["Response"]["User"]["Status"]["#text"]
            == "Configuration applied successfully."
        ):
            result["changed"] = True
        result["api_response"] = api_response

    elif state == "absent" and not exist_check["exists"]:
        result["changed"] = False

    elif state == "updated" and exist_check["exists"]:
        api_response = update_user(connection, module, result)

        if api_response:
            if (
                api_response["Response"]["User"]["Status"]["#text"]
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
