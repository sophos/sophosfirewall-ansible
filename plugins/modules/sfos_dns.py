#!/usr/bin/python

# Copyright 2024 Sophos Ltd.  All rights reserved.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: sfos_dns

short_description: Manage DNS settings (Configure > Network > DNS)

version_added: "1.0.0"

description: Manage DNS servers (Configure > Network > DNS) on Sophos Firewall

extends_documentation_fragment:
  - sophos.sophos_firewall.fragments.base

options:
    ipv4_settings:
        description: IPv4 DNS Settings
        required: false
        type: dict
        suboptions:
            dns_source:
                description: DNS source (DHCP/PPPoE/Static)
                type: str
                choices: ["DHCP", "PPPoE", "Static"]
                required: false
            dns1:
                description: First IPv4 DNS server
                type: str
                required: false
            dns2:
                description: Second IPv4 DNS server
                type: str
                required: false
            dns3:
                description: Third IPv4 DNS server
                type: str
                required: false
    ipv6_settings:
        description: IPv4 DNS Settings
        required: false
        type: dict
        suboptions:
            dns_source:
                description: DNS source (DHCP/PPPoE/Static)
                type: str
                choices: ["DHCP", "PPPoE", "Static"]
                required: false
            dns1:
                description: First IPv4 DNS server
                type: str
                required: false
            dns2:
                description: Second IPv4 DNS server
                type: str
                required: false
            dns3:
                description: Third IPv4 DNS server
                type: str
                required: false
    dnsquery_config:
        description: Enable/Disable the login disclaimer
        type: str
        choices: ["ChooseServerBasedOnIncomingRequestsRecordType",
          "ChooseIPv6DNSServerOverIPv4",
          "ChooseIPv4DNSServerOverIPv6",
          "ChooseIPv6IfRequestOriginatorAddressIsIPv6",
          "ElseIPv4"]
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
- name: Update DNS servers
  sophos.sophos_firewall.sfos_dns:
    ipv4_settings:
      dns_source: Static
      dns1: 4.2.2.1
      dns2: 4.2.2.2
      dns3: 1.1.1.1
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


def get_dns_settings(connection, module, result):
    """Get current DNS settings from Sophos Firewall

    Args:
        connection (Connection): HTTPAPI Connection object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: Results of lookup
    """
    try:
        resp = connection.invoke_sdk("get_dns_forwarders")
    except Exception as error:
        module.fail_json("An unexpected error occurred: {0}".format(error), **result)

    if resp["success"] and not resp["exists"]:
        return {"exists": False, "api_response": resp["response"]}

    if not resp["success"]:
        module.fail_json(msg="An error occurred: {0}".format(resp["response"]))

    return {"exists": True, "api_response": resp["response"]}


def update_dns_settings(connection, module, result):
    """Update DNS settings on Sophos Firewall

    Args:
        connection (Connection): HTTPAPI Connection object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: API response
    """
    update_params = get_dns_settings(connection=connection, module=module, result=result)["api_response"]["Response"]["DNS"]

    ipv4_settings = module.params.get("ipv4_settings", {})
    if ipv4_settings:
        dns_source = ipv4_settings.get("dns_source")
        if dns_source:
            update_params["IPv4Settings"]["ObtainDNSFrom"] = dns_source
        if dns_source == "Static":
            dns1 = ipv4_settings.get("dns1")
            if dns1:
                update_params["IPv4Settings"]["DNSIPList"]["DNS1"] = dns1
            dns2 = ipv4_settings.get("dns2")
            if dns2:
                update_params["IPv4Settings"]["DNSIPList"]["DNS2"] = dns2
            dns3 = ipv4_settings.get("dns3")
            if dns3:
                update_params["IPv4Settings"]["DNSIPList"]["DNS3"] = dns3

    ipv6_settings = module.params.get("ipv6_settings", {})
    if ipv6_settings:
        dns_source = ipv6_settings.get("dns_source")
        if dns_source:
            update_params["IPv6Settings"]["ObtainDNSFrom"] = dns_source
        if dns_source == "Static":
            dns1 = ipv6_settings.get("dns1")
            if dns1:
                update_params["IPv6Settings"]["DNSIPList"]["DNS1"] = dns1
            dns2 = ipv6_settings.get("dns2")
            if dns2:
                update_params["IPv6Settings"]["DNSIPList"]["DNS2"] = dns2
            dns3 = ipv6_settings.get("dns3")
            if dns3:
                update_params["IPv6Settings"]["DNSIPList"]["DNS3"] = dns3

    if module.params.get("dnsquery_config"):
        update_params["DNSQueryConfiguration"] = module.params.get("dnsquery_config")

    # module.exit_json(msg=f"update_params: {update_params}")

    resp = connection.invoke_sdk("update", module_args={"xml_tag": "DNS", "update_params": update_params})

    return resp["response"]



def eval_changed(module, exist_settings):
    """Evaluate the provided arguments against existing settings.

    Args:
        module (AnsibleModule): AnsibleModule object
        exist_settings (dict): Response from the call to get_admin_settings()

    Returns:
        bool: Return true if any settings are different, otherwise return false
    """
    exist_settings = exist_settings["api_response"]["Response"]["DNS"]

    ipv4_settings = module.params.get("ipv4_settings", {})
    if ipv4_settings:
        dns_source = module.params["ipv4_settings"].get("dns_source")
        dns1 = module.params["ipv4_settings"].get("dns1")
        dns2 = module.params["ipv4_settings"].get("dns2")
        dns3 = module.params["ipv4_settings"].get("dns3")

        if (
            dns_source
            and not dns_source == exist_settings["IPv4Settings"]["ObtainDNSFrom"]
            or dns1
            and not dns1 == exist_settings["IPv4Settings"]["DNSIPList"]["DNS1"]
            or dns2
            and not dns2 == exist_settings["IPv4Settings"]["DNSIPList"]["DNS2"]
            or dns3
            and not dns3 == exist_settings["IPv4Settings"]["DNSIPList"]["DNS3"]
        ):
            return True

    ipv6_settings = module.params.get("ipv6_settings", {})
    if ipv6_settings:
        dns_source = module.params["ipv6_settings"].get("dns_source")
        dns1 = module.params["ipv6_settings"].get("dns1")
        dns2 = module.params["ipv6_settings"].get("dns2")
        dns3 = module.params["ipv6_settings"].get("dns3")

        if (
            dns_source
            and not dns_source == exist_settings["IPv6Settings"]["ObtainDNSFrom"]
            or dns1
            and not dns1 == exist_settings["IPv6Settings"]["DNSIPList"]["DNS1"]
            or dns2
            and not dns2 == exist_settings["IPv6Settings"]["DNSIPList"]["DNS2"]
            or dns3
            and not dns3 == exist_settings["IPv6Settings"]["DNSIPList"]["DNS3"]
        ):
            return True

    dnsquery_config = module.params.get("dnsquery_config")
    if (
        dnsquery_config
        and not dnsquery_config == exist_settings["DNSQueryConfiguration"]
    ):
        return True

    return False


def main():
    """Code executed at run time."""
    argument_spec = {
        "ipv4_settings": {
            "type": "dict",
            "required": False,
            "options": {
                "dns_source": {
                    "type": "str",
                    "required": False,
                    "choices": ["DHCP", "PPPoE", "Static"],
                },
                "dns1": {"type": "str", "required": False},
                "dns2": {"type": "str", "required": False},
                "dns3": {"type": "str", "required": False},
            },
        },
        "ipv6_settings": {
            "type": "dict",
            "required": False,
            "options": {
                "dns_source": {
                    "type": "str",
                    "required": False,
                    "choices": ["DHCP", "PPPoE", "Static"],
                },
                "dns1": {"type": "str", "required": False},
                "dns2": {"type": "str", "required": False},
                "dns3": {"type": "str", "required": False},
            },
        },
        "dnsquery_config": {
            "type": "str",
            "required": False,
            "choices": [
                "ChooseServerBasedOnIncomingRequestsRecordType",
                "ChooseIPv6DNSServerOverIPv4",
                "ChooseIPv4DNSServerOverIPv6",
                "ChooseIPv6IfRequestOriginatorAddressIsIPv6",
                "ElseIPv4",
            ],
        },
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

    exist_settings = get_dns_settings(connection, module, result)
    result["api_response"] = exist_settings["api_response"]

    if state == "query":
        module.exit_json(**result)

    if module.check_mode:
        result["check_mode"] = True
        module.exit_json(**result)

    elif state == "updated":
        if eval_changed(module, exist_settings):
            api_response = update_dns_settings(connection, module, result)
            if api_response:
                if (
                    api_response["Response"]["DNS"]["Status"]["#text"]
                    == "Configuration applied successfully."
                ):
                    result["changed"] = True
                result["api_response"] = api_response
            else:
                result["changed"] = False

    module.exit_json(**result)


if __name__ == "__main__":
    main()
