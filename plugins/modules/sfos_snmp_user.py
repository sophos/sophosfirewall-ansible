#!/usr/bin/python

# Copyright 2024 Sophos Ltd.  All rights reserved.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: sfos_snmp_user

short_description: Manage SNMPv3 User (System > Administration > SNMP)

version_added: "1.1.0"

description: Manage SNMP User (System > Administration > SNMP) on Sophos Firewall

extends_documentation_fragment:
  - sophos.sophos_firewall.fragments.base

options:
    name:
        description: SNMPv3 Username
        type: str
        required: false
    accept_queries:
        description: Enable or Disable querying
        type: str
        choices: ["Enable", "Disable"]
        required: false
    send_traps:
        description: Enable or Disable sending of SNMP traps
        type: str
        choices: ["Enable", "Disable"]
        required: false
    authorized_hosts:
        description: List of authorized hosts
        type: list
        elements: str
        required: false
    encryption_algorithm:
        description: Encryption algorithm
        type: str
        choices: ["AES", "DES", "None"]
        required: false
    encryption_password:
        description: Encryption password
        type: str
        required: false
    authentication_algorithm:
        description: Authentication algorithm
        type: str
        choices: ["MD5", "SHA256", "SHA512"]
        required: false
    authentication_password:
        description: Authentication password
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
- name: Add SNMPv3 User
  sophos.sophos_firewall.sfos_snmp_user:
    enabled: true
    name: snmpv3user
    send_queries: Enable
    send_traps: Disable
    authorized_hosts:
        - 10.100.1.104
        - 10.100.1.105
    encryption_algorithm: AES
    encryption_password: "{{ encryption_password }}"
    authentication_algorithm: MD5
    authentication_password: "{{ authentication_password }}"
    state: present 

- name: Query SNMPv3 User
  sophos.sophos_firewall.sfos_snmp_user:
    username: "{{ username }}"
    password: "{{ password }}"
    hostname: "{{ inventory_hostname }}"
    port: 4444
    verify: false
    name: snmpv3user
    state: query

- name: Update SNMPv3 User
  sophos.sophos_firewall.sfos_snmp_user:
    enabled: true
    name: snmpv3user
    send_queries: Disable
    encryption_algorithm: AES
    encryption_password: "{{ encryption_password }}"
    authentication_password: "{{ authentication_password }}"
    state: present

- name: Remove SNMPv3 User
  sophos.sophos_firewall.sfos_snmp_user:
    enabled: true
    name: snmpv3user
    state: absent
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


def get_snmp_user(connection, module, result):
    """Get SNMP user from Sophos Firewall

    Args:
        connection (Connection): Ansible Connection object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: Results of lookup
    """
    try:
        resp = connection.invoke_sdk("get_tag_with_filter", module_args={"xml_tag": "SNMPv3User",
                                                                         "key": "Username",
                                                                         "value": module.params.get("name")})
    except Exception as error:
        module.fail_json("An unexpected error occurred: {0}".format(error), **result)

    if resp["success"] and not resp["exists"]:
        return {"exists": False, "api_response": resp["response"]}

    if not resp["success"]:
        module.fail_json(msg="An error occurred: {0}".format(resp["response"]))

    return {"exists": True, "api_response": resp["response"]}

def create_snmp_user(connection, module, result, api_version):
    """Create an SNMPv3 User on Sophos Firewall

    Args:
        connection (Connection): Ansible Connection object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console
        api_version (str): API version of the Sophos Firewall

    Returns:
        dict: API response
    """
    payload = """
        <SNMPv3User>
          <Username>{{ name }}</Username>
          {% if api_version.startswith("22") %}
          <Name>{{ name }}</Name>
          {% endif %}
          <AcceptQueries>{{ accept_queries }}</AcceptQueries>
          <SendTraps>{{ send_traps }}</SendTraps>
          {% for host in authorized_hosts %}
          {% if api_version.startswith("22") %}
          <AuthorizedHostsIpv4>{{ host }}</AuthorizedHostsIpv4>
            {% else %}
          <AuthorizedHosts>{{ host }}</AuthorizedHosts>
          {% endif %}
          {% endfor %}
          {% if api_version.startswith("22") %}
          <AuthorizedHostsIpv6></AuthorizedHostsIpv6>
          {% endif %}
          {% if encryption_algorithm == 'AES' %}
          <EncryptionAlgorithm>1</EncryptionAlgorithm>
          {% elif encryption_algorithm == 'DES' %}
          <EncryptionAlgorithm>2</EncryptionAlgorithm>
          {% elif encryption_algorithm == 'None' %}
          <EncryptionAlgorithm>3</EncryptionAlgorithm>
          {% endif %}
          <EncryptionPassword>{{ encryption_password }}</EncryptionPassword>
          {% if authentication_algorithm == 'MD5' %}
          <AuthenticationAlgorithm>1</AuthenticationAlgorithm>
          {% elif encryption_algorithm == 'SHA256' %}
          <AuthenticationAlgorithm>2</AuthenticationAlgorithm>
          {% elif encryption_algorithm == 'SHA512' %}
          <AuthenticationAlgorithm>3</AuthenticationAlgorithm>
          {% endif %}
          <AuthenticationPassword>{{ authentication_password }}</AuthenticationPassword>
        </SNMPv3User>
    """
    
    if api_version.startswith("22"):
        accept_queries = "true" if module.params.get("accept_queries") == "Enable" else "false"
        send_traps = "true" if module.params.get("send_traps") == "Enable" else "false"
    else:
        accept_queries = module.params.get("accept_queries")
        send_traps = module.params.get("send_traps")

    template_vars = {
        "api_version": api_version,
        "name": module.params.get("name"),
        "accept_queries": accept_queries,
        "send_traps": send_traps,
        "authorized_hosts": module.params.get("authorized_hosts"),
        "encryption_algorithm": module.params.get("encryption_algorithm"),
        "encryption_password": module.params.get("encryption_password"),
        "authentication_algorithm": module.params.get("authentication_algorithm"),
        "authentication_password": module.params.get("authentication_password")
    }

    try:
        with contextlib.redirect_stdout(output_buffer):
            resp = connection.invoke_sdk("submit_xml", module_args={
                "template_data": payload,
                "template_vars": template_vars,
                "debug": True
                }
            )
    except Exception as error:
        module.fail_json("An unexpected error occurred: {0}".format(error), **result)

    if not resp["success"]:
        module.fail_json(msg="An error occurred: {0}".format(resp["response"]))

    return resp["response"]

def update_snmp_user(connection, exist_settings, module, result, api_version):
    """Update SNMPv3 user configuration on Sophos Firewall

    Args:
        connection (Connection): Ansible Connection object
        exist_settings (dict): API response containing existing SNMPv3 user
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console
        api_version (str): API version of the Sophos Firewall

    Returns:
        dict: API response
    """
    update_params = {}
    
    update_params["Username"] = module.params.get("name")

    if api_version.startswith("22"):
        if module.params.get("accept_queries"):
            accept_queries = "true" if module.params.get("accept_queries") == "Enable" else "false"
            update_params["AcceptQueries"] = accept_queries

        if module.params.get("send_traps"):
            send_traps = "true" if module.params.get("send_traps") == "Enable" else "false"
            update_params["SendTraps"] = send_traps
    else:
        if module.params.get("accept_queries"):
            update_params["AcceptQueries"] = module.params.get("accept_queries")

        if module.params.get("send_traps"):
            update_params["SendTraps"] = module.params.get("send_traps")

    if module.params.get("authorized_hosts"):
        if api_version.startswith("22"):
            auth_hosts_key = "AuthorizedHostsIpv4"
        else:
            auth_hosts_key = "AuthorizedHosts"
        if isinstance(exist_settings["Response"]["SNMPv3User"][auth_hosts_key], str):
            update_params[auth_hosts_key] = [exist_settings["Response"]["SNMPv3User"][auth_hosts_key]]
            for host in module.params.get("authorized_hosts"):
                if not host in exist_settings["Response"]["SNMPv3User"][auth_hosts_key]:
                    update_params[auth_hosts_key].append(host)
        if isinstance(exist_settings["Response"]["SNMPv3User"][auth_hosts_key], list):
            host_list = exist_settings["Response"]["SNMPv3User"][auth_hosts_key]
            for host in module.params.get("authorized_hosts"):
                if not host in host_list:
                    host_list.append(host)
            update_params[auth_hosts_key] = host_list
    
    if module.params.get("encryption_algorithm"):
        encr_algo = module.params.get("encryption_algorithm")
        if encr_algo == "AES":
            update_params["EncryptionAlgorithm"] = "1"
        if encr_algo == "DES":
            update_params["EncryptionAlgorithm"] = "2"
        if encr_algo == "None":
            update_params["EncryptionAlgorithm"] = "3"
    
    if module.params.get("encryption_password"):
        update_params["EncryptionPassword"] = module.params.get("encryption_password")
    
    if module.params.get("authentication_algorithm"):
        auth_algo = module.params.get("authentication_algorithm")
        if auth_algo == "MD5":
            update_params["AuthenticationAlgorithm"] = "1"
        if auth_algo == "SHA256":
            update_params["AuthenticationAlgorithm"] = "2"
        if auth_algo == "SHA512":
            update_params["AuthenticationAlgorithm"] = "3"

    if module.params.get("authentication_password"):
        update_params["AuthenticationPassword"] = module.params.get("authentication_password")
    try:
        with contextlib.redirect_stdout(output_buffer):
            resp = connection.invoke_sdk("update", module_args={"xml_tag": "SNMPv3User",
                                 "update_params": update_params,
                                 "name": module.params.get("name"),
                                 "lookup_key": "Username",
                                 "debug": True})
    except Exception as error:
        module.fail_json("An unexpected error occurred: {0}".format(error), **result)

    if not resp["success"]:
        module.fail_json(msg="An error occurred: {0}".format(resp["response"]))

    return resp["response"]

def eval_changed(module, exist_settings, api_version):
    """Evaluate the provided arguments against existing settings.

    Args:
        module (AnsibleModule): AnsibleModule object
        exist_settings (dict): Response from the call to get_admin_settings()
        api_version (str): API version of the Sophos Firewall

    Returns:
        bool: Return true if any settings are different, otherwise return false
    """
    exist_settings = exist_settings["api_response"]["Response"]["SNMPv3User"]

    if api_version.startswith("22"):
        if module.params.get("accept_queries"):
            accept_queries = "true" if module.params.get("accept_queries") == "Enable" else "false"
        else:
            accept_queries = None
        if module.params.get("send_traps"):
            send_traps = "true" if module.params.get("send_traps") == "Enable" else "false"
        else:
            send_traps = None
    else:
        accept_queries = module.params.get("accept_queries")
        send_traps = module.params.get("send_traps")

    if (accept_queries and not accept_queries == exist_settings["AcceptQueries"] or
        send_traps and not send_traps == exist_settings["SendTraps"]
        ):
        return True

    if module.params.get("encryption_algorithm") == "AES":
        if not exist_settings["EncryptionAlgorithm"] == "1":
            return True
    
    if module.params.get("encryption_algorithm") == "DES":
        if not exist_settings["EncryptionAlgorithm"] == "2":
            return True

    if module.params.get("encryption_algorithm") == "None":
        if not exist_settings["EncryptionAlgorithm"] == "3":
            return True
    
    if module.params.get("encryption_password"):
        return True
    
    if module.params.get("authentication_algorithm") == "MD5":
        if not exist_settings["AuthenticationAlgorithm"] == "1":
            return True
    
    if module.params.get("authentication_algorithm") == "SHA256":
        if not exist_settings["AuthenticationAlgorithm"] == "2":
            return True

    if module.params.get("authentication_algorithm") == "SHA512":
        if not exist_settings["AuthenticationAlgorithm"] == "3":
            return True
    
    if module.params.get("authentication_password"):
        return True

    return False

def remove_snmp_user(connection, module, result):
    """Remove an SNMPv3 User from Sophos Firewall.

    Args:
        connection (Connection): Ansible Connection object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: API response
    """
    try:
        resp = connection.invoke_sdk("remove", module_args={"xml_tag": "SNMPv3User", "name": module.params.get("name")})
    except Exception as error:
        module.fail_json("An unexpected error occurred: {0}".format(error), **result)

    if not resp["success"]:
        module.fail_json(msg="An error occurred: {0}".format(resp["response"]))

    return resp["response"]

def main():
    """Code executed at run time."""
    argument_spec = {
        "name": {"type": "str", "required": True},
        "accept_queries": {"type": "str", "choices": ["Enable", "Disable"], "required": False},
        "send_traps": {"type": "str", "choices": ["Enable", "Disable"], "required": False},
        "authorized_hosts": {"type": "list", "elements": "str", "required": False},
        "encryption_algorithm": {"type": "str", "choices": ["AES", "DES", "None"], "required": False},
        "encryption_password": {"type": "str", "required": False, "no_log": True},
        "authentication_algorithm": {"type": "str", "choices": ["MD5", "SHA256", "SHA512"], "required": False},
        "authentication_password": {"type": "str", "required": False, "no_log": True},
        "state": {"type": "str", "required": True, "choices": ["present", "updated", "query", "absent"]},
    }

    required_if = [
        (
            "state",
            "present",
            [
                "name",
                "accept_queries",
                "send_traps",
                "authorized_hosts",
                "encryption_algorithm",
                "encryption_password",
                "authentication_algorithm",
                "authentication_password"
            ],
            False,
        ),
        (
            "state",
            "updated",
            [
                "name"
            ],
            False,
        ),
        (
            "state",
            "query",
            [
                "name"
            ],
            False,
        ),
        (
            "send_traps",
            "Enable",
            [
                "authorized_hosts"
            ],
            False,
        )
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

    exist_settings = get_snmp_user(connection, module, result)
    result["api_response"] = exist_settings["api_response"]

    if exist_settings["exists"]:
        api_version = exist_settings["api_response"]["Response"]["@APIVersion"]
    else:
        resp = connection.invoke_sdk("login")
        api_version = resp["response"]["Response"]["@APIVersion"]

    if state == "query":
        module.exit_json(**result)

    if module.check_mode:
        result["check_mode"] = True
        module.exit_json(**result)

    if state == "present" and not exist_settings["exists"]:
        api_response = create_snmp_user(connection, module, result, api_version=api_version)
        if (
            "Operation Successful" in api_response["Response"]["SNMPv3User"]["Status"]["#text"] or
            "Configuration applied successfully" in api_response["Response"]["SNMPv3User"]["Status"]["#text"]
        ):
            result["changed"] = True
            result["api_response"] = api_response

    elif state == "present" and exist_settings["exists"]:
        result["changed"] = False

    elif state == "absent" and exist_settings["exists"]:
        api_response = remove_snmp_user(connection, module, result)
        if (
            "Configuration applied successfully" in api_response["Response"]["SNMPv3User"]["Status"]["#text"]
        ):
            result["changed"] = True
        result["api_response"] = api_response

    elif state == "absent" and not exist_settings["exists"]:
        result["changed"] = False

    elif state == "updated" and exist_settings["exists"]:
        if eval_changed(module, exist_settings, api_version=api_version):
            api_response = update_snmp_user(connection, exist_settings["api_response"], module, result, api_version=api_version)

            if api_response:
                result["api_response"] = api_response
                if (
                    "Operation Successful" in api_response["Response"]["SNMPv3User"]["Status"]["#text"]
                    or "Configuration applied successfully" in api_response["Response"]["SNMPv3User"]["Status"]["#text"]
                ):
                    result["changed"] = True
    
    elif state == "updated" and not exist_settings["exists"]:
        result["changed"] = False
        module.fail_json(exist_settings["api_response"], **result)

    module.exit_json(**result)


if __name__ == "__main__":
    main()