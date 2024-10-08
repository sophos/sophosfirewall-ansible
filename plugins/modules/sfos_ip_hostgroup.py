#!/usr/bin/python

# Copyright 2024 Sophos Ltd.  All rights reserved.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r'''
---
module: sfos_ip_hostgroup

short_description: Manage IP Hostgroup (System > Hosts & services > IP host group)

version_added: "1.0.0"

description: Creates, updates or removes an IP Host Group  (System > Hosts & services > IP host group) on Sophos Firewall

extends_documentation_fragment:
  - sophos.sophos_firewall.fragments.base

options:
    name:
        description: Name of the IP Host Group object to create, update, or delete
        required: true
        type: str
    description:
        description:
            - Description to be included on the IP Host Group object.
        required: false
        type: str
    host_list:
        description:
            - List of IP Host objects to be included in the IP Hostgroup
        type: list
        required: false
        elements: str
    action:
        description:
            - Indicates whether to add or remove hosts from the list, or replace the list entirely.
        type: str
        choices: [add, remove, replace]
        required: false
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
- name: Retrieve IP Host Group
  sophos.sophos_firewall.sfos_ip_hostgroup:
    username: "{{ username }}"
    password: "{{ password }}"
    hostname: myfirewallhostname.sophos.net
    port: 4444
    verify: false
    name: TESTHOSTGROUP
    state: query
  delegate_to: localhost

- name: Create IP Host Group
  sophos.sophos_firewall.sfos_ip_hostgroup:
    username: "{{ username }}"
    password: "{{ password }}"
    hostname: myfirewallhostname.sophos.net
    port: 4444
    verify: false
    name: TESTHOSTGROUP
    description: Test Host Group
    host_list:
      - TESTHOST1
      - TESTHOST2
    state: present
  delegate_to: localhost

- name: Add Hosts to IP Host Group
  sophos.sophos_firewall.sfos_ip_hostgroup:
    username: "{{ username }}"
    password: "{{ password }}"
    hostname: myfirewallhostname.sophos.net
    port: 4444
    verify: false
    name: TESTHOSTGROUP
    description: Test Host Group
    host_list:
      - TESTHOST3
      - TESTHOST4
    action: add
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


def get_hostgroup(fw_obj, module, result):
    """Get IP Host Group from Sophos Firewall

    Args:
        fw_obj (SophosFirewall): SophosFirewall object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: Results of lookup
    """
    try:
        resp = fw_obj.get_ip_hostgroup(name=module.params.get("name"))
    except SophosFirewallZeroRecords as error:
        return {"exists": False, "api_response": str(error)}
    except SophosFirewallAuthFailure as error:
        module.fail_json(msg="Authentication error: {0}".format(error), **result)
    except SophosFirewallAPIError as error:
        module.fail_json(msg="API Error: {0}".format(error), **result)
    except RequestException as error:
        module.fail_json(msg="Error communicating to API: {0}".format(error), **result)

    return {"exists": True, "api_response": resp}


def create_hostgroup(fw_obj, module, result):
    """Create an IP Host Group on Sophos Firewall

    Args:
        fw_obj (SophosFirewall): SophosFirewall object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: API response
    """
    try:
        resp = fw_obj.create_ip_hostgroup(
            name=module.params.get("name"),
            description=module.params.get("description"),
            host_list=module.params.get("host_list")
        )
    except SophosFirewallAuthFailure as error:
        module.fail_json(msg="Authentication error: {0}".format(error), **result)
    except SophosFirewallAPIError as error:
        module.fail_json(msg="API Error: {0}".format(error), **result)
    except RequestException as error:
        module.fail_json(msg="Error communicating to API: {0}".format(error), **result)
    else:
        return resp


def remove_hostgroup(fw_obj, module, result):
    """Remove an IP Host Group from Sophos Firewall

    Args:
        fw_obj (SophosFirewall): SophosFirewall object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: API response
    """
    try:
        resp = fw_obj.remove(
            xml_tag="IPHostGroup", name=module.params.get("name")
        )
    except SophosFirewallAuthFailure as error:
        module.fail_json(msg="Authentication error: {0}".format(error), **result)
    except SophosFirewallAPIError as error:
        module.fail_json(msg="API Error: {0}".format(error), **result)
    except RequestException as error:
        module.fail_json(msg="Error communicating to API: {0}".format(error), **result)
    else:
        return resp


def update_hostgroup(fw_obj, module, result):
    """Update an existing IP Host Group on Sophos Firewall

    Args:
        fw_obj (SophosFirewall): SophosFirewall object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: API response
    """
    try:
        resp = fw_obj.update_ip_hostgroup(
            name=module.params.get("name"),
            host_list=module.params.get("host_list"),
            description=module.params.get("description"),
            action=module.params.get("action")
        )
    except SophosFirewallAuthFailure as error:
        module.fail_json(msg="Authentication error: {0}".format(error), **result)
    except SophosFirewallAPIError as error:
        module.fail_json(msg="API Error: {0}".format(error), **result)
    except RequestException as error:
        module.fail_json(msg="Error communicating to API: {0}".format(error), **result)
    else:
        return resp


def main():
    """Code executed at run time."""
    argument_spec = {
        "username": {"required": True},
        "password": {"required": True, "no_log": True},
        "hostname": {"required": True},
        "port": {"type": "int", "default": 4444},
        "verify": {"type": "bool", "default": True},
        "name": {"required": True},
        "description": {"type": "str", "default": None},
        "host_list": {"type": "list", "default": [], "elements": "str"},
        "action": {"type": "str", "choices": ["add", "remove", "replace"], "default": None},
        "state": {"required": True, "choices": ["present", "absent", "updated", "query"]},
    }
    required_if = [
        ('state', 'present', ('host_list',), True),
        ('state', 'updated', ('action',), True)
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
    exist_check = get_hostgroup(fw, module, result)
    result["api_response"] = exist_check["api_response"]

    if state == "query":
        module.exit_json(**result)

    if module.check_mode:
        result["check_mode"] = True
        module.exit_json(**result)

    if state == "present" and not exist_check["exists"]:
        api_response = create_hostgroup(fw, module, result)
        if (
            api_response["Response"]["IPHostGroup"]["Status"]["#text"]
            == "Configuration applied successfully."
        ):
            result["changed"] = True
            result["api_response"] = api_response

    elif state == "present" and exist_check["exists"]:
        result["changed"] = False

    elif state == "absent" and exist_check["exists"]:
        api_response = remove_hostgroup(fw, module, result)
        if (api_response["Response"]["IPHostGroup"]["Status"]["#text"]
                == "Configuration applied successfully."):
            result["changed"] = True
        result["api_response"] = api_response

    elif state == "absent" and not exist_check["exists"]:
        result["changed"] = False

    elif state == "updated" and exist_check["exists"]:
        if (sorted(exist_check["api_response"]["Response"]["IPHostGroup"]["HostList"]["Host"])
                != sorted(module.params.get("host_list"))):
            api_response = update_hostgroup(fw, module, result)
            if (api_response["Response"]["IPHostGroup"]["Status"]["#text"]
                    == "Configuration applied successfully."):
                result["changed"] = True
            result["api_response"] = api_response
        else:
            result["changed"] = False

    elif state == "updated" and not exist_check["exists"]:
        result["changed"] = False
        module.fail_json(exist_check["api_response"], **result)

    module.exit_json(**result)


if __name__ == "__main__":
    main()
