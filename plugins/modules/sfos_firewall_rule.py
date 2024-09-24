#!/usr/bin/python

# Copyright 2024 Sophos Ltd.  All rights reserved.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r'''
---
module: sfos_firewall_rule

short_description: Manage Firewall Rules on Sophos Firewall

version_added: "1.0.0"

description: Creates, updates or removes firewall rules on Sophos Firewall

extends_documentation_fragment:
  - sophos.sophos_firewall.fragments.base

options:
    name:
        description: Name of the firewall rule to create, update, or delete
        required: true
        type: str
    status:
        description: Enabled or Disabled state of the rule
        choices: ["enable", "disable"]
        type: str
        required: false
    position:
        description: Indicates where the rule should be inserted.
        choices: ["top", "bottom", "after", "before"]
        type: str
        required: false
        default: bottom
    after_rulename:
        description:
            - Name of the rule to insert this rule after.
        required: false
        type: str
    before_rulename:
        description:
            - Name of the rule to insert this rule before.
        required: false
        type: str
    action:
        description:
            - The rule action.
        choices: ["accept", "drop", "reject"]
        required: true
        type: str
    log:
        description:
            - Enable or disable logging.
        choices: ["enable", "disable"]
        required: true
        type: str
    description:
        description:
            - Rule description.
        required: true
        type: str
    src_zones:
        description:
            - Source zone(s).
        required: true
        type: list
        elements: str
    dst_zones:
        description:
            - Destination zone(s).
        required: true
        type: list
        elements: str
    src_networks:
        description:
            - Source network(s). 
        required: true
        type: list
        elements: str
    dst_networks:
        description:
            - Destination network(s).
        type: list
        elements: str
    services:
        description:
            - Name of service(s).
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
- name: Create Firewall Rule
  sophos.sophos_firewall.sfos_firewall_rule:
    username: "{{ username }}"
    password: "{{ password }}"
    hostname: myfirewallhostname.sophos.net
    port: 4444
    verify: false
    name: TEST RULE 100
    after_rulename: TEST RULE 99
    action: accept
    description: Test rule created by Ansible
    log: enable
    status: enable
    position: bottom
    src_zones:
      - LAN
    dst_zones:
      - WAN
    src_networks:
      - SRCNET1
      - SRCNET2
    dst_networks:
      - DSTNET1
      - DSTNET2
    services:
      - HTTPS
      - SSH
    state: present
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


def get_firewallrule(fw_obj, module, result):
    """Get firewall rule from Sophos Firewall

    Args:
        fw_obj (SophosFirewall): SophosFirewall object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: Results of lookup
    """
    try:
        resp = fw_obj.get_rule(name=module.params.get("name"))
    except SophosFirewallZeroRecords as error:
        return {"exists": False, "api_response": str(error)}
    except SophosFirewallAuthFailure as error:
        module.fail_json(msg="Authentication error: {0}".format(error), **result)
    except SophosFirewallAPIError as error:
        module.fail_json(msg="API Error: {0}".format(error), **result)
    except RequestException as error:
        module.fail_json(msg="Error communicating to API: {0}".format(error), **result)

    return {"exists": True, "api_response": resp}

def create_firewallrule(fw_obj, module, result):
    """Create a firewall rule on Sophos Firewall.

    Args:
        fw_obj (SophosFirewall): SophosFirewall object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: API response
    """
    rule_params = {
        "rulename": module.params.get("name"),
        "status": module.params.get("status").capitalize() if module.params.get("status") else None,
        "position": module.params.get("position").capitalize() if module.params.get("position") else None,
        "after_rulename": module.params.get("after_rulename"),
        "before_rulename": module.params.get("before_rulename"),
        "action": module.params.get("action").capitalize() if module.params.get("action") else None,
        "log": module.params.get("log").capitalize() if module.params.get("log") else None,
        "description": module.params.get("description"),
        "src_zones": module.params.get("src_zones"),
        "dst_zones": module.params.get("dst_zones"),
        "src_networks": module.params.get("src_networks"),
        "dst_networks": module.params.get("dst_networks"),
        "service_list": module.params.get("service_list")
    }

    try:
        resp = fw_obj.create_rule(rule_params=rule_params)
    except SophosFirewallAuthFailure as error:
        module.fail_json(msg="Authentication error: {0}".format(error), **result)
    except SophosFirewallAPIError as error:
        module.fail_json(msg="API Error: {0}".format(error), **result)
    except RequestException as error:
        module.fail_json(msg="Error communicating to API: {0}".format(error), **result)
    else:
        return resp

def remove_firewallrule(fw_obj, module, result):
    """Remove a firewall rule from Sophos Firewall.

    Args:
        fw_obj (SophosFirewall): SophosFirewall object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: API response
    """
    try:
        resp = fw_obj.remove(
            xml_tag="FirewallRule", name=module.params.get("name")
        )
    except SophosFirewallAuthFailure as error:
        module.fail_json(msg="Authentication error: {0}".format(error), **result)
    except SophosFirewallAPIError as error:
        module.fail_json(msg="API Error: {0}".format(error), **result)
    except RequestException as error:
        module.fail_json(msg="Error communicating to API: {0}".format(error), **result)
    else:
        return resp


def update_firewallrule(fw_obj, module, result):
    """Update an existing firewall rule on Sophos Firewall

    Args:
        fw_obj (SophosFirewall): SophosFirewall object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: API response
    """
    rule_params = {
        "rulename": module.params.get("name"),
        "status": module.params.get("status").capitalize() if module.params.get("status") else None,
        "position": module.params.get("position"),
        "after_rulename": module.params.get("after_rulename"),
        "before_rulename": module.params.get("before_rulename"),
        "action": module.params.get("action").capitalize() if module.params.get("action") else None,
        "log": module.params.get("log").capitalize() if module.params.get("log") else None,
        "description": module.params.get("description"),
        "src_zones": module.params.get("src_zones"),
        "dst_zones": module.params.get("dst_zones"),
        "src_networks": module.params.get("src_networks"),
        "dst_networks": module.params.get("dst_networks"),
        "service_list": module.params.get("service_list")
    }
    try:
        resp = fw_obj.update_rule(
            name=module.params.get("name"),
            rule_params=rule_params
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
        "status": {"choices": ["enable", "disable"]},
        "position": {"choices": ["top", "bottom", "after", "before"], "default": "bottom"},
        "after_rulename": {"type": "str"},
        "before_rulename": {"type": "str"},
        "action": {"choices": ["accept", "drop", "reject"]},
        "description": {"type": "str"},
        "log": {"choices": ["enable","disable"]},
        "src_zones": {"type": "list", "elements": "str"},
        "dst_zones": {"type": "list", "elements": "str"},
        "src_networks": {"type": "list", "elements": "str"},
        "dst_networks": {"type": "list", "elements": "str"},
        "service_list": {"type": "list", "elements": "str"},
        "state": {"required": True, "choices": ["present", "absent", "updated", "query"]},
    }

    required_if = [
        ('position', 'after', ('after_rulename',), True),
        ('position', 'before', ('before_rulename',), True)
    ]

    # required_together = [
    #     ["start_ip", "end_ip"],
    #     ["network", "mask"]
    # ]

    module = AnsibleModule(argument_spec=argument_spec,
                            required_if=required_if,
                        #    required_together=required_together,
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

    exist_check = get_firewallrule(fw, module, result)
    result["api_response"] = exist_check["api_response"]

    if state == "query":
        module.exit_json(**result)

    if module.check_mode:
        result["check_mode"] = True
        module.exit_json(**result)

    if state == "present" and not exist_check["exists"]:
        api_response = create_firewallrule(fw, module, result)
        if (
            api_response["Response"]["FirewallRule"]["Status"]["#text"]
            == "Configuration applied successfully."
        ):
            result["changed"] = True
            result["api_response"] = api_response

    elif state == "present" and exist_check["exists"]:
        result["changed"] = False

    elif state == "absent" and exist_check["exists"]:
        api_response = remove_firewallrule(fw, module, result)
        if (api_response["Response"]["FirewallRule"]["Status"]["#text"]
                == "Configuration applied successfully."):
            result["changed"] = True
        result["api_response"] = api_response

    elif state == "absent" and not exist_check["exists"]:
        result["changed"] = False

    elif state == "updated" and exist_check["exists"]:
        api_response = update_firewallrule(fw, module, result)

        if api_response:
            if (api_response["Response"]["FirewallRule"]["Status"]["#text"]
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
