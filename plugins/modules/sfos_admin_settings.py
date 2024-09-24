#!/usr/bin/python

# Copyright 2024 Sophos Ltd.  All rights reserved.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r'''
---
module: sfos_admin_settings

short_description: Manage Admin and user settings (System > Administration)

version_added: "1.0.0"

description: Manage settings under System > Administration > Admin and user settings

extends_documentation_fragment:
  - sophos.sophos_firewall.fragments.base

options:
    hostname_settings:
        description: Hostname settings.
        required: false
        type: dict
        suboptions:
            hostname:
                description: Hostname of the firewall
                type: str
                required: false
            description:
                description: Description field in the hostname settings
                type: str
                required: false
    webadmin_settings:
        description: Web admin settings
        type: dict
        required: false
        suboptions:
            certificate:
                description: Certificate used for the admin interface
                type: str
                required: false
            https_port:
                description: HTTPS port for the administrative interface
                type: str
                required: false
            userportal_https_port:
                description: HTTPS port for the user portal
                type: str
                required: false
            vpnportal_https_port:
                description: HTTPS port for the VPN portal
                type: str
                required: false
            portal_redirect_mode:
                description: Redirect mode
                type: str
                choices: ["ip"]
                required: false
            portal_custom_hostname:
                description: Custom portal hostname
                type: str
                required: false
    login_security:
        description: Login security settings
        type: dict
        required: false
        suboptions:
            logout_session:
                description: Enable to logout Admin Session after configured timeout. Specify number of minutes to enable (1-120)
                type: str
                required: false
            block_login:
                description: Enable to block Admin login after configured number of failed attempts within configured time span. 
                type: str
                choices: ["Enable", "Disable"]
                required: false
            unsuccessful_attempt:
                description: Number of unsuccessful attempts
                type: str
                required: false
            duration:
                description: Time span within which if Admin Login attempts exceed configured Unsuccessful Attempts, then Admin Login gets blocked. (1-120 seconds).
                type: str
                required: false
            minutes:
                description: Time interval for which Admin Login is blocked (1-60 minutes)
                type: str
                required: false
    password_complexity:
        description: Password complexity settings
        type: dict
        required: false
        suboptions:
            complexity_check:
                description: Enable/Disable complexity check
                type: str
                choices: ["Enable", "Disable"]
                required: false
            enforce_min_length:
                description: Enable/Disable enforcement of minimum password length
                type: str
                choices: ["Enable", "Disable"]
            include_alpha:
                description: Enable/Disable special character requirement
                type: str
                choices: ["Enable", "Disable"]
                required: false
            include_numeric:
                description: Enable/Disable special character requirement
                type: str
                choices: ["Enable", "Disable"]
                required: false
            include_special:
                description: Enable/Disable special character requirement
                type: str
                choices: ["Enable", "Disable"]
                required: false
            min_length:
                description: Minimum password length
                type: str
                required: false
    login_disclaimer:
        description: Enable/Disable the login disclaimer
        type: str
        choices: ["Enable", "Disable"]
        required: false
    state:
        description:
            - Use C(query) to retrieve or C(updated) to modify
        choices: [updated, query]
        type: str
        required: true

author:
    - Matt Mullen (@mamullen13316)
'''

EXAMPLES = r'''
- name: Update hostname settings
    sophos.sophos_firewall.sfos_admin_settings:
    username: "{{ username }}"
    password: "{{ password }}"
    hostname: "{{ inventory_hostname }}"
    port: 4444
    verify: false
    hostname_settings:
        hostname: sophos-firewall-dev1
        description: Automation Testing 1
    state: updated
    delegate_to: localhost

- name: Update webadmin settings
    sophos.sophos_firewall.sfos_admin_settings:
    username: "{{ username }}"
    password: "{{ password }}"
    hostname: "{{ inventory_hostname }}"
    port: 4444
    verify: false
    webadmin_settings:
        vpnportal_https_port: 444
        userportal_https_port: 4445
    state: updated
    delegate_to: localhost

- name: Update loginsecurity settings
    sophos.sophos_firewall.sfos_admin_settings:
    username: "{{ username }}"
    password: "{{ password }}"
    hostname: "{{ inventory_hostname }}"
    port: 4444
    verify: false
    login_security:
        logout_session: 120
        block_login: Enable
        unsuccessful_attempt: 3
        duration: 30
        minutes: 1
    state: updated
    delegate_to: localhost

- name: Update administrator password complexity settings
    sophos.sophos_firewall.sfos_admin_settings:
    username: "{{ username }}"
    password: "{{ password }}"
    hostname: "{{ inventory_hostname }}"
    port: 4444
    verify: false
    password_complexity:
        complexity_check: Enable
        enforce_min_length: Enable
        include_alpha: Enable
        include_numeric: Enable
        include_special: Enable
        min_length: 10
    state: updated
    delegate_to: localhost

- name: Update login disclaimer
    sophos.sophos_firewall.sfos_admin_settings:
    username: "{{ username }}"
    password: "{{ password }}"
    hostname: "{{ inventory_hostname }}"
    port: 4444
    verify: false
    login_disclaimer: Enable
    state: updated
    delegate_to: localhost

- name: Query admin settings
    sophos.sophos_firewall.sfos_admin_settings:
    username: "{{ username }}"
    password: "{{ password }}"
    hostname: "{{ inventory_hostname }}"
    port: 4444
    verify: false
    state: query
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


def get_admin_settings(fw_obj, module, result):
    """Get current admin settings from Sophos Firewall

    Args:
        fw_obj (SophosFirewall): SophosFirewall object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: Results of lookup
    """
    try:
        resp = fw_obj.get_admin_settings()
    except SophosFirewallZeroRecords as error:
        return {"exists": False, "api_response": str(error)}
    except SophosFirewallAuthFailure as error:
        module.fail_json(msg="Authentication error: {0}".format(error), **result)
    except SophosFirewallAPIError as error:
        module.fail_json(msg="API Error: {0}".format(error), **result)
    except RequestException as error:
        module.fail_json(msg="Error communicating to API: {0}".format(error), **result)

    return {"exists": True, "api_response": resp}


def update_admin_settings(fw_obj, module, result):
    """Update admin settings on Sophos Firewall

    Args:
        fw_obj (SophosFirewall): SophosFirewall object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: API response
    """
    resp_list = []
 
    hostname_settings = module.params.get("hostname_settings", {})
    if hostname_settings:
       resp_list.append(update_request(module, result, fw_obj.update_hostname_settings, **hostname_settings))

    webadmin_settings = module.params.get("webadmin_settings", {})
    if webadmin_settings:
        resp_list.append(update_request(module, result, fw_obj.update_webadmin_settings, **webadmin_settings))

    login_security = module.params.get("login_security", {})
    if login_security:
        resp_list.append(update_request(module, result, fw_obj.update_loginsecurity_settings, **login_security))

    password_complexity = module.params.get("password_complexity", {})
    if password_complexity:
        resp_list.append(update_request(module, result, fw_obj.update_passwordcomplexity_settings, **password_complexity))
    
    login_disclaimer_setting = module.params.get("login_disclaimer")
    if login_disclaimer_setting:
        login_disclaimer={"enabled": True} if login_disclaimer_setting == "Enable" else {"enabled": False}
        resp_list.append(update_request(module, result, fw_obj.update_login_disclaimer, **login_disclaimer))
    
    return resp_list

def update_request(module, result, method, **args):
    """Generate the update request using the SDK.

    Args:
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console
        method (method): SophosFirewall object method to be used for the request

    Returns:
        list: List of API responses
    """
    try:
        with contextlib.redirect_stdout(output_buffer):
            resp = method(**args)
    except SophosFirewallAuthFailure as error:
        module.fail_json(msg="Authentication error: {0}".format(error), **result)
    except SophosFirewallAPIError as error:
        module.fail_json(msg="API Error: {0},{1}".format(error, output_buffer.getvalue()), **result)
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
    exist_settings = exist_settings["api_response"]["Response"]["AdminSettings"]

    hostname_settings = module.params.get("hostname_settings", {})
    if hostname_settings:
        hostname = module.params["hostname_settings"].get("hostname")
        description = module.params["hostname_settings"].get("description")
        if (hostname and not hostname == exist_settings["HostnameSettings"]["HostName"] or
            description and not description == exist_settings["HostnameSettings"]["HostNameDesc"]):
            return True
    
    webadmin_settings = module.params.get("webadmin_settings", {})
    if webadmin_settings:
        certificate = module.params["webadmin_settings"].get("certificate")
        https_port = module.params["webadmin_settings"].get("https_port")
        userportal_https_port = module.params["webadmin_settings"].get("userportal_https_port")
        vpnportal_https_port = module.params["webadmin_settings"].get("vpnportal_https_port")
        portal_redirect_mode = module.params["webadmin_settings"].get("portal_redirect_mode")
        portal_custom_hostname = module.params["webadmin_settings"].get("portal_custom_hostname")
        if (certificate and not certificate == exist_settings["WebAdminSettings"]["Certificate"] or
            https_port and not https_port == exist_settings["WebAdminSettings"]["HTTPSPort"] or
            userportal_https_port and not userportal_https_port == exist_settings["WebAdminSettings"]["UserPortalHTTPSPort"] or
            vpnportal_https_port and not vpnportal_https_port == exist_settings["WebAdminSettings"]["VPNPortalHTTPSPort"] or
            portal_redirect_mode and not portal_redirect_mode == exist_settings["WebAdminSettings"]["PortalRedirectMode"] or
            portal_custom_hostname and not portal_custom_hostname == exist_settings["WebAdminSettings"]["PortalCustomHostname"]
        ):  
            return True

    login_security = module.params.get("login_security", {})
    if login_security:
        logout_session = module.params["login_security"].get("logout_session")
        block_login = module.params["login_security"].get("block_login")
        unsuccessful_attempt = module.params["login_security"].get("unsuccessful_attempt")
        duration = module.params["login_security"].get("duration")
        minutes = module.params["login_security"].get("minutes")
        if (logout_session and not logout_session == exist_settings["LoginSecurity"]["LogoutSession"] or
            block_login and not block_login == exist_settings["LoginSecurity"]["BlockLogin"] or
            unsuccessful_attempt and not unsuccessful_attempt == exist_settings["LoginSecurity"]["BlockLoginSettings"]["UnsucccessfulAttempt"] or
            duration and not duration == exist_settings["LoginSecurity"]["BlockLoginSettings"]["Duration"] or
            minutes and not minutes == exist_settings["LoginSecurity"]["BlockLoginSettings"]["ForMinutes"]
            ):
            return True

    password_complexity = module.params.get("password_complexity", {})
    if password_complexity:
        complexity_check = module.params["password_complexity"].get("complexity_check")
        enforce_min_length = module.params["password_complexity"].get("enforce_min_length")
        include_alpha = module.params["password_complexity"].get("include_alpha")
        include_numeric = module.params["password_complexity"].get("include_numeric")
        include_special = module.params["password_complexity"].get("include_special")
        min_length = module.params["password_complexity"].get("min_length")
        if (complexity_check and not complexity_check == exist_settings["PasswordComplexitySettings"]["PasswordComplexityCheck"] or
            enforce_min_length and not enforce_min_length == exist_settings["PasswordComplexitySettings"]["PasswordComplexity"]["MinimumPasswordLength"] or
            include_alpha and not include_alpha == exist_settings["PasswordComplexitySettings"]["PasswordComplexity"]["IncludeAlphabeticCharacters"] or
            include_numeric and not include_numeric == exist_settings["PasswordComplexitySettings"]["PasswordComplexity"]["IncludeNumericCharacter"] or
            include_special and not include_special == exist_settings["PasswordComplexitySettings"]["PasswordComplexity"]["IncludeSpecialCharacter"] or
            min_length and not min_length == exist_settings["PasswordComplexitySettings"]["PasswordComplexity"]["MinimumPasswordLengthValue"]
            ):
            return True

    login_disclaimer = module.params.get("login_disclaimer")
    if login_disclaimer and not login_disclaimer == exist_settings["LoginDisclaimer"]:
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
        "hostname_settings": {"type": "dict", "required": False, "options": {
            "hostname": {"type": "str", "required": False},
            "description": {"type": "str", "required": False}
            }
        },
        "webadmin_settings": {"type": "dict", "required": False, "options": {
            "certificate": {"type": "str", "required": False},
            "https_port": {"type": "str", "required": False},
            "userportal_https_port": {"type": "str", "required": False},
            "vpnportal_https_port": {"type": "str", "required": False},
            "portal_redirect_mode": {"type": "str", "required": False},
            "portal_custom_hostname": {"type": "str", "required": False},
            }
        },
        "login_security": {"type": "dict", "required": False, "options": {
            "logout_session": {"type": "str"},
            "block_login": {"type": "str", "choices": ["Enable", "Disable"]},
            "unsuccessful_attempt": {"type": "str", "required": False},
            "duration": {"type": "str", "required": False},
            "minutes": {"type": "str", "required": False}
            }
        },
        "password_complexity": {"type": "dict", "required": False, "options": {
            "complexity_check": {"type": "str", "choices": ["Enable", "Disable"]},
            "enforce_min_length": {"type": "str", "choices": ["Enable", "Disable"]},
            "include_alpha": {"type": "str", "required": False},
            "include_numeric": {"type": "str", "required": False},
            "include_special": {"type": "str", "required": False},
            "min_length": {"type": "str", "required": False},
            }
        },
        "login_disclaimer": {"type": "str", "required": False, "choices": ["Enable", "Disable"]},
        "state": {"type": "str", "required": True, "choices": ["updated", "query"]},
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

    exist_settings = get_admin_settings(fw, module, result)
    result["api_response"] = exist_settings["api_response"]

    if state == "query":
        module.exit_json(**result)

    if module.check_mode:
        result["check_mode"] = True
        module.exit_json(**result)

    elif state == "updated":
        if eval_changed(module, exist_settings):
            api_response = update_admin_settings(fw, module, result)

            result["api_response"] = []
            if api_response:
                for response in api_response:
                    for xml_tag in ["LoginDisclaimer", "HostnameSettings", "WebAdminSettings", "LoginSecurity", "PasswordComplexitySettings"]:
                        if xml_tag in response["Response"]:
                            if response["Response"][xml_tag]["Status"]["#text"] == "Configuration applied successfully.":
                                result["changed"] = True
                            result["api_response"].append(response)

    module.exit_json(**result)


if __name__ == "__main__":
    main()
