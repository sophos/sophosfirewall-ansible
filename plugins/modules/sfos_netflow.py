#!/usr/bin/python

# Copyright 2024 Sophos Ltd.  All rights reserved.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: sfos_netflow
short_description: Manage NetFlow server configurations on Sophos Firewall.
version_added: "1.3.0" # Version for this refactored module
description:
  - Allows adding, updating, removing, and querying NetFlow server configurations on a Sophos Firewall device.
  - Each NetFlow server is identified by a unique server_name.
  - Operations are performed by targeting individual server entries.
extends_documentation_fragment:
  - sophos.sophos_firewall.fragments.base
options:
  state:
    description:
      - C(present) - Add a new NetFlow server configuration. Fails if server_name already exists.
      - C(updated) - Modify an existing NetFlow server configuration. Fails if server_name does not exist.
      - C(absent) - Remove a NetFlow server configuration.
      - C(query) - Retrieve NetFlow server configuration(s).
    type: str
    required: true
    choices: [present, updated, absent, query]
  server_name:
    description:
      - Unique identifier for the NetFlow server configuration.
      - Required for all states except C(query) when fetching all servers.
    type: str
    required: false
  netflow_server:
    description:
      - IP address or hostname of the NetFlow collector.
      - Required for C(state=present) and C(state=updated).
    type: str
    required: false
  netflow_server_port:
    description:
      - UDP port number for the NetFlow collector.
      - Required for C(state=present) and C(state=updated).
    type: int
    required: false
author:
  - @mamullen13316
"""

EXAMPLES = r"""
- name: Add a new NetFlow server configuration 'collector1'
  sophos.sophos_firewall.sfos_netflow:
    state: present
    server_name: "collector1"
    netflow_server: "192.168.1.100"
    netflow_server_port: 2055

- name: Update NetFlow server 'collector1' to a new port
  sophos.sophos_firewall.sfos_netflow:
    state: updated
    server_name: "collector1"
    netflow_server: "192.168.1.100" # Current or new IP
    netflow_server_port: 2056      # New port

- name: Query all NetFlow server configurations
  sophos.sophos_firewall.sfos_netflow:
    state: query
  register: all_netflow_configs

- name: Remove NetFlow server 'collector1'
  sophos.sophos_firewall.sfos_netflow:
    state: absent
    server_name: "collector1"
"""

RETURN = r"""
api_response:
  description: The full API response from the Sophos Firewall for the last operation.
  type: dict
  returned: always
changed:
  description: Whether or not the resource was changed.
  type: bool
  returned: always
netflow_servers:
  description: A list of configured NetFlow servers. Returned when state is 'query'.
  type: list
  elements: dict
  returned: on query
  sample:
    - ServerName: "collector1"
      NetflowServer: "192.168.1.100"
      NetflowServerPort: "2055"
"""

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


def get_netflow_collector(connection, module, result):
    """Get Netflow configuration from Sophos Firewall.

    Args:
        connection (Connection): Ansible Connection object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: Results of lookup
    """
    template = """<Get> 
        <NetFlowConfiguration>
        </NetFlowConfiguration>
        </Get>"""
    try:
        resp = connection.invoke_sdk("submit_xml", module_args={"template_data": template,
                                                                "set_operation": "",
                                                                "debug": True})
    except Exception as error:
        module.fail_json("An unexpected error occurred: {0}".format(error), **result)

    if resp["success"] and not 'NetFlowConfiguration' in resp["response"]["Response"]:
        return {"exists": False, "api_response": resp["response"]}
    
    if resp["success"] and "NetFlowConfiguration" in resp["response"]["Response"]:
        if isinstance(resp["response"]["Response"]["NetFlowConfiguration"]["Server"]["ServerName"], str):
            if resp["response"]["Response"]["NetFlowConfiguration"]["Server"]["ServerName"] == module.params.get("server_name"):
                return {"exists": True, "api_response": resp["response"]}
        if isinstance(resp["response"]["Response"]["NetFlowConfiguration"]["Server"]["ServerName"], list):
            for server in resp["response"]["Response"]["NetFlowConfiguration"]["Server"]["ServerName"]:
                if server == module.params.get("server_name"):
                    return {"exists": True, "api_response": resp["response"]}
    if not resp["success"]:
        module.fail_json(msg="An error occurred: {0}".format(resp["response"]))

    return {"exists": False, "api_response": resp["response"]}

def create_netflow_collector(connection, exist_settings, module, result):
    """Create Netflow collector on Sophos Firewall.

    Args:
        connection (Connection): Ansible Connection object
        exist_settings (dict): API response containing existing Netflow collector settings
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: API response
    """
    # API for Netflow does not support adding to the list of already existing servers, so we need to make a list
    # of the existing plus the new one. 
    server_list = [{"ServerName": module.params.get("server_name"),
                    "NetflowServer": module.params.get("netflow_server"),
                    "NetflowServerPort": module.params.get("netflow_server_port")}]
    if "NetFlowConfiguration" in exist_settings["api_response"]["Response"]:
        if isinstance(exist_settings["api_response"]["Response"]["NetFlowConfiguration"]["Server"]["ServerName"], str):
            server_list.append(exist_settings["api_response"]["Response"]["NetFlowConfiguration"]["Server"])
        elif isinstance(exist_settings["api_response"]["Response"]["NetFlowConfiguration"]["Server"], list):
            for index, server in enumerate(exist_settings["api_response"]["Response"]["NetFlowConfiguration"]["Server"]["ServerName"]):
                server_list.append({
                "ServerName": server,
                "NetflowServer": exist_settings["api_response"]["Response"]["NetFlowConfiguration"]["Server"]["NetflowServer"][index],
                "NetflowServerPort": exist_settings["api_response"]["Response"]["NetFlowConfiguration"]["Server"]["NetflowServerPort"][index]})
        
    payload = """
  <NetFlowConfiguration>
    {% for server in server_list %}
    <Server>
      <ServerName>{{ server.ServerName }}</ServerName>
      <NetflowServer>{{ server.NetflowServer }}</NetflowServer>
      <NetflowServerPort>{{ server.NetflowServerPort }}</NetflowServerPort>
    </Server>
    {% endfor %}
  </NetFlowConfiguration>
    """
    template_vars = {
        "server_list": server_list
    }

    try:
        with contextlib.redirect_stdout(output_buffer):
            resp = connection.invoke_sdk("submit_xml", module_args={
                "template_data": payload,
                "template_vars": template_vars,
                "set_operation": "update",  # Netflow API doesn't support add, so we must use update
                "debug": True
                }
            )
    except Exception as error:
        module.fail_json("An unexpected error occurred: {0}".format(error), **result)

    if not resp["success"]:
        module.fail_json(msg="An error occurred: {0}".format(resp["response"]))

    return resp["response"]

def update_netflow_collector(connection, exist_settings, module, result):
    """Update Netflow collector configuration on Sophos Firewall.

    Args:
        connection (Connection): Ansible Connection object
        exist_settings (dict): API response containing existing Netflow collector settings
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: API response
    """
    server_list = []
    if "NetFlowConfiguration" in exist_settings["api_response"]["Response"]:
        if isinstance(exist_settings["api_response"]["Response"]["NetFlowConfiguration"]["Server"]["ServerName"], str):
            if exist_settings["api_response"]["Response"]["NetFlowConfiguration"]["Server"]["ServerName"] == module.params.get("server_name"):
                server_list.append({
                    "ServerName": exist_settings["api_response"]["Response"]["NetFlowConfiguration"]["Server"]["ServerName"],
                    "NetflowServer": module.params.get("netflow_server") if module.params.get("netflow_server") else exist_settings["api_response"]["Response"]["NetFlowConfiguration"]["Server"]["NetflowServer"],
                    "NetflowServerPort": module.params.get("netflow_server_port") if module.params.get("netflow_server_port") else exist_settings["api_response"]["Response"]["NetFlowConfiguration"]["Server"]["NetflowServerPort"]
                })
            else:
                server_list.append(exist_settings["api_response"]["Response"]["NetFlowConfiguration"]["Server"])
        elif isinstance(exist_settings["api_response"]["Response"]["NetFlowConfiguration"]["Server"]["ServerName"], list):
            for index, server in enumerate(exist_settings["api_response"]["Response"]["NetFlowConfiguration"]["Server"]["ServerName"]):
                if server == module.params.get("server_name"):
                    server_list.append({
                        "ServerName": server,
                        "NetflowServer": module.params.get("netflow_server") if module.params.get("netflow_server") else exist_settings["api_response"]["Response"]["NetFlowConfiguration"]["Server"]["NetflowServer"][index],
                        "NetflowServerPort": module.params.get("netflow_server_port") if module.params.get("netflow_server_port") else exist_settings["api_response"]["Response"]["NetFlowConfiguration"]["Server"]["NetflowServerPort"][index]
                    })
                    continue
                # If the server is not the one we are updating, we keep it as is    
                server_list.append({
                "ServerName": server,
                "NetflowServer": exist_settings["api_response"]["Response"]["NetFlowConfiguration"]["Server"]["NetflowServer"][index],
                "NetflowServerPort": exist_settings["api_response"]["Response"]["NetFlowConfiguration"]["Server"]["NetflowServerPort"][index]})
        
    payload = """
  <NetFlowConfiguration>
    {% for server in server_list %}
    <Server>
      <ServerName>{{ server.ServerName }}</ServerName>
      <NetflowServer>{{ server.NetflowServer }}</NetflowServer>
      <NetflowServerPort>{{ server.NetflowServerPort }}</NetflowServerPort>
    </Server>
    {% endfor %}
  </NetFlowConfiguration>
    """

    template_vars = {
        "server_list": server_list
    }

    try:
        with contextlib.redirect_stdout(output_buffer):
            resp = connection.invoke_sdk("submit_xml", module_args={
                "template_data": payload,
                "template_vars": template_vars,
                "set_operation": "update",  # Netflow API doesn't support add, so we must use update
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
    exist_settings = exist_settings["api_response"]["Response"]["NetFlowConfiguration"]["Server"]

    if isinstance(exist_settings["ServerName"], str):
        if exist_settings["ServerName"] == module.params.get("server_name"):
            if (module.params.get("netflow_server") and not module.params.get("netflow_server") == exist_settings["NetflowServer"]):
                return True
            if (module.params.get("netflow_server_port") and not str(module.params.get("netflow_server_port")) == exist_settings["NetflowServerPort"]):
                return True
    elif isinstance(exist_settings["ServerName"], list):
        for index, server in enumerate(exist_settings["ServerName"]):
            if server == module.params.get("server_name"):
                if (module.params.get("netflow_server") and not module.params.get("netflow_server") == exist_settings["NetflowServer"][index]):
                    return True
                if (module.params.get("netflow_server_port") and not str(module.params.get("netflow_server_port")) == exist_settings["NetflowServerPort"][index]):
                    return True

    return False

def remove_netflow_collector(connection, exist_settings, module, result):
    """Remove an Netflow collector from Sophos Firewall.

    Args:
        connection (Connection): Ansible Connection object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: API response
    """
    server_list = []
    if isinstance(exist_settings["api_response"]["Response"]["NetFlowConfiguration"]["Server"]["ServerName"], str):
        if exist_settings["api_response"]["Response"]["NetFlowConfiguration"]["Server"]["ServerName"] == module.params.get("server_name"):
            payload = """<NetFlowConfiguration></NetFlowConfiguration>"""
    elif isinstance(exist_settings["api_response"]["Response"]["NetFlowConfiguration"]["Server"]["ServerName"], list):
        for index, server in enumerate(exist_settings["api_response"]["Response"]["NetFlowConfiguration"]["Server"]["ServerName"]):
            if server == module.params.get("server_name"):
                continue
            server_list.append({
                "ServerName": exist_settings["api_response"]["Response"]["NetFlowConfiguration"]["Server"]["ServerName"][index],
                "NetflowServer": exist_settings["api_response"]["Response"]["NetFlowConfiguration"]["Server"]["NetflowServer"][index],
                "NetflowServerPort": exist_settings["api_response"]["Response"]["NetFlowConfiguration"]["Server"]["NetflowServerPort"][index]
            })

        payload = """
            <NetFlowConfiguration>
                {% for server in server_list %}
                <Server>
                <ServerName>{{ server.ServerName }}</ServerName>
                <NetflowServer>{{ server.NetflowServer }}</NetflowServer>
                <NetflowServerPort>{{ server.NetflowServerPort }}</NetflowServerPort>
                </Server>
                {% endfor %}
            </NetFlowConfiguration>
            """
    template_vars = {
        "server_list": server_list
    }

    try:
        with contextlib.redirect_stdout(output_buffer):
            resp = connection.invoke_sdk("submit_xml", module_args={
                "template_data": payload,
                "template_vars": template_vars,
                "set_operation": "update",  # Netflow API doesn't support add, so we must use update
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
        "server_name": {"type": "str", "required": False},
        "netflow_server": {"type": "str", "required": False, "default": None},
        "netflow_server_port": {"type": "int", "required": False},
        "state": {"type": "str", "required": True, "choices": ["present", "updated", "query", "absent"]},
    }

    required_if = [
        (
            "state",
            "present",
            [
                "server_name",
                "netflow_server",
                "netflow_server_port",
            ],
            False,
        ),
        (
            "state",
            "updated",
            [
                "server_name"
            ],
            False,
        )
    ]

    module = AnsibleModule(
        argument_spec=argument_spec, required_if=required_if, supports_check_mode=True
    )

    if not PREREQ_MET["result"]:
        module.fail_json(msg=missing_required_lib(PREREQ_MET["missing_module"]))

    result = {"changed": False, "check_mode": False}

    state = module.params.get("state")

    try:
        connection = Connection(module._socket_path)
    except AssertionError as e:
        module.fail_json(msg="Connection error: Ensure you are targeting a remote host and not using 'delegate_to: localhost'.")

    if not hasattr(connection, "httpapi"):
        module.fail_json(msg="HTTPAPI plugin is not initialized. Ensure the connection is set to 'httpapi'.")

    exist_settings = get_netflow_collector(connection, module, result)
    result["api_response"] = exist_settings["api_response"]

    if state == "query":
        module.exit_json(**result)

    if module.check_mode:
        result["check_mode"] = True
        module.exit_json(**result)

    if state == "present" and not exist_settings["exists"]:
        api_response = create_netflow_collector(connection, exist_settings, module, result)
        if (
            "Configuration applied successfully." in api_response["Response"]["NetFlowConfiguration"]["Status"]["#text"]
        ):
            result["changed"] = True
            result["api_response"] = api_response

    elif state == "present" and exist_settings["exists"]:
        result["changed"] = False

    elif state == "absent" and exist_settings["exists"]:
        api_response = remove_netflow_collector(connection, exist_settings, module, result)
        if (
            "Configuration applied successfully" in api_response["Response"]["NetFlowConfiguration"]["Status"]["#text"]
        ):
            result["changed"] = True
        result["api_response"] = api_response

    elif state == "absent" and not exist_settings["exists"]:
        result["changed"] = False

    elif state == "updated" and exist_settings["exists"]:
        if eval_changed(module, exist_settings):
            api_response = update_netflow_collector(connection, exist_settings, module, result)

            if api_response:
                result["api_response"] = api_response
                if (
                    "Configuration applied successfully" in api_response["Response"]["NetFlowConfiguration"]["Status"]["#text"]
                ):
                    result["changed"] = True
    
    elif state == "updated" and not exist_settings["exists"]:
        result["changed"] = False
        module.fail_json(exist_settings["api_response"], **result)

    module.exit_json(**result)


if __name__ == "__main__":
    main()