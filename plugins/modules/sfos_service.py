#!/usr/bin/python

# Copyright 2024 Sophos Ltd.  All rights reserved.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r'''
---
module: sfos_service

short_description: Manage Service objects on Sophos Firewall

version_added: "1.0.0"

description: Creates, updates or removes a Service object on Sophos Firewall

extends_documentation_fragment:
  - sophos.sophos_firewall.fragments.base

options:
    name:
        description: Name of the Service object to create, update, or delete
        required: true
        type: str
    type:
        description:
            - Type of service object.
        type: str
        choices: [tcporudp, ip, icmp, icmpv6]
    service_list:
        description:
          - A list of ports/protocols to be included in the service definition.
        type: list
        elements: dict
        suboptions:
            src_port:
                description:
                    - Source TCP or UDP port.
                type: str
                default: 1:65535
            dst_port:
                description:
                    - Destination TCP or UDP port.
                type: str
            protocol:
                description: 
                    - TCP, UDP, or IP protocol number
                type: str
            icmp_type:
                description:
                    - ICMP type in numeric format.
                type: str
            icmp_code:
                description:
                    - ICMP code in numeric format.
                type: str
    action:
        description:
            - When performing an update, use to add or remove services from the list, or replace the list entirely
        choices: [add, remove, replace]
        type: str
        default: replace
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
- name: Retrieve Service
  sophos.sophos_firewall.sfos_service:
    username: "{{ username }}"
    password: "{{ password }}"
    hostname: myfirewallhostname.sophos.net
    port: 4444
    verify: false
    name: TESTSERVICE
    state: query
  delegate_to: localhost

- name: Create Service
  sophos.sophos_firewall.sfos_service:
    username: "{{ username }}"
    password: "{{ password }}"
    hostname: myfirewallhostname.sophos.net
    port: 4444
    verify: false
    name: TESTSERVICEWEB
    type: tcporudp
    service_list:
      - protocol: tcp
        src_port: 1:65535
        dst_port: 80
      - protocol: tcp
        src_port: 1:65535
        dst_port: 443
    state: present
  delegate_to: localhost

- name: Add service to service list
  sophos.sophos_firewall.sfos_service:
    username: "{{ username }}"
    password: "{{ password }}"
    hostname: myfirewallhostname.sophos.net
    port: 4444
    verify: false
    name: TESTSERVICEWEB
    service_list:
      - protocol: tcp
        src_port: 1:65535
        dst_port: 8888
    action: add
    state: updated
  delegate_to: localhost

- name: Add ICMP service
  sophos.sophos_firewall.sfos_service:
    username: "{{ username }}"
    password: "{{ password }}"
    hostname: myfirewallhostname.sophos.net
    port: 4444
    verify: false
    name: TESTICMP
    type: icmp
    service_list:
    - icmp_type: "Echo Reply"
      icmp_code: "Any Code"
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
    from requests.exceptions import RequestException
    PREREQ_MET = {"result": True}
except ImportError as errMsg:
    PREREQ_MET = {"result": False, "missing_module": errMsg.name}


from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.basic import missing_required_lib

def build_service_list(module):
    """Generate the service list based on provided arguments.

    Args:
        module (obj): AnsibleModule object
    """
    service_list = []
    service_type = module.params.get("type")
    if service_type == "tcporudp":
        svc_type = "TCPorUDP"
        for service in module.params.get("service_list"):
            service_list.append(dict(
                protocol=service["protocol"].upper(),
                src_port=service["src_port"],
                dst_port=service["dst_port"]
            ))
    if service_type == "ip":
        svc_type = "IP"
        for service in module.params.get("service_list"):
            service_list.append(dict(
                protocol=service["protocol"].upper()
            ))
    if service_type == "icmp" or service_type == "icmpv6":
        svc_type = service_type.upper() if service_type == "icmp" else "ICMPv6"
        for service in module.params.get("service_list"):
            service_list.append(dict(
                icmp_type=str(service["icmp_type"]),
                icmp_code=str(service["icmp_code"])
            ))
    
    return svc_type, service_list


def get_service(fw_obj, module, result):
    """Get Service from Sophos Firewall

    Args:
        fw_obj (SophosFirewall): SophosFirewall object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: Results of lookup
    """
    try:
        resp = fw_obj.get_service(name=module.params.get("name"))
    except SophosFirewallZeroRecords as error:
        return {"exists": False, "api_response": str(error)}
    except SophosFirewallAuthFailure as error:
        module.fail_json(msg="Authentication error: {0}".format(error), **result)
    except SophosFirewallAPIError as error:
        module.fail_json(msg="API Error: {0}".format(error), **result)
    except RequestException as error:
        module.fail_json(msg="Error communicating to API: {0}".format(error), **result)

    return {"exists": True, "api_response": resp}


def create_service(fw_obj, module, result):
    """Create an Service on Sophos Firewall

    Args:
        fw_obj (SophosFirewall): SophosFirewall object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: API response
    """

    svc_type, service_list = build_service_list(module)

    # module.fail_json(f"service_list: {service_list}")

    try:
        resp = fw_obj.create_service(
            name=module.params.get("name"),
            service_type=svc_type,
            service_list=service_list
        )
    except SophosFirewallAuthFailure as error:
        module.fail_json(msg="Authentication error: {0}".format(error), **result)
    except SophosFirewallAPIError as error:
        module.fail_json(msg="API Error: {0}".format(error), **result)
    except RequestException as error:
        module.fail_json(msg="Error communicating to API: {0}".format(error), **result)
    else:
        return resp


def remove_service(fw_obj, module, result):
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
            xml_tag="Services", name=module.params.get("name")
        )
    except SophosFirewallAuthFailure as error:
        module.fail_json(msg="Authentication error: {0}".format(error), **result)
    except SophosFirewallAPIError as error:
        module.fail_json(msg="API Error: {0}".format(error), **result)
    except RequestException as error:
        module.fail_json(msg="Error communicating to API: {0}".format(error), **result)
    else:
        return resp


def update_service(fw_obj, module, result):
    """Update an existing Service on Sophos Firewall

    Args:
        fw_obj (SophosFirewall): SophosFirewall object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: API response
    """
    svc_type, service_list = build_service_list(module)

    try:
        resp = fw_obj.update_service(
            name=module.params.get("name"),
            service_type=svc_type,
            service_list=service_list,
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
        "type": {"type": "str", "choices": ["tcporudp", "ip", "icmp", "icmpv6"]},
        "service_list": {"type": "list", "elements": "dict", "options": {
            "protocol": {
                "type": "str"
            },
            "src_port": {
                "type": "str",
                "default": "1:65535"
            },
            "dst_port": {
                "type": "str",
            },
            "icmp_type": {
                "type": "str"
            },
            "icmp_code": {
                "type": "str"
            }
        }},
        "action": {"type": "str", "choices": ["add", "remove", "replace"], "default": None},
        "state": {"required": True, "choices": ["present", "absent", "updated", "query"]},
    }
    required_if = [
        ('state', 'present', ('service_list',), True),
        ('state', 'updated', ('action',), True),
        ('state', 'created', ('type',), True),
        ('state', 'updated', ('type',), True)
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
    exist_check = get_service(fw, module, result)
    result["api_response"] = exist_check["api_response"]

    if state == "query":
        module.exit_json(**result)

    if module.check_mode:
        result["check_mode"] = True
        module.exit_json(**result)

    if state == "present" and not exist_check["exists"]:
        api_response = create_service(fw, module, result)
        if (
            api_response["Response"]["Services"]["Status"]["#text"]
            == "Configuration applied successfully."
        ):
            result["changed"] = True
            result["api_response"] = api_response

    elif state == "present" and exist_check["exists"]:
        result["changed"] = False

    elif state == "absent" and exist_check["exists"]:
        api_response = remove_service(fw, module, result)
        if (api_response["Response"]["Services"]["Status"]["#text"]
                == "Configuration applied successfully."):
            result["changed"] = True
        result["api_response"] = api_response

    elif state == "absent" and not exist_check["exists"]:
        result["changed"] = False

    elif state == "updated" and exist_check["exists"]:
        new_service_list = [dict(
            DestinationPort=service['dst_port'],
            Protocol=service['protocol'].upper(),
            SourcePort=service['src_port']
            ) for service in module.params.get("service_list")]
        if (sorted(ensure_list(exist_check["api_response"]["Response"]["Services"]["ServiceDetails"]["ServiceDetail"]), key=lambda d: sorted(d.items()))
                != sorted(new_service_list,key=lambda d: sorted(d.items()))):
            api_response = update_service(fw, module, result)
            if (api_response["Response"]["Services"]["Status"]["#text"]
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
