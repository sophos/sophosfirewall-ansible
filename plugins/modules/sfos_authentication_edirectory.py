#!/usr/bin/python

# Copyright 2024 Sophos Ltd.  All rights reserved.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
import sys

__metaclass__ = type

DOCUMENTATION = r"""
---
module: sfos_authentication_edirectory.py

short_description: Manage Authentication settings eDirectory

version_added: "1.3.0"

description: Manage authentication servers (Configure > Authentication > Servers> Add) on Sophos Firewall

extends_documentation_fragment:
  - sophos.sophos_firewall.fragments.base

options:
    servername:
        description: Name of Server
        type: str
        required: false
    serveripdomain:
        description: Server IP Address
        type: str
        required: false
    port_edir:
        description: Port
        type: str
        required: false
    binddn:
        description: Bind Username CN=user1,CN=Users,DC=example,DC=com
        type: str
        required: false
    dn_password:
        description: password for bind
        type: str
        required: false
    connectionsecurity:
        description: Encryption
        type: str
        choices: [Simple, SSL, TLS]
    validateservercertificate:
        description: Validate Server Certificate
        type: str
        choices: [Enable, Disable]
        required: false
    clientcertificate:
        description: Client Certificate type
        type: str
        choices: [Webadmin, ApplianceCertificate, None]
        required: false
    basedn:
        description: BaseDN
        type: str
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
"""

EXAMPLES = r"""
- name: Update eDirectory 
  sophos.sophos_firewall.sfos_authentication_edirectory:
    username: "{{ username }}"
    password: "{{ password }}"
    hostname: "{{ inventory_hostname }}"
    port: 4444
    verify: false
    servername: Test
    serveripdomain: '192.168.0.1'
    port_edir: '1812'
    binddn: CN=user1,CN=Users,DC=example,DC=com
    dn_password: testtest
    connectionsecurity: TLS
    validateservercertificate: Enable
    clientcertificate: Webadmin
    basedn: o=sophos.com
    state: updated
    delegate_to: localhost

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


def get_edirectory_settings(fw_obj, module, result):
    """Get current settings from Sophos Firewall

    Args:
        fw_obj (SophosFirewall): SophosFirewall object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: Results of lookup
    """
    try:
        resp = fw_obj.get_tag("AuthenticationServer")['Response']['AuthenticationServer']["EDirectory"]
            
    except SophosFirewallZeroRecords as error:
        return {"exists": False, "api_response": str(error)}
    except SophosFirewallAuthFailure as error:
        module.fail_json(msg="Authentication error: {0}".format(error), **result)
    except SophosFirewallAPIError as error:
        module.fail_json(msg="API Error: {0}".format(error), **result)
    except RequestException as error:
        module.fail_json(msg="Error communicating to API: {0}".format(error), **result)

    return {"exists": True, "api_response": resp}

def create_edirectory(fw_obj, module, result):
    """Create an eDirectory Server on Sophos Firewall when none exists

    Args:
        fw_obj (SophosFirewall): SophosFirewall object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: API response
    """
    payload = """
        <AuthenticationServer>
          <EDirectory>
		  <ServerName>{{ name }}</ServerName>
		  <ServerIpDomain>{{ serveripdomain }}</ServerIpDomain>
		  <Port>{{ port_edir }}</Port>
		  <Username>{{ binddn }}</Username>
          <Password>{{ dn_password }}</Password>
          <ConnectionSecurity>{{ connectionsecurity }}</ConnectionSecurity>
		  <BaseDN>{{ basedn }}</BaseDN>
          <ValidateServerCertificate>{{ validateservercertificate }}</ValidateServerCertificate>
          <ClientCertificate>{{ clientcertificate }}</ClientCertificate>
	      </EDirectory>
        </AuthenticationServer>
    
    """
    template_vars = {
        "name": module.params.get("servername"),
        "serveripdomain": module.params.get("serveripdomain"),
        "port_edir": module.params.get("port_edir"),
        "binddn": module.params.get("binddn"),
        "connectionsecurity": module.params.get("connectionsecurity"),
        "basedn": module.params.get("basedn"),
        "validateservercertificate": module.params.get("validateservercertificate"),
        "clientcertificate": module.params.get("clientcertificate"),
        "dn_password": module.params.get("dn_password")
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

def update_edirectory_add(fw_obj, module, result):
    """Add additional eDirectory server on Sophos Firewall

    Args:
        fw_obj (SophosFirewall): SophosFirewall object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: API response
    """
    payload = """
        <AuthenticationServer>
          <EDirectory>
		  <ServerName>{{ name }}</ServerName>
		  <ServerIpDomain>{{ serveripdomain }}</ServerIpDomain>
		  <Port>{{ port_edir }}</Port>
		  <Username>{{ binddn }}</Username>
          <Password>{{ dn_password }}</Password>
          <ConnectionSecurity>{{ connectionsecurity }}</ConnectionSecurity>
		  <BaseDN>{{ basedn }}</BaseDN>
          <ValidateServerCertificate>{{ validateservercertificate }}</ValidateServerCertificate>
          <ClientCertificate>{{ clientcertificate }}</ClientCertificate>
	      </EDirectory>
        </AuthenticationServer>
    
    """
    template_vars = {
        "name": module.params.get("servername"),
        "serveripdomain": module.params.get("serveripdomain"),
        "port_edir": module.params.get("port_edir"),
        "binddn": module.params.get("binddn"),
        "connectionsecurity": module.params.get("connectionsecurity"),
        "basedn": module.params.get("basedn"),
        "validateservercertificate": module.params.get("validateservercertificate"),
        "clientcertificate": module.params.get("clientcertificate"),
        "dn_password": module.params.get("dn_password")
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
    
    
    return resp

def update_edirectory_update(fw_obj, module, result):
    """Update existing eDirectory settings on Sophos Firewall

    Args:
        fw_obj (SophosFirewall): SophosFirewall object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: API response
    """
    payload = """
        <AuthenticationServer>
          <EDirectory>
		  <ServerName>{{ name }}</ServerName>
		  <ServerIpDomain>{{ serveripdomain }}</ServerIpDomain>
		  <Port>{{ port_edir }}</Port>
		  <Username>{{ binddn }}</Username>
          <Password>{{ dn_password }}</Password>
          <ConnectionSecurity>{{ connectionsecurity }}</ConnectionSecurity>
		  <BaseDN>{{ basedn }}</BaseDN>
          <ValidateServerCertificate>{{ validateservercertificate }}</ValidateServerCertificate>
          <ClientCertificate>{{ clientcertificate }}</ClientCertificate>
	      </EDirectory>
        </AuthenticationServer>
    
    """
    template_vars = {
        "name": module.params.get("servername"),
        "serveripdomain": module.params.get("serveripdomain"),
        "port_edir": module.params.get("port_edir"),
        "binddn": module.params.get("binddn"),
        "connectionsecurity": module.params.get("connectionsecurity"),
        "basedn": module.params.get("basedn"),
        "validateservercertificate": module.params.get("validateservercertificate"),
        "clientcertificate": module.params.get("clientcertificate"),
        "dn_password": module.params.get("dn_password")
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
    serveripdomain = module.params.get("serveraddress", {})
    port_edir = module.params.get("port_edir", {})
    binddn = module.params.get("binddn", {})
    dn_password = module.params.get("dn_password", {})
    connectionsecurity = module.params.get("connectionsecurity", {})
    basedn = module.params.get("basedn", {})
    validateservercertificate = module.params.get("validateservercertificate", {})
    clientcertificate = module.params.get("clientcertificate", {})
    
    
    if servername and not servername == exist_settings["ServerName"]:
        return True
    if serveripdomain and not serveripdomain == exist_settings["ServerIpDomain"]:
        return True
    if port_edir and not port_edir == exist_settings["Port"]:
        return True
    if binddn and not binddn == exist_settings["Username"]:
        return True
    if connectionsecurity and not connectionsecurity == exist_settings["ConnectionSecurity"]:
        return True
    if basedn and not basedn == exist_settings["BaseDN"]:
        return True
    if validateservercertificate and not validateservercertificate == exist_settings["ValidateServerCertificate"]:
            return True
    if clientcertificate and not clientcertificate == exist_settings["ClientCertificate"]:
            return True
    if module.params.get("dn_password"): 
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
    serveripdomain = module.params.get("serveraddress", {})
    port_edir = module.params.get("port_edir", {})
    binddn = module.params.get("binddn", {})
    dn_password = module.params.get("dn_password", {})
    connectionsecurity = module.params.get("connectionsecurity", {})
    basedn = module.params.get("basedn", {})
    validateservercertificate = module.params.get("validateservercertificate", {})
    clientcertificate = module.params.get("clientcertificate", {})
    
    list_len = len(exist_settings)
    for i in range(list_len):
       
        if (exist_settings[i]["ServerName"]) == servername:
            
            if serveripdomain and not serveripdomain == exist_settings[i]["ServerIpDomain"]:
                return True, i
            if port_edir and not port_edir == exist_settings[i]["Port"]:
                return True, i
            if binddn and not binddn == exist_settings[i]["Username"]:
                return True, i
            if dn_password and not dn_password == exist_settings[i]["Password"]:
                return True, i
            if connectionsecurity and not connectionsecurity == exist_settings[i]["ConnectionSecurity"]:
                return True, i
            if basedn and not basedn == exist_settings[i]["BaseDN"]:
                return True, i
            if validateservercertificate and not validateservercertificate == exist_settings[i]["ValidateServerCertificate"]:
                    return True, i
            if clientcertificate and not clientcertificate == exist_settings[i]["ClientCertificate"]:
                    return True, i
            if module.params.get("dn_password"): 
                return True, i
            
    return False


def remove_edirectory(fw_obj, module, result):
    """Remove a eDirectory Server on a Sophos Firewall

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
            <EDirectory>
		    <ServerName>{{ name }}</ServerName>
            </EDirectory>
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
        "serveripdomain": {"type": "str", "required": False},
        "port_edir": {"type": "str", "required": False},
        "binddn": {"type": "str", "required": False},
        "dn_password": {"type": "str", "required": False},
        "validateservercertificate": {"type": "str", "required": False, "choices": ["Enable", "Disable"]},
        "clientcertificate": {"type": "str", "required": False, "choices": ["Webadmin", "ApplianceCertificate", "None"]},
        "connectionsecurity": {"type": "str", "choices": ["Simple", "SSL", "TLS"]},
        "basedn": {"type": "str", "required": False},
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

    exist_settings = get_edirectory_settings(fw, module, result)
    result["api_response"] = exist_settings["api_response"]
    
    
    if state == "absent":
                
                api_response = remove_edirectory(fw, module, result)
                
                if api_response:
                    if api_response['Response']["AuthenticationServer"]["EDirectory"]["Status"]["#text"] == "Configuration applied successfully.":
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
            
                
                api_response = create_edirectory(fw, module, result)
                
                if api_response:
                    if api_response['Response']["EDirectory"]["Status"]["#text"] == "Configuration applied successfully.":
                        result["changed"] = True
                    result["api_response"] = api_response
                else:
                    result["changed"] = False
    
        
        elif state == "updated" and "ServerName" in result["api_response"]:
            
            if eval_servername(module, exist_settings):
                if eval_changed(module, exist_settings):
                    
                    api_response = update_edirectory_add(fw, module, result)
                    
            
                    if api_response:
                        if (api_response["Response"]["EDirectory"]["Status"]["#text"]
                        
                                == "Configuration applied successfully."):
                            result["changed"] = True
                        result["api_response"] = api_response
                    else:
                        result["changed"] = False
                        
            if not eval_servername(module, exist_settings):
                if eval_changed(module, exist_settings):
                    # module.exit_json(msg=f"eval=true")
                    api_response = update_edirectory_update(fw, module, result)
                    
            
                    if api_response:
                        if (api_response["Response"]["EDirectory"]["Status"]["#text"]
                        
                                == "Configuration applied successfully."):
                            result["changed"] = True
                        result["api_response"] = api_response
                    else:
                        result["changed"] = False
                        
    if isinstance(result["api_response"], list):
        
        if eval_list_new_servername(module, exist_settings):
                    
                    api_response = update_edirectory_add(fw, module, result)
                    
            
                    if api_response:
                        if (api_response["Response"]["EDirectory"]["Status"]["#text"]
                        
                                == "Configuration applied successfully."):
                            result["changed"] = True
                        result["api_response"] = api_response
                    else:
                        result["changed"] = False
        else:
    
            if eval_list_update_server(module, exist_settings):
                
                api_response = update_edirectory_update(fw, module, result)
                    
                if api_response:
                    if (api_response["Response"]["EDirectory"]["Status"]["#text"] == "Configuration applied successfully."):
                        result["changed"] = True
                    result["api_response"] = api_response
                else:
                    result["changed"] = False
    
    
                    

    module.exit_json(**result)
  

if __name__ == "__main__":
    main()