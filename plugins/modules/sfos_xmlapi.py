#!/usr/bin/python

# Copyright 2024 Sophos Ltd.  All rights reserved.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: sfos_service

short_description: Use the XML API to get, create, update, or delete settings on Sophos Firewall. 

version_added: "1.0.0"

description: Creates, updates or removes objects on Sophos Firewall using XML tags and/or payloads.

extends_documentation_fragment:
  - sophos.sophos_firewall.fragments.base

options:
    name:
        description: Name of an object to retrieve when using query option, or to delete when using absent.
        type: str
        required: true
    xml_tag:
        description:
            - The XML tag for the lookup when using the query option, or the top-level tag when creating/updating.
        type: str
        required: true
    key:
        description:
            - Optional search key when using the query option.
        type: str
    value:
        description:
            - Optional search value when using the query option.
        type: str
    operator:
        description:
            - Optional search operator when using the query option.
        type: str
        choices: ['=', '!=', 'like']
    data:
        description:
            - XML payload data for use with the present (add) or updated (update) state.
        type: str
    state:
        description:
            - Use C(query) to retrieve, C(present) to create, C(absent) to remove, or C(updated) to modify
        choices: [present, absent, updated, query]
        type: str
        required: true

author:
    - Matt Mullen (@mamullen13316)
"""

EXAMPLES = r"""
- name: CREATE MAC HOST
  sophos.sophos_firewall.sfos_xmlapi:
    username: "{{ username }}"
    password: "{{ password }}"
    hostname: "{{ inventory_hostname }}"
    port: 4444
    verify: false
    xml_tag: MACHost
    data: |
            <MACHost>
                <Name>TESTMACHOST1</Name>
                <Description>Created by Ansible xmlapi module</Description>
                <Type>MACAddress</Type>
                <MACAddress>00:16:76:49:33:FF</MACAddress>
            </MACHost>
    state: present
  delegate_to: localhost

- name: UPDATE MAC HOST
  sophos.sophos_firewall.sfos_xmlapi:
    username: "{{ username }}"
    password: "{{ password }}"
    hostname: "{{ inventory_hostname }}"
    port: 4444
    verify: false
    xml_tag: MACHost
    data: |
            <MACHost>
                <Name>TESTMACHOST1</Name>
                <Description>UPDATED by Ansible xmlapi module</Description>
                <Type>MACAddress</Type>
                <MACAddress>00:16:76:49:01:01</MACAddress>
            </MACHost>
    state: updated
  delegate_to: localhost

- name: GET MAC HOST
  sophos.sophos_firewall.sfos_xmlapi:
    username: "{{ username }}"
    password: "{{ password }}"
    hostname: "{{ inventory_hostname }}"
    port: 4444
    verify: false
    xml_tag: MACHost
    name: TESTMACHOST1
    state: query
  delegate_to: localhost

- name: REMOVE MAC HOST
  sophos.sophos_firewall.sfos_xmlapi:
    username: "{{ username }}"
    password: "{{ password }}"
    hostname: "{{ inventory_hostname }}"
    port: 4444
    verify: false
    name: TESTMACHOST1
    xml_tag: MACHost
    state: absent
  delegate_to: localhost
"""

RETURN = r"""
api_response:
    description: Serialized object containing the API response.
    type: dict
    returned: always

"""

try:
    from sophosfirewall_python.firewallapi import (
        SophosFirewall,
        SophosFirewallZeroRecords,
        SophosFirewallAuthFailure,
        SophosFirewallAPIError,
    )
    from requests.exceptions import RequestException
    from xmltodict import parse

    PREREQ_MET = {"result": True}
except ImportError as errMsg:
    PREREQ_MET = {"result": False, "missing_module": errMsg.name}

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.basic import missing_required_lib


def query(fw_obj, module, result):
    """Retrieve data from Sophos Firewall using XML tag.

    Args:
        fw_obj (SophosFirewall): SophosFirewall object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: Results of lookup
    """
    name = module.params.get("name")
    xml_tag = module.params.get("xml_tag")
    key = module.params.get("key")
    value = module.params.get("value")
    data = module.params.get("data")
    state = module.params.get("state")

    if state == "present" or state == "updated":
        if data:
            xml_data = parse(data)
            if "Name" in xml_data[xml_tag]:
                name = xml_data[xml_tag]["Name"]

    try:
        if name:
            resp = fw_obj.get_tag_with_filter(xml_tag=xml_tag, key="Name", value=name)
        if key and not name:
            resp = fw_obj.get_tag_with_filter(xml_tag=xml_tag, key=key, value=value)
        if not key and not name:
            resp = fw_obj.get_tag(xml_tag=xml_tag)
    except SophosFirewallZeroRecords as error:
        return {"exists": False, "api_response": str(error)}
    except SophosFirewallAuthFailure as error:
        module.fail_json(msg="Authentication error: {0}".format(error), **result)
    except SophosFirewallAPIError as error:
        module.fail_json(msg="API Error: {0}".format(error), **result)
    except RequestException as error:
        module.fail_json(msg="Error communicating to API: {0}".format(error), **result)

    return {"exists": True, "api_response": resp}


def create(fw_obj, module, result):
    """Perform API add operation on Sophos Firewall.

    Args:
        fw_obj (SophosFirewall): SophosFirewall object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: API response
    """

    try:
        resp = fw_obj.submit_xml(template_data=module.params.get("data"))
    except SophosFirewallAuthFailure as error:
        module.fail_json(msg="Authentication error: {0}".format(error), **result)
    except SophosFirewallAPIError as error:
        module.fail_json(msg="API Error: {0}".format(error), **result)
    except RequestException as error:
        module.fail_json(msg="Error communicating to API: {0}".format(error), **result)
    else:
        return resp


def remove(fw_obj, module, result):
    """Remove an object from Sophos Firewall

    Args:
        fw_obj (SophosFirewall): SophosFirewall object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: API response
    """
    try:
        resp = fw_obj.remove(
            xml_tag=module.params.get("xml_tag"), name=module.params.get("name")
        )
    except SophosFirewallAuthFailure as error:
        module.fail_json(msg="Authentication error: {0}".format(error), **result)
    except SophosFirewallAPIError as error:
        module.fail_json(msg="API Error: {0}".format(error), **result)
    except RequestException as error:
        module.fail_json(msg="Error communicating to API: {0}".format(error), **result)
    else:
        return resp


def update(fw_obj, module, result):
    """Perform API update operation on Sophos Firewall.

    Args:
        fw_obj (SophosFirewall): SophosFirewall object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: API response
    """

    try:
        resp = fw_obj.submit_xml(
            template_data=module.params.get("data"), set_operation="update"
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
        "name": {"type": "str"},
        "xml_tag": {"type": "str", "required": True},
        "key": {"type": "str"},
        "value": {"type": "str"},
        "operator": {"type": "str", "choices": ["=", "!=", "like"], "default": "="},
        "data": {"type": "str"},
        "state": {
            "required": True,
            "choices": ["present", "absent", "updated", "query"],
        },
    }
    required_if = [
        ("state", "present", ("data", "xml_tag"), True),
        ("state", "updated", ("data", "xml_tag"), True),
        ("state", "query", ("xml_tag",), True),
    ]

    module = AnsibleModule(
        argument_spec=argument_spec, required_if=required_if, supports_check_mode=True
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

    result = {"changed": False, "check_mode": False}

    state = module.params.get("state")
    exist_check = query(fw, module, result)
    result["api_response"] = exist_check["api_response"]

    if state == "query":
        module.exit_json(**result)

    if module.check_mode:
        result["check_mode"] = True
        module.exit_json(**result)

    if state == "present" and not exist_check["exists"]:
        api_response = create(fw, module, result)
        if (
            api_response["Response"][module.params.get("xml_tag")]["Status"]["#text"]
            == "Configuration applied successfully."
        ):
            result["changed"] = True
            result["api_response"] = api_response

    elif state == "present" and exist_check["exists"]:
        result["changed"] = False

    elif state == "absent" and exist_check["exists"]:
        api_response = remove(fw, module, result)
        if (
            api_response["Response"][module.params.get("xml_tag")]["Status"]["#text"]
            == "Configuration applied successfully."
        ):
            result["changed"] = True
        result["api_response"] = api_response

    elif state == "absent" and not exist_check["exists"]:
        result["changed"] = False

    elif state == "updated" and exist_check["exists"]:
        xml_tag = module.params.get("xml_tag")
        xml_data = parse(module.params.get("data"))
        exist_check["api_response"]["Response"][xml_tag].pop("@transactionid")

        # module.exit_json(msg=f"xml_data: {xml_data}, exist_check: {exist_check['api_response']['Response']}")

        if exist_check["api_response"]["Response"][xml_tag] != xml_data[xml_tag]:
            api_response = update(fw, module, result)
            if (
                api_response["Response"][xml_tag]["Status"]["#text"]
                == "Configuration applied successfully."
            ):
                result["changed"] = True
                result["api_response"] = api_response
            else:
                result["changed"] = False
        else:
            result["changed"] = False

    elif state == "updated" and not exist_check["exists"]:
        result["changed"] = False
        module.fail_json(exist_check["api_response"], **result)

    module.exit_json(**result)


if __name__ == "__main__":
    main()
