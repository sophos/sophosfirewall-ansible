#!/usr/bin/python

# Copyright 2024 Sophos Ltd.  All rights reserved.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
import sys

__metaclass__ = type

DOCUMENTATION = r'''
---
module: sfos_authentication_radius.py

short_description: Manage Authentication settings Radius

version_added: "1.3.0"

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
        description: Directory tenant ID
        type: str
        required: false
    SharedSecret:
        description: Client secret
        type: str
        required: false
    GroupNameAttribute:
        description: Redirect URI
        type: str
        required: false
    Timeout:
        description: Display name use "upn"
        type: str
        required: false
    DomainName:
        description: e-mail address use "email"
        type: str
        required: false
    EnableAccounting:
        description: enable accounting
        type: str
        choices: [Enable, None]
        required: false
    Attributes:
        description: User type selection
        type: str
        choices: [user, administrator]
        required: false
        suboptions:
            NAS-Identifier:
                type: str
                required: false
            NAS-Port-Type:
                type: str
                required: false
    AccountingPort:
        description: port number"
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
'''

EXAMPLES = r'''
- name: Update Azure AD SSO
  sophos.sophos_firewall.sfos_authentication_radius:
    servername: Test
    serveraddress: '192.168.0.1'
    port_radius: '1812'
    sharedsecret: sophosfirewall
    groupnameattribute: upn
    timeout: 3
    domainname: sophos.com
    enableaccounting: Enable
    attributes:
        nas_identifier: test
        nas_port_type: 0
    accountingport: 4444
    state: updated

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
from ansible.module_utils.connection import Connection


def get_radius_settings(connection, module, result):
    """Get current settings from Sophos Firewall

    Args:
        connection (Connection): Ansible Connection object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: Results of lookup
    """
    try:
        resp = connection.invoke_sdk("get_tag", module_args={"xml_tag": "AuthenticationServer"})
            
    except Exception as error:
        module.fail_json("An unexpected error occurred: {0}".format(error), **result)

    if resp["success"] and not resp["exists"]:
        return {"exists": False, "api_response": resp["response"]}

    if not resp["success"]:
        module.fail_json(msg="An error occurred: {0}".format(resp["response"]))

    return {"exists": True, "api_response": resp["response"]['Response']['AuthenticationServer']["RADIUSServer"]}

def create_radius(connection, module, result):
    """Create an Radius Server on Sophos Firewall when none exists

    Args:
        connection (Connection): Ansible Connection object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: API response
    """
    payload = """
        <AuthenticationServer>
          <RADIUSServer>
		  <ServerName>{{ name }}</ServerName>
		  <ServerAddress>{{ ipaddress }}</ServerAddress>
		  <Port>{{ port_radius }}</Port>
		  <SharedSecret>{{ sharedsecret }}</SharedSecret>
          <GroupNameAttribute>{{ groupnameattribute }}</GroupNameAttribute>
          <Timeout>{{ timeout }}</Timeout>
		  <DomainName>{{ domainname }}</DomainName>
          <EnableAccounting>{{ enableaccounting }}</EnableAccounting>
		  <Attributes>
            <NAS-Identifier>{{ nas_identifier }}</NAS-Identifier>
            <NAS-Port-Type>{{ nas_port_type }}</NAS-Port-Type>
          </Attributes>
          <AccountingPort>{{ accountingport }}</AccountingPort>
	      </RADIUSServer>
        </AuthenticationServer>
    
    """
    template_vars = {
        "name": module.params.get("servername"),
        "ipaddress": module.params.get("serveraddress"),
        "port_radius": module.params.get("port_radius"),
        "groupnameattribute": module.params.get("groupnameattribute"),
        "timeout": module.params.get("timeout"),
        "enableaccounting": module.params.get("enableaccounting"),
        "nas_identifier": module.params.get("attributes", {}).get("nas_identifier"),
        "nas_port_type": module.params.get("attributes", {}).get("nas_port_type"),
        "port_radius": module.params.get("port_radius"),
        "accountingport": module.params.get("accountingport"),
        "sharedsecret": module.params.get("sharedsecret")
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

def update_radius_add(connection, module, result):
    """Add additional radius server on Sophos Firewall

    Args:
        connection (Connection): Ansible Connection object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: API response
    """
    payload = """
        <AuthenticationServer>
          <RADIUSServer>
		  <ServerName>{{ name }}</ServerName>
		  <ServerAddress>{{ ipaddress }}</ServerAddress>
		  <Port>{{ port_radius }}</Port>
		  <SharedSecret>{{ sharedsecret }}</SharedSecret>
          <GroupNameAttribute>{{ groupnameattribute }}</GroupNameAttribute>
          <Timeout>{{ timeout }}</Timeout>
		  <DomainName>{{ domainname }}</DomainName>
          <EnableAccounting>{{ enableaccounting }}</EnableAccounting>
		  <Attributes>
            <NAS-Identifier>{{ nas_identifier }}</NAS-Identifier>
            <NAS-Port-Type>{{ nas_port_type }}</NAS-Port-Type>
          </Attributes>
          <AccountingPort>{{ accountingport }}</AccountingPort>
	      </RADIUSServer>
        </AuthenticationServer>
    
    """
    template_vars = {
        "name": module.params.get("servername"),
        "ipaddress": module.params.get("serveraddress"),
        "port_radius": module.params.get("port_radius"),
        "groupnameattribute": module.params.get("groupnameattribute"),
        "timeout": module.params.get("timeout"),
        "domainname": module.params.get("domainname"),
        "enableaccounting": module.params.get("enableaccounting"),
        "nas_identifier": module.params.get("attributes", {}).get("nas_identifier"),
        "nas_port_type": module.params.get("attributes", {}).get("nas_port_type"),
        "port_radius": module.params.get("port_radius"),
        "accountingport": module.params.get("accountingport"),
        "sharedsecret": module.params.get("sharedsecret")
    }
  
    try:
        with contextlib.redirect_stdout(output_buffer):
            resp = connection.invoke_sdk("submit_xml", module_args={
                "template_data": payload,
                "template_vars": template_vars,
                "set_operation": "add",
                "debug": True
                }
            )
    except Exception as error:
        module.fail_json("An unexpected error occurred: {0}".format(error), **result)

    if not resp["success"]:
        module.fail_json(msg="An error occurred: {0}".format(resp["response"]))

    return resp["response"]

def update_radius_update(connection, module, result):
    """Update existing radius settings on Sophos Firewall

    Args:
        connection (Connection): Ansible Connection object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: API response
    """
    payload = """
        <AuthenticationServer>
          <RADIUSServer>
		  <ServerName>{{ name }}</ServerName>
		  <ServerAddress>{{ ipaddress }}</ServerAddress>
		  <Port>{{ port_radius }}</Port>
		  <SharedSecret>{{ sharedsecret }}</SharedSecret>
          <GroupNameAttribute>{{ groupnameattribute }}</GroupNameAttribute>
          <Timeout>{{ timeout }}</Timeout>
		  <DomainName>{{ domainname }}</DomainName>
          <EnableAccounting>{{ enableaccounting }}</EnableAccounting>
		  <Attributes>
            <NAS-Identifier>{{ nas_identifier }}</NAS-Identifier>
            <NAS-Port-Type>{{ nas_port_type }}</NAS-Port-Type>
          </Attributes>
          <AccountingPort>{{ accountingport }}</AccountingPort>
	      </RADIUSServer>
        </AuthenticationServer>
    
    """
    template_vars = {
        "name": module.params.get("servername"),
        "ipaddress": module.params.get("serveraddress"),
        "port_radius": module.params.get("port_radius"),
        "groupnameattribute": module.params.get("groupnameattribute"),
        "timeout": module.params.get("timeout"),
        "domainname": module.params.get("domainname"),
        "enableaccounting": module.params.get("enableaccounting"),
        "nas_identifier": module.params.get("attributes", {}).get("nas_identifier"),
        "nas_port_type": module.params.get("attributes", {}).get("nas_port_type"),
        "port_radius": module.params.get("port_radius"),
        "accountingport": module.params.get("accountingport"),
        "sharedsecret": module.params.get("sharedsecret")
    }
   
    try:
        with contextlib.redirect_stdout(output_buffer):
            resp = connection.invoke_sdk("submit_xml", module_args={
                "template_data": payload,
                "template_vars": template_vars,
                "set_operation": "update",
                "debug": True
                }
            )
    except Exception as error:
        module.fail_json("An unexpected error occurred: {0}".format(error), **result)

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
    exist_settings = exist_settings["api_response"]
    servername = module.params.get("servername", {})
    serveraddress = module.params.get("serveraddress", {})
    port_radius = module.params.get("port_radius", {})
    sharedsecret = module.params.get("sharedsecret", {})
    groupnameattribute = module.params.get("groupnameattribute", {})
    timeout = module.params.get("timeout", {})
    domainname = module.params.get("domainname", {})
    enableaccounting = module.params.get("enableaccounting", {})
    nas_identifier = module.params.get("attributes", {}).get("nas_identifier")
    nas_port_type = module.params.get("attributes", {}).get("nas_port_type")
    accountingport = module.params.get("accountingport")
    
    
    if servername and not servername == exist_settings["ServerName"]:
        return True
    if serveraddress and not serveraddress == exist_settings["ServerAddress"]:
        return True
    if port_radius and not port_radius == exist_settings["Port"]:
        return True
    if groupnameattribute and not groupnameattribute == exist_settings["GroupNameAttribute"]:
        return True
    if timeout and not timeout == exist_settings["Timeout"]:
        return True
    if domainname and not domainname == exist_settings["DomainName"]:
        return True
    if enableaccounting and not enableaccounting == exist_settings["EnableAccounting"]:
        return True
    if nas_identifier and not nas_identifier == exist_settings["Attributes"]["NAS-Identifier"]:
            return True
    if nas_port_type and not nas_port_type == exist_settings["Attributes"]["NAS-Port-Type"]:
            return True
    if accountingport and not accountingport == exist_settings["AccountingPort"]:
            return True
    if module.params.get("sharedsecret"): 
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
    port_radius = module.params.get("port_radius", {})
    sharedsecret = module.params.get("sharedsecret", {})
    groupnameattribute = module.params.get("groupnameattribute", {})
    timeout = module.params.get("timeout", {})
    domainname = module.params.get("domainname", {})
    enableaccounting = module.params.get("enableaccounting", {})
    nas_identifier = module.params.get("attributes", {}).get("nas_identifier")
    nas_port_type = module.params.get("attributes", {}).get("nas_port_type")
    accountingport = module.params.get("accountingport")
    
    list_len = len(exist_settings)
    for i in range(list_len):
       
        if (exist_settings[i]["ServerName"]) == servername:
            
            if serveraddress and not serveraddress == exist_settings[i]["ServerAddress"]:
                return True, i
            if port_radius and not port_radius == exist_settings[i]["Port"]:
                return True, i
            if groupnameattribute and not groupnameattribute == exist_settings[i]["GroupNameAttribute"]:
                return True, i
            if timeout and not timeout == exist_settings[i]["Timeout"]:
                return True, i
            if domainname and not domainname == exist_settings[i]["DomainName"]:
                return True, i
            if enableaccounting and not enableaccounting == exist_settings[i]["EnableAccounting"]:
                return True, i
            if nas_identifier and not nas_identifier == exist_settings[i]["Attributes"]["NAS-Identifier"]:
                    return True, i
            if nas_port_type and not nas_port_type == exist_settings[i]["Attributes"]["NAS-Port-Type"]:
                    return True, i
            if accountingport and not accountingport == exist_settings[i]["AccountingPort"]:
                    return True, i
            if module.params.get("sharedsecret"): 
                return True, i
            
    return False


def remove_radius(connection, module, result):
    """Remove a Radius Server on a Sophos Firewall

    Args:
        connection (Connection): Ansible Connection object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: API response
    """
    payload = """
            <Remove>
            <AuthenticationServer>
            <RADIUSServer>
		    <ServerName>{{ name }}</ServerName>
            </RADIUSServer>
            </AuthenticationServer>
            </Remove>
    """
    template_vars = {
        "name": module.params.get("servername")
    }
    
    try:
        with contextlib.redirect_stdout(output_buffer):
            resp = connection.invoke_sdk("submit_xml", module_args={
                "template_data": payload,
                "template_vars": template_vars,
                "set_operation": None,
                "debug": True
                }
            )
    except Exception as error:
        module.fail_json("An unexpected error occurred: {0}".format(error), **result)

    if not resp["success"]:
        module.fail_json(msg="An error occurred: {0}".format(resp["response"]))

    return resp["response"]

def main():
    """Code executed at run time."""
    argument_spec = {
        "servername": {"type": "str", "required": False},
        "serveraddress": {"type": "str", "required": False},
        "port_radius": {"type": "str", "required": False},
        "sharedsecret": {"type": "str", "required": False},
        "groupnameattribute": {"type": "str", "required": False},
        "timeout": {"type": "str", "required": False},
        "domainname": {"type": "str", "required": False},
        "enableaccounting": {"type": "str", "choices": ["Enable", "None"]},
        "accountingport": {"type": "str", "required": False},
        "attributes": {"type": "dict", "required": False},
        "state": {"type": "str", "required": True, "choices": ["updated", "query", "absent"]}
    }

    
    module = AnsibleModule(argument_spec=argument_spec,
                           supports_check_mode=True
                           )

    if not PREREQ_MET["result"]:
        module.fail_json(msg=missing_required_lib(PREREQ_MET["missing_module"]))

    result = {
        "changed": False,
        "check_mode": False
    }

    state = module.params.get("state")

    try:
        connection = Connection(module._socket_path)
    except AssertionError as e:
        module.fail_json(msg="Connection error: Ensure you are targeting a remote host and not using 'delegate_to: localhost'.")

    if not hasattr(connection, "httpapi"):
        module.fail_json(msg="HTTPAPI plugin is not initialized. Ensure the connection is set to 'httpapi'.")

    exist_settings = get_radius_settings(connection, module, result)
    result["api_response"] = exist_settings["api_response"]
    
    
    if state == "absent":
               
                api_response = remove_radius(connection, module, result)
                
                if api_response:
                    if api_response['Response']["AuthenticationServer"]["RADIUSServer"]["Status"]["#text"] == "Configuration applied successfully.":
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
            
                
                api_response = create_radius(connection, module, result)
                
                if api_response:
                    if api_response['Response']["RADIUSServer"]["Status"]["#text"] == "Configuration applied successfully.":
                        result["changed"] = True
                    result["api_response"] = api_response
                else:
                    result["changed"] = False
    
        
        elif state == "updated" and "ServerName" in result["api_response"]:
            
            if eval_servername(module, exist_settings):
                if eval_changed(module, exist_settings):
                    
                    api_response = update_radius_add(connection, module, result)
                    
            
                    if api_response:
                        if (api_response["Response"]["RADIUSServer"]["Status"]["#text"]
                        
                                == "Configuration applied successfully."):
                            result["changed"] = True
                        result["api_response"] = api_response
                    else:
                        result["changed"] = False
                        
            if not eval_servername(module, exist_settings):
                if eval_changed(module, exist_settings):
                    
                    api_response = update_radius_update(connection, module, result)
                    
            
                    if api_response:
                        if (api_response["Response"]["RADIUSServer"]["Status"]["#text"]
                        
                                == "Configuration applied successfully."):
                            result["changed"] = True
                        result["api_response"] = api_response
                    else:
                        result["changed"] = False
                        
    if isinstance(result["api_response"], list):
        
        if eval_list_new_servername(module, exist_settings):
                   
                    api_response = update_radius_add(connection, module, result)
                  
            
                    if api_response:
                        if (api_response["Response"]["RADIUSServer"]["Status"]["#text"]
                        
                                == "Configuration applied successfully."):
                            result["changed"] = True
                        result["api_response"] = api_response
                    else:
                        result["changed"] = False
        else:
    
            if eval_list_update_server(module, exist_settings):
               
                api_response = update_radius_update(connection, module, result)
                    
                if api_response:
                    if (api_response["Response"]["RADIUSServer"]["Status"]["#text"] == "Configuration applied successfully."):
                        result["changed"] = True
                    result["api_response"] = api_response
                else:
                    result["changed"] = False
    
    
                    

    module.exit_json(**result)
  

if __name__ == "__main__":
    main()