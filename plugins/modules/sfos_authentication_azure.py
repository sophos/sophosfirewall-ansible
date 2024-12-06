#!/usr/bin/python

# Copyright 2024 Sophos Ltd.  All rights reserved.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
import sys

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
        choices: [upn]
        required: false
    emailaddress:
        description: e-mail address use "email"
        type: str
        choices: [email]
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
    - Philip Finucane (@philfinucane)
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


def get_azure_settings(fw_obj, module, result):
    """Get current settings from Sophos Firewall

    Args:
        fw_obj (SophosFirewall): SophosFirewall object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: Results of lookup
    """
    try:
        resp = fw_obj.get_tag("azureadsso")['Response']['AzureADSSO']
            
    except SophosFirewallZeroRecords as error:
        return {"exists": False, "api_response": str(error)}
    except SophosFirewallAuthFailure as error:
        module.fail_json(msg="Authentication error: {0}".format(error), **result)
    except SophosFirewallAPIError as error:
        module.fail_json(msg="API Error: {0}".format(error), **result)
    except RequestException as error:
        module.fail_json(msg="Error communicating to API: {0}".format(error), **result)

    return {"exists": True, "api_response": resp}

def create_azure(fw_obj, module, result):
    """Create an Azure Server on Sophos Firewall when none exists

    Args:
        fw_obj (SophosFirewall): SophosFirewall object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: API response
    """
    payload = """
        <AzureADSSO>
          <ServerName>{{ name }}</ServerName>
          <ApplicationID>{{ applicationid }}</ApplicationID>
          <TenantID>{{ tenantid }}</TenantID>
          <ClientSecret>{{ clientsecret }}</ClientSecret>
          <RedirectURI>{{ redirecturi }}</RedirectURI>
          <DisplayName>{{ displayname }}</DisplayName>
          <EmailAddress>{{ emailaddress }}</EmailAddress>
          <FallbackUserGroup>{{ fallbackusergroup }}</FallbackUserGroup>
          <UserType>{{ usertype }}</UserType>
          <RoleMapping>
          <IdentifierTypeAndProfile>
          {% for item in identifiertype %}
           <identifiertype>{{ item }}</identifiertype>
          {% endfor %}
          {% for item in identifiervalue %}
           <identifiervalue>{{ item }}</identifiervalue>
          {% endfor %}
          {% for item in profileid %}
           <profileid>{{ item }}</profileid>
          {% endfor %}
          </IdentifierTypeAndProfile>
          </RoleMapping>
        </AzureADSSO>
    
    """
    
    
    template_vars = {
        "name": module.params.get("servername", {}),
        "applicationid": module.params.get("applicationid", {}),
        "tenantid": module.params.get("tenantid", {}),
        "clientsecret": module.params.get("clientsecret", {}),
        "redirecturi": module.params.get("redirecturi", {}),
        "displayname": module.params.get("displayname", {}),
        "emailaddress": module.params.get("emailaddress", {}),
        "fallbackusergroup": module.params.get("fallbackusergroup", {}),
        "usertype": module.params.get("usertype", {}),
        "identifiertype": module.params.get("rolemapping", {}).get("identifiertypeandprofile", {}).get("identifiertype", {}),
        "identifiervalue": module.params.get("rolemapping").get("identifiertypeandprofile", {}).get("identifiervalue", {}),
        "profileid": module.params.get("rolemapping").get("identifiertypeandprofile", {}).get("profileid", {})
    }
    
  
  
    try:
        
        with contextlib.redirect_stdout(output_buffer):
            resp = fw_obj.submit_xml(
                template_data=payload,
                template_vars=template_vars,
                debug=True
            )
    except SophosFirewallAuthFailure as error:
        module.fail_json(msg="Authentication error: {0}".format(error), **result)
    except SophosFirewallAPIError as error:
        module.fail_json(
            msg="API Error: {0},{1}".format(error, output_buffer.getvalue()), **result
        )
    except RequestException as error:
        module.fail_json(msg="Error communicating to API: {0}".format(error), **result)
    
    
    return resp
    
def create_azure_user(fw_obj, module, result):
        """Create an Azure Server on Sophos Firewall when none exists

        Args:
            fw_obj (SophosFirewall): SophosFirewall object
            module (AnsibleModule): AnsibleModule object
            result (dict): Result output to be sent to the console

        Returns:
            dict: API response
        """
        payload2 = """
            <AzureADSSO>
            <ServerName>{{ name }}</ServerName>
            <ApplicationID>{{ applicationid }}</ApplicationID>
            <TenantID>{{ tenantid }}</TenantID>
            <ClientSecret>{{ clientsecret }}</ClientSecret>
            <RedirectURI>{{ redirecturi }}</RedirectURI>
            <DisplayName>{{ displayname }}</DisplayName>
            <EmailAddress>{{ emailaddress }}</EmailAddress>
            <FallbackUserGroup>{{ fallbackusergroup }}</FallbackUserGroup>
            <UserType>{{ usertype }}</UserType>
            </AzureADSSO>
        
        """
        
        
        template_vars2 = {
            "name": module.params.get("servername", {}),
            "applicationid": module.params.get("applicationid", {}),
            "tenantid": module.params.get("tenantid", {}),
            "clientsecret": module.params.get("clientsecret", {}),
            "redirecturi": module.params.get("redirecturi", {}),
            "displayname": module.params.get("displayname", {}),
            "emailaddress": module.params.get("emailaddress", {}),
            "fallbackusergroup": module.params.get("fallbackusergroup", {}),
            "usertype": module.params.get("usertype", {}),
        }
        
    
    
        try:
            
            with contextlib.redirect_stdout(output_buffer):
                resp = fw_obj.submit_xml(
                    template_data=payload2,
                    template_vars=template_vars2,
                    debug=True
                )
        except SophosFirewallAuthFailure as error:
            module.fail_json(msg="Authentication error: {0}".format(error), **result)
        except SophosFirewallAPIError as error:
            module.fail_json(
                msg="API Error: {0},{1}".format(error, output_buffer.getvalue()), **result
            )
        except RequestException as error:
            module.fail_json(msg="Error communicating to API: {0}".format(error), **result)
        
        
        return resp
        
    
    
    
    

def update_azure_add(fw_obj, module, result):
    """Add additional Azure server on Sophos Firewall

    Args:
        fw_obj (SophosFirewall): SophosFirewall object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: API response
    """
    payload = """
        <AzureADSSO>
          <ServerName>{{ name }}</ServerName>
          <ApplicationID>{{ applicationid }}</ApplicationID>
          <TenantID>{{ tenantid }}</TenantID>
          <ClientSecret>{{ clientsecret }}</ClientSecret>
          <RedirectURI>{{ redirecturi }}</RedirectURI>
          <DisplayName>{{ displayname }}</DisplayName>
          <EmailAddress>{{ emailaddress }}</EmailAddress>
          <FallbackUserGroup>{{ fallbackusergroup }}</FallbackUserGroup>
          <UserType>{{ usertype }}</UserType>
          <RoleMapping>
          <IdentifierTypeAndProfile>
          {% for item in identifiertype %}
           <identifiertype>{{ item }}</identifiertype>
          {% endfor %}
          {% for item in identifiervalue %}
           <identifiervalue>{{ item }}</identifiervalue>
          {% endfor %}
          {% for item in profileid %}
           <profileid>{{ item }}</profileid>
          {% endfor %}
          </IdentifierTypeAndProfile>
          </RoleMapping>
        </AzureADSSO>
    
    """
    template_vars = {
        "name": module.params.get("servername"),
        "applicationid": module.params.get("applicationid"),
        "tenantid": module.params.get("tenantid"),
        "clientsecret": module.params.get("clientsecret"),
        "redirecturi": module.params.get("redirecturi"),
        "displayname": module.params.get("displayname"),
        "emailaddress": module.params.get("emailaddress"),
        "fallbackusergroup": module.params.get("fallbackusergroup"),
        "usertype": module.params.get("usertype"),
        "identifiertype": module.params.get("rolemapping", {}).get("identifiertypeandprofile", {}).get("identifiertype", {}),
        "identifiervalue": module.params.get("rolemapping").get("identifiertypeandprofile", {}).get("identifiervalue", {}),
        "profileid": module.params.get("rolemapping").get("identifiertypeandprofile", {}).get("profileid", {})
    }
    
    try:
        with contextlib.redirect_stdout(output_buffer):
            resp = fw_obj.submit_xml(
                template_data=payload,
                template_vars=template_vars,
                set_operation="add",
                debug=True
            )
    except SophosFirewallAuthFailure as error:
        module.fail_json(msg="Authentication error: {0}".format(error), **result)
    except SophosFirewallAPIError as error:
        module.fail_json(
            msg="API Error: {0},{1}".format(error, output_buffer.getvalue()), **result
        )
    except RequestException as error:
        module.fail_json(msg="Error communicating to API: {0}".format(error), **result)
    
    # module.fail_json(msg=f"{resp['Response']}, {output_buffer.getvalue()}")
    return resp

def update_azure_add_user(fw_obj, module, result):
    """Add additional Azure server on Sophos Firewall

    Args:
        fw_obj (SophosFirewall): SophosFirewall object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: API response
    """
    payload2 = """
            <AzureADSSO>
            <ServerName>{{ name }}</ServerName>
            <ApplicationID>{{ applicationid }}</ApplicationID>
            <TenantID>{{ tenantid }}</TenantID>
            <ClientSecret>{{ clientsecret }}</ClientSecret>
            <RedirectURI>{{ redirecturi }}</RedirectURI>
            <DisplayName>{{ displayname }}</DisplayName>
            <EmailAddress>{{ emailaddress }}</EmailAddress>
            <FallbackUserGroup>{{ fallbackusergroup }}</FallbackUserGroup>
            <UserType>{{ usertype }}</UserType>
            </AzureADSSO>
        
        """
    template_vars2 = {
            "name": module.params.get("servername", {}),
            "applicationid": module.params.get("applicationid", {}),
            "tenantid": module.params.get("tenantid", {}),
            "clientsecret": module.params.get("clientsecret", {}),
            "redirecturi": module.params.get("redirecturi", {}),
            "displayname": module.params.get("displayname", {}),
            "emailaddress": module.params.get("emailaddress", {}),
            "fallbackusergroup": module.params.get("fallbackusergroup", {}),
            "usertype": module.params.get("usertype", {}),
        }
    
    try:
        with contextlib.redirect_stdout(output_buffer):
            resp = fw_obj.submit_xml(
                template_data=payload2,
                template_vars=template_vars2,
                set_operation="add",
                debug=True
            )
    except SophosFirewallAuthFailure as error:
        module.fail_json(msg="Authentication error: {0}".format(error), **result)
    except SophosFirewallAPIError as error:
        module.fail_json(
            msg="API Error: {0},{1}".format(error, output_buffer.getvalue()), **result
        )
    except RequestException as error:
        module.fail_json(msg="Error communicating to API: {0}".format(error), **result)
    
   
    return resp




def update_azure_update(fw_obj, module, result):
    """Update existing azure settings on Sophos Firewall

    Args:
        fw_obj (SophosFirewall): SophosFirewall object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: API response
    """
    payload = """
        <AzureADSSO>
          <ServerName>{{ name }}</ServerName>
          <ApplicationID>{{ applicationid }}</ApplicationID>
          <TenantID>{{ tenantid }}</TenantID>
          <ClientSecret>{{ clientsecret }}</ClientSecret>
          <RedirectURI>{{ redirecturi }}</RedirectURI>
          <DisplayName>{{ displayname }}</DisplayName>
          <EmailAddress>{{ emailaddress }}</EmailAddress>
          <FallbackUserGroup>{{ fallbackusergroup }}</FallbackUserGroup>
          <UserType>{{ usertype }}</UserType>
          <RoleMapping>
          <IdentifierTypeAndProfile>
          {% for item in identifiertype %}
           <identifiertype>{{ item }}</identifiertype>
          {% endfor %}
          {% for item in identifiervalue %}
           <identifiervalue>{{ item }}</identifiervalue>
          {% endfor %}
          {% for item in profileid %}
           <profileid>{{ item }}</profileid>
          {% endfor %}
          </IdentifierTypeAndProfile>
          </RoleMapping>
        </AzureADSSO>
    
    """
    template_vars = {
        "name": module.params.get("servername"),
        "applicationid": module.params.get("applicationid"),
        "tenantid": module.params.get("tenantid"),
        "clientsecret": module.params.get("clientsecret"),
        "redirecturi": module.params.get("redirecturi"),
        "displayname": module.params.get("displayname"),
        "emailaddress": module.params.get("emailaddress"),
        "fallbackusergroup": module.params.get("fallbackusergroup"),
        "usertype": module.params.get("usertype"),
        "identifiertype": module.params.get("rolemapping", {}).get("identifiertypeandprofile", {}).get("identifiertype", {}),
        "identifiervalue": module.params.get("rolemapping").get("identifiertypeandprofile", {}).get("identifiervalue", {}),
        "profileid": module.params.get("rolemapping").get("identifiertypeandprofile", {}).get("profileid", {})
    }
    
    try:
        with contextlib.redirect_stdout(output_buffer):
            resp = fw_obj.submit_xml(
                template_data=payload,
                template_vars=template_vars,
                set_operation="update",
                debug=True
            )
    except SophosFirewallAuthFailure as error:
        module.fail_json(msg="Authentication error: {0}".format(error), **result)
    except SophosFirewallAPIError as error:
        module.fail_json(
            msg="API Error: {0},{1}".format(error, output_buffer.getvalue()), **result
        )
    except RequestException as error:
        module.fail_json(msg="Error communicating to API: {0}".format(error), **result)
    
    
    return resp


def update_azure_update_user(fw_obj, module, result):
    """Update existing Azure settings on Sophos Firewall

    Args:
        fw_obj (SophosFirewall): SophosFirewall object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: API response
    """
    payload2 = """
            <AzureADSSO>
            <ServerName>{{ name }}</ServerName>
            <ApplicationID>{{ applicationid }}</ApplicationID>
            <TenantID>{{ tenantid }}</TenantID>
            <ClientSecret>{{ clientsecret }}</ClientSecret>
            <RedirectURI>{{ redirecturi }}</RedirectURI>
            <DisplayName>{{ displayname }}</DisplayName>
            <EmailAddress>{{ emailaddress }}</EmailAddress>
            <FallbackUserGroup>{{ fallbackusergroup }}</FallbackUserGroup>
            <UserType>{{ usertype }}</UserType>
            </AzureADSSO>
        
        """
    template_vars2 = {
            "name": module.params.get("servername", {}),
            "applicationid": module.params.get("applicationid", {}),
            "tenantid": module.params.get("tenantid", {}),
            "clientsecret": module.params.get("clientsecret", {}),
            "redirecturi": module.params.get("redirecturi", {}),
            "displayname": module.params.get("displayname", {}),
            "emailaddress": module.params.get("emailaddress", {}),
            "fallbackusergroup": module.params.get("fallbackusergroup", {}),
            "usertype": module.params.get("usertype", {}),
        }
    
    try:
        with contextlib.redirect_stdout(output_buffer):
            resp = fw_obj.submit_xml(
                template_data=payload2,
                template_vars=template_vars2,
                set_operation="update",
                debug=True
            )
    except SophosFirewallAuthFailure as error:
        module.fail_json(msg="Authentication error: {0}".format(error), **result)
    except SophosFirewallAPIError as error:
        module.fail_json(
            msg="API Error: {0},{1}".format(error, output_buffer.getvalue()), **result
        )
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
    exist_settings = exist_settings["api_response"]
    servername = module.params.get("servername", {})
    applicationid = module.params.get("applicationid", {})
    tenantid = module.params.get("tenantid", {})
    clientsecret = module.params.get("clientsecret", {})
    redirecturi = module.params.get("redirecturi", {})
    displayname = module.params.get("displayname", {})
    emailaddress = module.params.get("emailaddress", {})
    fallbackusergroup = module.params.get("fallbackusergroup", {})
    usertype = module.params.get("usertype", {})
    displayname = module.params.get("displayname", {})
    identifiertype = module.params.get("rolemapping", {}).get("identifiertypeandprofile", {}).get("identifiertype")
    identifiervalue = module.params.get("rolemapping", {}).get("identifiertypeandprofile", {}).get("identifiervalue")
    profileid = module.params.get("rolemapping", {}).get("identifiertypeandprofile", {}).get("profileid")
    
    
    if servername and not servername == exist_settings["ServerName"]:
        return True
    if applicationid and not applicationid == exist_settings["ApplicationID"]:
        return True
    if tenantid and not tenantid == exist_settings["TenantID"]:
        return True
    if redirecturi and not redirecturi == exist_settings["RedirectURI"]:
        return True
    if displayname and not displayname == exist_settings["DisplayName"]:
        return True
    if emailaddress and not emailaddress == exist_settings["EmailAddress"]:
        return True
    if fallbackusergroup and not fallbackusergroup == exist_settings["FallbackUserGroup"]:
        return True
    if fallbackusergroup and not fallbackusergroup == exist_settings["UserType"]:
        return True
    if usertype and not usertype == exist_settings["Attributes"]["NAS-Identifier"]:
            return True
    if identifiertype and not identifiertype == exist_settings["RoleMapping"]["IdentifierTypeAndProfile"]["identifiertype"]:
            return True
    if identifiervalue and not identifiervalue == exist_settings["RoleMapping"]["IdentifierTypeAndProfile"]["identifiertype"]:
            return True
    if profileid and not profileid == exist_settings["RoleMapping"]["IdentifierTypeAndProfile"]["identifiertype"]:
            return True
    if module.params.get("clientsecret"): 
        return True
            
    return False
    
    
def eval_servername(module, exist_settings):
    """Evaluate the Servername provided arguments against existing settings.
    When not a list

    Args:
        module (AnsibleModule): AnsibleModule object
        exist_settings (dict): Response from the call to get_admin_settings()

    Returns:
        bool: Return true if any settings are different, otherwise return false
    """
    exist_settings = exist_settings["api_response"]
    servername = module.params.get("servername", {})
    
    if servername and not servername == exist_settings["ServerName"]:
        return True
    
    return False
    
def eval_list_new_servername(module, exist_settings):
    """Evaluate the Servername provided arguments against existing settings.
    When a list 

    Args:
        module (AnsibleModule): AnsibleModule object
        exist_settings (dict): Response from the call to get_admin_settings()

    Returns:
        bool: Return true if any settings are different, otherwise return false
    """
    
    exist_settings = exist_settings["api_response"]
    servername = module.params.get("servername", {})
    
    for item in exist_settings[::-1]:
        if servername == item["ServerName"]:
            return False
            
    return True


def eval_list_update_server(module, exist_settings):
    """Evaluate the provided arguments against existing settings when checking list. 

    Args:
        module (AnsibleModule): AnsibleModule object
        exist_settings (dict): Response from the call to get_admin_settings()

    Returns:
        bool: Return true if any settings are different, otherwise return false
    """
    
    exist_settings = exist_settings["api_response"]
    servername = module.params.get("servername", {})
    applicationid = module.params.get("applicationid", {})
    tenantid = module.params.get("tenantid", {})
    clientsecret = module.params.get("clientsecret", {})
    redirecturi = module.params.get("redirecturi", {})
    displayname = module.params.get("displayname", {})
    emailaddress = module.params.get("emailaddress", {})
    fallbackusergroup = module.params.get("fallbackusergroup", {})
    usertype = module.params.get("usertype", {})
    displayname = module.params.get("displayname", {})
    identifiertype = module.params.get("rolemapping", {}).get("identifiertypeandprofile", {}).get("identifiertype")
    identifiervalue = module.params.get("rolemapping", {}).get("identifiertypeandprofile", {}).get("identifiervalue")
    profileid = module.params.get("rolemapping", {}).get("identifiertypeandprofile", {}).get("profileid")
    
    list_len = len(exist_settings)
    for i in range(list_len):
       
        if servername and not servername == exist_settings[i]["ServerName"]:
            return True
        if applicationid and not applicationid == exist_settings[i]["ApplicationID"]:
            return True
        if tenantid and not tenantid == exist_settings[i]["TenantID"]:
            return True
        if redirecturi and not redirecturi == exist_settings[i]["RedirectURI"]:
            return True
        if displayname and not displayname == exist_settings[i]["DisplayName"]:
            return True
        if emailaddress and not emailaddress == exist_settings[i]["EmailAddress"]:
            return True
        if fallbackusergroup and not fallbackusergroup == exist_settings[i]["FallbackUserGroup"]:
            return True
        if fallbackusergroup and not fallbackusergroup == exist_settings[i]["UserType"]:
            return True
        if identifiertype and not identifiertype == exist_settings[i]["RoleMapping"]["IdentifierTypeAndProfile"]["identifiertype"]:
                return True
        if identifiervalue and not identifiervalue == exist_settings[i]["RoleMapping"]["IdentifierTypeAndProfile"]["identifiertype"]:
                return True
        if profileid and not profileid == exist_settings[i]["RoleMapping"]["IdentifierTypeAndProfile"]["identifiertype"]:
                return True
        if module.params.get("clientsecret"): 
            return True
            
    return False


def eval_list_update_server_user(module, exist_settings):
    """Evaluate the provided arguments against existing settings when checking list. 

    Args:
        module (AnsibleModule): AnsibleModule object
        exist_settings (dict): Response from the call to get_admin_settings()

    Returns:
        bool: Return true if any settings are different, otherwise return false
    """
    
    exist_settings = exist_settings["api_response"]
    servername = module.params.get("servername", {})
    applicationid = module.params.get("applicationid", {})
    tenantid = module.params.get("tenantid", {})
    clientsecret = module.params.get("clientsecret", {})
    redirecturi = module.params.get("redirecturi", {})
    displayname = module.params.get("displayname", {})
    emailaddress = module.params.get("emailaddress", {})
    fallbackusergroup = module.params.get("fallbackusergroup", {})
    usertype = module.params.get("usertype", {})
    displayname = module.params.get("displayname", {})
    
    
    list_len = len(exist_settings)
    for i in range(list_len):
       
        if servername and not servername == exist_settings[i]["ServerName"]:
            return True
        if applicationid and not applicationid == exist_settings[i]["ApplicationID"]:
            return True
        if tenantid and not tenantid == exist_settings[i]["TenantID"]:
            return True
        if redirecturi and not redirecturi == exist_settings[i]["RedirectURI"]:
            return True
        if displayname and not displayname == exist_settings[i]["DisplayName"]:
            return True
        if emailaddress and not emailaddress == exist_settings[i]["EmailAddress"]:
            return True
        if fallbackusergroup and not fallbackusergroup == exist_settings[i]["FallbackUserGroup"]:
            return True
        if fallbackusergroup and not fallbackusergroup == exist_settings[i]["UserType"]:
            return True
        if usertype and not usertype == exist_settings[i]["Attributes"]["NAS-Identifier"]:
                return True
        if module.params.get("clientsecret"): 
            return True
            
    return False



def remove_azure(fw_obj, module, result):
    """Remove a Azure Server on a Sophos Firewall

    Args:
        fw_obj (SophosFirewall): SophosFirewall object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: API response
    """
    payload = """
            <Remove>
            <AzureADSSO>
		    <ServerName>{{ name }}</ServerName>
            </AzureADSSO>
            </Remove>
    """
    template_vars = {
        "name": module.params.get("servername")
    }
    
    try:
        with contextlib.redirect_stdout(output_buffer):
            resp = fw_obj.submit_xml(
                template_data=payload,
                template_vars=template_vars,
                set_operation=None,
                debug=True
            )
    except SophosFirewallAuthFailure as error:
        module.fail_json(msg="Authentication error: {0}".format(error), **result)
    except SophosFirewallAPIError as error:
        module.fail_json(
            msg="API Error: {0},{1}".format(error, output_buffer.getvalue()), **result
        )
    except RequestException as error:
        module.fail_json(msg="Error communicating to API: {0}".format(error), **result)
    
    
    return resp


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
        "displayname": {"type": "str", "required": False, "choices": ["upn"]},
        "emailaddress": {"type": "str", "required": False, "choices": ["email"]},
        "fallbackusergroup": {"type": "str", "choices": ["Open Group", "Guest Group"]},
        "usertype": {"type": "str", "choices": ["User", "Administrator"]},
        "rolemapping": {"type": "dict", "required": False},
        "identifiertypeandprofile": {"type": "dict", "required": False},
        "identifiertype": {"type": "list", "elements": "str", "required": False, "choices": ["groups", "roles"]},
        "identifiervalue": {"type": "list", "elements": "str", "required": False},
        "profileid": {"type": "list", "elements": "str", "required": False},
        "state": {"type": "str", "required": True, "choices": ["updated", "query", "absent"]}
    }

    module = AnsibleModule(argument_spec=argument_spec,

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
    usertype = module.params.get("usertype")

    exist_settings = get_azure_settings(fw, module, result)
    result["api_response"] = exist_settings["api_response"]
    
    
    if state == "absent":
                
                api_response = remove_azure(fw, module, result)
               
                if api_response:
                    if api_response['Response']['AzureADSSO']["Status"]["#text"] == "Configuration applied successfully.":
                        result["changed"] = True
                    result["api_response"] = api_response
                    module.exit_json(**result)
                else:
                    result["changed"] = False
    
    if isinstance(result["api_response"], dict):

        if state == "query":
            module.exit_json(**result)

        if module.check_mode:
            result["check_mode"] = True
            module.exit_json(**result)

        elif state == "updated" and result["api_response"].get('Status') == 'No. of records Zero.':
        
            if usertype == "Administrator":
                
                api_response = create_azure(fw, module, result)
                
                if api_response:
                    if api_response['Response']['AzureADSSO']["Status"]["#text"] == "Configuration applied successfully.":
                        result["changed"] = True
                    result["api_response"] = api_response
                else:
                    result["changed"] = False
            else:
                
                if usertype == "User":
                    api_response = create_azure_user(fw, module, result)
                    
                    if api_response:
                        if api_response['Response']['AzureADSSO']["Status"]["#text"] == "Configuration applied successfully.":
                            result["changed"] = True
                        result["api_response"] = api_response
                    else:
                        result["changed"] = False
    
        
        elif state == "updated" and "ServerName" in result["api_response"]:
            
            if usertype == "Administrator":
            
                if eval_servername(module, exist_settings):
                    if eval_changed(module, exist_settings):
                       
                        api_response = update_azure_add(fw, module, result)
                        print(f'toppp2',api_response)
                
                        if api_response:
                            if (api_response['Response']['AzureADSSO']["Status"]["#text"]
                            
                                    == "Configuration applied successfully."):
                                result["changed"] = True
                            result["api_response"] = api_response
                        else:
                            result["changed"] = False
                            
                if not eval_servername(module, exist_settings):
                    if eval_changed(module, exist_settings):
                        
                        api_response = update_azure_update(fw, module, result)
                        print(f'toppp2',api_response)
                
                        if api_response:
                            if (api_response['Response']['AzureADSSO']["Status"]["#text"]
                            
                                    == "Configuration applied successfully."):
                                result["changed"] = True
                            result["api_response"] = api_response
                        else:
                            result["changed"] = False
            else:
                if usertype == "User":
                    
                    if eval_servername(module, exist_settings):
                        if eval_changed(module, exist_settings):
                            
                            api_response = update_azure_add_user(fw, module, result)
                            print(f'toppp2',api_response)
                    
                            if api_response:
                                if (api_response['Response']['AzureADSSO']["Status"]["#text"]
                                
                                        == "Configuration applied successfully."):
                                    result["changed"] = True
                                result["api_response"] = api_response
                            else:
                                result["changed"] = False
                                
                    if not eval_servername(module, exist_settings):
                        if eval_changed(module, exist_settings):
                            
                            api_response = update_azure_update_user(fw, module, result)
                            print(f'toppp2',api_response)
                    
                            if api_response:
                                if (api_response['Response']['AzureADSSO']["Status"]["#text"]
                                
                                        == "Configuration applied successfully."):
                                    result["changed"] = True
                                result["api_response"] = api_response
                            else:
                                result["changed"] = False
                    
                    
                    
                        
    if isinstance(result["api_response"], list):
        
        if usertype == "Administrator":
        
            if eval_list_new_servername(module, exist_settings):
                        module.exit_json(msg=f"eval=true44")
                        api_response = update_azure_add(fw, module, result)
                        print(f'toppp2',api_response)
                
                        if api_response:
                            if (api_response['Response']['AzureADSSO']["Status"]["#text"]
                            
                                    == "Configuration applied successfully."):
                                result["changed"] = True
                            result["api_response"] = api_response
                        else:
                            result["changed"] = False
            else:
        
                if eval_list_update_server(module, exist_settings):
                    
                    api_response = update_azure_update(fw, module, result)
                        
                    if api_response:
                        if (api_response['Response']['AzureADSSO']["Status"]["#text"] == "Configuration applied successfully."):
                            result["changed"] = True
                        result["api_response"] = api_response
                    else:
                        result["changed"] = False
        else:
            if usertype == "User":
                
                if eval_list_new_servername(module, exist_settings):
                            
                            api_response = update_azure_add_user(fw, module, result)
                            print(f'toppp2',api_response)
                    
                            if api_response:
                                if (api_response['Response']['AzureADSSO']["Status"]["#text"]
                                
                                        == "Configuration applied successfully."):
                                    result["changed"] = True
                                result["api_response"] = api_response
                            else:
                                result["changed"] = False
                else:
            
                    if eval_list_update_server_user(module, exist_settings):
                        
                        api_response = update_azure_update_user(fw, module, result)
                            
                        if api_response:
                            if (api_response['Response']['AzureADSSO']["Status"]["#text"] == "Configuration applied successfully."):
                                result["changed"] = True
                            result["api_response"] = api_response
                        else:
                            result["changed"] = False
    
                    

    module.exit_json(**result)
  

if __name__ == "__main__":
    main()