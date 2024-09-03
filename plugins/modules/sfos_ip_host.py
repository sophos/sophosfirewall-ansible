#!/usr/bin/python

# Copyright 2024 Sophos Ltd.  All rights reserved.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r'''
---
module: sfos_ip_host

short_description: Manage IP Host objects on Sophos Firewall

version_added: "1.0.0"

description: Creates, updates or removes IP Host objects from Sophos Firewall

extends_documentation_fragment:
  - sophos.sophos_firewall.fragments.base

options:
    name:
        description: Name of the IP Host object to create, update, or delete
        required: true
        type: str
    ip_address:
        description:
            - IP Address for use when creating an IP address.
        required: false
        type: str
    start_ip:
        description:
            - Starting IP address for use when an creating IP range.
        required: false
        type: str
    end_ip:
        description:
            - Ending IP address for use when creating an IP range.
        required: false
        type: str
    network:
        description:
            - Network address for use when creating an IP network.
        required: false
        type: str
    mask:
        description:
            - Network mask for use when creating an IP network.
    host_type:
        description:
            - Type of IP Host object. 
        choices: [ip, network, range]
        type: str
        default: ip
    state:
        description:
            - Use C(present) to create, C(absent) to remove, or C(updated) to modify
        choices: [present, absent, updated, query]
        type: str
        required: true

author:
    - Matt Mullen (@mamullen13316)
'''

EXAMPLES = r'''
- name: Create IP Host
  sophos.sophos_firewall.sfos_ip_host:
    username: "{{ username }}"
    password: "{{ password }}"
    hostname: myfirewallhostname.sophos.net
    port: 4444
    verify: false
    name: TESTHOST
    ip_address: 1.1.1.1
    state: present
  delegate_to: localhost

- name: Create IP Network
  sophos.sophos_firewall.sfos_ip_host:
    username: "{{ username }}"
    password: "{{ password }}"
    hostname: myfirewallhostname.sophos.net
    port: 4444
    verify: false
    name: TESTNETWORK
    network: 1.1.1.0
    mask: 255.255.255.0
    host_type: network
    state: present
  delegate_to: localhost

- name: Create IP Range
  sophos.sophos_firewall.sfos_ip_host:
    username: "{{ username }}"
    password: "{{ password }}"
    hostname: myfirewallhostname.sophos.net
    port: 4444
    verify: false
    name: TESTRANGE
    start_ip: 10.1.1.1
    end_ip: 10.1.1.2
    host_type: range
    state: present
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
    PREREQ_MET = {"result": True}
except ImportError:
    PREREQ_MET = {"result": False, "missing_module": "sophosfirewall-python"}

try:
    from requests.exceptions import RequestException
    PREREQ_MET = {"result": True}
except ImportError:
    PREREQ_MET = {"result": False, "missing_module": "requests"}

from ipaddress import IPv4Address
from ipaddress import AddressValueError

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.basic import missing_required_lib


def get_host(fw_obj, module, result):
    """Get IP Host from Sophos Firewall

    Args:
        fw_obj (SophosFirewall): SophosFirewall object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: Results of lookup
    """
    try:
        resp = fw_obj.get_ip_host(name=module.params.get("name"))
    except SophosFirewallZeroRecords as error:
        return {"exists": False, "api_response": str(error)}
    except SophosFirewallAuthFailure as error:
        module.fail_json(msg="Authentication error: {0}".format(error), **result)
    except SophosFirewallAPIError as error:
        module.fail_json(msg="API Error: {0}".format(error), **result)
    except RequestException as error:
        module.fail_json(msg="Error communicating to API: {0}".format(error), **result)

    return {"exists": True, "api_response": resp}

def make_request(request_method, module, result, **kwargs):
    try:
        resp = request_method(**kwargs)
    except SophosFirewallAuthFailure as error:
        module.fail_json(msg="Authentication error: {0}".format(error), **result)
    except SophosFirewallAPIError as error:
        module.fail_json(msg="API Error: {0}".format(error), **result)
    except RequestException as error:
        module.fail_json(msg="Error communicating to API: {0}".format(error), **result)
    else:
        return resp

def create_host(fw_obj, module, result):
    """Create an IP Host on Sophos Firewall

    Args:
        fw_obj (SophosFirewall): SophosFirewall object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: API response
    """
        # try:
        #     resp = fw_obj.create_ip_host(
        #         name=module.params.get("name"), ip_address=module.params.get("ip_address")
        #     )
        # except SophosFirewallAuthFailure as error:
        #     module.fail_json(msg="Authentication error: {0}".format(error), **result)
        # except SophosFirewallAPIError as error:
        #     module.fail_json(msg="API Error: {0}".format(error), **result)
        # except RequestException as error:
        #     module.fail_json(msg="Error communicating to API: {0}".format(error), **result)
        # else:
        #     return resp
    kwargs = dict(name=module.params.get("name"))
    
    if module.params.get("host_type") == "ip": 
        kwargs["ip_address"] = module.params.get("ip_address")
        return make_request(fw_obj.create_ip_host, module, result, **kwargs)
    
    if module.params.get("host_type") == "network":
        kwargs["ip_address"] = module.params.get("network")
        kwargs["mask"] = module.params.get("mask")
        kwargs["host_type"] = "Network"
        return make_request(fw_obj.create_ip_host, module, result, **kwargs)
    
    if module.params.get("host_type") == "range":
        kwargs["start_ip"] = module.params.get("start_ip")
        kwargs["end_ip"] = module.params.get("end_ip")
        kwargs["host_type"] = "IPRange"
        return make_request(fw_obj.create_ip_host, module, result, **kwargs)


def remove_host(fw_obj, module, result):
    """Remove an IP Host from Sophos Firewall

    Args:
        fw_obj (SophosFirewall): SophosFirewall object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: API response
    """
    try:
        resp = fw_obj.remove(
            xml_tag="IPHost", name=module.params.get("name")
        )
    except SophosFirewallAuthFailure as error:
        module.fail_json(msg="Authentication error: {0}".format(error), **result)
    except SophosFirewallAPIError as error:
        module.fail_json(msg="API Error: {0}".format(error), **result)
    except RequestException as error:
        module.fail_json(msg="Error communicating to API: {0}".format(error), **result)
    else:
        return resp


def update_host(fw_obj, module, result):
    """Update an existing IP Host on Sophos Firewall

    Args:
        fw_obj (SophosFirewall): SophosFirewall object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: API response
    """
    # try:
    #     resp = fw_obj.update(
    #         xml_tag="IPHost",
    #         update_params={"IPAddress": module.params.get("ip_address")},
    #         name=module.params.get("name")
    #     )
    # except SophosFirewallAuthFailure as error:
    #     module.fail_json(msg="Authentication error: {0}".format(error), **result)
    # except SophosFirewallAPIError as error:
    #     module.fail_json(msg="API Error: {0}".format(error), **result)
    # except RequestException as error:
    #     module.fail_json(msg="Error communicating to API: {0}".format(error), **result)
    # else:
    #     return resp

    kwargs = dict(name=module.params.get("name"),
                  xml_tag="IPHost")
    
    if module.params.get("host_type") == "ip": 
        kwargs["update_params"] = {"IPAddress": module.params.get("ip_address")}
        return make_request(fw_obj.update, module, result, **kwargs)
    
    if module.params.get("host_type") == "network":
        kwargs["update_params"] = {
            "IPAddress": module.params.get("network"),
            "Subnet": module.params.get("mask")
            }
        return make_request(fw_obj.update, module, result, **kwargs)
    
    if module.params.get("host_type") == "range":
        kwargs["update_params"] = {
            "StartIPAddress": module.params.get("start_ip"),
            "EndIPAddress": module.params.get("end_ip")
        }
        return make_request(fw_obj.update, module, result, **kwargs)


def validate_ip(ip_address, module, result):
    """Validate IP address format.

    Args:
        ip_address (str): IP Address
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console
    """
    try:
        IPv4Address(ip_address)
    except AddressValueError as error:
        module.fail_json(msg="IP address error: {0}".format(error), **result)


def main():
    """Code executed at run time."""
    argument_spec = {
        "username": {"required": True},
        "password": {"required": True, "no_log": True},
        "hostname": {"required": True},
        "port": {"type": "int", "default": 4444},
        "verify": {"type": "bool", "default": True},
        "name": {"required": True},
        "ip_address": {"type": "str"},
        "start_ip": {"type": "str"},
        "end_ip": {"type": "str"},
        "network": {"type": "str"},
        "mask": {"type": "str"},
        "host_type": {"choices": ["ip","range", "network"], "default": "ip"},
        "state": {"required": True, "choices": ["present", "absent", "updated", "query"]},
    }
    required_if = [
        ('state', 'present', ('ip_address', 'network', 'mask', 'start_ip', 'end_ip',), True),
        ('state', 'updated', ('ip_address','network', 'mask', 'start_ip', 'end_ip',), True),
        ('host_type', 'range', ('start_ip', 'end_ip',), True),
        ('host_type', 'network', ('network', 'mask',), True)
    ]

    required_together = [
        ["start_ip", "end_ip"],
        ["network", "mask"]
    ]

    module = AnsibleModule(argument_spec=argument_spec,
                           required_if=required_if,
                           required_together=required_together,
                           supports_check_mode=True)

    if not PREREQ_MET["result"]:
        module.fail_json(msg=missing_required_lib(PREREQ_MET["msg"]))
        

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
    if state == "present" or state == "updated":
        if module.params.get("host_type") == "ip":
            validate_ip(module.params.get("ip_address"), module, result)
        if module.params.get("host_type") == "range":
            validate_ip(module.params.get("start_ip"), module, result)
            validate_ip(module.params.get("end_ip"), module, result)
        if module.params.get("host_type") == "network":
            validate_ip(module.params.get("network"), module, result)
            validate_ip(module.params.get("mask"), module, result)

    exist_check = get_host(fw, module, result)
    result["api_response"] = exist_check["api_response"]

    if state == "query":
        module.exit_json(**result)

    if module.check_mode:
        result["check_mode"] = True
        module.exit_json(**result)

    if state == "present" and not exist_check["exists"]:
        api_response = create_host(fw, module, result)
        if (
            api_response["Response"]["IPHost"]["Status"]["#text"]
            == "Configuration applied successfully."
        ):
            result["changed"] = True
            result["api_response"] = api_response

    elif state == "present" and exist_check["exists"]:
        result["changed"] = False

    elif state == "absent" and exist_check["exists"]:
        api_response = remove_host(fw, module, result)
        if (api_response["Response"]["IPHost"]["Status"]["#text"]
                == "Configuration applied successfully."):
            result["changed"] = True
        result["api_response"] = api_response

    elif state == "absent" and not exist_check["exists"]:
        result["changed"] = False

    elif state == "updated" and exist_check["exists"]:
        api_response = None
        if module.params.get("host_type") == "ip":
            if exist_check["api_response"]["Response"]["IPHost"]["IPAddress"] != module.params.get("ip_address"):
                api_response = update_host(fw, module, result)
        
        if module.params.get("host_type") == "network":
            if exist_check["api_response"]["Response"]["IPHost"]["IPAddress"] != module.params.get("network") \
            or exist_check["api_response"]["Response"]["IPHost"]["Subnet"] != module.params.get("mask"):
                api_response = update_host(fw, module, result)
        
        if module.params.get("host_type") == "range":
            if exist_check["api_response"]["Response"]["IPHost"]["StartIPAddress"] != module.params.get("start_ip") \
            or exist_check["api_response"]["Response"]["IPHost"]["EndIPAddress"] != module.params.get("end_ip"):
                api_response = update_host(fw, module, result)

        if api_response:
            if (api_response["Response"]["IPHost"]["Status"]["#text"]
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
