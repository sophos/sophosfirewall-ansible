#!/usr/bin/python

# Copyright 2024 Sophos Ltd.  All rights reserved.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r'''
---
module: sfos_authentication_azureadsso.py

short_description: Manage Authentication settings AzureADSSO

version_added: "1.0.0"

description: Manage authentication servers (Configure > Authentication > Servers> Add) on Sophos Firewall

extends_documentation_fragment:
  - sophos.sophos_firewall.fragments.base

options:
    servername:
        description: Name of Server
        type: str
        required: false
    applicationid:
        description: Aplication Client ID
        type: str
        required: false
    tenantid:
        description: Directory tenant ID
        type: str
        required: false
    clientsecret:
        description: Client secret
        type: str
        required: false
    redirecturi:
        description: Redirect URI
        type: str
        required: false
    displayname:
        description: Display name use "upn"
        type: str
        required: false
    emailaddress:
        description: e-mail address use "email"
        type: str
        required: false
    fallbackusergroup:
        description: Fallback user group auto completed
        type: str
        choices: [open group, guest group]
        required: false
    usertype:
        description: User type selection
        type: str
        choices: [user, administrator]
        required: false
    rolemapping:
        description: Identifier type and profile for administrator user type
        type: str
        required: false
        suboptions:
            identifiertype:
                type: list
                elements: str
                required: false
            identifiervalue:
                type: list
                elements: str
                required: false
            profileid:
                type: list
                elements: str
                required: false


author:
    - Matt Mullen (@mamullen13316)
'''

EXAMPLES = r'''
- name: Update Azure AD SSO
  sophos.sophos_firewall.sfos_authentication_azureadsso:
    username: "{{ username }}"
    password: "{{ password }}"
    hostname: "{{ inventory_hostname }}"
    port: 4444
    verify: false
    servername: SophosFirewallSSO
    applicationid: 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx'
    tenantid: 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx'
    redirecturi: sophosfirewall.net
    displayname: upn
    emailaddress: email
    fallbackusergroup: Open Group
    usertype: Administrator
    rolemapping:
    identifiertypeandprofile:
        identifiertype:
            - groups
            - groups
            - groups
        identifiervalue:
            - AAD-SFNetAdministrators
            - AAD-SFEEReadOnly
            - AAD-SFAudit
        profileid:
            - Administrator
            - ReadOnly
            - Audit Admin
    state: updated
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


def get_azureadsso_settings(fw_obj, module, result):
    """Get current DNS settings from Sophos Firewall

    Args:
        fw_obj (SophosFirewall): SophosFirewall object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: Results of lookup
    """
    try:
        resp = fw_obj.get_tag("azureadsso")
    except SophosFirewallZeroRecords as error:
        return {"exists": False, "api_response": str(error)}
    except SophosFirewallAuthFailure as error:
        module.fail_json(msg="Authentication error: {0}".format(error), **result)
    except SophosFirewallAPIError as error:
        module.fail_json(msg="API Error: {0}".format(error), **result)
    except RequestException as error:
        module.fail_json(msg="Error communicating to API: {0}".format(error), **result)

    return {"exists": True, "api_response": resp}


def update_azureadsso_settings(fw_obj, module, result):
    """Update Azure AD SSO settings on Sophos Firewall

    Args:
        fw_obj (SophosFirewall): SophosFirewall object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: API response
    """
    update_params = fw_obj.get_tag("AzureADSSO")['Response']['AzureADSSO']
 
    
    if module.params.get("servername"):
        update_params["ServerName"] = module.params.get("servername")
            
    if module.params.get("applicationid"):
        update_params["ApplicationID"] = module.params.get("applicationid")
            
    if module.params.get("tenantid"):
        update_params["TenantID"] = module.params.get("tenantid")
    
    clientsecret_setting = module.params.get("clientsecret", {})
    if clientsecret_setting:
        clientsecret = clientsecret_setting("clientsecret")
        if clientsecret:
            update_params["ClientSecret"]["#text"] = clientsecret
    if module.params.get("clientsecret"):
        update_params["ClientSecret"] = module.params.get("clientsecret")           
    
    if module.params.get("redirecturi"):
        update_params["RedirectURI"] = module.params.get("redirecturi") 
    
    if module.params.get("displayname"):
        update_params["DisplayName"] = module.params.get("displayname") 
            
    if module.params.get("emailaddress"):
        update_params["EmailAddress"] = module.params.get("emailaddress")
            
    if module.params.get("fallbackusergroup"):
        update_params["FallbackUserGroup"] = module.params.get("fallbackusergroup") 
    
    usertype_setting = module.params.get("usertype", {})
    if module.params.get("usertype"):
        update_params["UserType"] = module.params.get("usertype")
            
    if usertype_setting == "Administrator":
        identifiertype_setting = module.params.get("rolemapping", {}).get("identifiertypeandprofile", {}).get("identifiertype", {})
        print('test', identifiertype_setting)
        if identifiertype_setting:
            identifiertype = identifiertype_setting
            if identifiertype:
                print('test2', update_params)
                if "RoleMapping" in update_params and "IdentifierTypeAndProfile" in update_params["RoleMapping"] and "identifiertype" in update_params["RoleMapping"]["IdentifierTypeAndProfile"]:
                    update_params["RoleMapping"]["IdentifierTypeAndProfile"]["identifiertype"] = identifiertype
    
            
        
        identifiervalue_setting = module.params.get("rolemapping", {}).get("identifiertypeandprofile", {}).get("identifiervalue", {})
        if identifiervalue_setting:
            identifiervalue = identifiervalue_setting
            print('topie =', identifiervalue)
            if identifiervalue:
                if "RoleMapping" in update_params and "IdentifierTypeAndProfile" in update_params["RoleMapping"] and "identifiervalue" in update_params["RoleMapping"]["IdentifierTypeAndProfile"]:
                    update_params["RoleMapping"]["IdentifierTypeAndProfile"]["identifiervalue"] = identifiervalue
                else:
                    identifiervalue_setting = identifiervalue
        
        profileid_setting = module.params.get("rolemapping", {}).get("identifiertypeandprofile", {}).get("profileid", {})
        if profileid_setting:
            profileid = profileid_setting
            if profileid:
                if "RoleMapping" in update_params and "IdentifierTypeAndProfile" in update_params["RoleMapping"] and "profileid" in update_params["RoleMapping"]["IdentifierTypeAndProfile"]:
                    update_params["RoleMapping"]["IdentifierTypeAndProfile"]["profileid"] = profileid
                else:
                    profileid_setting = profileid
    
    
    if usertype_setting == "Administrator":
        identifiertype_setting = module.params.get("rolemapping", {}).get("identifiertypeandprofile", {}).get("identifiertype", {})
        identifiervalue_setting = module.params.get("rolemapping", {}).get("identifiertypeandprofile", {}).get("identifiervalue", {})
        profileid_setting = module.params.get("rolemapping", {}).get("identifiertypeandprofile", {}).get("profileid", {})
        if "RoleMapping" not in update_params:
            update_params["RoleMapping"]= {}
        if "IdentifierTypeAndProfile" not in update_params["RoleMapping"]:
            update_params["RoleMapping"]["IdentifierTypeAndProfile"] = {}
            
        if "identifiertype" not in update_params["RoleMapping"]["IdentifierTypeAndProfile"]:
            update_params["RoleMapping"]["IdentifierTypeAndProfile"]["identifiertype"] = {}
            
        if "identifiervalue" not in update_params["RoleMapping"]["IdentifierTypeAndProfile"]:
            update_params["RoleMapping"]["IdentifierTypeAndProfile"]["identifiervalue"] = {}
            
        if "profileid" not in update_params["RoleMapping"]["IdentifierTypeAndProfile"]:
            update_params["RoleMapping"]["IdentifierTypeAndProfile"]["profileid"] = {}

        update_params["RoleMapping"]["IdentifierTypeAndProfile"]["identifiertype"] = identifiertype_setting
        update_params["RoleMapping"]["IdentifierTypeAndProfile"]["identifiervalue"] = identifiervalue_setting
        update_params["RoleMapping"]["IdentifierTypeAndProfile"]["profileid"] = profileid_setting

    try:
        with contextlib.redirect_stdout(output_buffer):     
            resp = fw_obj.update(xml_tag="AzureADSSO", update_params=update_params, debug=True)
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
    exist_settings = exist_settings["api_response"]["Response"]
    servername = module.params.get("servername", {})
    applicationid = module.params.get("applicationid", {})
    tenantid = module.params.get("tenantid", {})
    clientsecret = module.params.get("clientsecret", {})
    redirecturi = module.params.get("redirecturi", {})
    displayname = module.params.get("displayname", {})
    emailaddress = module.params.get("emailaddress", {})
    fallbackusergroup = module.params.get("fallbackusergroup", {})
    usertype = module.params.get("usertype", {})
    identifiertype = module.params.get("rolemapping", {}).get("identifiertypeandprofile", {}).get("identifiertype", {})
    identifiervalue = module.params.get("rolemapping", {}).get("identifiertypeandprofile", {}).get("identifiervalue", {})
    profileid = module.params.get("rolemapping", {}).get("identifiertypeandprofile", {}).get("profileid", {})
    
    
    if servername and not servername == exist_settings["AzureADSSO"]["ServerName"]:
        return True
    if applicationid and not applicationid == exist_settings["AzureADSSO"]["ApplicationID"]:
        return True
    if tenantid and not tenantid == exist_settings["AzureADSSO"]["TenantID"]:
        return True
    if clientsecret and not clientsecret == exist_settings["AzureADSSO"]["ClientSecret"]:
        return True
    if redirecturi and not redirecturi == exist_settings["AzureADSSO"]["RedirectURI"]:
        return True
    if displayname and not displayname == exist_settings["AzureADSSO"]["DisplayName"]:
        return True
    if emailaddress and not emailaddress == exist_settings["AzureADSSO"]["EmailAddress"]:
        return True
    if fallbackusergroup and not fallbackusergroup == exist_settings["AzureADSSO"]["FallbackUserGroup"]:
        return True
    if usertype and not usertype == exist_settings["AzureADSSO"]["UserType"]:
        return True
    if usertype == "Administrator" :
        if identifiertype and not identifiertype == exist_settings["AzureADSSO"]["RoleMapping"]["IdentifierTypeAndProfile"]["identifiertype"]:
            return True
        if identifiervalue and not identifiervalue == exist_settings["AzureADSSO"]["RoleMapping"]["IdentifierTypeAndProfile"]["identifiervalue"]:
            return True
        if profileid and not profileid == exist_settings["AzureADSSO"]["RoleMapping"]["IdentifierTypeAndProfile"]["profileid"]:
            return True
        
    elif usertype == "User":
        if usertype and not usertype == exist_settings["AzureADSSO"]["UserType"]:
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
        "servername": {"type": "str", "required": False},
        "applicationid": {"type": "str", "required": False},
        "tenantid": {"type": "str", "required": False},
        "clientsecret": {"type": "str", "required": False},
        "redirecturi": {"type": "str", "required": False},
        "displayname": {"type": "str", "required": False},
        "emailaddress": {"type": "str", "required": False},
        "fallbackusergroup": {"type": "str", "choices": ["Open Group", "Guest Group"]},
        "usertype": {"type": "str", "choices": ["User", "Administrator"]},
        "rolemapping": {"type": "dict", "required": False},
        "identifiertypeandprofile": {"type": "dict", "required": False},
        "identifiertype": {"type": "list", "elements": "str", "required": False},
        "identifiervalue": {"type": "list", "elements": "str", "required": False},
        "profileid": {"type": "list", "elements": "str", "required": False},
        "state": {"type": "str", "required": True, "choices": ["updated", "query"]}
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

    exist_settings = get_azureadsso_settings(fw, module, result)
    result["api_response"] = exist_settings["api_response"]
    # print(result["api_response"])
    # print(f'top=', exist_settings["AzureADSSO"])

    if state == "query":
        module.exit_json(**result)

    if module.check_mode:
        result["check_mode"] = True
        module.exit_json(**result)

    elif state == "updated":
        if eval_changed(module, exist_settings):
            api_response = update_azureadsso_settings(fw, module, result)
            
            if api_response:
                if (api_response["Response"]["AzureADSSO"]["Status"]["#text"]
                        == "Configuration applied successfully."):
                    result["changed"] = True
                result["api_response"] = api_response
            else:
                result["changed"] = False

    module.exit_json(**result)


if __name__ == "__main__":
    main()
