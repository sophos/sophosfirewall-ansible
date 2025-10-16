#!/usr/bin/python

# Copyright 2024 Sophos Ltd.  All rights reserved.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: sfos_notification_target

short_description: Manage Notification Settings (System > Administration > Notification)

version_added: "2.5.0"

description: Manage notification settings for email notifications on Sophos Firewall

extends_documentation_fragment:
  - sophos.sophos_firewall.fragments.base

options:
    mail_server:
        description: Mail server IP address or hostname
        type: str
        required: false
    port:
        description: Mail server port
        type: int
        required: false
        default: 25
    authentication_required:
        description: Enable or disable authentication
        type: bool
        required: false
    oauth2_provider:
        description: OAuth2 provider for authentication
        type: str
        required: false
        choices: ['Gmail', 'Microsoft365']
    username:
        description: Username for mail server authentication
        type: str
        required: false
    password:
        description: Password for mail server authentication
        type: str
        required: false
    subject:
        description: Subject for mail notifications
        type: str
        required: false
    mail_body:
        description: Mail content/body for notifications
        type: str
        required: false
    sender_address:
        description: Sender email address
        type: str
        required: false
    recipient:
        description: Recipient email address
        type: str
        required: false
    connection_security:
        description: Connection security type
        type: str
        required: false
        choices: ['None', 'SSLTLS', 'STARTTLS']
        default: 'None'
    certificate:
        description: Certificate for secure connections
        type: str
        required: false
    management_interface:
        description: Management interface for notifications
        type: str
        required: false
    ip_family:
        description: IP family for connections
        type: str
        required: false
        choices: ['IPv4', 'IPv6']
        default: 'IPv4'
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
- name: Update notification settings
  sophos.sophos_firewall.sfos_notification_target:
    mail_server: "smtp.example.com"
    port: 587
    authentication_required: true
    username: "notifications@example.com"
    password: "secure_password"
    sender_address: "firewall@example.com"
    recipient: "admin@example.com"
    connection_security: "STARTTLS"
    subject: "Firewall Notification"
    mail_body: "This is an automated notification from your firewall."
    ip_family: "IPv4"
    state: updated

- name: Query notification settings
  sophos.sophos_firewall.sfos_notification_target:
    state: query

- name: Configure OAuth2 Gmail notifications
  sophos.sophos_firewall.sfos_notification_target:
    mail_server: "smtp.gmail.com"
    port: 587
    authentication_required: true
    oauth2_provider: "Gmail"
    username: "notifications@example.com"
    password: "app_password"
    sender_address: "firewall@example.com"
    recipient: "admin@example.com"
    connection_security: "STARTTLS"
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


def get_notification_settings(connection, module, result):
    """Get current notification settings from Sophos Firewall

    Args:
        connection (Connection): Ansible Connection object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: Results of lookup
    """
    try:
        resp = connection.invoke_sdk("get_tag", module_args={"xml_tag": "Notification"})
    except Exception as error:
        module.fail_json("An unexpected error occurred: {0}".format(error), **result)

    if resp["success"] and not resp["exists"]:
        return {"exists": False, "api_response": resp["response"]}

    if not resp["success"]:
        module.fail_json(msg="An error occurred: {0}".format(resp["response"]))

    return {"exists": True, "api_response": resp["response"]}


def update_notification_settings(connection, module, result):
    """Update notification settings on Sophos Firewall

    Args:
        connection (Connection): Ansible Connection object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: API response
    """
    update_params = {}
    
    if module.params.get("mail_server"):
        update_params["MailServer"] = module.params.get("mail_server")

    if module.params.get("port"):
        update_params["Port"] = str(module.params.get("port"))

    if module.params.get("authentication_required") is True:
        update_params["AuthenticationRequired"] = "Enable"
    elif module.params.get("authentication_required") is False:
        update_params["AuthenticationRequired"] = "Disable"

    if module.params.get("oauth2_provider"):
        update_params["Oauth2Provider"] = module.params.get("oauth2_provider")

    if module.params.get("username"):
        update_params["Username"] = module.params.get("username")

    if module.params.get("password"):
        update_params["Password"] = module.params.get("password")

    if module.params.get("subject"):
        update_params["Subject"] = module.params.get("subject")

    if module.params.get("mail_body"):
        update_params["MailBody"] = module.params.get("mail_body")

    if module.params.get("sender_address"):
        update_params["SenderAddress"] = module.params.get("sender_address")

    if module.params.get("recipient"):
        update_params["Recepient"] = module.params.get("recipient")  # Note: API uses "Recepient" (typo in API)

    if module.params.get("connection_security"):
        update_params["ConnectionSecurity"] = module.params.get("connection_security")

    if module.params.get("certificate"):
        update_params["Certificate"] = module.params.get("certificate")

    if module.params.get("management_interface"):
        update_params["ManagementInterface"] = module.params.get("management_interface")

    if module.params.get("ip_family"):
        update_params["IPFamily"] = module.params.get("ip_family")

    try:
        with contextlib.redirect_stdout(output_buffer):
            resp = connection.invoke_sdk("update", module_args={
                "xml_tag": "Notification", 
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
        exist_settings (dict): Response from the call to get_notification_settings()

    Returns:
        bool: Return true if any settings are different, otherwise return false
    """
    exist_settings = exist_settings["api_response"]["Response"]["Notification"]

    # Check mail_server
    if module.params.get("mail_server") and module.params.get("mail_server") != exist_settings.get("MailServer"):
        return True

    # Check port
    if module.params.get("port") and str(module.params.get("port")) != exist_settings.get("Port"):
        return True

    # Check authentication_required
    if module.params.get("authentication_required") is not None:
        auth_status = "Enable" if module.params.get("authentication_required") else "Disable"
        if auth_status != exist_settings.get("AuthenticationRequired"):
            return True

    # Check oauth2_provider
    if module.params.get("oauth2_provider") and module.params.get("oauth2_provider") != exist_settings.get("Oauth2Provider"):
        return True

    # Check username
    if module.params.get("username") and module.params.get("username") != exist_settings.get("Username"):
        return True

    # Check password (always consider changed if provided)
    if module.params.get("password"):
        return True

    # Check sender_address
    if module.params.get("sender_address") and module.params.get("sender_address") != exist_settings.get("SenderAddress"):
        return True

    # Check recipient (note API typo: "Recepient")
    if module.params.get("recipient") and module.params.get("recipient") != exist_settings.get("Recepient"):
        return True

    # Check connection_security
    if module.params.get("connection_security") and module.params.get("connection_security") != exist_settings.get("ConnectionSecurity"):
        return True

    # Check certificate
    if module.params.get("certificate") and module.params.get("certificate") != exist_settings.get("Certificate"):
        return True

    # Check management_interface
    if module.params.get("management_interface") and module.params.get("management_interface") != exist_settings.get("ManagementInterface"):
        return True

    # Check ip_family
    if module.params.get("ip_family") and module.params.get("ip_family") != exist_settings.get("IPFamily"):
        return True

    return False


def main():
    """Code executed at run time."""
    argument_spec = {
        "mail_server": {"type": "str", "required": False},
        "port": {"type": "int", "required": False, "default": 25},
        "authentication_required": {"type": "bool", "required": False},
        "oauth2_provider": {"type": "str", "required": False, "choices": ["Gmail", "Microsoft365"]},
        "username": {"type": "str", "required": False},
        "password": {"type": "str", "required": False, "no_log": True},
        "subject": {"type": "str", "required": False},
        "mail_body": {"type": "str", "required": False},
        "sender_address": {"type": "str", "required": False},
        "recipient": {"type": "str", "required": False},
        "connection_security": {"type": "str", "required": False, "choices": ["None", "SSLTLS", "STARTTLS"], "default": "None"},
        "certificate": {"type": "str", "required": False},
        "management_interface": {"type": "str", "required": False},
        "ip_family": {"type": "str", "required": False, "choices": ["IPv4", "IPv6"], "default": "IPv4"},
        "state": {"type": "str", "required": True, "choices": ["updated", "query"]},
    }

    required_if = [
        ("authentication_required", True, ["username"], False),
        ("connection_security", "SSLTLS", ["certificate"], False),
        ("connection_security", "STARTTLS", ["certificate"], False),
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

    exist_settings = get_notification_settings(connection, module, result)
    result["api_response"] = exist_settings["api_response"]

    if state == "query":
        module.exit_json(**result)

    if module.check_mode:
        result["check_mode"] = True
        module.exit_json(**result)

    elif state == "updated":
        if eval_changed(module, exist_settings):
            api_response = update_notification_settings(connection, module, result)

            if api_response:
                result["api_response"] = api_response
                if (
                    api_response["Response"]["Notification"]["Status"]["#text"]
                    == "Configuration applied successfully."
                ):
                    result["changed"] = True

    module.exit_json(**result)


if __name__ == "__main__":
    main()