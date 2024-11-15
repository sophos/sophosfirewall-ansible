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
        description: Aplication Client ID
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
'''

EXAMPLES = r'''
- name: Update Azure AD SSO
  sophos.sophos_firewall.sfos_authentication_radius:
    username: "{{ username }}"
    password: "{{ password }}"
    hostname: "{{ inventory_hostname }}"
    port: 4444
    verify: false
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


def get_radius_settings(fw_obj, module, result):
    """Get current settings from Sophos Firewall

    Args:
        fw_obj (SophosFirewall): SophosFirewall object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: Results of lookup
    """
    try:
        resp = fw_obj.get_tag("AuthenticationServer")['Response']['AuthenticationServer']["RADIUSServer"]
            
    except SophosFirewallZeroRecords as error:
        return {"exists": False, "api_response": str(error)}
    except SophosFirewallAuthFailure as error:
        module.fail_json(msg="Authentication error: {0}".format(error), **result)
    except SophosFirewallAPIError as error:
        module.fail_json(msg="API Error: {0}".format(error), **result)
    except RequestException as error:
        module.fail_json(msg="Error communicating to API: {0}".format(error), **result)

    return {"exists": True, "api_response": resp}

def create_radius(fw_obj, module, result):
    """Create an Radius Server on Sophos Firewall when none exists

    Args:
        fw_obj (SophosFirewall): SophosFirewall object
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
    # print(template_vars)
    # final_payload = payload.format(**template_vars)
    # print("Final Payload with Variables Substituted:")
    # print(final_payload)
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

def update_radius_add(fw_obj, module, result):
    """Add additional radius server on Sophos Firewall

    Args:
        fw_obj (SophosFirewall): SophosFirewall object
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
    # print(template_vars)
    # final_payload = payload.format(**template_vars)
    # print("Final Payload with Variables Substituted:")
    # print(final_payload)
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

def update_radius_update(fw_obj, module, result):
    """Update existing radius settings on Sophos Firewall

    Args:
        fw_obj (SophosFirewall): SophosFirewall object
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
    # print(template_vars)
    # final_payload = payload.format(**template_vars)
    # print("Final Payload with Variables Substituted:")
    # print(final_payload)
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
    
    # module.fail_json(msg=f"{resp['Response']}, {output_buffer.getvalue()}")
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


def remove_radius(fw_obj, module, result):
    """Remove a Radius Server on a Sophos Firewall

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
            <RADIUSServer>
		    <ServerName>{{ name }}</ServerName>
            </RADIUSServer>
            </AuthenticationServer>
            </Remove>
    """
    template_vars = {
        "name": module.params.get("servername")
    }
    # print(template_vars)
    # final_payload = payload.format(**template_vars)
    # print("Final Payload with Variables Substituted:")
    # print(final_payload)
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
    
    # module.fail_json(msg=f"{resp['Response']}, {output_buffer.getvalue()}")
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
        "port_radius": {"type": "str", "required": False},
        "sharedsecret": {"type": "str", "required": False},
        "groupnameattribute": {"type": "str", "required": False},
        "timeout": {"type": "str", "required": False},
        "domainname": {"type": "str", "required": False},
        "enableaccounting": {"type": "str", "choices": ["Enable", "None"]},
        # "nas_identifier": {"type": "str", "required": False},
        # "nas_port_type": {"type": "str", "required": False},
        "accountingport": {"type": "str", "required": False},
        "attributes": {"type": "dict", "required": False},
        "state": {"type": "str", "required": True, "choices": ["updated", "query", "absent"]}
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

    exist_settings = get_radius_settings(fw, module, result)
    result["api_response"] = exist_settings["api_response"]
    
    
    if state == "absent":
                # module.exit_json(msg=f"eval=true")
                api_response = remove_radius(fw, module, result)
                
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
            
                
                api_response = create_radius(fw, module, result)
                
                if api_response:
                    if api_response['Response']["RADIUSServer"]["Status"]["#text"] == "Configuration applied successfully.":
                        result["changed"] = True
                    result["api_response"] = api_response
                else:
                    result["changed"] = False
    
        
        elif state == "updated" and "ServerName" in result["api_response"]:
            
            if eval_servername(module, exist_settings):
                if eval_changed(module, exist_settings):
                    # module.exit_json(msg=f"eval=true")
                    api_response = update_radius_add(fw, module, result)
                    print(f'toppp2',api_response)
            
                    if api_response:
                        if (api_response["Response"]["RADIUSServer"]["Status"]["#text"]
                        
                                == "Configuration applied successfully."):
                            result["changed"] = True
                        result["api_response"] = api_response
                    else:
                        result["changed"] = False
                        
            if not eval_servername(module, exist_settings):
                if eval_changed(module, exist_settings):
                    # module.exit_json(msg=f"eval=true")
                    api_response = update_radius_update(fw, module, result)
                    print(f'toppp2',api_response)
            
                    if api_response:
                        if (api_response["Response"]["RADIUSServer"]["Status"]["#text"]
                        
                                == "Configuration applied successfully."):
                            result["changed"] = True
                        result["api_response"] = api_response
                    else:
                        result["changed"] = False
                        
    if isinstance(result["api_response"], list):
        
        if eval_list_new_servername(module, exist_settings):
                    # module.exit_json(msg=f"eval=true")
                    api_response = update_radius_add(fw, module, result)
                    print(f'toppp2',api_response)
            
                    if api_response:
                        if (api_response["Response"]["RADIUSServer"]["Status"]["#text"]
                        
                                == "Configuration applied successfully."):
                            result["changed"] = True
                        result["api_response"] = api_response
                    else:
                        result["changed"] = False
        else:
    
            if eval_list_update_server(module, exist_settings):
                # module.exit_json(msg=f"eval=true")
                api_response = update_radius_update(fw, module, result)
                    
                if api_response:
                    if (api_response["Response"]["RADIUSServer"]["Status"]["#text"] == "Configuration applied successfully."):
                        result["changed"] = True
                    result["api_response"] = api_response
                else:
                    result["changed"] = False
    
    
                    

    module.exit_json(**result)
  

if __name__ == "__main__":
    main()