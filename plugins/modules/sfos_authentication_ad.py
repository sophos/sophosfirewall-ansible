#!/usr/bin/python

# Copyright 2024 Sophos Ltd.  All rights reserved.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
import sys

__metaclass__ = type

DOCUMENTATION = r'''
---
module: sfos_authentication_ad.py

short_description: Manage Authentication settings Active Directory

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
    NetBIOSDomain:
        description: NetBIOS Domain
        type: str
        required: false
    ADSUsername:
        description: ADS user name
        type: str
        required: false
    AD_Password:
        description: Password
        type: str
        required: false
    ConnectionSecurity:
        description: Connection security
        type: str
        choices: [Simple, StartTLS, SSL]
        required: false
    ValidCertReq:
        description: enable accounting
        type: str
        choices: [Enable, Disable]
        required: false
    DisplayNameAttribute:
        description: Display name attribute
        type: str
        required: false
    EmailAddressAttribute:
        description: Email address attribute
        type: str
        required: false
    DomainName:
        description: Domain name
        type: str
        required: false
    SearchQueries:
        description: Search queries
        type: list
        elements: str
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
- name: Update Active Directory Auth
  sophos.sophos_firewall.sfos_authentication_ad:
    servername: Test
    serveraddress: '192.168.0.1'
    ad_port: '636'
    netbiosdomain: test.sophos.com
    adsusername: admin
    ad_password: testtest
    connectionsecurity: SSL
    validcertreq: Disable
    displaynameattribute: dn
    emailaddressattribute: mail
    domainname: sophos.com
    searchqueries:
        - dc=sophos,dc=com
        - dc=sophos,dc=ie
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


def get_ad_settings(connection, module, result):
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

    return {"exists": True, "api_response": resp["response"]['Response']['AuthenticationServer']["ActiveDirectory"]}

def create_ad(connection, module, result):
    """Create an Active Directory Server on Sophos Firewall when none exists

    Args:
        connection (Connection): Ansible Connection object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: API response
    """
    payload = """
        <AuthenticationServer>
          <ActiveDirectory>
		  <ServerName>{{ name }}</ServerName>
		  <ServerAddress>{{ ipaddress }}</ServerAddress>
		  <Port>{{ ad_port }}</Port>
		  <NetBIOSDomain>{{ netbiosdomain }}</NetBIOSDomain>
          <ADSUsername>{{ ad_username }}</ADSUsername>
          <Password>{{ ad_password }}</Password>
          <ConnectionSecurity>{{ connectionsecurity }}</ConnectionSecurity>
          <ValidCertReq>{{ validcertreq }}</ValidCertReq>
          <DisplayNameAttribute>{{ displaynameattribute }}</DisplayNameAttribute>
          <EmailAddressAttribute>{{ emailaddressattribute }}</EmailAddressAttribute>
		  <DomainName>{{ domainname }}</DomainName>
          <SearchQueries>
          {% for item in searchqueries %}
           <Query>{{ item }}</Query>
        {% endfor %}
          </SearchQueries>
	      </ActiveDirectory>
        </AuthenticationServer>
    
    """
    template_vars = {
        "name": module.params.get("servername"),
        "ipaddress": module.params.get("serveraddress"),
        "ad_port": module.params.get("ad_port"),
        "netbiosdomain": module.params.get("netbiosdomain"),
        "ad_username": module.params.get("adsusername"),
        "ad_password": module.params.get("ad_password"),
        "connectionsecurity": module.params.get("connectionsecurity"),
        "validcertreq": module.params.get("validcertreq"),
        "displaynameattribute": module.params.get("displaynameattribute"),
        "emailaddressattribute": module.params.get("emailaddressattribute"),
        "domainname": module.params.get("domainname"),
        "searchqueries": module.params.get("searchqueries")
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

def update_ad_add(connection, module, result):
    """Add additional Active Directory server on Sophos Firewall

    Args:
        connection (Connection): HTTPAPI Connection object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: API response
    """
    payload = """
        <AuthenticationServer>
          <ActiveDirectory>
		  <ServerName>{{ name }}</ServerName>
		  <ServerAddress>{{ ipaddress }}</ServerAddress>
		  <Port>{{ ad_port }}</Port>
		  <NetBIOSDomain>{{ netbiosdomain }}</NetBIOSDomain>
          <ADSUsername>{{ ad_username }}</ADSUsername>
          <Password>{{ ad_password }}</Password>
          <ConnectionSecurity>{{ connectionsecurity }}</ConnectionSecurity>
          <ValidCertReq>{{ validcertreq }}</ValidCertReq>
          <DisplayNameAttribute>{{ displaynameattribute }}</DisplayNameAttribute>
          <EmailAddressAttribute>{{ emailaddressattribute }}</EmailAddressAttribute>
		  <DomainName>{{ domainname }}</DomainName>
          <SearchQueries>
          {% for item in searchqueries %}
           <Query>{{ item }}</Query>
        {% endfor %}
          </SearchQueries>
	      </ActiveDirectory>
        </AuthenticationServer>
    
    """
    template_vars = {
        "name": module.params.get("servername"),
        "ipaddress": module.params.get("serveraddress"),
        "ad_port": module.params.get("ad_port"),
        "netbiosdomain": module.params.get("netbiosdomain"),
        "ad_username": module.params.get("adsusername"),
        "ad_password": module.params.get("ad_password"),
        "connectionsecurity": module.params.get("connectionsecurity"),
        "validcertreq": module.params.get("validcertreq"),
        "displaynameattribute": module.params.get("displaynameattribute"),
        "emailaddressattribute": module.params.get("emailaddressattribute"),
        "domainname": module.params.get("domainname"),
        "searchqueries": module.params.get("searchqueries")
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
    

def update_ad_update(connection, module, result):
    """Update existing Active Directory settings on Sophos Firewall

    Args:
        connection (Connection): HTTPAPI Connection object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: API response
    """
    payload = """
        <AuthenticationServer>
          <ActiveDirectory>
		  <ServerName>{{ name }}</ServerName>
		  <ServerAddress>{{ ipaddress }}</ServerAddress>
		  <Port>{{ ad_port }}</Port>
		  <NetBIOSDomain>{{ netbiosdomain }}</NetBIOSDomain>
          <ADSUsername>{{ ad_username }}</ADSUsername>
          <Password>{{ ad_password }}</Password>
          <ConnectionSecurity>{{ connectionsecurity }}</ConnectionSecurity>
          <ValidCertReq>{{ validcertreq }}</ValidCertReq>
          <DisplayNameAttribute>{{ displaynameattribute }}</DisplayNameAttribute>
          <EmailAddressAttribute>{{ emailaddressattribute }}</EmailAddressAttribute>
		  <DomainName>{{ domainname }}</DomainName>
          <SearchQueries>
          {% for item in searchqueries %}
           <Query>{{ item }}</Query>
        {% endfor %}
          </SearchQueries>
	      </ActiveDirectory>
        </AuthenticationServer>
    
    """
    template_vars = {
        "name": module.params.get("servername"),
        "ipaddress": module.params.get("serveraddress"),
        "ad_port": module.params.get("ad_port"),
        "netbiosdomain": module.params.get("netbiosdomain"),
        "ad_username": module.params.get("adsusername"),
        "ad_password": module.params.get("ad_password"),
        "connectionsecurity": module.params.get("connectionsecurity"),
        "validcertreq": module.params.get("validcertreq"),
        "displaynameattribute": module.params.get("displaynameattribute"),
        "emailaddressattribute": module.params.get("emailaddressattribute"),
        "domainname": module.params.get("domainname"),
        "searchqueries": module.params.get("searchqueries")
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
    ad_port = module.params.get("ad_port", {})
    netbiosdomain = module.params.get("netbiosdomain", {})
    ad_username = module.params.get("ad_username", {})
    ad_password = module.params.get("ad_password", {})
    connectionsecurity = module.params.get("connectionsecurity", {})
    validcertreq = module.params.get("validcertreq", {})
    displaynameattribute = module.params.get("displaynameattribute", {})
    emailaddressattribute = module.params.get("emailaddressattribute", {})
    domainname = module.params.get("domainname")
    searchqueries = module.params.get("searchqueries")
    
    
    if servername and not servername == exist_settings["ServerName"]:
        return True
    if serveraddress and not serveraddress == exist_settings["ServerAddress"]:
        return True
    if ad_port and not ad_port == exist_settings["Port"]:
        return True
    if netbiosdomain and not netbiosdomain == exist_settings["NetBIOSDomain"]:
        return True
    if ad_username and not ad_username == exist_settings["ADSUsername"]:
        return True
    if domainname and not domainname == exist_settings["DomainName"]:
        return True
    if connectionsecurity and not connectionsecurity == exist_settings["ConnectionSecurity"]:
            return True
    if validcertreq and not validcertreq == exist_settings["ValidCertReq"]:
            return True
    if displaynameattribute and not displaynameattribute == exist_settings["DisplayNameAttribute"]:
            return True
    if emailaddressattribute and not emailaddressattribute == exist_settings["EmailAddressAttribute"]:
            return True
    if searchqueries and not searchqueries == exist_settings["SearchQueries"]["Query"]:
        return True
            
    if module.params.get("ad_password"): 
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
    ad_port = module.params.get("ad_port", {})
    netbiosdomain = module.params.get("netbiosdomain", {})
    ad_username = module.params.get("ad_username", {})
    ad_password = module.params.get("ad_password", {})
    connectionsecurity = module.params.get("connectionsecurity", {})
    validcertreq = module.params.get("validcertreq", {})
    displaynameattribute = module.params.get("displaynameattribute", {})
    emailaddressattribute = module.params.get("emailaddressattribute", {})
    domainname = module.params.get("domainname")
    searchqueries = module.params.get("searchqueries")
    
    list_len = len(exist_settings)
    for i in range(list_len):
       
        if (exist_settings[i]["ServerName"]) == servername:
            
            if serveraddress and not serveraddress == exist_settings[i]["ServerAddress"]:
                return True, i
            if ad_port and not ad_port == exist_settings[i]["Port"]:
                return True,i
            if netbiosdomain and not netbiosdomain == exist_settings[i]["NetBIOSDomain"]:
                return True,i
            if ad_username and not ad_username == exist_settings[i]["ADSUsername"]:
                return True,i
            if domainname and not domainname == exist_settings[i]["DomainName"]:
                return True,i
            if connectionsecurity and not connectionsecurity == exist_settings[i]["ConnectionSecurity"]:
                return True,i
            if validcertreq and not validcertreq == exist_settings[i]["ValidCertReq"]:
                return True,i
            if displaynameattribute and not displaynameattribute == exist_settings[i]["DisplayNameAttribute"]:
                return True,i
            if emailaddressattribute and not emailaddressattribute == exist_settings[i]["EmailAddressAttribute"]:
                return True,i
            if searchqueries and not searchqueries == exist_settings[i]["SearchQueries"]["Query"]:
                return True,i
            if module.params.get("ad_password"): 
                return True,i
            
    return False


def remove_ad(connection, module, result):
    """Remove a Active Directory Server on a Sophos Firewall

    Args:
        connection (Connection): HTTPAPI Connection object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: API response
    """
    payload = """
            <Remove>
            <AuthenticationServer>
            <ActiveDirectory>
		    <ServerName>{{ name }}</ServerName>
            </ActiveDirectory>
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
        "ad_port": {"type": "str", "required": False},
        "netbiosdomain": {"type": "str", "required": False},
        "adsusername": {"type": "str", "required": False},
        "ad_password": {"type": "str", "required": False},
        "connectionsecurity": {"type": "str", "choices": ["Simple", "StartTLS", "SSL"]},
        "validcertreq": {"type": "str", "choices": ["Enable", "Disable"]},
        "displaynameattribute": {"type": "str", "required": False},
        "emailaddressattribute": {"type": "str", "required": False},
        "domainname": {"type": "str", "required": False},
        "searchqueries": {"type": "list", "required": False},
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

    exist_settings = get_ad_settings(connection, module, result)
    result["api_response"] = exist_settings["api_response"]
    
    
    if state == "absent":
                # module.exit_json(msg=f"eval=true")
                api_response = remove_ad(connection, module, result)
                if api_response:
                    if api_response['Response']["AuthenticationServer"]["ActiveDirectory"]["Status"]["#text"] == "Configuration applied successfully.":
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
            
                
                api_response = create_ad(connection, module, result)
                
                if api_response:
                    if api_response['Response']["ActiveDirectory"]["Status"]["#text"] == "Configuration applied successfully.":
                        result["changed"] = True
                    result["api_response"] = api_response
                else:
                    result["changed"] = False
    
        
        elif state == "updated" and "ServerName" in result["api_response"]:
            
            if eval_servername(module, exist_settings):
                
                if eval_changed(module, exist_settings):
                    
                    api_response = update_ad_add(connection, module, result)
                    
            
                    if api_response:
                        if (api_response["Response"]["ActiveDirectory"]["Status"]["#text"]
                        
                                == "Configuration applied successfully."):
                            result["changed"] = True
                        result["api_response"] = api_response
                    else:
                        result["changed"] = False
                        
            if not eval_servername(module, exist_settings):
                if eval_changed(module, exist_settings):
                    
                    api_response = update_ad_update(connection, module, result)
                    
            
                    if api_response:
                        if (api_response["Response"]["ActiveDirectory"]["Status"]["#text"]
                        
                                == "Configuration applied successfully."):
                            result["changed"] = True
                        result["api_response"] = api_response
                    else:
                        result["changed"] = False
                        
    if isinstance(result["api_response"], list):
        
        if eval_list_new_servername(module, exist_settings):
                    
                    api_response = update_ad_add(connection, module, result)
                    
            
                    if api_response:
                        if (api_response["Response"]["ActiveDirectory"]["Status"]["#text"]
                        
                                == "Configuration applied successfully."):
                            result["changed"] = True
                        result["api_response"] = api_response
                    else:
                        result["changed"] = False
        else:
    
            if eval_list_update_server(module, exist_settings):
                
                api_response = update_ad_update(connection, module, result)
                    
                if api_response:
                    if (api_response["Response"]["ActiveDirectory"]["Status"]["#text"] == "Configuration applied successfully."):
                        result["changed"] = True
                    result["api_response"] = api_response
                else:
                    result["changed"] = False
    
    
                    

    module.exit_json(**result)
  

if __name__ == "__main__":
    main()