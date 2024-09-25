#!/usr/bin/python

# Copyright 2024 Sophos Ltd.  All rights reserved.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r'''
---
module: sfos_zone

short_description: Manage Zones on Sophos Firewall

version_added: "1.0.0"

description: Creates, updates or removes firewall zones on Sophos Firewall

extends_documentation_fragment:
  - sophos.sophos_firewall.fragments.base

options:
    name:
        description: Name of the zone to create, update, or delete
        required: true
        type: str
    zone_type:
        description: Type of zone to create (LAN/DMZ)
        choices: ["LAN", "DMZ"]
        type: str
        required: false
    description:
        description: Description for the zone
        type: str
        required: false
    https:
        description:
            - Enable/Disable HTTPS administrative service
        choices: ["Enable", "Disable"]
        type: str
        required: false
    ssh:
        description:
            - Enable/Disable SSH administrative service
        choices: ["Enable", "Disable"]
        type: str
        required: false
    client_authen:
        description:
            - Enable/Disable client authentication service
        choices: ["Enable", "Disable"]
        type: str
        required: false
    captive_portal:
        description:
            - Enable/Disable captive portal
        choices: ["Enable", "Disable"]
        type: str
        required: false
    ad_sso:
        description:
            - Enable/Disable SSO with Active Directory
        choices: ["Enable", "Disable"]
        type: str
        required: false
    radius_sso:
        description:
            - Enable/Disable SSO with Radius
        choices: ["Enable", "Disable"]
        type: str
        required: false
    chromebook_sso:
        description:
            - Enable/Disable Chromebook SSO
        choices: ["Enable", "Disable"]
        type: str
        required: false
    dns:
        description:
            - Enable/Disable DNS network service
        choices: ["Enable", "Disable"]
        type: str
        required: false
    ping:
        description:
            - Enable/Disable Ping network service
        choices: ["Enable", "Disable"]
        type: str
        required: false
    ipsec:
        description:
            - Enable/Disable IPSec VPN service
        choices: ["Enable", "Disable"]
        type: str
        required: false
    red:
        description:
            - Enable/Disable RED service
        choices: ["Enable", "Disable"]
        type: str
        required: false
    sslvpn:
        description:
            - Enable/Disable SSLVPN service
        choices: ["Enable", "Disable"]
        type: str
        required: false
    vpn_portal:
        description:
            - Enable/Disable VPN Portal
        choices: ["Enable", "Disable"]
        type: str
        required: false
    web_proxy:
        description:
            - Enable/Disable Web Proxy
        choices: ["Enable", "Disable"]
        type: str
        required: false
    wireless_protection:
        description:
            - Enable/Disable Wireless Protection
        choices: ["Enable", "Disable"]
        type: str
        required: false
    user_portal:
        description:
            - Enable/Disable user portal
        choices: ["Enable", "Disable"]
        type: str
        required: false
    dynamic_routing:
        description:
            - Enable/Disable Dynamic Routing
        choices: ["Enable", "Disable"]
        type: str
        required: false
    smtp_relay:
        description:
            - Enable/Disable SMTP Relay
        choices: ["Enable", "Disable"]
        type: str
        required: false
    snmp:
        description:
            - Enable/Disable SNMP
        choices: ["Enable", "Disable"]
        type: str
        required: false
    state:
        description:
            - Use C(query) to retrieve, C(present) to create, C(absent) to remove, or C(updated) to modify
        choices: [present, absent, updated, query]
        type: str
        required: true

author:
    - Matt Mullen (@mamullen13316)
'''

EXAMPLES = r'''
- name: Create Zone
  sophos.sophos_firewall.sfos_firewall_rule:
    username: "{{ username }}"
    password: "{{ password }}"
    hostname: myfirewallhostname.sophos.net
    port: 4444
    verify: false
    name: TESTZONE
    description: Zone created by Ansible
    zone_type: LAN
    state: present

- name: Display Existing Zone
  sophos.sophos_firewall.sfos_firewall_rule:
    username: "{{ username }}"
    password: "{{ password }}"
    hostname: myfirewallhostname.sophos.net
    port: 4444
    verify: false
    name: TESTZONE
    state: query

- name: Update Zone Admin Services
  sophos.sophos_firewall.sfos_firewall_rule:
    username: "{{ username }}"
    password: "{{ password }}"
    hostname: myfirewallhostname.sophos.net
    port: 4444
    verify: false
    name: TESTZONE
    https: Enable
    ssh: Enable
    state: updated

- name: Remove Zone
  sophos.sophos_firewall.sfos_firewall_rule:
    username: "{{ username }}"
    password: "{{ password }}"
    hostname: myfirewallhostname.sophos.net
    port: 4444
    verify: false
    name: TESTZONE
    state: absent
'''

RETURN = r'''
api_response:
    description: Serialized object containing the API response.
    type: dict
    returned: always

'''

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


def get_zone(fw_obj, module, result):
    """Get firewall rule from Sophos Firewall

    Args:
        fw_obj (SophosFirewall): SophosFirewall object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: Results of lookup
    """
    try:
        resp = fw_obj.get_zone(name=module.params.get("name"))
    except SophosFirewallZeroRecords as error:
        return {"exists": False, "api_response": str(error)}
    except SophosFirewallAuthFailure as error:
        module.fail_json(msg="Authentication error: {0}".format(error), **result)
    except SophosFirewallAPIError as error:
        module.fail_json(msg="API Error: {0}".format(error), **result)
    except RequestException as error:
        module.fail_json(msg="Error communicating to API: {0}".format(error), **result)

    return {"exists": True, "api_response": resp}

def create_zone(fw_obj, module, result):
    """Create a firewall rule on Sophos Firewall.

    Args:
        fw_obj (SophosFirewall): SophosFirewall object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: API response
    """
    zone_params = {
        "description": module.params.get("description"),
        "https": module.params.get("https"),
        "ssh": module.params.get("ssh"),
        "client_authen": module.params.get("client_authen"),
        "captive_portal": module.params.get("captive_portal"),
        "ad_sso": module.params.get("ad_sso"),
        "radius_sso": module.params.get("radius_sso"),
        "chromebook_sso": module.params.get("chromebook_sso"),
        "dns": module.params.get("dns"),
        "ping": module.params.get("ping"),
        "ipsec": module.params.get("ipsec"),
        "red": module.params.get("red"),
        "sslvpn": module.params.get("sslvpn"),
        "vpn_portal": module.params.get("vpn_portal"),
        "web_proxy": module.params.get("web_proxy"),
        "wireless_protection": module.params.get("wireless_protection"),
        "user_portal": module.params.get("user_portal"),
        "dynamic_routing": module.params.get("dynamic_routing"),
        "smtp_relay": module.params.get("smtp_relay"),
        "snmp": module.params.get("snmp")
    }

    try:
        resp = fw_obj.create_zone(name=module.params.get("name"), zone_type=module.params.get("zone_type"), zone_params=zone_params)
    except SophosFirewallAuthFailure as error:
        module.fail_json(msg="Authentication error: {0}".format(error), **result)
    except SophosFirewallAPIError as error:
        module.fail_json(msg="API Error: {0}".format(error), **result)
    except RequestException as error:
        module.fail_json(msg="Error communicating to API: {0}".format(error), **result)
    else:
        return resp

def remove_zone(fw_obj, module, result):
    """Remove a zone from Sophos Firewall.

    Args:
        fw_obj (SophosFirewall): SophosFirewall object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: API response
    """
    try:
        resp = fw_obj.remove(
            xml_tag="Zone", name=module.params.get("name")
        )
    except SophosFirewallAuthFailure as error:
        module.fail_json(msg="Authentication error: {0}".format(error), **result)
    except SophosFirewallAPIError as error:
        module.fail_json(msg="API Error: {0}".format(error), **result)
    except RequestException as error:
        module.fail_json(msg="Error communicating to API: {0}".format(error), **result)
    else:
        return resp


def update_zone(fw_obj, module, result):
    """Update an existing zone on Sophos Firewall

    Args:
        fw_obj (SophosFirewall): SophosFirewall object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: API response
    """
    zone_params = {
        "description": module.params.get("description"),
        "https": module.params.get("https"),
        "ssh": module.params.get("ssh"),
        "client_authen": module.params.get("client_authen"),
        "captive_portal": module.params.get("captive_portal"),
        "ad_sso": module.params.get("ad_sso"),
        "radius_sso": module.params.get("radius_sso"),
        "chromebook_sso": module.params.get("chromebook_sso"),
        "dns": module.params.get("dns"),
        "ping": module.params.get("ping"),
        "ipsec": module.params.get("ipsec"),
        "red": module.params.get("red"),
        "sslvpn": module.params.get("sslvpn"),
        "vpn_portal": module.params.get("vpn_portal"),
        "web_proxy": module.params.get("web_proxy"),
        "wireless_protection": module.params.get("wireless_protection"),
        "user_portal": module.params.get("user_portal"),
        "dynamic_routing": module.params.get("dynamic_routing"),
        "smtp_relay": module.params.get("smtp_relay"),
        "snmp": module.params.get("snmp")
    }

    try:
        resp = fw_obj.update_zone(
            name=module.params.get("name"),
            zone_params=zone_params
        )
    except SophosFirewallAuthFailure as error:
        module.fail_json(msg="Authentication error: {0}".format(error), **result)
    except SophosFirewallAPIError as error:
        module.fail_json(msg="API Error: {0}".format(error), **result)
    except RequestException as error:
        module.fail_json(msg="Error communicating to API: {0}".format(error), **result)
    else:
        return resp

def eval_changed(module, exist_settings):
    """Evaluate the provided arguments against existing settings. 

    Args:
        module (AnsibleModule): AnsibleModule object
        exist_settings (dict): Response from the call to get_admin_settings()

    Returns:
        bool: Return true if any settings are different, otherwise return false
    """
    exist_settings = exist_settings["Response"]["Zone"]

    description = module.params.get("description")
    if description and not exist_settings["Description"] == description:
        return True
    
    settings = [{"key": "HTTPS", "value": module.params.get("https"), "group": "AdminServices"},
        {"key": "SSH", "value": module.params.get("ssh"), "group": "AdminServices"},
        {"key": "ClientAuthentication", "value": module.params.get("client_authen"), "group": "AuthenticationServices"},
        {"key": "CaptivePortal", "value": module.params.get("captive_portal"),"group": "AuthenticationServices"},
        {"key": "ADSSO", "value": module.params.get("ad_sso"),"group": "AuthenticationServices"},
        {"key": "RadiusSSO", "value": module.params.get("radius_sso"), "group": "AuthenticationServices"},
        {"key": "ChromebookSSO", "value": module.params.get("chromebook_sso"), "group": "AuthenticationServices"},
        {"key": "DNS", "value": module.params.get("dns"), "group": "NetworkServices"},
        {"key": "Ping", "value": module.params.get("ping"), "group": "NetworkServices"},
        {"key": "IPsec", "value": module.params.get("ipsec"), "group": "VPNServices"},
        {"key": "RED", "value": module.params.get("red"),"group": "VPNServices"},
        {"key": "SSLVPN", "value": module.params.get("sslvpn"), "group": "VPNServices"},
        {"key": "VPNPortal", "value": module.params.get("vpn_portal"), "group": "VPNServices"},
        {"key": "WebProxy", "value": module.params.get("web_proxy"), "group": "OtherServices"},
        {"key": "WirelessProtection", "value": module.params.get("wireless_protection"), "group": "OtherServices"},
        {"key": "UserPortal", "value": module.params.get("user_portal"),"group": "OtherServices"},
        {"key": "DynamicRouting", "value": module.params.get("dynamic_routing"), "group": "OtherServices"},
        {"key": "SMTPRelay", "value": module.params.get("smtp_relay"), "group": "OtherServices"},
        {"key": "SNMP", "value": module.params.get("snmp"), "group": "OtherServices"}
    ]
    result_list = []
    for params in settings:
        result = eval_settings(exist_settings, **params)
        if result:
             result_list.append(True)

    if True in result_list:
        return True

    return False

def eval_settings(exist_settings, key, value, group):
    """Evaluates current settings vs. the configured argument

    Args:
        exist_settings (dict): The API response from the get_zone() method
        key (str): The XML key that contains the value in the current settings
        value (str): The value of the argument passed into Ansible in the task
        group (str): The XML container for the key (AdminServices, NetworkServices, etc.)

    Returns:
        bool: Returns True if the current setting differs from the value in the Ansible task
    """
    if value == "Enable":
        if exist_settings.get("ApplianceAccess",{}):
            if exist_settings["ApplianceAccess"].get(group, {}):
                if exist_settings["ApplianceAccess"][group].get(key, {}):
                    if not exist_settings["ApplianceAccess"][group][key] == value:
                        return True
                else:
                    return True
            else:
                return True
        else:
            return True

    if value == "Disable":
        if exist_settings.get("ApplianceAccess",{}):
            if exist_settings["ApplianceAccess"].get(group, {}):
                if exist_settings["ApplianceAccess"][group].get(key, {}):
                    if not exist_settings["ApplianceAccess"][group][key] == value:
                        return True
                else:
                    return False
            else:
                return False
        else:
            return False
    return False

def main():
    """Code executed at run time."""
    argument_spec = {
        "username": {"required": True},
        "password": {"required": True, "no_log": True},
        "hostname": {"required": True},
        "port": {"type": "int", "default": 4444},
        "verify": {"type": "bool", "default": True},
        "name": {"required": True},
        "zone_type": {"choices": ["LAN", "DMZ"], "required": False},
        "description": {"type": "str", "required": False},
        "https": {"type": "str", "choices": ["Enable", "Disable"]},
        "ssh": {"type": "str", "choices": ["Enable", "Disable"]},
        "client_authen": {"type": "str", "choices": ["Enable", "Disable"]},
        "captive_portal": {"type": "str", "choices": ["Enable", "Disable"]},
        "ad_sso": {"type": "str", "choices": ["Enable", "Disable"]},
        "radius_sso": {"type": "str", "choices": ["Enable", "Disable"]},
        "chromebook_sso": {"type": "str", "choices": ["Enable", "Disable"]},
        "dns": {"type": "str", "choices": ["Enable", "Disable"]},
        "ping": {"type": "str", "choices": ["Enable", "Disable"]},
        "ipsec": {"type": "str", "choices": ["Enable", "Disable"]},
        "red": {"type": "str", "choices": ["Enable", "Disable"]},
        "sslvpn": {"type": "str", "choices": ["Enable", "Disable"]},
        "vpn_portal": {"type": "str", "choices": ["Enable", "Disable"]},
        "web_proxy": {"type": "str", "choices": ["Enable", "Disable"]},
        "wireless_protection": {"type": "str", "choices": ["Enable", "Disable"]},
        "user_portal": {"type": "str", "choices": ["Enable", "Disable"]},
        "dynamic_routing": {"type": "str", "choices": ["Enable", "Disable"]},
        "smtp_relay": {"type": "str", "choices": ["Enable", "Disable"]},
        "snmp": {"type": "str", "choices": ["Enable", "Disable"]},
        "state": {"required": True, "choices": ["present", "absent", "updated", "query"]},
    }

    required_if = [
        ('state', 'present', ('zone_type',), True),
    ]

    # required_together = [
    #     ["start_ip", "end_ip"],
    #     ["network", "mask"]
    # ]

    module = AnsibleModule(argument_spec=argument_spec,
                            required_if=required_if,
                        #    required_together=required_together,
                           supports_check_mode=True)

    if not PREREQ_MET["result"]:
        module.fail_json(msg=missing_required_lib(PREREQ_MET["missing_module"]))
        
    fw = SophosFirewall(
        username=module.params.get("username"),
        password=module.params.get("password"),
        hostname=module.params.get("hostname"),
        port=module.params.get("port"),
        verify=module.params.get("verify"),
    )

    result = {
        "changed": False,
        "check_mode": False
    }

    state = module.params.get("state")

    exist_check = get_zone(fw, module, result)
    result["api_response"] = exist_check["api_response"]

    if state == "query":
        module.exit_json(**result)

    if module.check_mode:
        result["check_mode"] = True
        module.exit_json(**result)

    if state == "present" and not exist_check["exists"]:
        api_response = create_zone(fw, module, result)
        if (
            api_response["Response"]["Zone"]["Status"]["#text"]
            == "Configuration applied successfully."
        ):
            result["changed"] = True
            result["api_response"] = api_response

    elif state == "present" and exist_check["exists"]:
        result["changed"] = False

    elif state == "absent" and exist_check["exists"]:
        api_response = remove_zone(fw, module, result)
        if (api_response["Response"]["Zone"]["Status"]["#text"]
                == "Configuration applied successfully."):
            result["changed"] = True
        result["api_response"] = api_response

    elif state == "absent" and not exist_check["exists"]:
        result["changed"] = False

    elif state == "updated" and exist_check["exists"]:
        if eval_changed(module, exist_check["api_response"]):
            api_response = update_zone(fw, module, result)

            if api_response:
                if (api_response["Response"]["Zone"]["Status"]["#text"]
                        == "Configuration applied successfully."):
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
