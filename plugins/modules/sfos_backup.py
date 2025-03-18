#!/usr/bin/python

# Copyright 2024 Sophos Ltd.  All rights reserved.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
from ipaddress import ip_address

__metaclass__ = type

DOCUMENTATION = r"""
---
module: sfos_backup

short_description: Manage Backup settings (System > Backup & firmware)

version_added: "1.0.0"

description: Manage Backup settings (System > Backup & firmware) on Sophos Firewall

extends_documentation_fragment:
  - sophos.sophos_firewall.fragments.base

options:
    mode:
        description: 
          - Backup mode (Local/FTP/Email)
        choices: ["Local", "FTP", "Email"]
        required: false
        type: str
    prefix:
        description: 
          - Prefix for the backup file
        required: false
        type: str
    frequency:
        description: 
          - Backup frequency (Never/Daily/Weekly/Monthly)
        choices: ["Never", "Daily", "Email"]
        required: false
        type: str
    day:
        description: 
            - Day
        type: str
        choices: ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        required: false
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
    date:
        description:
            - Day of month to be used when frequency is set to monthly
        type: int
        required: false
    ftp_server:
        description:
            - IP address of FTP server (hostname not currently allowed)
        type: str
        required: false
    ftp_username:
        description:
            - FTP username
        type: str
        required: false
    ftp_password:
        description:
            - "FTP password. If this argument is specified, module will always return changed."
        type: str
        required: false
    ftp_path:
        description:
            - FTP directory path
        type: str
        required: false
    email_address:
        description:
            - Email address to be used when using Email mode
        type: str
        required: false
    encryption_password:
        description:
            - "Encryption password for the backup file. If this argument is specified, module will always return changed."
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
- name: Update Backup Settings
  sophos.sophos_firewall.sfos_backup:
    mode: FTP
    prefix: devfirewall
    ftp_server: 10.10.10.1
    ftp_username: ftpuser
    ftp_password: ftppassword
    ftp_path: home/backup
    frequency: Weekly
    day: Sunday
    hour: 10
    minute: 30
    encryption_password: backupencryptionpassword
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


def get_backup(connection, module, result):
    """Get current backup settings from Sophos Firewall

    Args:
        connection (Connection): Ansible Connection object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: Results of lookup
    """
    try:
        resp = connection.invoke_sdk("get_backup")
    except Exception as error:
        module.fail_json("An unexpected error occurred: {0}".format(error), **result)

    if resp["success"] and not resp["exists"]:
        return {"exists": False, "api_response": resp["response"]}

    if not resp["success"]:
        module.fail_json(msg="An error occurred: {0}".format(resp["response"]))

    return {"exists": True, "api_response": resp["response"]}


def update_backup(connection, module, result):
    """Update Time settings on Sophos Firewall

    Args:
        connection (Connection): Ansible Connection object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: API response
    """
    backup_params = {}
    mode = module.params.get("mode")
    if mode:
        backup_params["BackupMode"] = mode

    if module.params.get("prefix"):
        backup_params["BackupPrefix"] = module.params.get("prefix")

    if mode == "FTP":
        backup_params["FTPServer"] = module.params.get("ftp_server")
        backup_params["Username"] = module.params.get("ftp_username")
        backup_params["Password"] = module.params.get("ftp_password")
        backup_params["FtpPath"] = module.params.get("ftp_path")

    if mode == "Mail":
        backup_params["EmailAddress"] = module.params.get("email_address")

    frequency = module.params.get("frequency")

    if frequency:
        backup_params["BackupFrequency"] = frequency

    if frequency and not frequency == "Never":
        backup_params["Hour"] = module.params.get("hour")
        backup_params["Minute"] = module.params.get("minute")

    if frequency == "Weekly":
        backup_params["Day"] = module.params.get("day")

    if frequency == "Monthly":
        backup_params["Date"] = module.params.get("date")

    if module.params.get("encryption_password"):
        backup_params["EncryptionPassword"] = module.params.get("encryption_password")

    try:
        with contextlib.redirect_stdout(output_buffer):
            resp = connection.invoke_sdk("update_backup", module_args={
                "backup_params": backup_params, "debug": module.params.get("debug", False)
                }
            )
    except Exception as error:
        module.fail_json("An unexpected error occurred: {0}".format(error), **result)

    if resp["success"] and not resp["exists"]:
        return {"exists": False, "api_response": resp["response"]}

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
    

    exist_settings = exist_settings["api_response"]["Response"]["BackupRestore"].get(
        "ScheduleBackup"
    )
    # FTP Password and Encryption password must be ignored because they are encrypted in the API response
    exist_settings.pop("Password")
    exist_settings.pop("EncryptionPassword")
    # FTP path is ignored for comparison because it retains the previously set value in the API response.
    exist_settings.pop("FtpPath")

    ansible_args = {
        "BackupMode": module.params.get("mode"),
        "BackupPrefix": module.params.get("prefix"),
        "Username": module.params.get("ftp_username"),
        "FTPServer": module.params.get("ftp_server"),
        "EmailAddress": module.params.get("email_address"),
        "BackupFrequency": module.params.get("frequency"),
        "Day": module.params.get("day"),
        "Hour": str(module.params["hour"]) if module.params.get("hour") else None,
        "Minute": str(module.params.get("minute"))
        if module.params.get("minute")
        else None,
        "Date": str(module.params.get("date")) if module.params.get("date") else None,
    }
    if (
        module.params.get("ftp_password")
        or module.params.get("encryption_password")
        or module.params.get("ftp_path")
    ):
        return True

    if not exist_settings == ansible_args:
        return True

    return False


def main():
    """Code executed at run time."""
    argument_spec = {
        "mode": {"type": "str", "choices": ["Local", "FTP", "Mail"], "required": False},
        "prefix": {"type": "str", "required": False},
        "ftp_server": {"type": "str", "required": False},
        "ftp_username": {"type": "str", "required": False},
        "ftp_password": {"type": "str", "required": False, "no_log": True},
        "ftp_path": {"type": "str", "required": False},
        "email_address": {"type": "str", "required": False},
        "frequency": {
            "type": "str",
            "choices": ["Never", "Daily", "Weekly", "Monthly"],
        },
        "date": {"type": "int", "required": False},
        "day": {"type": "str", "required": False},
        "hour": {"type": "int", "required": False},
        "minute": {"type": "int", "required": False},
        "encryption_password": {"type": "str", "required": False, "no_log": True},
        "state": {"type": "str", "required": True, "choices": ["updated", "query"]},
        "debug": {"type": "bool", "required": False},
    }

    required_if = [
        (
            "mode",
            "FTP",
            ["ftp_server", "ftp_username", "ftp_password", "ftp_path"],
            False,
        ),
        ("mode", "Mail", ["email_address"], False),
        ("frequency", "Daily", ["hour", "minute"], False),
        ("frequency", "Weekly", ["day", "hour", "minute"], False),
        ("frequency", "Monthly", ["date", "hour", "minute"], False),
    ]

    mutually_exclusive = [["day", "date"]]

    module = AnsibleModule(
        argument_spec=argument_spec,
        required_if=required_if,
        mutually_exclusive=mutually_exclusive,
        supports_check_mode=True,
    )
    if (
        module.params.get("encryption_password")
        and len(module.params.get("encryption_password")) < 12
    ):
        module.fail_json(msg="Encryption password must be minimum of 12 characters")

    if module.params.get("ftp_server"):
        try:
            ip_address(module.params.get("ftp_server"))
        except ValueError:
            module.fail_json(msg="FTP server must be an IP address")

    if not PREREQ_MET["result"]:
        module.fail_json(msg=missing_required_lib(PREREQ_MET["missing_module"]))

    try:
        connection = Connection(module._socket_path)
    except AssertionError as e:
        module.fail_json(msg="Connection error: Ensure you are targeting a remote host and not using 'delegate_to: localhost'.")

    if not hasattr(connection, "httpapi"):
        module.fail_json(msg="HTTPAPI plugin is not initialized. Ensure the connection is set to 'httpapi'.")

    result = {"changed": False, "check_mode": False}

    state = module.params.get("state")

    exist_settings = get_backup(connection, module, result)
    result["api_response"] = exist_settings["api_response"]

    if state == "query":
        module.exit_json(**result)

    if module.check_mode:
        result["check_mode"] = True
        module.exit_json(**result)

    elif state == "updated":
        if eval_changed(module, exist_settings):
            api_response = update_backup(connection, module, result)
            if api_response:
                if (
                    api_response["Response"]["BackupRestore"]["Status"]["#text"]
                    == "Configuration applied successfully."
                ):
                    result["changed"] = True
                result["api_response"] = api_response
            else:
                result["changed"] = False

    module.exit_json(**result)


if __name__ == "__main__":
    main()
