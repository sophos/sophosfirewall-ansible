#!/usr/bin/python

# Copyright 2024 Sophos Ltd.  All rights reserved.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: sfos_ipsec_connection

short_description: Manage IPSec Connection (Configure > Site-to-site VPN > IPSec)

version_added: "1.5.0"

description: Manage IPSec Connection (Configure > Site-to-site VPN > IPSec) on Sophos Firewall

extends_documentation_fragment:
  - sophos.sophos_firewall.fragments.base

options:
    name:
        description: VPN Connection name
        type: str
        required: true
    description:
        description: VPN Connection description
        type: str
        required: false
    ip_version:
        description: IP address family of local and remote subnets 
        type: str
        choices: ["IPv4", "IPv6"]
        default: IPv4
        required: false
    connection_type:
        description: Type of VPN connection
        type: str
        choices: ["RemoteAccess", "SiteToSite", "HostToHost", "TunnelInterface"]
        required: false
    gateway_type:
        description: Action to be taken when VPN Services restarts
        type: str
        choices: ["Disable", "RespondOnly", "Initiate"]
        default: RespondOnly
        required: false
    profile:
        description: IPSec Profile to be used for connection
        type: str
        choices: ["Default Profile", "Microsof Azure (IKEv2)", "IKEv2", "DefaultRemoteAccess", "DefaultL2TP", "DefaultHeadOffice", "DefaultBranchOffice", "Branch Office (IKEv2)", "Head office (IKEv2)"]
        required: false
    authentication_type:
        description: Authentication type based on the Connection type
        type: str
        choices: ["PresharedKey", "DigitalCertificate", "RSAKey"]
        required: false
    preshared_key:
        description: Preshared key
        type: str
        required: false
    local_certificate:
        description: Name of local certificate to be used when C(authentication_type)=DigitalCertificate
        type: str
        required: false
    remote_certificate:
        description: Name of remote certificate to be used when C(authentication_type)=DigitalCertificate
        type: str
        required: false
    remote_rsa_key:
        description: RSA key of remote peer
        type: str
        required: false
    listening_interface:
        description: A WAN interface on the local firewall
        type: str
        required: false
    gateway_address:
        description: Remote host
        type: str
        required: false
    local_subnet:
        description: Local subnet
        type: list
        elements: str
        required: false
    nat_lan:
        description: Host for NAT (Hide) mode
        type: str
        required: false
    local_id_type:
        description: Local ID type
        type: str
        choices: ["DNS", "IP Address", "Email", "DER ASN1 DN (X.509)"]
        required: false
    local_id:
        description: Local ID
        type: str
        required: false
    allow_nat_traversal:
        description: Enable or Disable NAT traversal
        type: str
        choices: ["Enable", "Disable"]
        required: false
    remote_subnet:
        description: Remote network for RemoteAccess or HostToHost connection type
        type: list
        elements: str
        required: false
    remote_id_type:
        description: Remote ID type to be used with RemoteAccess or HostToHost connection type
        type: str
        choices: ["DNS", "IP Address", "Email", "DER ASN1 DN (X.509)"]
        required: false
    remote_id:
        description: Remote ID to be used with RemoteAccess or HostToHost connection type
        type: str
        required: false
    user_authentication_mode:
        description: User authentication mode for RemoteAccess or HostToHost connection type
        type: str
        choices: ["Disable", "AsServer", "AsClient"]
        required: false
    as_client_username:
        description: Username for user authentication in AsClient authentication mode
        type: str
        required: false
    as_client_password:
        description: Password for user authentication in AsClient authentication mode
        type: str
        required: false
    as_server_user:
        description: User for user authentication in AsServer authentication mode
        type: str
        required: false
    protocol:
        description: Protocol
        type: str
        choices: ["ALL", "UDP", "TCP", "ICMP"]
        required: false
    local_port:
        description: Local port
        type: str
        required: false
    remote_port:
        description: Remote port
        type: str
        required: false
    disconnect_on_idle_interval:
        description: Disconnect on idle interval in seconds
        type: str
        required: false
    active:
        description: Activate the connection (only available after creation)
        type: bool
        required: false
    connection:
        description: Establish a connection (only available after creation)
        type: bool
        required: false
    state:
        description:
            - Use C(query) to retrieve or C(updated) to modify
        choices: [present, updated, query]
        type: str
        required: true

author:
    - Matt Mullen (@mamullen13316)
"""

EXAMPLES = r"""
- name: Create IPSec Connection Site-to-Site
  sophos.sophos_firewall.sfos_ipsec_connection:
    name: Test_IPSec_Connection_S2S
    description: Testing IPSec Connection from Ansible
    connection_type: SiteToSite
    gateway_type: RespondOnly
    profile: IKEv2 
    authentication_type: PresharedKey
    preshared_key: testkey1234567890!
    listening_interface: PortB
    gateway_address: 10.100.100.10
    local_id_type: DNS
    local_id: portB.example.vpn.sophos.com
    local_subnet: 
        - TESTVPNSUB1
    remote_subnet: 
        - TESTVPNSUB2
    state: present

- name: Create IPSec Connection with Tunnel Interface
  sophos.sophos_firewall.sfos_ipsec_connection:
    name: Test_IPSec_Connection_Tunnel
    description: Testing IPSec Connection from Ansible
    connection_type: TunnelInterface
    gateway_type: RespondOnly
    profile: DefaultBranchOffice 
    authentication_type: RSAKey
    remote_rsa_key: testkey
    listening_interface: PortB
    gateway_address: 10.10.10.1
    local_id_type: DNS
    local_id: portB.example.vpn.sophos.com
    remote_id_type: IP Address
    remote_id: 2.2.2.2
    state: present 
  tags: tunnel

- name: Query IPSec Connection
  sophos.sophos_firewall.sfos_ipsec_connection:
    name: Test IPSec Connection
    state: query

- name: Activate IPSec Connection
  sophos.sophos_firewall.sfos_ipsec_connection:
    enabled: true
    name: Test IPSec Connection
    active: true
    state: updated

- name: Remove IPSec Connection
  sophos.sophos_firewall.sfos_ipsec_connection:
    enabled: true
    name: snmpv3user
    state: absent
"""

RETURN = r"""
api_response:
    description: Serialized object containing the API response.
    type: dict
    returned: always

"""
import io
import contextlib
import ast

output_buffer = io.StringIO()

try:
    from sophosfirewall_python.firewallapi import (
        SophosFirewall,
        SophosFirewallZeroRecords,
        SophosFirewallAuthFailure,
        SophosFirewallAPIError,
    )
    from requests.exceptions import RequestException
    from xmltodict import unparse

    PREREQ_MET = {"result": True}
except ImportError as errMsg:
    PREREQ_MET = {"result": False, "missing_module": errMsg.name}


from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.basic import missing_required_lib
from ansible.module_utils.connection import Connection


def get_with_default(d, key, default):
    value = d.get(key)
    return default if value is None else value


def get_ipsec_connection(connection, module, result):
    """Get IPSec Connection from Sophos Firewall

    Args:
        connection (Connection): Ansible Connection object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: Results of lookup
    """
    payload = """
    <Get>
        <VPNIPSecConnection>
           <Configuration>
           <Filter>
                <key name="Name" 
                criteria="=">{{ name }}</key>
            </Filter>
          </Configuration>
        </VPNIPSecConnection>
    </Get>
"""
    try:
        resp = connection.invoke_sdk("submit_xml", module_args={
            "template_data": payload,
            "set_operation":None,
            "template_vars": {"name": module.params.get("name")},
            }
        )

    except Exception as error:
        module.fail_json("An unexpected error occurred: {0}".format(error), **result)

    if resp["success"] and not resp["exists"]:
        return {"exists": False, "api_response": resp["response"]}
    

    if not resp["success"]:
        module.fail_json(msg="An error occurred: {0}".format(resp["response"]))

    if (
        resp["response"]["Response"]["VPNIPSecConnection"]["Configuration"]["Status"]
        == "No. of records Zero."
    ):
        return {"exists": False, "api_response": resp["response"]}

    return {"exists": True, "api_response": resp["response"]}


def create_ipsec_connection(connection, module, result):
    """Create an IPSec VPN Connection on Sophos Firewall

    Args:
        connection (Connection): Ansible Connection object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: API response
    """
    payload = """
    <VPNIPSecConnection>
		<Configuration>
			<Name>{{ name }}</Name>
			<Description>{{ description }}</Description>
			<ConnectionType>{{ connection_type }}</ConnectionType>
			<Policy>{{ profile }}</Policy>
			<ActionOnVPNRestart>{{ gateway_type }}</ActionOnVPNRestart>
			<AuthenticationType>{{ authentication_type }}</AuthenticationType>
			{% if authentication_type == 'PresharedKey' %}
			<PresharedKey>{{ preshared_key }}</PresharedKey>
            {% elif authentication_type == 'DigitalCertificate' %}
			<LocalCertificate>{{ local_certificate }}</LocalCertificate>
			<RemoteCertificate>{{ remote_certificate }}</RemoteCertificate>
            {% elif authentication_type == 'RSAKey' %}
			<RemoteRSAKey>{{ remote_rsa_key }}</RemoteRSAKey>
            {% endif %}
			<SubnetFamily>{{ ip_version }}</SubnetFamily>
			<EndpointFamily>{{ ip_version }}</EndpointFamily>
			<LocalWANPort>{{ listening_interface }}</LocalWANPort>
			<AliasLocalWANPort>{{ listening_interface }}</AliasLocalWANPort>
			<RemoteHost>{{ gateway_address }}</RemoteHost>
            {% if local_subnet %}
            {% for subnet in local_subnet %}
			<LocalSubnet>{{ subnet }}</LocalSubnet>
            {% endfor %}
            {% elif connection_type == 'TunnelInterface' %}
            <LocalSubnet>Any</LocalSubnet>
            {% endif %}
			<NATedLAN>{{ nat_lan }}</NATedLAN>
            {% if local_id_type %}
			<LocalIDType>{{ local_id_type }}</LocalIDType>
			<LocalID>{{ local_id }}</LocalID>
            {% else %}
            <LocalIDType/>
            <LocalID/>
            {% endif %}
            {% if allow_nat_traversal %}
			<AllowNATTraversal>{{ allow_nat_traversal }}</AllowNATTraversal>
            {% else %}
            <AllowNATTraversal/>
            {% endif %}
            {% if remote_subnet %}
			<RemoteNetwork>
                {% for subnet in remote_subnet %}
				<Network>{{ subnet }}</Network>
                {% endfor %}
			</RemoteNetwork>
            {% endif %}
            {% if connection_type == 'TunnelInterface' %}
            <RemoteNetwork>
              <Network>Any</Network>
            </RemoteNetwork>
            {% endif %}
            {% if remote_id_type %}
			<RemoteIDType>{{ remote_id_type }}</RemoteIDType>
			<RemoteID>{{ remote_id }}</RemoteID>
            {% else %}
            <RemoteIDType/>
            <RemoteID/>
            {% endif %}
            {% if user_authentication_mode %}
			<UserAuthenticationMode>{{ user_authentication_mode }}</UserAuthenticationMode>
			{% if user_authentication_mode == 'AsClient' %}
			<Username>{{ as_client_username }}</Username>
			<Password>{{ as_client_password }}</Password>
            {% endif %}
			{% if user_authentication_mode == 'AsServer' %}
			<AllowedUser>
				<User>{{ as_server_username }}</User>
			</AllowedUser>
            {% endif %}
            {% else %}
            <UserAuthenticationMode>Disable</UserAuthenticationMode>
            {% endif %}
            {% if protocol %}
			<Protocol>{{ protocol }}</Protocol>
            {% endif %}
			<LocalPort>{{ local_port }}</LocalPort>
			<RemotePort>{{ remote_port }}</RemotePort>
            {% if disconnect_on_idle_interval %}
			<DisconnectOnIdleInterval>{{ disconnect_on_idle_interval }}</DisconnectOnIdleInterval>
            {% endif %}
		</Configuration>
    </VPNIPSecConnection>
    """
    try:
        with contextlib.redirect_stdout(output_buffer):
            resp = connection.invoke_sdk("submit_xml", module_args={
                "template_data": payload, 
                "template_vars": module.params,
                "debug": True
                }
            )
    except Exception as error:
        module.fail_json("An unexpected error occurred: {0}".format(error), **result)
    
    if not resp["success"]:
        output = output_buffer.getvalue() if module._verbosity >= 2 else ""
        if "Entity having same parameter details" in resp["response"]:
            module.fail_json(
                msg=f"ERROR: {resp['response']},  INFO: Possible causes: 1. Gateway address already in use on another VPN connection 2. One or more specified local or remote subnets does not exist on the firewall.",
                **result,
            )
        if "Configuration parameters validation failed" in resp['response']:
            error_dict = ast.literal_eval(resp['response'])
            if (
                error_dict.get("InvalidParams").get("Params")
                == "/VPNIPSecConnection/Configuration/RemoteNetwork/Network"
            ):
                module.fail_json(
                    msg=f"ERROR: {resp['response']}, INFO: This error may indicate one or more specified remote subnets does not exist on the firewall.",
                    **result,
                )
            elif (
                error_dict.get("InvalidParams").get("Params")
                == "/VPNIPSecConnection/Configuration/LocalSubnet"
            ):
                module.fail_json(
                    msg=f"ERROR: {resp['response']}, INFO: This error may indicate one or more specified local subnets does not exist on the firewall.",
                    **result,
                )
            elif (
                error_dict.get("InvalidParams").get("Params")
                == "/VPNIPSecConnection/Configuration/AliasLocalWANPort"
            ):
                module.fail_json(
                    msg=f"ERROR: {resp['response']}, INFO: This error may indicate a missing or invalid value specified for listening_interface argument.",
                    **result,
                )
            else:
                module.fail_json(
                    msg=f"ERROR: {resp['response']}, INFO: This error may indicate invalid values for arguments passed to the module. INVALID_ARGS: {error_dict.get('InvalidParams').get('Params')} {output}",
                    **result,
                )

    return resp["response"]


def update_ipsec_connection(connection, exist_settings, module, result):
    """Update IPSec connection configuration on Sophos Firewall

    Args:
        connection (Connection): Ansible Connection object
        exist_settings (dict): API response containing existing IPSec connection configuration
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: API response
    """
    ipsec_connection = exist_settings["Response"]["VPNIPSecConnection"]

    param_map = [
        ("description", "Description"),
        ("connection_type", "ConnectionType"),
        ("ip_version", "SubnetFamily"),
        ("ip_version", "EndpointFamily"),
        ("gateway_type", "ActionOnVPNRestart"),
        ("profile", "Policy"),
        ("authentication_type", "AuthenticationType"),
        ("preshared_key", "PresharedKey"),
        ("local_certificate", "LocalCertificate"),
        ("remote_certificate", "RemoteCertificate"),
        ("remote_rsa_key", "RemoteRSAKey"),
        ("listening_interface", "LocalWANPort"),
        ("listening_interface", "AliasLocalWANPort"),
        ("gateway_address", "RemoteHost"),
        ("local_subnet", "LocalSubnet"),
        ("nat_lan", "NATedLAN"),
        ("local_id_type", "LocalIDType"),
        ("local_id", "LocalID"),
        ("allow_nat_traversal", "AllowNATTraversal"),
        ("remote_subnet", "RemoteNetwork"),
        ("remote_id_type", "RemoteIDType"),
        ("remote_id", "RemoteID"),
        ("user_authentication_mode", "UserAuthenticationMode"),
        ("as_client_username", "Username"),
        ("as_client_password", "Password"),
        ("as_server_user", "AllowedUser"),
        ("protocol", "Protocol"),
        ("local_port", "LocalPort"),
        ("remote_port", "RemotePort"),
        ("disconnect_on_idle_interval", "DisconnectOnIdleInterval"),
    ]

    for item in param_map:
        param, key = item
        if module.params.get(param) is not None:
            if key == "RemoteNetwork":
                ipsec_connection["Configuration"][key]["Network"] = module.params[param]
            else:
                ipsec_connection["Configuration"][key] = module.params[param]

    ipsec_connection.pop("@transactionid")
    configuration = (
        unparse(ipsec_connection, pretty=True)
        .replace('<?xml version="1.0" encoding="utf-8"?>', "")
        .lstrip()
    )

    payload = """
    <VPNIPSecConnection>
          {{ configuration | safe }}
          {% if active == True %}
          <Active><Name>{{ name }}</Name></Active>
          {% elif active == False %}
          <DeActive><Name>{{ name }}</Name></DeActive>
          {% endif %}
          {% if connection == True %}
          <Connection><Name>{{ name }}</Name></Connection>
          {% elif connection == False %}
          <DisConnection><Name>{{ name }}</Name></DisConnection>
          {% endif %}
    </VPNIPSecConnection>
    """

    template_vars = dict(
        name=module.params.get("name"),
        configuration=configuration,
        active=module.params.get("active", False),
        connection=module.params.get("connection", False),
    )

    try:
        with contextlib.redirect_stdout(output_buffer):
            resp = connection.invoke_sdk("submit_xml", module_args={
                "template_data": payload,
                "set_operation": "update",
                "template_vars": template_vars,
                "debug":True,
                }
            )
    except Exception as error:
        module.fail_json("An unexpected error occurred: {0}".format(error), **result)
    
    if not resp["success"]:
        output = output_buffer.getvalue() if module._verbosity >= 2 else ""
        if "Entity having same parameter details" in resp["response"]:
            module.fail_json(
                msg=f"ERROR: {resp['response']},  INFO: Possible causes: 1. Gateway address already in use on another VPN connection 2. One or more specified local or remote subnets does not exist on the firewall.",
                **result,
            )
        if "Configuration parameters validation failed" in resp['response']:
            error_dict = ast.literal_eval(resp['response'])
            if (
                error_dict.get("InvalidParams").get("Params")
                == "/VPNIPSecConnection/Configuration/RemoteNetwork/Network"
            ):
                module.fail_json(
                    msg=f"ERROR: {resp['response']}, INFO: This error may indicate one or more specified remote subnets does not exist on the firewall.",
                    **result,
                )
            elif (
                error_dict.get("InvalidParams").get("Params")
                == "/VPNIPSecConnection/Configuration/LocalSubnet"
            ):
                module.fail_json(
                    msg=f"ERROR: {resp['response']}, INFO: This error may indicate one or more specified local subnets does not exist on the firewall.",
                    **result,
                )
            elif (
                error_dict.get("InvalidParams").get("Params")
                == "/VPNIPSecConnection/Configuration/AliasLocalWANPort"
            ):
                module.fail_json(
                    msg=f"ERROR: {resp['response']}, INFO: This error may indicate a missing or invalid value specified for listening_interface argument.",
                    **result,
                )
            else:
                module.fail_json(
                    msg=f"ERROR: {resp['response']}, INFO: This error may indicate invalid values for arguments passed to the module. INVALID_ARGS: {error_dict.get('InvalidParams').get('Params')} {output}",
                    **result,
                )

    return resp["response"]


def eval_changed(module, exist_settings):
    """Evaluate the provided arguments against existing settings.

    Args:
        module (AnsibleModule): AnsibleModule object
        exist_settings (dict): Response from the call to get_admin_settings()

    Returns:
        bool: Return true if any settings are different, otherwise return false
    """
    exist_settings = exist_settings["api_response"]["Response"]["VPNIPSecConnection"]

    if (
        module.params.get("preshared_key")
        or module.params.get("active") is not None
        or module.params.get("connection") is not None
    ):
        return True

    param_map = [
        ("description", "Description"),
        ("connection_type", "ConnectionType"),
        ("ip_version", "SubnetFamily"),
        ("ip_version", "EndpointFamily"),
        ("gateway_type", "ActionOnVPNRestart"),
        ("profile", "Policy"),
        ("authentication_type", "AuthenticationType"),
        ("local_certificate", "LocalCertificate"),
        ("remote_certificate", "RemoteCertificate"),
        ("remote_rsa_key", "RemoteRSAKey"),
        ("listening_interface", "LocalWANPort"),
        ("listening_interface", "AliasLocalWANPort"),
        ("gateway_address", "RemoteHost"),
        ("local_subnet", "LocalSubnet"),
        ("nat_lan", "NATedLAN"),
        ("local_id_type", "LocalIDType"),
        ("local_id", "LocalID"),
        ("allow_nat_traversal", "AllowNATTraversal"),
        ("remote_subnet", "RemoteNetwork"),
        ("remote_id_type", "RemoteIDType"),
        ("remote_id", "RemoteID"),
        ("user_authentication_mode", "UserAuthenticationMode"),
        ("as_client_username", "Username"),
        ("as_client_password", "Password"),
        ("as_server_user", "AllowedUser"),
        ("protocol", "Protocol"),
        ("local_port", "LocalPort"),
        ("remote_port", "RemotePort"),
        ("disconnect_on_idle_interval", "DisconnectOnIdleInterval"),
    ]

    for item in param_map:
        param, key = item
        if (
            module.params.get(param) is not None
            and exist_settings["Configuration"].get(key) is not None
        ):
            if key == "RemoteNetwork":
                if not isinstance(
                    exist_settings["Configuration"]["RemoteNetwork"]["Network"], list
                ):
                    if (
                        not [
                            exist_settings["Configuration"]["RemoteNetwork"]["Network"]
                        ]
                        == module.params["remote_subnet"]
                    ):
                        return True
                else:
                    if (
                        not exist_settings["Configuration"]["RemoteNetwork"]["Network"]
                        == module.params["remote_subnet"]
                    ):
                        return True
            elif key == "LocalSubnet":
                if not isinstance(exist_settings["Configuration"]["LocalSubnet"], list):
                    if (
                        not [exist_settings["Configuration"]["LocalSubnet"]]
                        == module.params["local_subnet"]
                    ):
                        return True
                else:
                    if (
                        not exist_settings["Configuration"]["LocalSubnet"]
                        == module.params["local_subnet"]
                    ):
                        return True
            else:
                if not exist_settings["Configuration"][key] == module.params[param]:
                    return True

    return False


def remove_ipsec_connection(connection, module, result):
    """Remove an IPSec Connection from Sophos Firewall.

    Args:
        connection (Connection): Ansible Connection object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: API response
    """
    payload = """
    <Remove>
      <VPNIPSecConnection>
        <Configuration>
            <Name>{{ name }}</Name>
        </Configuration>
      </VPNIPSecConnection>
    </Remove>
    """
    try:
        resp = connection.invoke_sdk("submit_xml", module_args={
            "template_data": payload,
            "set_operation": None,
            "template_vars": {"name": module.params.get("name")},
            }
        )
    except Exception as error:
        module.fail_json("An unexpected error occurred: {0}".format(error), **result)

    if not resp["success"]:
        module.fail_json(msg="An error occurred: {0}".format(resp["response"]))

    return resp["response"]


def no_spaces(value):
    if " " in value:
        raise ValueError("Spaces are not allowed in this argument.")
    return value


def main():
    """Code executed at run time."""
    argument_spec = {
        "name": {"type": "str", "required": True},
        "description": {"type": "str", "required": False},
        "ip_version": {
            "type": "str",
            "choices": ["IPv4", "IPv6"],
            "default": "IPv4",
            "required": False,
        },
        "connection_type": {
            "type": "str",
            "choices": ["RemoteAccess", "SiteToSite", "HostToHost", "TunnelInterface"],
            "required": False,
        },
        "gateway_type": {
            "type": "str",
            "choices": ["Disable", "RespondOnly", "Initiate"],
            "required": False,
            "default": "RespondOnly",
        },
        "profile": {
            "type": "str",
            "choices": [
                "Default Profile",
                "Microsof Azure (IKEv2)",
                "IKEv2",
                "DefaultRemoteAccess",
                "DefaultL2TP",
                "DefaultHeadOffice",
                "DefaultBranchOffice",
                "Branch Office (IKEv2)",
                "Head office (IKEv2)",
            ],
            "required": False,
        },
        "authentication_type": {
            "type": "str",
            "choices": ["PresharedKey", "DigitalCertificate", "RSAKey"],
            "required": False,
        },
        "preshared_key": {"type": "str", "required": False, "no_log": True},
        "local_certificate": {"type": "str", "required": False},
        "remote_certificate": {"type": "str", "required": False},
        "remote_rsa_key": {"type": "str", "required": False, "no_log": True},
        "listening_interface": {"type": "str", "required": False},
        "gateway_address": {"type": "str", "required": False},
        "local_subnet": {"type": "list", "elements": "str", "required": False},
        "nat_lan": {"type": "str", "required": False},
        "local_id_type": {
            "type": "str",
            "choices": ["DNS", "IP Address", "Email", "DER ASN1 DN (X.509)"],
            "required": False,
        },
        "local_id": {"type": "str", "required": False},
        "allow_nat_traversal": {
            "type": "str",
            "choices": ["Enable", "Disable"],
            "required": False,
        },
        "remote_subnet": {"type": "list", "elements": "str", "required": False},
        "remote_id_type": {
            "type": "str",
            "choices": ["DNS", "IP Address", "Email", "DER ASN1 DN (X.509)"],
            "required": False,
        },
        "remote_id": {"type": "str", "required": False},
        "user_authentication_mode": {
            "type": "str",
            "choices": ["Disable", "AsServer", "AsClient"],
            "required": False,
        },
        "as_client_username": {"type": "str", "required": False},
        "as_client_password": {"type": "str", "required": False, "no_log": True},
        "as_server_user": {"type": "str", "required": False},
        "protocol": {
            "type": "str",
            "choices": ["ALL", "UDP", "TCP", "ICMP"],
            "required": False,
        },
        "local_port": {"type": "str", "required": False},
        "remote_port": {"type": "str", "required": False},
        "disconnect_on_idle_interval": {"type": "str", "required": False},
        "active": {"type": "bool", "required": False},
        "connection": {"type": "bool", "required": False},
        "state": {
            "type": "str",
            "required": True,
            "choices": ["present", "updated", "query", "absent"],
        },
    }

    required_if = [
        (
            "state",
            "present",
            [
                "name",
                "connection_type",
                "profile",
                "authentication_type",
                "listening_interface",
            ],
            False,
        ),
        (
            "state",
            "updated",
            ["name"],
            False,
        ),
        (
            "state",
            "query",
            ["name"],
            False,
        ),
        (
            "connection_type",
            "SiteToSite",
            [
                "local_subnet",
                "remote_subnet",
            ],
            False,
        ),
        (
            "authentication_type",
            "PresharedKey",
            [
                "preshared_key",
            ],
            False,
        ),
        (
            "authentication_type",
            "DigitalCertificate",
            [
                "local_certificate",
                "remote_certificate",
            ],
            False,
        ),
        (
            "authentication_type",
            "RSAKey",
            [
                "remote_rsa_key",
            ],
            False,
        ),
        (
            "gateway_address",
            "*",
            ["local_id_type", "remote_id_type", "local_id", "remote_id"],
        ),
    ]

    module = AnsibleModule(
        argument_spec=argument_spec, required_if=required_if, supports_check_mode=True
    )

    if " " in module.params.get("name"):
        module.fail_json(msg="Spaces are not allowed in name argument.")

    if module.params.get("connection_type") == "TunnelInterface":
        if module.params.get("local_subnet") or module.params.get("remote_subnet"):
            module.fail_json(
                msg="Cannot specify local and remote subnets for TunnelInterface connection type."
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

    exist_settings = get_ipsec_connection(connection, module, result)
    result["api_response"] = exist_settings["api_response"]

    if state == "query":
        module.exit_json(**result)

    if module.check_mode:
        result["check_mode"] = True
        module.exit_json(**result)

    if state == "present" and not exist_settings["exists"]:
        api_response = create_ipsec_connection(connection, module, result)
        if (
            "Configuration applied successfully"
            in api_response["Response"]["Configuration"]["Status"]["#text"]
        ):
            result["changed"] = True
            result["api_response"] = api_response

    elif state == "present" and exist_settings["exists"]:
        result["changed"] = False

    elif state == "absent" and exist_settings["exists"]:
        api_response = remove_ipsec_connection(connection, module, result)
        if (
            "Configuration applied successfully"
            in api_response["Response"]["VPNIPSecConnection"]["Configuration"][
                "Status"
            ]["#text"]
        ):
            result["changed"] = True
        result["api_response"] = api_response

    elif state == "absent" and not exist_settings["exists"]:
        result["changed"] = False

    elif state == "updated" and exist_settings["exists"]:
        if eval_changed(module, exist_settings):
            api_response = update_ipsec_connection(
                connection, exist_settings["api_response"], module, result
            )

            if api_response:
                result["api_response"] = api_response
                if (
                    "Configuration applied successfully"
                    in api_response["Response"]["Configuration"]["Status"]["#text"]
                ):
                    result["changed"] = True

    elif state == "updated" and not exist_settings["exists"]:
        result["changed"] = False
        module.fail_json(exist_settings["api_response"], **result)

    module.exit_json(**result)


if __name__ == "__main__":
    main()
