#!/usr/bin/python

# Copyright 2024 Sophos Ltd.  All rights reserved.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
import sys

__metaclass__ = type

DOCUMENTATION = r'''
---
module: sfos_authentication_tacacs.py

short_description: Manage Authentication settings Tacacs

version_added: "1.3.0"

description: Manage authentication servers (Configure > Authentication > Servers> Add) on Sophos Firewall

extends_documentation_fragment:
  - sophos.sophos_firewall.fragments.base

options:
    Servername:
        description: Name of Server
        type: str
        required: false
    ServerAddress:
        description: Server IP Address
        type: str
        required: false
    port:
        description: Directory tenant ID
        type: str
        required: false
    SharedSecret:
        description: Shared Secret
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
- name: Update TACACS Auth
  sophos.sophos_firewall.sfos_authentication_tacacs:
    username: "{{ username }}"
    password: "{{ password }}"
    hostname: "{{ inventory_hostname }}"
    port: 4444
    verify: false
    servername: Test
    serveraddress: '192.168.0.1'
    tac_port: '49'
    sharedsecret: testtest
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


def get_tacacs_settings(fw_obj, module, result):
    """Get current settings from Sophos Firewall

    Args:
        fw_obj (SophosFirewall): SophosFirewall object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: Results of lookup
    """
    try:
        resp = fw_obj.get_tag("AuthenticationServer")['Response']['AuthenticationServer']["TACACSServer"]
            
    except SophosFirewallZeroRecords as error:
        return {"exists": False, "api_response": str(error)}
    except SophosFirewallAuthFailure as error:
        module.fail_json(msg="Authentication error: {0}".format(error), **result)
    except SophosFirewallAPIError as error:
        module.fail_json(msg="API Error: {0}".format(error), **result)
    except RequestException as error:
        module.fail_json(msg="Error communicating to API: {0}".format(error), **result)

    return {"exists": True, "api_response": resp}

def create_tacacs(fw_obj, module, result):
    """Create an TACACS Server on Sophos Firewall when none exists

    Args:
        fw_obj (SophosFirewall): SophosFirewall object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: API response
    """
    payload = """
        <AuthenticationServer>
          <TACACSServer>
		  <ServerName>{{ name }}</ServerName>
		  <ServerAddress>{{ ipaddress }}</ServerAddress>
		  <Port>{{ tac_port }}</Port>
		  <SharedSecret>{{ sharedsecret }}</SharedSecret>
	      </TACACSServer>
        </AuthenticationServer>
    
    """
    template_vars = {
        "name": module.params.get("servername"),
        "ipaddress": module.params.get("serveraddress"),
        "tac_port": module.params.get("tac_port"),
        "sharedsecret": module.params.get("sharedsecret")
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

def update_tacacs_add(fw_obj, module, result):
    """Add additional TACACS server on Sophos Firewall

    Args:
        fw_obj (SophosFirewall): SophosFirewall object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: API response
    """
    payload = """
        <AuthenticationServer>
          <TACACSServer>
		  <ServerName>{{ name }}</ServerName>
		  <ServerAddress>{{ ipaddress }}</ServerAddress>
		  <Port>{{ tac_port }}</Port>
		  <SharedSecret>{{ sharedsecret }}</SharedSecret>
	      </TACACSServer>
        </AuthenticationServer>
    
    """
    template_vars = {
        "name": module.params.get("servername"),
        "ipaddress": module.params.get("serveraddress"),
        "tac_port": module.params.get("tac_port"),
        "sharedsecret": module.params.get("sharedsecret")
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

def update_tacacs_update(fw_obj, module, result):
    """Update existing TACACS settings on Sophos Firewall

    Args:
        fw_obj (SophosFirewall): SophosFirewall object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: API response
    """
    payload = """
        <AuthenticationServer>
          <TACACSServer>
		  <ServerName>{{ name }}</ServerName>
		  <ServerAddress>{{ ipaddress }}</ServerAddress>
		  <Port>{{ tac_port }}</Port>
		  <SharedSecret>{{ sharedsecret }}</SharedSecret>
	      </TACACSServer>
        </AuthenticationServer>
    
    """
    template_vars = {
        "name": module.params.get("servername"),
        "ipaddress": module.params.get("serveraddress"),
        "tac_port": module.params.get("tac_port"),
        "sharedsecret": module.params.get("sharedsecret")
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
    serveraddress = module.params.get("serveraddress", {})
    tac_port = module.params.get("tac_port", {})
    sharedsecret = module.params.get("sharedsecret")
    
    
    if servername and not servername == exist_settings["ServerName"]:
        return True
    if serveraddress and not serveraddress == exist_settings["ServerAddress"]:
        return True
    if tac_port and not tac_port == exist_settings["Port"]:
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
    tac_port = module.params.get("tac_port", {})
    sharedsecret = module.params.get("sharedsecret")
    
    list_len = len(exist_settings)
    for i in range(list_len):
       
        if (exist_settings[i]["ServerName"]) == servername:
            
            if serveraddress and not serveraddress == exist_settings[i]["ServerAddress"]:
                return True, i
            if tac_port and not tac_port == exist_settings[i]["Port"]:
                return True,i
            if module.params.get("sharedsecret"): 
                return True,i
            
    return False


def remove_tacacs(fw_obj, module, result):
    """Remove a Tacacs Server on a Sophos Firewall

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
            <TACACSServer>
		    <ServerName>{{ name }}</ServerName>
            </TACACSServer>
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
        "tac_port": {"type": "str", "required": False},
        "sharedsecret": {"type": "str", "required": False},
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

    exist_settings = get_tacacs_settings(fw, module, result)
    result["api_response"] = exist_settings["api_response"]
    
    
    if state == "absent":
                
                api_response = remove_tacacs(fw, module, result)
                if api_response:
                    if api_response['Response']["AuthenticationServer"]["TACACSServer"]["Status"]["#text"] == "Configuration applied successfully.":
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
            
                
                api_response = create_tacacs(fw, module, result)
                
                if api_response:
                    if api_response['Response']["TACACSServer"]["Status"]["#text"] == "Configuration applied successfully.":
                        result["changed"] = True
                    result["api_response"] = api_response
                else:
                    result["changed"] = False
    
        
        elif state == "updated" and "ServerName" in result["api_response"]:
            
            if eval_servername(module, exist_settings):
                
                if eval_changed(module, exist_settings):
                    
                    api_response = update_tacacs_add(fw, module, result)
                    
            
                    if api_response:
                        if (api_response["Response"]["TACACSServer"]["Status"]["#text"]
                        
                                == "Configuration applied successfully."):
                            result["changed"] = True
                        result["api_response"] = api_response
                    else:
                        result["changed"] = False
                        
            if not eval_servername(module, exist_settings):
                if eval_changed(module, exist_settings):
                    
                    api_response = update_tacacs_update(fw, module, result)
                    
            
                    if api_response:
                        if (api_response["Response"]["TACACSServer"]["Status"]["#text"]
                        
                                == "Configuration applied successfully."):
                            result["changed"] = True
                        result["api_response"] = api_response
                    else:
                        result["changed"] = False
                        
    if isinstance(result["api_response"], list):
        
        if eval_list_new_servername(module, exist_settings):
                    
                    api_response = update_tacacs_add(fw, module, result)
                   
            
                    if api_response:
                        if (api_response["Response"]["TACACSServer"]["Status"]["#text"]
                        
                                == "Configuration applied successfully."):
                            result["changed"] = True
                        result["api_response"] = api_response
                    else:
                        result["changed"] = False
        else:
    
            if eval_list_update_server(module, exist_settings):
                
                api_response = update_tacacs_update(fw, module, result)
                    
                if api_response:
                    if (api_response["Response"]["TACACSServer"]["Status"]["#text"] == "Configuration applied successfully."):
                        result["changed"] = True
                    result["api_response"] = api_response
                else:
                    result["changed"] = False
    
    
                    

    module.exit_json(**result)
  

if __name__ == "__main__":
    main()