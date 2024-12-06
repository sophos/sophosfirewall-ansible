#!/usr/bin/python

# Copyright 2024 Sophos Ltd.  All rights reserved.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
import sys

__metaclass__ = type

DOCUMENTATION = r'''
---
module: sfos_authentication_ldap.py

short_description: Manage Authentication settings LDAP

version_added: "1.0.0"

description: Manage authentication servers (Configure > Authentication > Servers> Add) on Sophos Firewall

extends_documentation_fragment:
  - sophos.sophos_firewall.fragments.base

options:
    servername:
        description: Name of Server
        type: str
        required: false
    serverAddress:
        description: Server IP Address
        type: str
        required: false
    port:
        description: Port number
        type: str
        required: false
    version:
        description: Client secret
        type: str
        choices: [2, 3]
        required: false
    connectionSecurity:
        description: Encryption
        choices: [Simple, SSL, TLS]
        type: str
        required: false
    anonymousLogin:
        description: Anonymous Login
        type: str
        choices: [Enable, Disable]
        required: false
    baseDN:
        description: BaseDN
        type: str
        required: false   
    appendbaseDN:
        description: Append BaseDN
        type: str
        choices: [Enable, Disable]
        required: false
    authenticationattribute:
        description: Authentication Attribute
        type: str
        required: false
    displaynameattribute:
        description: Display Name Attribute
        type: str
        required: false
    emailaddressattribute:
        description: Email Address Attribute
        type: str
        required: false
    expirydateattribute:
        description: date
        type: str
        required: false
    bindDN:
        description: Username
        type: str
        required: false
    ldap_password:
        description: Password
        type: str
        required: false
    validateservercertificate:
        description: Password
        type: str
        choices: [Enable, Disable]
        required: false
    clientcertificate:
        description: Password
        type: str
        choices: [None, ApplianceCertificate, Webadmin]
        required: false
    state:
        description:
            - Use C(query) to retrieve, C(updated) to create, C(absent) to remove, or C(updated) to modify
        choices: [absent, updated, query]
        type: str
        required: true

author:
    - Matt Mullen (@mamullen13316)
    - Philip Finucane (@philfinucane)
'''

EXAMPLES = r'''
- name: Update Azure AD SSO
  sophos.sophos_firewall.sfos_authentication_ldap:
    username: "{{ username }}"
    password: "{{ password }}"
    hostname: "{{ inventory_hostname }}"
    port: 4444
    verify: false
    servername: Test
    serveraddress: '192.168.0.1'
    port_ldap: '636'
    anonymouslogin: Disable
    connectionsecurity: SSL
    bindDN: admin
    ldap_password: sophosfirewall
    appendbaseDN: Enable
    baseDN: DC=sophos,DC=com
    authenticationattribute: johndoe
    displaynameattribute: John Doe
    groupnameattribute: 1001
    expirydateattribute: date
    validateservercertificate: Enable
    clientCertificate: ApplianceCertificate
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


def get_ldap_settings(fw_obj, module, result):
    """Get current settings from Sophos Firewall

    Args:
        fw_obj (SophosFirewall): SophosFirewall object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: Results of lookup
    """
    try:
        resp = fw_obj.get_tag("AuthenticationServer")['Response']['AuthenticationServer']["LDAPServer"]
            
    except SophosFirewallZeroRecords as error:
        return {"exists": False, "api_response": str(error)}
    except SophosFirewallAuthFailure as error:
        module.fail_json(msg="Authentication error: {0}".format(error), **result)
    except SophosFirewallAPIError as error:
        module.fail_json(msg="API Error: {0}".format(error), **result)
    except RequestException as error:
        module.fail_json(msg="Error communicating to API: {0}".format(error), **result)

    return {"exists": True, "api_response": resp}

def create_ldap(fw_obj, module, result):
    """Create an LDAP Server on Sophos Firewall when none exists

    Args:
        fw_obj (SophosFirewall): SophosFirewall object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: API response
    """
    payload = """
        <AuthenticationServer>
          <LDAPServer>
		  <ServerName>{{ name }}</ServerName>
		  <ServerAddress>{{ ipaddress }}</ServerAddress>
		  <Port>{{ port_ldap }}</Port>
		  <Version>{{ version }}</Version>
          <AnonymousLogin>{{ anonymouslogin }}</AnonymousLogin>
          <ConnectionSecurity>{{ connectionsecurity }}</ConnectionSecurity>
		  <BaseDN>{{ baseDN }}</BaseDN>
          <AuthenticationAttribute>{{ authenticationattribute }}</AuthenticationAttribute>
          <DisplayNameAttribute>{{ displaynameattribute }}</DisplayNameAttribute>
          <EmailAddressAttribute>{{ emailaddressattribute }}</EmailAddressAttribute>
          <GroupNameAttribute>{{ groupnameattribute }}</GroupNameAttribute>
          <ExpiryDateAttribute>{{ expirydateattribute }}</ExpiryDateAttribute>
          <ValidateServerCertificate>{{ validateservercertificate }}</ValidateServerCertificate>
          <ClientCertificate>{{ clientcertificate }}</ClientCertificate>
	      </LDAPServer>
        </AuthenticationServer>
    
    """
    
    payload2 = """
        <AuthenticationServer>
          <LDAPServer>
		  <ServerName>{{ name }}</ServerName>
		  <ServerAddress>{{ ipaddress }}</ServerAddress>
		  <Port>{{ port_ldap }}</Port>
		  <Version>{{ version }}</Version>
          <AnonymousLogin>{{ anonymouslogin }}</AnonymousLogin>
          <ConnectionSecurity>{{ connectionsecurity }}</ConnectionSecurity>
		  <BaseDN>{{ baseDN }}</BaseDN>
          <AuthenticationAttribute>{{ authenticationattribute }}</AuthenticationAttribute>
          <DisplayNameAttribute>{{ displaynameattribute }}</DisplayNameAttribute>
          <EmailAddressAttribute>{{ emailaddressattribute }}</EmailAddressAttribute>
          <GroupNameAttribute>{{ groupnameattribute }}</GroupNameAttribute>
          <ExpiryDateAttribute>{{ expirydateattribute }}</ExpiryDateAttribute>
          <Administrator>{{ bindDN }}</Administrator>
          <Password>{{ ldap_password }}</Password>
          <AppendBaseDN>{{ appendbaseDN }}</AppendBaseDN>
          <ValidateServerCertificate>{{ validateservercertificate }}</ValidateServerCertificate>
          <ClientCertificate>{{ clientcertificate }}</ClientCertificate>
	      </LDAPServer>
        </AuthenticationServer>
    
    """
    template_vars = {
        "name": module.params.get("servername"),
        "ipaddress": module.params.get("serveraddress"),
        "port_ldap": module.params.get("port_ldap"),
        "version": module.params.get("version"),
        "anonymouslogin": module.params.get("anonymouslogin"),
        "connectionsecurity": module.params.get("connectionsecurity"),
        "baseDN": module.params.get("baseDN"),
        "authenticationattribute": module.params.get("authenticationattribute"),
        "displaynameattribute": module.params.get("displaynameattribute", {}),
        "emailaddressattribute": module.params.get("emailaddressattribute"),
        "accountingport": module.params.get("accountingport"),
        "groupnameattribute": module.params.get("groupnameattribute"),
        "expirydateattribute": module.params.get("expirydateattribute"),
        "validateservercertificate": module.params.get("validateservercertificate"),
        "clientcertificate": module.params.get("clientcertificate"),
        "appendbaseDN": module.params.get("appendbaseDN", {}),
        "ldap_password": module.params.get("ldap_password", {}),
        "bindDN": module.params.get("bindDN", {})
    }
   
    anonymous = module.params.get("anonymouslogin")
    if anonymous == "Enable":
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
        
    # module.fail_json(msg=f"{resp['Response']}, {output_buffer.getvalue()}")
        return resp
    else:
        if anonymous == "Disable":
            try:
                with contextlib.redirect_stdout(output_buffer):
                    resp = fw_obj.submit_xml(
                        template_data=payload2,
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
            

def update_ldap_add(fw_obj, module, result):
    """Add additional LDAP server on Sophos Firewall

    Args:
        fw_obj (SophosFirewall): SophosFirewall object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: API response
    """
    payload = """
        <AuthenticationServer>
          <LDAPServer>
		  <ServerName>{{ name }}</ServerName>
		  <ServerAddress>{{ ipaddress }}</ServerAddress>
		  <Port>{{ port_ldap }}</Port>
		  <Version>{{ version }}</Version>
          <AnonymousLogin>{{ anonymouslogin }}</AnonymousLogin>
          <ConnectionSecurity>{{ connectionsecurity }}</ConnectionSecurity>
		  <BaseDN>{{ baseDN }}</BaseDN>
          <AuthenticationAttribute>{{ authenticationattribute }}</AuthenticationAttribute>
          <DisplayNameAttribute>{{ displaynameattribute }}</DisplayNameAttribute>
          <EmailAddressAttribute>{{ emailaddressattribute }}</EmailAddressAttribute>
          <GroupNameAttribute>{{ groupnameattribute }}</GroupNameAttribute>
          <ExpiryDateAttribute>{{ expirydateattribute }}</ExpiryDateAttribute>
          <ValidateServerCertificate>{{ validateservercertificate }}</ValidateServerCertificate>
          <ClientCertificate>{{ clientcertificate }}</ClientCertificate>
	      </LDAPServer>
        </AuthenticationServer>
    
    """
    
    payload2 = """
        <AuthenticationServer>
          <LDAPServer>
		  <ServerName>{{ name }}</ServerName>
		  <ServerAddress>{{ ipaddress }}</ServerAddress>
		  <Port>{{ port_ldap }}</Port>
		  <Version>{{ version }}</Version>
          <AnonymousLogin>{{ anonymouslogin }}</AnonymousLogin>
          <ConnectionSecurity>{{ connectionsecurity }}</ConnectionSecurity>
		  <BaseDN>{{ baseDN }}</BaseDN>
          <AuthenticationAttribute>{{ authenticationattribute }}</AuthenticationAttribute>
          <DisplayNameAttribute>{{ displaynameattribute }}</DisplayNameAttribute>
          <EmailAddressAttribute>{{ emailaddressattribute }}</EmailAddressAttribute>
          <GroupNameAttribute>{{ groupnameattribute }}</GroupNameAttribute>
          <ExpiryDateAttribute>{{ expirydateattribute }}</ExpiryDateAttribute>
          <Administrator>{{ bindDN }}</Administrator>
          <Password>{{ ldap_password }}</Password>
          <AppendBaseDN>{{ appendbaseDN }}</AppendBaseDN>
          <ValidateServerCertificate>{{ validateservercertificate }}</ValidateServerCertificate>
          <ClientCertificate>{{ clientcertificate }}</ClientCertificate>
	      </LDAPServer>
        </AuthenticationServer>
    
    """
    
    
    template_vars = {
        "name": module.params.get("servername"),
        "ipaddress": module.params.get("serveraddress"),
        "port_ldap": module.params.get("port_ldap"),
        "version": module.params.get("version"),
        "anonymouslogin": module.params.get("anonymouslogin"),
        "connectionsecurity": module.params.get("connectionsecurity"),
        "baseDN": module.params.get("baseDN"),
        "authenticationattribute": module.params.get("authenticationattribute"),
        "displaynameattribute": module.params.get("displaynameattribute", {}),
        "emailaddressattribute": module.params.get("emailaddressattribute"),
        "accountingport": module.params.get("accountingport"),
        "groupnameattribute": module.params.get("groupnameattribute"),
        "expirydateattribute": module.params.get("expirydateattribute"),
        "validateservercertificate": module.params.get("validateservercertificate"),
        "clientcertificate": module.params.get("clientcertificate"),
        "appendbaseDN": module.params.get("appendbaseDN", {}),
        "ldap_password": module.params.get("ldap_password", {}),
        "bindDN": module.params.get("bindDN", {})
    }
    
    anonymous = module.params.get("anonymouslogin")
    if anonymous == "Enable":
  
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
        
        
        return resp
    else:
        if anonymous == "Disable":
            try:
                with contextlib.redirect_stdout(output_buffer):
                    resp = fw_obj.submit_xml(
                        template_data=payload2,
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

def update_ldap_update(fw_obj, module, result):
    """Update existing LDAP settings on Sophos Firewall

    Args:
        fw_obj (SophosFirewall): SophosFirewall object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: API response
    """
    payload = """
        <AuthenticationServer>
          <LDAPServer>
		  <ServerName>{{ name }}</ServerName>
		  <ServerAddress>{{ ipaddress }}</ServerAddress>
		  <Port>{{ port_ldap }}</Port>
		  <Version>{{ version }}</Version>
          <AnonymousLogin>{{ anonymouslogin }}</AnonymousLogin>
          <ConnectionSecurity>{{ connectionsecurity }}</ConnectionSecurity>
		  <BaseDN>{{ baseDN }}</BaseDN>
          <AuthenticationAttribute>{{ authenticationattribute }}</AuthenticationAttribute>
          <DisplayNameAttribute>{{ displaynameattribute }}</DisplayNameAttribute>
          <EmailAddressAttribute>{{ emailaddressattribute }}</EmailAddressAttribute>
          <GroupNameAttribute>{{ groupnameattribute }}</GroupNameAttribute>
          <ExpiryDateAttribute>{{ expirydateattribute }}</ExpiryDateAttribute>
          <ValidateServerCertificate>{{ validateservercertificate }}</ValidateServerCertificate>
          <ClientCertificate>{{ clientcertificate }}</ClientCertificate>
	      </LDAPServer>
        </AuthenticationServer>
    
    """
    
    payload2 = """
        <AuthenticationServer>
          <LDAPServer>
		  <ServerName>{{ name }}</ServerName>
		  <ServerAddress>{{ ipaddress }}</ServerAddress>
		  <Port>{{ port_ldap }}</Port>
		  <Version>{{ version }}</Version>
          <AnonymousLogin>{{ anonymouslogin }}</AnonymousLogin>
          <ConnectionSecurity>{{ connectionsecurity }}</ConnectionSecurity>
		  <BaseDN>{{ baseDN }}</BaseDN>
          <AuthenticationAttribute>{{ authenticationattribute }}</AuthenticationAttribute>
          <DisplayNameAttribute>{{ displaynameattribute }}</DisplayNameAttribute>
          <EmailAddressAttribute>{{ emailaddressattribute }}</EmailAddressAttribute>
          <GroupNameAttribute>{{ groupnameattribute }}</GroupNameAttribute>
          <ExpiryDateAttribute>{{ expirydateattribute }}</ExpiryDateAttribute>
          <Administrator>{{ bindDN }}</Administrator>
          <Password>{{ ldap_password }}</Password>
          <AppendBaseDN>{{ appendbaseDN }}</AppendBaseDN>
          <ValidateServerCertificate>{{ validateservercertificate }}</ValidateServerCertificate>
          <ClientCertificate>{{ clientcertificate }}</ClientCertificate>
	      </LDAPServer>
        </AuthenticationServer>
    
    """
    template_vars = {
        "name": module.params.get("servername"),
        "ipaddress": module.params.get("serveraddress"),
        "port_ldap": module.params.get("port_ldap"),
        "version": module.params.get("version"),
        "anonymouslogin": module.params.get("anonymouslogin"),
        "connectionsecurity": module.params.get("connectionsecurity"),
        "baseDN": module.params.get("baseDN"),
        "authenticationattribute": module.params.get("authenticationattribute"),
        "displaynameattribute": module.params.get("displaynameattribute", {}),
        "emailaddressattribute": module.params.get("emailaddressattribute"),
        "accountingport": module.params.get("accountingport"),
        "groupnameattribute": module.params.get("groupnameattribute"),
        "expirydateattribute": module.params.get("expirydateattribute"),
        "validateservercertificate": module.params.get("validateservercertificate"),
        "clientcertificate": module.params.get("clientcertificate"),
        "appendbaseDN": module.params.get("appendbaseDN", {}),
        "ldap_password": module.params.get("ldap_password", {}),
        "bindDN": module.params.get("bindDN", {})
    }
   
    
    anonymous = module.params.get("anonymouslogin")
    if anonymous == "Enable":
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
    else:
        if anonymous == "Disable":

            try:
                with contextlib.redirect_stdout(output_buffer):
                    resp = fw_obj.submit_xml(
                        template_data=payload2,
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
    serveraddress = module.params.get("serveraddress", {})
    port_ldap =  module.params.get("port_ldap", {})
    version = module.params.get("version", {})
    anonymouslogin = module.params.get("anonymouslogin", {})
    connectionsecurity = module.params.get("connectionsecurity", {})
    baseDN = module.params.get("baseDN", {})
    authenticationattribute = module.params.get("authenticationattribute", {})
    displaynameattribute = module.params.get("displaynameattribute", {})
    emailaddressattribute = module.params.get("emailaddressattribute", {})
    groupnameattribute = module.params.get("groupnameattribute", {})
    expirydateattribute = module.params.get("expirydateattribute", {})
    validateservercertificate = module.params.get("validateservercertificate", {})
    clientcertificate = module.params.get("clientcertificate", {})
    appendbaseDN = module.params.get("appendbaseDN", {})
    ldap_password = module.params.get("ldap_password", {})
    bindDN = module.params.get("bindDN", {})
    
    anonymous = module.params.get("anonymouslogin")
    
    if anonymous == "Enable":
    
        if servername and not servername == exist_settings["ServerName"]:
            return True
        if serveraddress and not serveraddress == exist_settings["ServerAddress"]:
            return True
        if port_ldap and not port_ldap == exist_settings["Port"]:
            return True
        if version and not version == exist_settings["Version"]:
            return True
        if anonymouslogin and not anonymouslogin == exist_settings["AnonymousLogin"]:
            return True
        if connectionsecurity and not connectionsecurity == exist_settings["ConnectionSecurity"]:
            return True
        if baseDN and not baseDN == exist_settings["BaseDN"]:
            return True
        if authenticationattribute and not authenticationattribute == exist_settings["AuthenticationAttribute"]:
                return True
        if displaynameattribute and not displaynameattribute == exist_settings["DisplayNameAttribute"]:
                return True
        if emailaddressattribute and not emailaddressattribute == exist_settings["EmailAddressAttribute"]:
                return True
        if groupnameattribute and not groupnameattribute == exist_settings["ExpiryDateAttribute"]:
            return True
        if expirydateattribute and not expirydateattribute == exist_settings["ExpiryDateAttribute"]:
            return True
        if validateservercertificate and not validateservercertificate == exist_settings["ValidateServerCertificate"]:
            return True
        if module.params.get("ldap_password"): 
            return True
                
        return False
    else:
        if anonymous == "Disable":
            if servername and not servername == exist_settings["ServerName"]:
                return True
            if serveraddress and not serveraddress == exist_settings["ServerAddress"]:
                return True
            if port_ldap and not port_ldap == exist_settings["Port"]:
                return True
            if version and not version == exist_settings["Version"]:
                return True
            if anonymouslogin and not anonymouslogin == exist_settings["AnonymousLogin"]:
                return True
            if connectionsecurity and not connectionsecurity == exist_settings["ConnectionSecurity"]:
                return True
            if baseDN and not baseDN == exist_settings["BaseDN"]:
                return True
            if authenticationattribute and not authenticationattribute == exist_settings["AuthenticationAttribute"]:
                    return True
            if displaynameattribute and not displaynameattribute == exist_settings["DisplayNameAttribute"]:
                    return True
            if emailaddressattribute and not emailaddressattribute == exist_settings["EmailAddressAttribute"]:
                    return True
            if groupnameattribute and not groupnameattribute == exist_settings["ExpiryDateAttribute"]:
                return True
            if expirydateattribute and not expirydateattribute == exist_settings["ExpiryDateAttribute"]:
                return True
            if validateservercertificate and not validateservercertificate == exist_settings["ValidateServerCertificate"]:
                return True
            if clientcertificate and not clientcertificate == exist_settings["ClientCertificate"]:
                return True
            if appendbaseDN and not appendbaseDN == exist_settings["AppendBaseDN"]:
                return True
            if bindDN and not bindDN == exist_settings["Administrator"]:
                return True

            if module.params.get("ldap_password"): 
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
    serveraddress = module.params.get("serveraddress", {})
    port_ldap =  module.params.get("port_ldap", {})
    version = module.params.get("version", {})
    anonymouslogin = module.params.get("anonymouslogin", {})
    connectionsecurity = module.params.get("connectionsecurity", {})
    baseDN = module.params.get("baseDN", {})
    authenticationattribute = module.params.get("authenticationattribute", {})
    displaynameattribute = module.params.get("displaynameattribute", {})
    emailaddressattribute = module.params.get("emailaddressattribute", {})
    groupnameattribute = module.params.get("groupnameattribute", {})
    expirydateattribute = module.params.get("expirydateattribute", {})
    validateservercertificate = module.params.get("validateservercertificate", {})
    clientcertificate = module.params.get("clientcertificate", {})
    appendbaseDN = module.params.get("appendbaseDN", {})
    ldap_password = module.params.get("ldap_password", {})
    bindDN = module.params.get("bindDN", {})
    
    anonymous = module.params.get("anonymouslogin")
    list_len = len(exist_settings)
    
    if anonymous == "Enable":
        for i in range(list_len):
        
            if (exist_settings[i]["ServerName"]) == servername:
                
                if serveraddress and not serveraddress == exist_settings[i]["ServerAddress"]:
                    return True
                if port_ldap and not port_ldap == exist_settings[i]["Port"]:
                    return True
                if version and not version == exist_settings[i]["Version"]:
                    return True
                if anonymouslogin and not anonymouslogin == exist_settings[i]["AnonymousLogin"]:
                    return True
                if connectionsecurity and not connectionsecurity == exist_settings[i]["ConnectionSecurity"]:
                    return True
                if baseDN and not baseDN == exist_settings[i]["BaseDN"]:
                    return True
                if authenticationattribute and not authenticationattribute == exist_settings[i]["AuthenticationAttribute"]:
                        return True
                if displaynameattribute and not displaynameattribute == exist_settings[i]["DisplayNameAttribute"]:
                        return True
                if emailaddressattribute and not emailaddressattribute == exist_settings[i]["EmailAddressAttribute"]:
                        return True
                if groupnameattribute and not groupnameattribute == exist_settings[i]["ExpiryDateAttribute"]:
                    return True
                if expirydateattribute and not expirydateattribute == exist_settings[i]["ExpiryDateAttribute"]:
                    return True
                if validateservercertificate and not validateservercertificate == exist_settings[i]["ValidateServerCertificate"]:
                    return True
                if module.params.get("ldap_password"): 
                    return True
    if anonymous == "Disable":
        
        for i in range(list_len):
        
            if (exist_settings[i]["ServerName"]) == servername:
                
                
                if serveraddress and not serveraddress == exist_settings[i]["ServerAddress"]:
                    return True
                if port_ldap and not port_ldap == exist_settings[i]["Port"]:
                    return True
                if version and not version == exist_settings[i]["Version"]:
                    return True
                if anonymouslogin and not anonymouslogin == exist_settings[i]["AnonymousLogin"]:
                    return True
                if connectionsecurity and not connectionsecurity == exist_settings[i]["ConnectionSecurity"]:
                    return True
                if baseDN and not baseDN == exist_settings[i]["BaseDN"]:
                    return True
                if authenticationattribute and not authenticationattribute == exist_settings[i]["AuthenticationAttribute"]:
                        return True
                if displaynameattribute and not displaynameattribute == exist_settings[i]["DisplayNameAttribute"]:
                        return True
                if emailaddressattribute and not emailaddressattribute == exist_settings[i]["EmailAddressAttribute"]:
                        return True
                if groupnameattribute and not groupnameattribute == exist_settings[i]["ExpiryDateAttribute"]:
                    return True
                if expirydateattribute and not expirydateattribute == exist_settings[i]["ExpiryDateAttribute"]:
                    return True
                if validateservercertificate and not validateservercertificate == exist_settings[i]["ValidateServerCertificate"]:
                    return True
                if clientcertificate and not clientcertificate == exist_settings[i]["ClientCertificate"]:
                    return True
                if appendbaseDN and not appendbaseDN == exist_settings[i]["AppendBaseDN"]:
                    return True
                if bindDN and not bindDN == exist_settings[i]["Administrator"]:
                    return True

                if module.params.get("ldap_password"): 
                    return True
    
    return False


def remove_ldap(fw_obj, module, result):
    """Remove a LDAP Server on a Sophos Firewall

    Args:
        fw_obj (SophosFirewall): SophosFirewall object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: API response
    """
    payload = """
            <Remove>
            <AuthenticationServer>
            <LDAPServer>
		    <ServerName>{{ name }}</ServerName>
            </LDAPServer>
            </AuthenticationServer>
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
        "serveraddress": {"type": "str", "required": False},
        "port_ldap": {"type": "str", "required": False},
        "version": {"type": "str", "choices": ["2", "3"], "required": False},
        "anonymouslogin": {"type": "str", "choices": ["Enable", "Disable"], "required": False},
        "connectionsecurity": {"type": "str", "choices": ["Simple", "SSL", "TLS"], "required": False},
        "bindDN": {"type": "str", "required": False},
        "ldap_password": {"type": "str", "required": False},
        "groupnameattribute": {"type": "str", "required": False},
        "baseDN": {"type": "str", "required": False},
        "appendbaseDN": {"type": "str", "choices": ["Enable", "Disable"], "required": False},
        "expirydateattribute": {"type": "str", "required": False},
        "authenticationattribute": {"type": "str", "required": False},
        "displaynameattribute": {"type": "str", "required": False},
        "emailaddressattribute": {"type": "str", "required": False},
        "validateservercertificate": {"type": "str", "choices": ["Enable", "Disable"]},
        "clientcertificate": {"type": "str", "choices": ["None", "ApplianceCertificate", "Webadmin"]},
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

    exist_settings = get_ldap_settings(fw, module, result)
    result["api_response"] = exist_settings["api_response"]
    
    
    if state == "absent":
                
                api_response = remove_ldap(fw, module, result)
                
                if api_response:
                    if api_response['Response']["AuthenticationServer"]["LDAPServer"]["Status"]["#text"] == "Configuration applied successfully.":
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
            
                
                api_response = create_ldap(fw, module, result)
                
                if api_response:
                    
                    if api_response['Response']["LDAPServer"]["Status"]["#text"] == "Configuration applied successfully.":
                        result["changed"] = True
                    result["api_response"] = api_response
                else:
                    result["changed"] = False
    
        
        elif state == "updated" and "ServerName" in result["api_response"]:
            
            if eval_servername(module, exist_settings):
                if eval_changed(module, exist_settings):
                    
                    api_response = update_ldap_add(fw, module, result)
                   
            
                    if api_response:
                        if (api_response["Response"]["LDAPServer"]["Status"]["#text"]
                        
                                == "Configuration applied successfully."):
                            result["changed"] = True
                        result["api_response"] = api_response
                    else:
                        result["changed"] = False
                        
            if not eval_servername(module, exist_settings):
                if eval_changed(module, exist_settings):
                    
                    api_response = update_ldap_update(fw, module, result)
                    
            
                    if api_response:
                        if (api_response["Response"]["LDAPServer"]["Status"]["#text"]
                        
                                == "Configuration applied successfully."):
                            result["changed"] = True
                        result["api_response"] = api_response
                    else:
                        result["changed"] = False
                        
    if isinstance(result["api_response"], list):
        
        if eval_list_new_servername(module, exist_settings):
                    
                    api_response = update_ldap_add(fw, module, result)
                    
            
                    if api_response:
                        if (api_response["Response"]["LDAPServer"]["Status"]["#text"]
                        
                                == "Configuration applied successfully."):
                            result["changed"] = True
                        result["api_response"] = api_response
                    else:
                        result["changed"] = False
        else:
    
            if eval_list_update_server(module, exist_settings):
                
                api_response = update_ldap_update(fw, module, result)
                    
                if api_response:
                    if (api_response["Response"]["LDAPServer"]["Status"]["#text"] == "Configuration applied successfully."):
                        result["changed"] = True
                    result["api_response"] = api_response
                else:
                    result["changed"] = False
    
    
                    

    module.exit_json(**result)
  

if __name__ == "__main__":
    main()