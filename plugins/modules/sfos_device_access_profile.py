#!/usr/bin/python

# Copyright 2024 Sophos Ltd.  All rights reserved.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r'''
---
module: sfos_device_access_profile

short_description: Manage Device Access Profiles

version_added: "1.0.0"

description: Manage Device Access Profiles on Sophos Firewall (System > Profiles > Device Access)

extends_documentation_fragment:
  - sophos.sophos_firewall.fragments.base

options:
    name:
        description: Name of the profile.
        required: true
        type: str
    default_permission:
        description: Default permission to use for unspecified arguments when creating profile.
        required: false
        type: str
        choices: ["Read-Write", "Read-Only", "None"]
    dashboard:
        description: Dashboard permissions.
        required: false
        type: str
        choices: ["Read-Write", "Read-Only", "None"]
    wizard:
        description: Wizard permissions.
        required: false
        type: str
        choices: ["Read-Write", "Read-Only", "None"]
    objects:
        description: Objects permissions.
        required: false
        type: str
        choices: ["Read-Write", "Read-Only", "None"]
    network:
        description: Network permissions.
        required: false
        type: str
        choices: ["Read-Write", "Read-Only", "None"]
    firewall:
        description: Firewall permissions.
        required: false
        type: str
        choices: ["Read-Write", "Read-Only", "None"]
    ips:
        description: IPS permissions.
        required: false
        type: str
        choices: ["Read-Write", "Read-Only", "None"]
    web_filter:
        description: Web Filter permissions.
        required: false
        type: str
        choices: ["Read-Write", "Read-Only", "None"]
    cloud_application_dashboard:
        description: Cloud Application Dashboard permissions.
        required: false
        type: str
        choices: ["Read-Write", "Read-Only", "None"]
    zero_day_protection:
        description: Zero day protection permissions.
        required: false
        type: str
        choices: ["Read-Write", "Read-Only", "None"]
    application_filter:
        description: Application Filter permissions.
        required: false
        type: str
        choices: ["Read-Write", "Read-Only", "None"]
    qos:
        description: QoS permissions.
        required: false
        type: str
        choices: ["Read-Write", "Read-Only", "None"]
    email_protection:
        description: Email Protection permissions.
        required: false
        type: str
        choices: ["Read-Write", "Read-Only", "None"]
    traffic_discovery:
        description: Traffic Discovery permissions.
        required: false
        type: str
        choices: ["Read-Write", "Read-Only", "None"]
    system:
        description: System permissions group.
        required: false
        type: dict
        suboptions:
            profile:
                description: Profile permissions.
                type: str
                required: false
                choices: ["Read-Write", "Read-Only", "None"]
            system_password:
                description: Manage system password
                type: str
                required: false
                choices: ["Read-Write", "Read-Only", "None"]
            central_management:
                description: Central Management permissions.
                type: str
                required: false
                choices: ["Read-Write", "Read-Only", "None"]
            backup:
                description: Backup permissions.
                type: str
                required: false
                choices: ["Read-Write", "Read-Only", "None"]
            restore:
                description: Restore permissions.
                type: str
                required: false
                choices: ["Read-Write", "Read-Only", "None"]
            firmware:
                description: Firmware permissions.
                type: str
                required: false
                choices: ["Read-Write", "Read-Only", "None"]
            licensing:
                description: Licensing permissions.
                type: str
                required: false
                choices: ["Read-Write", "Read-Only", "None"]
            services:
                description: Services permissions.
                type: str
                required: false
                choices: ["Read-Write", "Read-Only", "None"]
            updates:
                description: Updates permissions.
                type: str
                required: false
                choices: ["Read-Write", "Read-Only", "None"]
            reboot_shutdown:
                description: Reboot/Shutdown permissions.
                type: str
                required: false
                choices: ["Read-Write", "Read-Only", "None"]
            ha:
                description: HA permissions.
                type: str
                required: false
                choices: ["Read-Write", "Read-Only", "None"]
            download_certificates:
                description: Restore permissions.
                type: str
                required: false
                choices: ["Read-Write", "Read-Only", "None"]
            other_certificate_configuration:
                description: Other certificate configuration permissions.
                type: str
                required: false
                choices: ["Read-Write", "Read-Only", "None"]
    wireless_protection:
        description: Wireless protection permissions group
        type: dict
        required: false
        suboptions:
            wireless_protection_overview:
                description: Wireless protection overview permissions.
                type: str
                required: false
                choices: ["Read-Write", "Read-Only", "None"]
            wireless_protection_settings:
                description: Wireless protection permissions.
                type: str
                required: false
                choices: ["Read-Write", "Read-Only", "None"]
            wireless_protection_network:
                description: Wireless protection network permissions.
                type: str
                required: false
                choices: ["Read-Write", "Read-Only", "None"]
            wireless_protection_access_point:
                description: Wireless protection access point permissions.
                type: str
                required: false
                choices: ["Read-Write", "Read-Only", "None"]
            wireless_protection_mesh:
                description: Wireless protection mesh permissions.
                type: str
                required: false
                choices: ["Read-Write", "Read-Only", "None"]
    identity:
        description: Identity permissions group.
        type: dict
        required: false
        suboptions:
            authentication:
                description: Authentication permissions.
                type: str
                required: false
                choices: ["Read-Write", "Read-Only", "None"]
            groups:
                description: Groups permissions.
                type: str
                required: false
                choices: ["Read-Write", "Read-Only", "None"]
            guest_user_management:
                description: Guest user management permissions.
                type: str
                required: false
                choices: ["Read-Write", "Read-Only", "None"]
            policy:
                description: Policy permissions.
                type: str
                required: false
                choices: ["Read-Write", "Read-Only", "None"]
            test_external_server_connectivity:
                description: Test external server connectivity permissions.
                type: str
                required: false
                choices: ["Read-Write", "Read-Only", "None"]
            disconnect_live_user:
                description: Disconnect live user permissions.
                type: str
                required: false
                choices: ["Read-Write", "Read-Only", "None"]
    vpn:
        description: VPN permissions group
        type: dict
        required: false
        suboptions:
            connect_tunnel:
                description: Connect tunnel permissions. 
                type: str
                choices: ["Read-Write", "Read-Only", "None"]
                required: false
            other_vpn_configurations:
                description: Other VPN configurations permissions. 
                type: str
                choices: ["Read-Write", "Read-Only", "None"]
                required: false
    waf:
        description: WAF permissions group
        type: dict
        required: false
        suboptions:
            alerts:
                description: Alerts permissions.
                type: str
                choices: ["Read-Write", "Read-Only", "None"]
                required: false
            other_waf_configuration:
                description: Other WAF configuration permissions.
                type: str
                choices: ["Read-Write", "Read-Only", "None"]
                required: false
    logs_reports:
        description: Logs/Reports permissions group
        type: dict
        required: false
        suboptions:
            configuration:
                description: Configuration permissions.
                type: str
                choices: ["Read-Write", "Read-Only", "None"]
                required: false
            log_viewer:
                description: Log viewer permissions.
                type: str
                choices: ["Read-Write", "Read-Only", "None"]
                required: false
            reports_access:
                description: Reports access permissions.
                type: str
                choices: ["Read-Write", "Read-Only", "None"]
                required: false
            four_eye_authentication_settings:
                description: Four Eye authentication settings permissions.
                type: str
                choices: ["Read-Write", "Read-Only", "None"]
                required: false
            de_anonymization:
                description: De-anonymization permissions.
                type: str
                choices: ["Read-Write", "Read-Only", "None"]
                required: false
    state:
        description:
            - Use C(query) to retrieve or C(updated) to modify
        choices: [present, absent, updated, query]
        type: str
        required: true

author:
    - Matt Mullen (@mamullen13316)
'''

EXAMPLES = r'''
- name: CREATE A READ-ONLY PROFILE
  sophos.sophos_firewall.sfos_device_access_profile:
    username: "{{ username }}"
    password: "{{ password }}"
    hostname: "{{ inventory_hostname }}"
    port: 4444
    verify: false
    name: ReadOnlyAll
    default_permission: Read-Only
    state: present
    delegate_to: localhost

- name: CREATE A WIRELESS ADMIN PROFILE
  sophos.sophos_firewall.sfos_admin_settings:
    username: "{{ username }}"
    password: "{{ password }}"
    hostname: "{{ inventory_hostname }}"
    port: 4444
    verify: false
    name: WirelessAdmin
    default_permission: Read-Only
    wireless_protection:
        wireless_protection_overview: Read-Write
        wireless_protection_settings: Read-Write
        wireless_protection_network: Read-Write
        wireless_protection_access_point: Read-Write
        wireless_protection_mesh: Read-Write
    state: present
    delegate_to: localhost

- name: UPDATE PROFILE PERMISSIONS
  sophos.sophos_firewall.sfos_admin_settings:
    username: "{{ username }}"
    password: "{{ password }}"
    hostname: "{{ inventory_hostname }}"
    port: 4444
    verify: false
    name: ExampleProfile
    system:
        central_management: Read-Only
    logs_reports:
        log_viewer: Read-Write
        reports_access: Read-Write
    state: updated
    delegate_to: localhost

- name: RETRIEVE PROFILE
  sophos.sophos_firewall.sfos_admin_settings:
    username: "{{ username }}"
    password: "{{ password }}"
    hostname: "{{ inventory_hostname }}"
    port: 4444
    verify: false
    name: ExampleProfile
    state: query
    delegate_to: localhost

- name: DELETE PROFILE
  sophos.sophos_firewall.sfos_admin_settings:
    username: "{{ username }}"
    password: "{{ password }}"
    hostname: "{{ inventory_hostname }}"
    port: 4444
    verify: false
    name: ExampleProfile
    state: absent
    delegate_to: localhost
'''

RETURN = r'''
api_response:
    description: Serialized object containing the API response.
    type: dict
    returned: always

'''
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


def get_profile(fw_obj, module, result):
    """Get device access profile from Sophos Firewall

    Args:
        fw_obj (SophosFirewall): SophosFirewall object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: Results of lookup
    """
    try:
        resp = fw_obj.get_admin_profile(name=module.params.get("name"))
    except SophosFirewallZeroRecords as error:
        return {"exists": False, "api_response": str(error)}
    except SophosFirewallAuthFailure as error:
        module.fail_json(msg="Authentication error: {0}".format(error), **result)
    except SophosFirewallAPIError as error:
        module.fail_json(msg="API Error: {0}".format(error), **result)
    except RequestException as error:
        module.fail_json(msg="Error communicating to API: {0}".format(error), **result)

    return {"exists": True, "api_response": resp}

def flatten_args(module):
    """Convert all provided module arguments to a flattened dictionary.

    Args:
        module (AnsibleModule): AnsibleModule object

    Returns:
        dict: Flattened dict will all provided module arguments
    """
    params = {}
    for k,v in module.params.items():
        if isinstance(module.params[k], str):
            params[k] = v
        if isinstance(module.params[k], dict):
            for subkey, subval in module.params.get(k).items():
                if subval:
                    params[subkey] = subval
    return params

def create_profile(fw_obj, module, result):
    """Create a Device Access Profile on Sophos Firewall.

    Args:
        fw_obj (SophosFirewall): SophosFirewall object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: API response
    """
    create_params = flatten_args(module)

    try:
        resp = fw_obj.create_admin_profile(**create_params)
    except SophosFirewallAuthFailure as error:
        module.fail_json(msg="Authentication error: {0}".format(error), **result)
    except SophosFirewallAPIError as error:
        module.fail_json(msg="API Error: {0}".format(error), **result)
    except RequestException as error:
        module.fail_json(msg="Error communicating to API: {0}".format(error), **result)
    
    return resp

def update_profile(fw_obj, module, result):
    """Update admin settings on Sophos Firewall

    Args:
        fw_obj (SophosFirewall): SophosFirewall object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: API response
    """
    update_params = flatten_args(module)
    
    try:
        resp = fw_obj.update_admin_profile(**update_params)
    except SophosFirewallAuthFailure as error:
        module.fail_json(msg="Authentication error: {0}".format(error), **result)
    except SophosFirewallAPIError as error:
        module.fail_json(msg="API Error: {0}".format(error), **result)
    except RequestException as error:
        module.fail_json(msg="Error communicating to API: {0}".format(error), **result)
    
    return resp


def arg_to_xml(arg):
    """Handle the XML keys that don't convert to the correct XML key with .title()

    Args:
        arg (str): Ansible module argument

    Returns:
        str: Module argument converted to the appropriate XML key
    """
    all_upper = ["ips", "ha", "vpn", "waf"]
    if arg in all_upper:
        return arg.upper()
    if arg == "qos":
        return "QoS"
    if "vpn" in arg:
        return arg.title().replace("_","").replace("Vpn", "VPN")
    if "waf" in arg:
        return arg.title().replace("_","").replace("Waf", "WAF")
    if arg == "system_password":
        return "Password"
    if arg == "four_eye_authentication_settings":
        return "Four-EyeAuthenticationSettings"
    if arg == "de_anonymization":
        return "De-Anonymization"
    if arg == "wireless_protection_network":
        return "WirelessProtectionNetworkNetwork"
    return arg.title().replace("_", "")

def eval_changed(module, exist_settings):
    """Evaluate the provided arguments against existing settings. 

    Args:
        module (AnsibleModule): AnsibleModule object
        exist_settings (dict): Response from the call to get_admin_settings()

    Returns:
        bool: Return true if any settings are different, otherwise return false
    """
    exist_settings = exist_settings["api_response"]["Response"]["AdministrationProfile"]

    # Iterate through the provided arguments. If the argument has no suboptions, then it will be
    # a string and we can compare the converted argument name using .title() with the existing
    # setting. If the argument has suboptions, then it will be a dict and we must iterate again
    # over the suboptions and compare in the same manner. This strategy working relies on the arguments
    # converting with .title() to be the same as the XML key we are comparing against. The arg_to_xml
    # function handles situations where .title() doesn't convert to the correct XML key

    ignored_arguments = ["hostname", "username", "password", "port", "verify", "state"]
    arguments = {k:v for k,v in module.params.items() if module.params.get(k) and not k in ignored_arguments}

    for param, value in arguments.items():
        if isinstance(arguments.get(param), str):
            if not value == exist_settings[arg_to_xml(param)]:
                return True
        elif isinstance(arguments.get(param), dict):
            for subparam, subval in arguments.get(param).items():
                if subval and not subval == exist_settings[arg_to_xml(param)][arg_to_xml(subparam)]:
                    return True

    return False

def remove_profile(fw_obj, module, result):
    """Remove a Device Access Profile from Sophos Firewall.

    Args:
        fw_obj (SophosFirewall): SophosFirewall object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: API response
    """
    try:
        resp = fw_obj.remove(
            xml_tag="AdministrationProfile", name=module.params.get("name")
        )
    except SophosFirewallAuthFailure as error:
        module.fail_json(msg="Authentication error: {0}".format(error), **result)
    except SophosFirewallAPIError as error:
        module.fail_json(msg="API Error: {0}".format(error), **result)
    except RequestException as error:
        module.fail_json(msg="Error communicating to API: {0}".format(error), **result)
    else:
        return resp

def main():
    """Code executed at run time."""
    argument_spec = {
        "username": {"required": True},
        "password": {"required": True, "no_log": True},
        "hostname": {"required": True},
        "port": {"type": "int", "default": 4444},
        "verify": {"type": "bool", "default": True},
        "name": {"type": "str", "required": True},
        "default_permission": {"type": "str", "required": False, "choices": ["Read-Only", "Read-Write", "None"]},
        "dashboard": {"type": "str", "required": False},
        "wizard": {"type": "str", "required": False},
        "objects": {"type": "str", "required": False},
        "network": {"type": "str", "required": False},
        "firewall": {"type": "str", "required": False},
        "ips": {"type": "str", "required": False},
        "web_filter": {"type": "str", "required": False},
        "cloud_application_dashboard": {"type": "str", "required": False},
        "zero_day_protection": {"type": "str", "required": False},
        "application_filter": {"type": "str", "required": False},
        "qos": {"type": "str", "required": False},
        "email_protection": {"type": "str", "required": False},
        "traffic_discovery": {"type": "str", "required": False},
        "system": {"type": "dict", "required": False, "options": {
            "profile": {"type": "str", "required": False},
            "system_password": {"type": "str", "required": False},
            "central_management": {"type": "str", "required": False},
            "backup": {"type": "str", "required": False},
            "restore": {"type": "str", "required": False},
            "firmware": {"type": "str", "required": False},
            "licensing": {"type": "str", "required": False},
            "services": {"type": "str", "required": False},
            "updates": {"type": "str", "required": False},
            "reboot_shutdown": {"type": "str", "required": False},
            "ha": {"type": "str", "required": False},
            "download_certificates": {"type": "str", "required": False},
            "other_certificate_configuration": {"type": "str", "required": False},
            "diagnostics": {"type": "str", "required": False},
            "other_system_configuration": {"type": "str", "required": False},
            }
        },
        "wireless_protection": {"type": "dict", "required": False, "options": {
            "wireless_protection_overview": {"type": "str", "required": False},
            "wireless_protection_settings": {"type": "str", "required": False},
            "wireless_protection_network": {"type": "str", "required": False},
            "wireless_protection_access_point": {"type": "str", "required": False},
            "wireless_protection_mesh": {"type": "str", "required": False},
            }
        },
        "identity": {"type": "dict", "required": False, "options": {
            "authentication":{"type": "str", "required": False},
            "groups": {"type": "str", "required": False},
            "guest_users_management": {"type": "str", "required": False},
            "other_guest_user_settings": {"type": "str", "required": False},
            "policy": {"type": "str", "required": False},
            "test_external_server_connectivity": {"type": "str", "required": False},
            "disconnect_live_user": {"type": "str", "required": False},
            }
        },
        "vpn": {"type": "dict", "required": False, "options": {
            "connect_tunnel": {"type": "str", "required": False},
            "other_vpn_configurations": {"type": "str", "required": False}
            }
        },
        "waf": {"type": "dict", "required": False, "options": {
            "alerts": {"type": "str", "required": False},
            "other_waf_configuration": {"type": "str", "required": False},
            }
        },
        "logs_reports": {"type": "dict", "required": False, "options": {
            "configuration": {"type": "str", "required": False},
            "log_viewer": {"type": "str", "required": False},
            "reports_access": {"type": "str", "required": False},
            "four_eye_authentication_settings": {"type": "str", "required": False},
            "de_anonymization": {"type": "str", "required": False}
            }
        },
        "state": {"type": "str", "required": True, "choices": ["present", "absent", "updated", "query"]},
    }

    # required_if = [
    #     ('state', 'present', ['user_password', 'user_type', 'group', 'email'], False),
    #     ('user_type', 'Administrator', ['profile'], True)
    # ]

    # required_together = [
    #     ["start_ip", "end_ip"],
    #     ["network", "mask"]
    # ]

    module = AnsibleModule(argument_spec=argument_spec,
                        #    required_if=required_if,
                        #    required_together=required_together,
                           supports_check_mode=True
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

    result = {
        "changed": False,
        "check_mode": False
    }

    state = module.params.get("state")

    exist_check = get_profile(fw, module, result)
    result["api_response"] = exist_check["api_response"]

    if state == "query":
        module.exit_json(**result)

    if module.check_mode:
        result["check_mode"] = True
        module.exit_json(**result)

    if state == "present" and not exist_check["exists"]:
        api_response = create_profile(fw, module, result)
        if (
            api_response["Response"]["AdministrationProfile"]["Status"]["#text"]
            == "Configuration applied successfully."
        ):
            result["changed"] = True
            result["api_response"] = api_response

    elif state == "present" and exist_check["exists"]:
        result["changed"] = False

    elif state == "absent" and exist_check["exists"]:
        api_response = remove_profile(fw, module, result)
        if (api_response["Response"]["AdministrationProfile"]["Status"]["#text"]
                == "Configuration applied successfully."):
            result["changed"] = True
        result["api_response"] = api_response

    elif state == "absent" and not exist_check["exists"]:
        result["changed"] = False

    elif state == "updated" and exist_check["exists"]:
        if eval_changed(module, exist_check):
            api_response = update_profile(fw, module, result)

            if api_response:
                if (api_response["Response"]["AdministrationProfile"]["Status"]["#text"]
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
