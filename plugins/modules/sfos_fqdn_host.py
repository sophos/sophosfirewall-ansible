#!/usr/bin/python

# Copyright 2024 Sophos Ltd.  All rights reserved.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r'''
---
module: sfos_fqdn_host

short_description: Manage FQDN hosts (System > Hosts & services > FQDN host)

version_added: "1.0.0"

description: Creates, updates or removes a FQDN host (System > Hosts & services > FQDN host) on Sophos Firewall

extends_documentation_fragment:
  - sophos.sophos_firewall.fragments.base

options:
    name:
        description: Name of the FQDN object to create, update, or delete
        required: true
        type: str
    description:
        description: Description for the FQDN. 
        required: false
        type: str
    fqdn:
        description:
            - The FQDN string.
        type: str
    fqdn_group_list:
        description:
          - A list of FQDN groups this FQDN host should be placed into when created. The sfos_fqdn_hostgroup module can be used to manage this post-creation.
        type: list
        elements: str
    state:
        description:
            - Use C(query) to retrieve, C(present) to create, C(absent) to remove, or C(updated) to modify
        choices: [present, absent, updated, query]
        type: str
        required: true

author:
    - Matt Mullen (@mamullen13316)
'''

EXAMPLES = r'''
- name: Retrieve FQDN Host
  sophos.sophos_firewall.sfos_fqdn_host:
    username: "{{ username }}"
    password: "{{ password }}"
    hostname: myfirewallhostname.sophos.net
    port: 4444
    verify: false
    name: TESTFQDN
    state: query
  delegate_to: localhost

- name: Create FQDN Host
  sophos.sophos_firewall.sfos_fqdn_host:
    username: "{{ username }}"
    password: "{{ password }}"
    hostname: myfirewallhostname.sophos.net
    port: 4444
    verify: false
    name: TESTFQDN
    description: Testing FQDN creation
    fqdn: sophos.com
    state: present
  delegate_to: localhost

- name: Add FQDN to FQDN Group
  sophos.sophos_firewall.sfos_fqdn_host:
    username: "{{ username }}"
    password: "{{ password }}"
    hostname: myfirewallhostname.sophos.net
    port: 4444
    verify: false
    name: TESTFQDN
    fqdn_group_list:
      - TESTFQDNGROUP
    state: updated
  delegate_to: localhost
'''

RETURN = r'''
api_response:
    description: Serialized object containing the API response.
    type: dict
    returned: always

'''

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


def get_fqdn_host(fw_obj, module, result):
    """Get FQDN Host from Sophos Firewall

    Args:
        fw_obj (SophosFirewall): SophosFirewall object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: Results of lookup
    """
    try:
        resp = fw_obj.get_fqdn_host(name=module.params.get("name"))
    except SophosFirewallZeroRecords as error:
        return {"exists": False, "api_response": str(error)}
    except SophosFirewallAuthFailure as error:
        module.fail_json(msg="Authentication error: {0}".format(error), **result)
    except SophosFirewallAPIError as error:
        module.fail_json(msg="API Error: {0}".format(error), **result)
    except RequestException as error:
        module.fail_json(msg="Error communicating to API: {0}".format(error), **result)

    return {"exists": True, "api_response": resp}


def create_fqdn_host(fw_obj, module, result):
    """Create a FQDN Host on Sophos Firewall

    Args:
        fw_obj (SophosFirewall): SophosFirewall object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: API response
    """

    # module.fail_json(f"service_list: {service_list}")

    try:
        resp = fw_obj.create_fqdn_host(
            name=module.params.get("name"),
            fqdn=module.params.get("fqdn"),
            fqdn_group_list=module.params.get("fqdn_group_list"),
            description=module.params.get("description")
        )
    except SophosFirewallAuthFailure as error:
        module.fail_json(msg="Authentication error: {0}".format(error), **result)
    except SophosFirewallAPIError as error:
        module.fail_json(msg="API Error: {0}".format(error), **result)
    except RequestException as error:
        module.fail_json(msg="Error communicating to API: {0}".format(error), **result)
    else:
        return resp


def remove_fqdn_host(fw_obj, module, result):
    """Remove an Service from Sophos Firewall

    Args:
        fw_obj (SophosFirewall): SophosFirewall object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: API response
    """
    try:
        resp = fw_obj.remove(
            xml_tag="FQDNHost", name=module.params.get("name")
        )
    except SophosFirewallAuthFailure as error:
        module.fail_json(msg="Authentication error: {0}".format(error), **result)
    except SophosFirewallAPIError as error:
        module.fail_json(msg="API Error: {0}".format(error), **result)
    except RequestException as error:
        module.fail_json(msg="Error communicating to API: {0}".format(error), **result)
    else:
        return resp


def update_fqdn_host(fw_obj, module, result):
    """Update an existing FQDN Host on Sophos Firewall

    Args:
        fw_obj (SophosFirewall): SophosFirewall object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: API response
    """ 

    update_params = {
        "Description": module.params.get("description"),
        "FQDN": module.params.get("fqdn"),
    }

    # This is for adding the FQDN host to a FQDN Hostgroup during creation. FQDN HostGroup membership can be managed with the sfos_fqdn_hostgroup module.
    if module.params.get("fqdn_group_list"):
        update_params["FQDNHostGroupList"] =  {"FQDNHostGroup": module.params.get("fqdn_group_list")}

    try:
        resp = fw_obj.update(
            name=module.params.get("name"),
            xml_tag="FQDNHost",
            update_params=update_params
        )
    except SophosFirewallAuthFailure as error:
        module.fail_json(msg="Authentication error: {0}".format(error), **result)
    except SophosFirewallAPIError as error:
        module.fail_json(msg="API Error: {0}".format(error), **result)
    except RequestException as error:
        module.fail_json(msg="Error communicating to API: {0}".format(error), **result)
    else:
        return resp

def ensure_list(source):
    """Convert a provided dict to a list containing the dict if not already a list.

    Args:
        source (dict or list): Source dictionary or list.

    Returns:
        list: Returns the dictionary inside a list, or just returns the original list. 
    """
    if isinstance(source, dict):
        return [source]
    elif isinstance(source, list):
        return source

def main():
    """Code executed at run time."""
    argument_spec = {
        "username": {"required": True},
        "password": {"required": True, "no_log": True},
        "hostname": {"required": True},
        "port": {"type": "int", "default": 4444},
        "verify": {"type": "bool", "default": True},
        "name": {"required": True},
        "description": {"type": "str"},
        "fqdn": {"type": "str"},
        "fqdn_group_list": {"type": "list", "elements": "str"},
        "state": {"required": True, "choices": ["present", "absent", "updated", "query"]},
    }
    required_if = [
        ('state', 'present', ('fqdn',), True),
        # ('state', 'updated', ('action',), True),
    ]

    module = AnsibleModule(argument_spec=argument_spec,
                           required_if=required_if,
                           supports_check_mode=True)

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
    exist_check = get_fqdn_host(fw, module, result)
    result["api_response"] = exist_check["api_response"]

    if state == "query":
        module.exit_json(**result)

    if module.check_mode:
        result["check_mode"] = True
        module.exit_json(**result)

    if state == "present" and not exist_check["exists"]:
        api_response = create_fqdn_host(fw, module, result)
        if (
            api_response["Response"]["FQDNHost"]["Status"]["#text"]
            == "Configuration applied successfully."
        ):
            result["changed"] = True
            result["api_response"] = api_response

    elif state == "present" and exist_check["exists"]:
        result["changed"] = False

    elif state == "absent" and exist_check["exists"]:
        api_response = remove_fqdn_host(fw, module, result)
        if (api_response["Response"]["FQDNHost"]["Status"]["#text"]
                == "Configuration applied successfully."):
            result["changed"] = True
        result["api_response"] = api_response

    elif state == "absent" and not exist_check["exists"]:
        result["changed"] = False

    elif state == "updated" and exist_check["exists"]:

            api_response = update_fqdn_host(fw, module, result)
            if (api_response["Response"]["FQDNHost"]["Status"]["#text"]
                    == "Configuration applied successfully."):
                result["changed"] = True
            else:
                result["changed"] = False
            result["api_response"] = api_response

    elif state == "updated" and not exist_check["exists"]:
        result["changed"] = False
        module.fail_json(exist_check["api_response"], **result)

    module.exit_json(**result)


if __name__ == "__main__":
    main()
