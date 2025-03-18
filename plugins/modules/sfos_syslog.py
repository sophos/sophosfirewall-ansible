#!/usr/bin/python

# Copyright 2024 Sophos Ltd.  All rights reserved.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: sfos_syslog

short_description: Manage Syslog servers (Configure > System services > Log settings)

version_added: "1.2.0"

description: Manage Syslog Servers (Configure > System services > Log settings) on Sophos Firewall

extends_documentation_fragment:
  - sophos.sophos_firewall.fragments.base

options:
    name: 
        description: Name of syslog server configuration
        type: str
        required: true
    address:
        description: IP address or hostname of syslog server
        type: str
        required: false
    udp_port:
        description: UDP port of syslog server. Default=514.
        type: int
        required: false
        default: 514
    secure_connection:
        description: Enable or Disable secure connection
        type: str
        required: false
        default: Disable
    facility:
        description: Logging facility
        type: str
        required: false
        choices: ["DAEMON", "LOCAL0", "LOCAL1", "LOCAL2", "LOCAL3", "LOCAL4", "LOCAL5", "LOCAL6", "LOCAL7", "KERNEL", "USER"]
    severity:
        description: Logging severity
        type: str
        required: false
        choices: ["Emergency", "Alert", "Critical", "Error", "Warning", "Notification", "Information", "Debug"]
    format:
        description: Syslog message format
        type: str
        required: false
        choices: ["Device standard", "Standard syslog"]
    default_logging:
        description: Indicates whether unspecified logging settings should be Enabled or Disabled by default
        type: str
        required: false
        choices: ["Enable", "Disable"]
        default: Enable
    log_settings:
        description: Logging settings
        type: dict
        required: false
        suboptions:
            security_policy:
                description: Security policy log settings
                type: dict
                required: false
                suboptions:
                    policy_rules:
                        description: Enable/Disable logging for policy rules
                        type: str
                        required: false
                        choices: ["Enable", "Disable"]
                    invalid_traffic:
                        description: Enable/Disable logging for invalid traffic
                        type: str
                        required: false
                        choices: ["Enable", "Disable"]
                    local_acls:
                        description: Enable/Disable logging for local ACLs
                        type: str
                        required: false
                        choices: ["Enable", "Disable"]
                    dos_attack:
                        description: Enable/Disable logging for DoS Attack
                        type: str
                        required: false
                        choices: ["Enable", "Disable"]
                    dropped_icmpredirect:
                        description: Enable/Disable logging for dropped ICMP redirect
                        type: str
                        required: false
                        choices: ["Enable", "Disable"]
                    dropped_sourceroute:
                        description: Enable/Disable logging for dropped Source Routed packet
                        type: str
                        required: false
                        choices: ["Enable", "Disable"]
                    dropped_fragment:
                        description: Enable/Disable logging for dropped fragmented traffic
                        type: str
                        required: false
                        choices: ["Enable", "Disable"]
                    mac_filtering:
                        description: Enable/Disable logging for MAC filtering
                        type: str
                        required: false
                        choices: ["Enable", "Disable"]
                    ipmacpair_filtering:
                        description: Enable/Disable logging for IP-MAC pair filtering
                        type: str
                        required: false
                        choices: ["Enable", "Disable"]
                    ipspoof_prevention:
                        description: Enable/Disable logging for IP spoof prevention
                        type: str
                        required: false
                        choices: ["Enable", "Disable"]
                    ssl_vpntunnel:
                        description: Enable/Disable logging for SSL VPN Tunnel
                        type: str
                        required: false
                        choices: ["Enable", "Disable"]
                    protected_application_server:
                        description: Enable/Disable logging for Protected application server
                        type: str
                        required: false
                        choices: ["Enable", "Disable"]
                    heartbeat:
                        description: Enable/Disable logging for heartbeat
                        type: str
                        required: false
                        choices: ["Enable", "Disable"]
                    icmp_errormessage:
                        description: Enable/Disable logging for ICMP error message
                        type: str
                        required: false
                        choices: ["Enable", "Disable"]
                    bridge_acls:
                        description: Enable/Disable logging for bridge ACLs
                        type: str
                        required: false
                        choices: ["Enable", "Disable"]
            ips:
                description: IPS log settings
                type: dict
                required: false
                suboptions:
                    anomaly:
                        description: Enable/Disable logging for anomaly detection
                        type: str
                        required: false
                        choices: ["Enable", "Disable"]
                    signatures:
                        description: Enable/Disable logging for IPS signatures
                        type: str
                        required: false
                        choices: ["Enable", "Disable"]
            anti_virus:
                description: IPS log settings
                type: dict
                required: false
                suboptions:
                    http:
                        description: Enable/Disable logging for HTTP
                        type: str
                        required: false
                        choices: ["Enable", "Disable"]
                    ftp:
                        description: Enable/Disable logging for FTP
                        type: str
                        required: false
                        choices: ["Enable", "Disable"]
                    smtp:
                        description: Enable/Disable logging for SMTP
                        type: str
                        required: false
                        choices: ["Enable", "Disable"]
                    pop3:
                        description: Enable/Disable logging for POP3
                        type: str
                        required: false
                        choices: ["Enable", "Disable"]
                    imap:
                        description: Enable/Disable logging for IMAP
                        type: str
                        required: false
                        choices: ["Enable", "Disable"]
                    https:
                        description: Enable/Disable logging for HTTPS
                        type: str
                        required: false
                        choices: ["Enable", "Disable"]
                    smtps:
                        description: Enable/Disable logging for SMTPS
                        type: str
                        required: false
                        choices: ["Enable", "Disable"]
                    pops:
                        description: Enable/Disable logging for POPS
                        type: str
                        required: false
                        choices: ["Enable", "Disable"]
                    imaps:
                        description: Enable/Disable logging for IMAPS
                        type: str
                        required: false
                        choices: ["Enable", "Disable"]
            anti_spam:
                description: IPS log settings
                type: dict
                required: false
                suboptions:
                    pop3:
                        description: Enable/Disable logging for POP3
                        type: str
                        required: false
                        choices: ["Enable", "Disable"]
                    imap:
                        description: Enable/Disable logging for IMAP
                        type: str
                        required: false
                        choices: ["Enable", "Disable"]
                    smtps:
                        description: Enable/Disable logging for SMTPS
                        type: str
                        required: false
                        choices: ["Enable", "Disable"]
                    pops:
                        description: Enable/Disable logging for POPS
                        type: str
                        required: false
                        choices: ["Enable", "Disable"]
                    imaps:
                        description: Enable/Disable logging for IMAPS
                        type: str
                        required: false
                        choices: ["Enable", "Disable"]
            content_filtering:
                description: Content filtering log settings
                type: dict
                required: false
                suboptions:
                    web_filter:
                        description: Enable/Disable logging for web filter
                        type: str
                        required: false
                        choices: ["Enable", "Disable"]
                    application_filter:
                        description: Enable/Disable logging for Application filter
                        type: str
                        required: false
                        choices: ["Enable", "Disable"]
                    web_content_policy:
                        description: Enable/Disable logging for Web content policy
                        type: str
                        required: false
                        choices: ["Enable", "Disable"]
                    ssl_tls:
                        description: Enable/Disable logging for SSL/TLS
                        type: str
                        required: false
                        choices: ["Enable", "Disable"]
            events:
                description: Events log settings
                type: dict
                required: false
                suboptions:
                    admin:
                        description: Enable/Disable logging for admin events
                        type: str
                        required: false
                        choices: ["Enable", "Disable"]
                    authentication:
                        description: Enable/Disable logging for authentication events
                        type: str
                        required: false
                        choices: ["Enable", "Disable"]
                    system:
                        description: Enable/Disable logging for system events
                        type: str
                        required: false
                        choices: ["Enable", "Disable"]
            web_server_protection:
                description: Web server protection log settings
                type: dict
                required: false
                suboptions:
                    waf_events:
                        description: Enable/Disable logging for WAF events
                        type: str
                        required: false
                        choices: ["Enable", "Disable"]
            atp:
                description: Web server protection log settings
                type: dict
                required: false
                suboptions:
                    atp_events:
                        description: Enable/Disable logging for ATP events
                        type: str
                        required: false
                        choices: ["Enable", "Disable"]
            wireless:
                description: Wireless log settings
                type: dict
                required: false
                suboptions:
                    access_points_ssid:
                        description: Enable/Disable logging Access Point SSID events
                        type: str
                        required: false
                        choices: ["Enable", "Disable"]
            heartbeat:
                description: Heartbeat log settings
                type: dict
                required: false
                suboptions:
                    endpoint_status:
                        description: Enable/Disable logging endpoint status events
                        type: str
                        required: false
                        choices: ["Enable", "Disable"]
            system_health:
                description: System health log settings
                type: dict
                required: false
                suboptions:
                    usage:
                        description: Enable/Disable logging usage events
                        type: str
                        required: false
                        choices: ["Enable", "Disable"]
            zeroday_protection:
                description: Zero day protection log settings
                type: dict
                required: false
                suboptions:
                    zeroday_protection_events:
                        description: Enable/Disable logging zeroday protection events
                        type: str
                        required: false
                        choices: ["Enable", "Disable"]
            sdwan:
                description: SDWAN log settings
                type: dict
                required: false
                suboptions:
                    profile:
                        description: Enable/Disable logging profile events
                        type: str
                        required: false
                        choices: ["Enable", "Disable"]
                    sla:
                        description: Enable/Disable logging SLA events
                        type: str
                        required: false
                        choices: ["Enable", "Disable"]
                    route:
                        description: Enable/Disable logging route events
                        type: str
                        required: false
                        choices: ["Enable", "Disable"]
    state:
        description:
            - Use C(query) to retrieve or C(updated) to modify
        choices: [updated, query]
        type: str
        required: true

author:
    - Matt Mullen (@mamullen13316)
"""

EXAMPLES = r"""
- name: Create syslog server, all logging enabled
  sophos.sophos_firewall.sfos_syslog:
    name: TestSyslog
    address: 10.10.1.100
    udp_port: 514
    secure_connection: Disable
    facility: DAEMON
    severity: Emergency
    format: Device standard
    default_logging: Enable
    state: present

- name: Create syslog server, disable selected logs
  sophos.sophos_firewall.sfos_syslog:
    name: TestSyslog
    address: 10.10.1.100
    udp_port: 514
    secure_connection: Disable
    facility: DAEMON
    severity: Emergency
    format: Device standard
    default_logging: Enable
    log_settings:
      security_policy:
        invalid_traffic: Disable
        icmp_errormessage: Disable
      content_filtering:
        ssl_tls: Disable
    state: present


- name: Query syslog server
  sophos.sophos_firewall.sfos_syslog:
    name: TestSyslog
    state: query

- name: Remove syslog server
  sophos.sophos_firewall.sfos_syslog:
    name: TestSyslog
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


payload = """
    <SyslogServers>
        <Name>{{ name }}</Name>
        <ServerAddress>{{ address }}</ServerAddress>
        <Port>{{ udp_port }}</Port>
        <EnableSecureConnection>{{ secure_connection }}</EnableSecureConnection>
        <Facility>{{ facility }}</Facility>
        <SeverityLevel>{{ severity }}</SeverityLevel>
        <Format>{{ format }}</Format>
    <LogSettings>
        <SecurityPolicy>
        <PolicyRules>{{ policy_rules }}</PolicyRules>
        <InvalidTraffic>{{ invalid_traffic }}</InvalidTraffic>
        <LocalACLs>{{ local_acls }}</LocalACLs>
        <DoSAttack>{{ dos_attack }}</DoSAttack>
        <DroppedICMPRedirectedPacket>{{ dropped_icmpredirect }}</DroppedICMPRedirectedPacket>
        <DroppedSourceRoutedPacket>{{ dropped_sourceroute }}</DroppedSourceRoutedPacket>
        <DroppedFragmentedTraffic>{{ dropped_fragment }}</DroppedFragmentedTraffic>
        <MACFiltering>{{ mac_filtering }}</MACFiltering>
        <IP-MACPairFiltering>{{ ipmacpair_filtering }}</IP-MACPairFiltering>
        <IPSpoofPrevention>{{ ipspoof_prevention }}</IPSpoofPrevention>
        <SSLVPNTunnel>{{ ssl_vpntunnel }}</SSLVPNTunnel>
        <ProtectedApplicationServer>{{ protected_application_server }}</ProtectedApplicationServer>
        <Heartbeat>{{ heartbeat }}</Heartbeat>
        <ICMPErrorMessage>{{ icmp_errormessage }}</ICMPErrorMessage>
        <BridgeACLs>{{ bridge_acls }}</BridgeACLs>
    </SecurityPolicy>
    <IPS>
        <Anomaly>{{ anomaly }}</Anomaly>
        <Signatures>{{ signatures }}</Signatures>
    </IPS>
    <AntiVirus>
        <HTTP>{{ av_http }}</HTTP>
        <FTP>{{ av_ftp }}</FTP>
        <SMTP>{{ av_smtp }}</SMTP>
        <POP3>{{ av_pop3 }}</POP3>
        <IMAP>{{ av_imap }}</IMAP>
        <HTTPS>{{ av_https }}</HTTPS>
        <SMTPS>{{ av_smtps }}</SMTPS>
        <POPS>{{ av_pops }}</POPS>
        <IMAPS>{{ av_imaps }}</IMAPS>
    </AntiVirus>
    <AntiSpam>
        <SMTP>{{ as_smtp }}</SMTP>
        <POP3>{{ as_pop3 }}</POP3>
        <IMAP>{{ as_imap }}</IMAP>
        <SMTPS>{{ as_smtps }}</SMTPS>
        <POPS>{{ as_pops }}</POPS>
        <IMAPS>{{ as_imaps }}</IMAPS>
    </AntiSpam>
    <ContentFiltering>
        <WebFilter>{{ web_filter }}</WebFilter>
        <ApplicationFilter>{{ application_filter }}</ApplicationFilter>
        <WebContentPolicy>{{ web_content_policy }}</WebContentPolicy>
        <SSLTLS>{{ ssl_tls }}</SSLTLS>
    </ContentFiltering>
    <Events>
        <AdminEvents>{{ admin }}</AdminEvents>
        <AuthenticationEvents>{{ authentication }}</AuthenticationEvents>
        <SystemEvents>{{ system }}</SystemEvents>
    </Events>
    <WebServerProtection>
        <WAFEvents>{{ waf_events }}</WAFEvents>
    </WebServerProtection>
    <ATP>
        <ATPEvents>{{ atp_events }}</ATPEvents>
    </ATP>
    <Wireless>
        <AccessPoints_SSID>{{ access_points_ssid }}</AccessPoints_SSID>
    </Wireless>
    <Heartbeat>
        <EndpointStatus>{{ heartbeat }}</EndpointStatus>
    </Heartbeat>
    <SystemHealth>
        <Usage>{{ usage }}</Usage>
    </SystemHealth>
    <ZeroDayProtection>
        <ZeroDayProtectionEvents>{{ zeroday_protection_events }}</ZeroDayProtectionEvents>
    </ZeroDayProtection>
    <SDWAN>
        <Profile>{{ profile }}</Profile>
        <SLA>{{ sla }}</SLA>
        <Route>{{ route }}</Route>
    </SDWAN>
    </LogSettings>
</SyslogServers>
"""

def get_with_default(d, key, default):
    value = d.get(key)
    return default if value is None else value

def get_syslog(connection, module, result):
    """Get current syslog server settings from Sophos Firewall

    Args:
        connection (Connection): Ansible Connection object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: Results of lookup
    """
    try:
        resp = connection.invoke_sdk("get_tag_with_filter", module_args={"xml_tag": "SyslogServers", "key": "Name", "value": module.params.get("name")})
    except Exception as error:
        module.fail_json("An unexpected error occurred: {0}".format(error), **result)
    
    if resp["success"] and not resp["exists"]:
        return {"exists": False, "api_response": resp["response"]}

    if not resp["success"]:
        module.fail_json(msg="An error occurred: {0}".format(resp["response"]))    

    if isinstance(resp["response"]["Response"]["SyslogServers"], dict):
        return {"exists": False, "api_response": resp["response"]}
    if isinstance(resp["response"]["Response"]["SyslogServers"], list):
        for syslog_server in resp["response"]["Response"]["SyslogServers"]:
            if syslog_server["Name"] == module.params.get("name"):
                return {"exists": True, "api_response": resp["response"]}

    return {"exists": True, "api_response": resp["response"]}


def create_syslog(connection, module, result):
    """Create an Syslog server configuration on Sophos Firewall

    Args:
        connection (Connection): Ansible Connection object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: API response
    """

    syslog_format = "3" if module.params.get("format") == "Standard syslog" else "DeviceStandardFormat"

    default_logging = module.params.get("default_logging")
    log_settings = get_with_default(module.params, "log_settings", {})

    security_policy = get_with_default(log_settings, "security_policy", {})
    ips = get_with_default(log_settings, "ips", {})
    anti_virus = get_with_default(log_settings, "anti_virus", {})
    anti_spam = get_with_default(log_settings, "anti_spam", {})
    content_filtering = get_with_default(log_settings, "content_filtering", {})
    events = get_with_default(log_settings, "events", {})
    web_server_protection = get_with_default(log_settings, "web_server_protection", {})
    atp = get_with_default(log_settings, "atp", {})
    wireless = get_with_default(log_settings, "wireless", {})
    heartbeat = get_with_default(log_settings, "heartbeat", {})
    system_health = get_with_default(log_settings, "system_health", {})
    zeroday_protection = get_with_default(log_settings, "zeroday_protection", {})
    sdwan = get_with_default(log_settings, "sdwan", {})


    template_vars = {
        "name": module.params.get("name"),
        "address": module.params.get("address"),
        "udp_port": module.params.get("udp_port"),
        "secure_connection": module.params.get("secure_connection"),
        "facility": module.params.get("facility"),
        "severity": module.params.get("severity"),
        "format": syslog_format,
        "policy_rules": get_with_default(security_policy, "policy_rules", default_logging),
        "invalid_traffic": get_with_default(security_policy, "invalid_traffic", default_logging),
        "local_acls": get_with_default(security_policy, "local_acls", default_logging),
        "dos_attack": get_with_default(security_policy, "dos_attack", default_logging),
        "dropped_icmpredirect": get_with_default(security_policy, "dropped_icmpredirect", default_logging),
        "dropped_sourceroute": get_with_default(security_policy, "dropped_sourceroute", default_logging),
        "dropped_fragment": get_with_default(security_policy, "dropped_fragment", default_logging),
        "mac_filtering": get_with_default(security_policy, "mac_filtering", default_logging),
        "ipmacpair_filtering": get_with_default(security_policy, "ipmacpair_filtering", default_logging),
        "ipspoof_prevention": get_with_default(security_policy, "ipspoof_prevention", default_logging),
        "ssl_vpntunnel": get_with_default(security_policy, "ssl_vpntunnel", default_logging),
        "protected_application_server": get_with_default(security_policy, "protected_application_server", default_logging),
        "heartbeat": get_with_default(security_policy, "heartbeat", default_logging),
        "icmp_errormessage": get_with_default(security_policy, "icmp_errormessage", default_logging),
        "bridge_acls": get_with_default(security_policy, "bridge_acls", default_logging),
        "anomaly": get_with_default(ips, "anomaly", default_logging),
        "signatures": get_with_default(ips, "signatures", default_logging),
        "av_http": get_with_default(anti_virus, "http", default_logging),
        "av_ftp": get_with_default(anti_virus, "ftp", default_logging),
        "av_smtp": get_with_default(anti_virus, "smtp", default_logging),
        "av_pop3": get_with_default(anti_virus, "pop3", default_logging),
        "av_imap": get_with_default(anti_virus, "imap", default_logging),
        "av_https": get_with_default(anti_virus, "https", default_logging),
        "av_smtps": get_with_default(anti_virus, "smtps", default_logging),
        "av_pops": get_with_default(anti_virus, "pops", default_logging),
        "av_imaps": get_with_default(anti_virus, "imaps", default_logging),
        "as_smtp": get_with_default(anti_spam, "smtp", default_logging),
        "as_pop3": get_with_default(anti_spam, "pop3", default_logging),
        "as_imap": get_with_default(anti_spam, "imap", default_logging),
        "as_smtps": get_with_default(anti_spam, "smtps", default_logging),
        "as_pops": get_with_default(anti_spam, "pops", default_logging),
        "as_imaps": get_with_default(anti_spam, "imaps", default_logging),
        "web_filter": get_with_default(content_filtering, "web_filter", default_logging),
        "application_filter": get_with_default(content_filtering, "application_filter", default_logging),
        "web_content_policy": get_with_default(content_filtering, "web_content_policy", default_logging),
        "ssl_tls": get_with_default(content_filtering, "ssl_tls", default_logging),
        "admin": get_with_default(events, "admin", default_logging),
        "authentication": get_with_default(events, "authentication", default_logging),
        "system": get_with_default(events, "system", default_logging),
        "waf_events": get_with_default(web_server_protection, "waf_events", default_logging),
        "atp_events": get_with_default(atp, "atp_events", default_logging),
        "access_points_ssid": get_with_default(wireless, "access_points_ssid", default_logging),
        "endpoint_status": get_with_default(heartbeat, "endpoint_status", default_logging),
        "usage": get_with_default(system_health, "usage", default_logging),
        "zeroday_protection_events": get_with_default(zeroday_protection, "zeroday_protection_events", default_logging),
        "profile": get_with_default(sdwan, "profile", default_logging),
        "sla": get_with_default(sdwan, "sla", default_logging),
        "route": get_with_default(sdwan, "route", default_logging)
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

def update_syslog(connection, exist_settings, module, result):
    """Update admin settings on Sophos Firewall

    Args:
        connection (Connection): Ansible Connection object
        exist_settings (dict): Existing settings for the syslog server
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: API response
    """
    if isinstance(exist_settings["api_response"]["Response"]["SyslogServers"], dict):
        exist_settings = exist_settings["api_response"]["Response"]["SyslogServers"]
    if isinstance(exist_settings["api_response"]["Response"]["SyslogServers"], list):
        for syslog_server in exist_settings["api_response"]["Response"]["SyslogServers"]:
            if syslog_server["Name"] == module.params.get("name"):
                exist_settings = syslog_server

    log_settings = get_with_default(module.params, "log_settings", {})

    security_policy = get_with_default(log_settings,"security_policy", {})
    ips = get_with_default(log_settings,"ips", {})
    anti_virus = get_with_default(log_settings,"anti_virus", {})
    anti_spam = get_with_default(log_settings,"anti_spam", {})
    content_filtering = get_with_default(log_settings,"content_filtering", {})
    events = get_with_default(log_settings,"events", {})
    web_server_protection = get_with_default(log_settings,"web_server_protection", {})
    atp = get_with_default(log_settings,"atp", {})
    wireless = get_with_default(log_settings,"wireless", {})
    heartbeat = get_with_default(log_settings,"heartbeat", {})
    system_health = get_with_default(log_settings,"system_health", {})
    zeroday_protection = get_with_default(log_settings,"zeroday_protection", {})
    sdwan = get_with_default(log_settings,"sdwan", {})

    if module.params.get("format"):
        syslog_format = "3" if module.params.get("format") == "Standard syslog" else "DeviceStandardFormat"
    else:
        syslog_format = exist_settings["Format"]

    template_vars = {
        "name": module.params.get("name"),
        "address": get_with_default(module.params,"address", exist_settings["ServerAddress"]),
        "udp_port": get_with_default(module.params, "udp_port", exist_settings["Port"]),
        "secure_connection": get_with_default(module.params, "secure_connection", exist_settings["EnableSecureConnection"]),
        "facility": get_with_default(module.params, "facility", exist_settings["Facility"]),
        "severity": get_with_default(module.params,"severity", exist_settings["SeverityLevel"]),
        "format": syslog_format,
        "policy_rules": get_with_default(security_policy, "policy_rules", exist_settings["LogSettings"]["SecurityPolicy"]["PolicyRules"]),
        "invalid_traffic": get_with_default(security_policy, "invalid_traffic", exist_settings["LogSettings"]["SecurityPolicy"]["InvalidTraffic"]),
        "local_acls": get_with_default(security_policy, "local_acls", exist_settings["LogSettings"]["SecurityPolicy"]["LocalACLs"]),
        "dos_attack": get_with_default(security_policy, "dos_attack", exist_settings["LogSettings"]["SecurityPolicy"]["DoSAttack"]),
        "dropped_icmpredirect": get_with_default(security_policy, "dropped_icmpredirect", exist_settings["LogSettings"]["SecurityPolicy"]["DroppedICMPRedirectedPacket"]),
        "dropped_sourceroute": get_with_default(security_policy, "dropped_sourceroute", exist_settings["LogSettings"]["SecurityPolicy"]["DroppedSourceRoutedPacket"]),
        "dropped_fragment": get_with_default(security_policy, "dropped_fragment", exist_settings["LogSettings"]["SecurityPolicy"]["DroppedFragmentedTraffic"]),
        "mac_filtering": get_with_default(security_policy, "mac_filtering", exist_settings["LogSettings"]["SecurityPolicy"]["MACFiltering"]),
        "ipmacpair_filtering": get_with_default(security_policy, "ipmacpair_filtering", exist_settings["LogSettings"]["SecurityPolicy"]["IP-MACPairFiltering"]),
        "ipspoof_prevention": get_with_default(security_policy, "ipspoof_prevention", exist_settings["LogSettings"]["SecurityPolicy"]["IPSpoofPrevention"]),
        "ssl_vpntunnel": get_with_default(security_policy, "ssl_vpntunnel", exist_settings["LogSettings"]["SecurityPolicy"]["SSLVPNTunnel"]),
        "protected_application_server": get_with_default(security_policy, "protected_application_server", exist_settings["LogSettings"]["SecurityPolicy"]["ProtectedApplicationServer"]),
        "heartbeat": get_with_default(security_policy, "heartbeat", exist_settings["LogSettings"]["SecurityPolicy"]["Heartbeat"]),
        "icmp_errormessage": get_with_default(security_policy, "icmp_errormessage", exist_settings["LogSettings"]["SecurityPolicy"]["ICMPErrorMessage"]),
        "bridge_acls": get_with_default(security_policy, "bridge_acls", exist_settings["LogSettings"]["SecurityPolicy"]["BridgeACLs"]),
        "anomaly": get_with_default(ips, "anomaly", exist_settings["LogSettings"]["IPS"]["Anomaly"]),
        "signatures": get_with_default(ips, "signatures", exist_settings["LogSettings"]["IPS"]["Signatures"]),
        "av_http": get_with_default(anti_virus, "http", exist_settings["LogSettings"]["AntiVirus"]["HTTP"]),
        "av_ftp": get_with_default(anti_virus, "ftp", exist_settings["LogSettings"]["AntiVirus"]["FTP"]),
        "av_smtp": get_with_default(anti_virus, "smtp", exist_settings["LogSettings"]["AntiVirus"]["SMTP"]),
        "av_pop3": get_with_default(anti_virus, "pop3", exist_settings["LogSettings"]["AntiVirus"]["POP3"]),
        "av_imap": get_with_default(anti_virus, "imap", exist_settings["LogSettings"]["AntiVirus"]["IMAP"]),
        "av_https": get_with_default(anti_virus, "https", exist_settings["LogSettings"]["AntiVirus"]["HTTPS"]),
        "av_smtps": get_with_default(anti_virus, "smtps", exist_settings["LogSettings"]["AntiVirus"]["SMTPS"]),
        "av_pops": get_with_default(anti_virus, "pops", exist_settings["LogSettings"]["AntiVirus"]["POPS"]),
        "av_imaps": get_with_default(anti_virus, "imaps", exist_settings["LogSettings"]["AntiVirus"]["IMAPS"]),
        "as_pop3": get_with_default(anti_spam, "pop3", exist_settings["LogSettings"]["AntiSpam"]["POP3"]),
        "as_imap": get_with_default(anti_spam, "imap", exist_settings["LogSettings"]["AntiSpam"]["IMAP"]),
        "as_smtp": get_with_default(anti_spam, "smtp", exist_settings["LogSettings"]["AntiSpam"]["SMTP"]),
        "as_smtps": get_with_default(anti_spam, "smtps", exist_settings["LogSettings"]["AntiSpam"]["SMTPS"]),
        "as_pops": get_with_default(anti_spam, "pops", exist_settings["LogSettings"]["AntiSpam"]["POPS"]),
        "as_imaps": get_with_default(anti_spam, "imaps", exist_settings["LogSettings"]["AntiSpam"]["IMAPS"]),
        "web_filter": get_with_default(content_filtering, "web_filter", exist_settings["LogSettings"]["ContentFiltering"]["WebFilter"]),
        "application_filter": get_with_default(content_filtering, "application_filter", exist_settings["LogSettings"]["ContentFiltering"]["ApplicationFilter"]),
        "web_content_policy": get_with_default(content_filtering, "web_content_policy", exist_settings["LogSettings"]["ContentFiltering"]["WebContentPolicy"]),
        "ssl_tls": get_with_default(content_filtering, "ssl_tls", exist_settings["LogSettings"]["ContentFiltering"]["SSLTLS"]),
        "admin": get_with_default(events, "admin", exist_settings["LogSettings"]["Events"]["AdminEvents"]),
        "authentication": get_with_default(events, "authentication", exist_settings["LogSettings"]["Events"]["AuthenticationEvents"]),
        "system": get_with_default(events, "system", exist_settings["LogSettings"]["Events"]["SystemEvents"]),
        "waf_events": get_with_default(web_server_protection, "waf_events", exist_settings["LogSettings"]["WebServerProtection"]["WAFEvents"]),
        "atp_events": get_with_default(atp, "atp_events", exist_settings["LogSettings"]["ATP"]["ATPEvents"]),
        "access_points_ssid": get_with_default(wireless, "access_points_ssid", exist_settings["LogSettings"]["Wireless"]["AccessPoints_SSID"]),
        "endpoint_status": get_with_default(heartbeat, "endpoint_status", exist_settings["LogSettings"]["Heartbeat"]["EndpointStatus"]),
        "usage": get_with_default(system_health, "usage", exist_settings["LogSettings"]["SystemHealth"]["Usage"]),
        "zeroday_protection_events": get_with_default(zeroday_protection, "zeroday_protection_events", exist_settings["LogSettings"]["ZeroDayProtection"]["ZeroDayProtectionEvents"]),
        "profile": get_with_default(sdwan, "profile", exist_settings["LogSettings"]["SDWAN"]["Profile"]),
        "sla": get_with_default(sdwan, "sla", exist_settings["LogSettings"]["SDWAN"]["SLA"]),
        "route": get_with_default(sdwan, "route", exist_settings["LogSettings"]["SDWAN"]["Route"])
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

    if isinstance(exist_settings["api_response"]["Response"]["SyslogServers"], dict):
        exist_settings = exist_settings["api_response"]["Response"]["SyslogServers"]
    if isinstance(exist_settings["api_response"]["Response"]["SyslogServers"], list):
        for syslog_server in exist_settings["api_response"]["Response"]["SyslogServers"]:
            if syslog_server["Name"] == module.params.get("name"):
                exist_settings = syslog_server

    if module.params.get("address") and not module.params.get("address") == exist_settings["ServerAddress"]:
        return True
    
    if module.params.get("port") and not str(module.params.get("udp_port")) == exist_settings["Port"]:
        return True

    if module.params.get("secure_connection") and not module.params.get("secure_connection") == exist_settings["EnableSecureConnection"]:
        return True

    if module.params.get("facility") and not module.params.get("facility") == exist_settings["Facility"]:
        return True

    if module.params.get("severity") and not module.params.get("severity") == exist_settings["SeverityLevel"]:
        return True

    if module.params.get("format"):
        fmt = module.params.get("format")
        expected_format = "3" if fmt == "Standard syslog" else "DeviceStandardFormat"
        if not expected_format == exist_settings["Format"]:
            return True

    log_settings = module.params.get("log_settings", {})
        
    if log_settings.get("security_policy"):
        security_policy = log_settings.get("security_policy", {})
        policy_rules = security_policy.get("policy_rules")
        invalid_traffic = security_policy.get("invalid_traffic")
        local_acls = security_policy.get("local_acls")
        dos_attack = security_policy.get("dos_attack")
        dropped_icmpredirect = security_policy.get("dropped_icmpredirect")
        dropped_sourceroute = security_policy.get("dropped_sourceroute")
        dropped_fragment = security_policy.get("dropped_fragment")
        mac_filtering = security_policy.get("mac_filtering")
        ipmacpair_filtering = security_policy.get("ipmacpair_filtering")
        ipspoof_prevention = security_policy.get("ipspoof_prevention")
        ssl_vpntunnel = security_policy.get("ssl_vpntunnel")
        protected_application_server = security_policy.get("protected_application_server")
        heartbeat = security_policy.get("heartbeat")
        icmp_errormessage = security_policy.get("icmp_errormessage")
        bridge_acls = security_policy.get("bridge_acls")
        
        if (policy_rules and not policy_rules == exist_settings["LogSettings"]["SecurityPolicy"]["PolicyRules"] or
            invalid_traffic and not invalid_traffic == exist_settings["LogSettings"]["SecurityPolicy"]["InvalidTraffic"] or 
            local_acls and not local_acls == exist_settings["LogSettings"]["SecurityPolicy"]["InvalidTraffic"] or
            dos_attack and not dos_attack == exist_settings["LogSettings"]["SecurityPolicy"]["DoSAttack"] or
            dropped_icmpredirect and not dropped_icmpredirect == exist_settings["LogSettings"]["SecurityPolicy"]["DroppedICMPRedirectedPacket"] or
            dropped_sourceroute and not dropped_sourceroute == exist_settings["LogSettings"]["SecurityPolicy"]["DroppedSourceRoutedPacket"] or
            dropped_fragment and not dropped_fragment == exist_settings["LogSettings"]["SecurityPolicy"]["DroppedFragmentedTraffic"] or
            mac_filtering and not mac_filtering == exist_settings["LogSettings"]["SecurityPolicy"]["MACFiltering"] or
            ipmacpair_filtering and not ipmacpair_filtering == exist_settings["LogSettings"]["SecurityPolicy"]["IP-MACPairFiltering"] or
            ipspoof_prevention and not ipspoof_prevention == exist_settings["LogSettings"]["SecurityPolicy"].get("IP-IPSpoofPrevention") or
            ipspoof_prevention and not ipspoof_prevention == exist_settings["LogSettings"]["SecurityPolicy"].get("IPSpoofPrevention") or
            ssl_vpntunnel and not ssl_vpntunnel == exist_settings["LogSettings"]["SecurityPolicy"]["SSLVPNTunnel"] or
            protected_application_server and not protected_application_server == exist_settings["LogSettings"]["SecurityPolicy"]["ProtectedApplicationServer"] or
            heartbeat and not heartbeat == exist_settings["LogSettings"]["SecurityPolicy"]["Heartbeat"] or
            icmp_errormessage and not icmp_errormessage == exist_settings["LogSettings"]["SecurityPolicy"]["ICMPErrorMessage"] or
            bridge_acls and not bridge_acls == exist_settings["LogSettings"]["SecurityPolicy"]["BridgeACLs"]
            ):
            return True
    
    if log_settings.get("ips"):
        ips = log_settings.get("ips")
        anomaly = ips.get("anomaly")
        signatures = ips.get("signatures")
        if (anomaly and not anomaly == exist_settings["LogSettings"]["IPS"]["Anomaly"] or
            signatures and not signatures == exist_settings["LogSettings"]["IPS"]["Signatures"]
        ):
            return True

    if log_settings.get("anti_virus"):
        anti_virus = log_settings.get("anti_virus")
        http = anti_virus.get("http")
        ftp = anti_virus.get("ftp")
        smtp = anti_virus.get("smtp")
        pop3 = anti_virus.get("pop3")
        imap = anti_virus.get("imap")
        https = anti_virus.get("https")
        smtps = anti_virus.get("smtps")
        pops = anti_virus.get("pops")
        imaps = anti_virus.get("imaps")
        if (http and not http == exist_settings["LogSettings"]["AntiVirus"]["HTTP"] or
            ftp and not ftp == exist_settings["LogSettings"]["AntiVirus"]["FTP"] or
            smtp and not smtp == exist_settings["LogSettings"]["AntiVirus"]["SMTP"] or
            pop3 and not pop3 == exist_settings["LogSettings"]["AntiVirus"]["POP3"] or
            imap and not imap == exist_settings["LogSettings"]["AntiVirus"]["IMAP"] or
            https and not https == exist_settings["LogSettings"]["AntiVirus"]["HTTPS"] or
            pops and not pops == exist_settings["LogSettings"]["AntiVirus"]["POPS"] or
            smtps and not smtps == exist_settings["LogSettings"]["AntiVirus"]["SMTPS"] or
            imaps and not imaps == exist_settings["LogSettings"]["AntiVirus"]["IMAPS"]
        ):
            return True
    
    if log_settings.get("anti_spam"):
        anti_spam = log_settings.get("anti_spam")
        pop3 = anti_spam.get("pop3")
        imap = anti_spam.get("imap")
        smtp = anti_spam.get("smtp")
        smtps = anti_spam.get("smtps")
        pops = anti_spam.get("pops")
        imaps = anti_spam.get("imaps")
        if (pop3 and not pop3 == exist_settings["LogSettings"]["AntiSpam"]["POP3"] or
            imap and not imap == exist_settings["LogSettings"]["AntiSpam"]["IMAP"] or
            smtp and not smtp == exist_settings["LogSettings"]["AntiSpam"]["SMTP"] or
            smtps and not smtps == exist_settings["LogSettings"]["AntiSpam"]["SMTPS"] or
            pops and not pops == exist_settings["LogSettings"]["AntiSpam"]["POPS"] or
            imaps and not imaps == exist_settings["LogSettings"]["AntiSpam"]["IMAPS"]
            ):
            return True
        

    if log_settings.get("content_filtering"):
        content_filtering = log_settings.get("content_filtering")
        web_filter = content_filtering.get("web_filter")
        application_filter = content_filtering.get("application_filter")
        web_content_policy = content_filtering.get("web_content_policy")
        ssl_tls = content_filtering.get("ssl_tls")
        if (web_filter and not web_filter == exist_settings["LogSettings"]["ContentFiltering"]["WebFilter"] or
            application_filter and not application_filter == exist_settings["LogSettings"]["ContentFiltering"]["ApplicationFilter"] or
            web_content_policy and not web_content_policy == exist_settings["LogSettings"]["ContentFiltering"]["WebContentPolicy"] or
            ssl_tls and not ssl_tls == exist_settings["LogSettings"]["ContentFiltering"]["SSLTLS"]
        ):
            return True

    if log_settings.get("events"):
        events = log_settings.get("events")
        admin = events.get("admin")
        authentication = events.get("authentication")
        system = events.get("system")
        if (admin and not admin == exist_settings["LogSettings"]["Events"]["AdminEvents"] or
            authentication and not authentication == exist_settings["LogSettings"]["Events"]["AuthenticationEvents"] or
            system and not system == exist_settings["LogSettings"]["Events"]["SystemEvents"]
        ):
            return True

    if log_settings.get("web_server_protection"):
        web_server_protection = log_settings.get("web_server_protection")
        waf_events = web_server_protection.get("waf_events")
        if waf_events and not waf_events == exist_settings["LogSettings"]["WebServerProtection"]["WAFEvents"]:
            return True

    if log_settings.get("atp"):
        atp = log_settings.get("atp")
        atp_events = atp.get("atp_events")
        if atp_events and not atp_events == exist_settings["LogSettings"]["ATP"]["ATPEvents"]:
            return True
    
    if log_settings.get("wireless"):
        wireless = log_settings.get("wireless")
        access_points_ssid = wireless.get("access_points_ssid")
        if access_points_ssid and not access_points_ssid == exist_settings["LogSettings"]["Wireless"]["AccessPoints_SSID"]:
            return True
    
    if log_settings.get("heartbeat"):
        heartbeat = log_settings.get("heartbeat")
        endpoint_status = heartbeat.get("endpoint_status")
        if endpoint_status and not endpoint_status == exist_settings["LogSettings"]["Heartbeat"]["EndpointStatus"]:
            return True
    
    if log_settings.get("system_health"):
        system_health = log_settings.get("system_health")
        usage = system_health.get("usage")
        if usage and not usage == exist_settings["LogSettings"]["SystemHealth"]["Usage"]:
            return True
        
    if log_settings.get("zeroday_protection"):
        zeroday_protection = log_settings.get("zeroday_protection")
        zeroday_protection_events = zeroday_protection.get("zeroday_protection_events")
        if zeroday_protection_events and not zeroday_protection_events == exist_settings["LogSettings"]["ZeroDayProtection"]["ZeroDayProtectionEvents"]:
            return True

    if log_settings.get("sdwan"):
        sdwan = log_settings.get("sdwan")
        profile = sdwan.get("profile")
        sla = sdwan.get("sla")
        route = sdwan.get("route")
        if (profile and not profile == exist_settings["LogSettings"]["SDWAN"]["Profile"] or
            sla and not sla == exist_settings["LogSettings"]["SDWAN"]["SLA"] or
            route and not route == exist_settings["LogSettings"]["SDWAN"]["Route"]
        ):
            return True
    
    return False

def remove_syslog(connection, module, result):
    """Remove a Syslog server from Sophos Firewall.

    Args:
        connection (Connection): Ansible Connection object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: API response
    """
    try:
        resp = connection.invoke_sdk("remove", module_args={"xml_tag": "SyslogServers", "name": module.params.get("name")})
    except Exception as error:
        module.fail_json("An unexpected error occurred: {0}".format(error), **result)

    if not resp["success"]:
        module.fail_json(msg="An error occurred: {0}".format(resp["response"]))

    return resp["response"]

def main():
    """Code executed at run time."""
    argument_spec = {
        "enabled": {"type": "bool", "required": False},
        "name": {"type": "str", "required": True},
        "address": {"type": "str", "required": False},
        "udp_port": {"type": "int", "required": False, "default": 514},
        "secure_connection": {"type": "str", "required": False, "default": "Disable", "choices": ["Enable", "Disable"]},
        "facility": {"type": "str", "required": False, "choices": ["DAEMON", "LOCAL0", "LOCAL1", "LOCAL2", "LOCAL3", "LOCAL4", "LOCAL5", "LOCAL6", "LOCAL7", "KERNEL", "USER"]},
        "severity": {"type": "str", "required": False, "choices": ["Emergency", "Alert", "Critical", "Error", "Warning", "Notification", "Information", "Debug"]},
        "format": {"type": "str", "required": False, "choices": ["Device standard", "Standard syslog"]},
        "default_logging": {"type": "str", "required": False, "choices": ["Enable", "Disable"], "default": "Enable"},
        "log_settings": {"type": "dict", "required": False, "options": {
            "security_policy": {"type": "dict", "required": False, "options": {
                    "policy_rules": {"type": "str", "choices": ["Enable", "Disable"]},
                    "invalid_traffic": {"type": "str", "choices": ["Enable", "Disable"]},
                    "local_acls": {"type": "str", "choices": ["Enable", "Disable"]},
                    "dos_attack": {"type": "str", "choices": ["Enable", "Disable"]},
                    "dropped_icmpredirect": {"type": "str", "choices": ["Enable", "Disable"]},
                    "dropped_sourceroute": {"type": "str", "choices": ["Enable", "Disable"]},
                    "dropped_fragment": {"type": "str", "choices": ["Enable", "Disable"]},
                    "mac_filtering": {"type": "str", "choices": ["Enable", "Disable"]},
                    "ipmacpair_filtering": {"type": "str", "choices": ["Enable", "Disable"]},
                    "ipspoof_prevention": {"type": "str", "choices": ["Enable", "Disable"]},
                    "ssl_vpntunnel": {"type": "str", "choices": ["Enable", "Disable"]},
                    "protected_application_server": {"type": "str", "choices": ["Enable", "Disable"]},
                    "heartbeat": {"type": "str", "choices": ["Enable", "Disable"]},
                    "icmp_errormessage": {"type": "str", "choices": ["Enable", "Disable"]},
                    "bridge_acls": {"type": "str", "choices": ["Enable", "Disable"]}
                    }
                },
            "ips": {"type": "dict", "required": False, "default": {}, "options": {
                    "anomaly": {"type": "str", "choices": ["Enable", "Disable"]},
                    "signatures": {"type": "str", "choices": ["Enable", "Disable"]}
                    }
                },
            "anti_virus": {"type": "dict", "required": False, "default": {}, "options": {
                "http": {"type": "str", "choices": ["Enable", "Disable"]},
                "ftp": {"type": "str", "choices": ["Enable", "Disable"]},
                "smtp": {"type": "str", "choices": ["Enable", "Disable"]},
                "pop3": {"type": "str", "choices": ["Enable", "Disable"]},
                "imap": {"type": "str", "choices": ["Enable", "Disable"]},
                "https": {"type": "str", "choices": ["Enable", "Disable"]},
                "smtps": {"type": "str", "choices": ["Enable", "Disable"]},
                "pops": {"type": "str", "choices": ["Enable", "Disable"]},
                "imaps": {"type": "str", "choices": ["Enable", "Disable"]}
                    }
                },
            "anti_spam": {"type": "dict", "required": False, "default": {}, "options": {
                "pop3": {"type": "str", "choices": ["Enable", "Disable"]},
                "imap": {"type": "str", "choices": ["Enable", "Disable"]},
                "smtp": {"type": "str", "choices": ["Enable", "Disable"]},
                "smtps": {"type": "str", "choices": ["Enable", "Disable"]},
                "pops": {"type": "str", "choices": ["Enable", "Disable"]},
                "imaps": {"type": "str", "choices": ["Enable", "Disable"]}
                    }
                },
            "content_filtering": {"type": "dict", "required": False, "default": {}, "options": {
                "web_filter": {"type": "str", "choices": ["Enable", "Disable"]},
                "application_filter": {"type": "str", "choices": ["Enable", "Disable"]},
                "web_content_policy": {"type": "str", "choices": ["Enable", "Disable"]},
                "ssl_tls": {"type": "str", "choices": ["Enable", "Disable"]}
                    }
                },
            "events": {"type": "dict", "required": False, "default": {}, "options": {
                "admin": {"type": "str", "choices": ["Enable", "Disable"]},
                "authentication": {"type": "str", "choices": ["Enable", "Disable"]},
                "system": {"type": "str", "choices": ["Enable", "Disable"]}
                    }
                },
            "web_server_protection": {"type": "dict", "required": False, "default": {}, "options": {
                "waf_events": {"type": "str", "choices": ["Enable", "Disable"]}
                    }
                },
            "atp": {"type": "dict", "required": False, "default": {}, "options": {
                "atp_events": {"type": "str", "choices": ["Enable", "Disable"]}
                    }
                },
            "wireless": {"type": "dict", "required": False, "default": {}, "options": {
                "access_points_ssid": {"type": "str", "choices": ["Enable", "Disable"]}
                    }
                },
            "heartbeat": {"type": "dict", "required": False, "default": {}, "options": {
                "endpoint_status": {"type": "str", "choices": ["Enable", "Disable"]}
                    }
                },
            "system_health": {"type": "dict", "required": False, "default": {}, "options": {
                "usage": {"type": "str", "choices": ["Enable", "Disable"]}
                    }
                },
            "zeroday_protection": {"type": "dict", "required": False, "default": {}, "options": {
                "zeroday_protection_events": {"type": "str", "choices": ["Enable", "Disable"]}
                    }
                },
            "sdwan": {"type": "dict", "required": False, "default": {}, "options": {
                "profile": {"type": "str", "choices": ["Enable", "Disable"]},
                "sla": {"type": "str", "choices": ["Enable", "Disable"]},
                "route": {"type": "str", "choices": ["Enable", "Disable"]}
                    }
                }
            }
        },
        "state": {"type": "str", "required": True, "choices": ["present", "absent", "updated", "query"]}
    }
    

    required_if = [
        (
            "state",
            "present",
            [
                "address",
                "facility",
                "severity",
                "format"
            ],
            False,
        ),
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

    exist_settings = get_syslog(connection, module, result)
    result["api_response"] = exist_settings["api_response"]

    if state == "query":
        module.exit_json(**result)

    if module.check_mode:
        result["check_mode"] = True
        module.exit_json(**result)

    if state == "present" and not exist_settings["exists"]:
        api_response = create_syslog(connection, module, result)
        if (
            api_response["Response"]["SyslogServers"]["Status"]["#text"]
            == "Configuration applied successfully."
        ):
            result["changed"] = True
            result["api_response"] = api_response

    elif state == "present" and exist_settings["exists"]:
        result["changed"] = False

    elif state == "absent" and exist_settings["exists"]:
        api_response = remove_syslog(connection, module, result)
        if (
            api_response["Response"]["SyslogServers"]["Status"]["#text"]
            == "Configuration applied successfully."
        ):
            result["changed"] = True
        result["api_response"] = api_response

    elif state == "absent" and not exist_settings["exists"]:
        result["changed"] = False

    elif state == "updated" and exist_settings["exists"]:
        if eval_changed(module, exist_settings):
            api_response = update_syslog(connection, exist_settings, module, result)

            if api_response:
                result["api_response"] = api_response
                if (
                    api_response["Response"]["SyslogServers"]["Status"]["#text"]
                    == "Configuration applied successfully."
                ):
                    result["changed"] = True

    elif state == "updated" and not exist_settings["exists"]:
        result["changed"] = False
        module.fail_json(f"Attempting to update non-existing resource: {module.params.get('name')}", **result)

    module.exit_json(**result)


if __name__ == "__main__":
    main()
