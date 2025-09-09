#!/usr/bin/python

# Copyright 2024 Sophos Ltd.  All rights reserved.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: sfos_qos_policy

short_description: Manage QoS Policies (Configure > System Services > Traffic Shaping)

version_added: "2.3.0"

description: Manage QoS Policies (Configure > System Services > Traffic Shaping) on Sophos Firewall

extends_documentation_fragment:
  - sophos.sophos_firewall.fragments.base

options:
    name:
        description: Specify a name for the QoS Policy.
        type: str
        required: true
    policy_type:
        description: Select the type of Policy.
        type: str
        choices: ["Strict", "Committed"]
        required: false
    implementation_on:
        description: Specify implementation strategy of Policy.
        type: str
        choices: ["Total", "Individual"]
        required: false
    priority:
        description: Set the Bandwidth priority.
        type: str
        choices: ["RealTime", "BusinessCritical", "Normal2", "Normal3", "Normal4", "Normal5", "BulkyFTP", "BestEffort"]
        required: true
    policy_based_on:
        description: Select an option for whom the policy is created.
        type: str
        choices: ["User", "Firewall", "Application", "WebCategory"]
        required: false
    bandwidth_usage_type:
        description: Select the type of Bandwidth usage.
        type: str
        choices: ["Individual", "Shared"]
        required: false
    total_bandwidth:
        description: Specify allowed total bandwidth for 'Strict' policy type and 'Total' implementation strategy (KB).
        type: int
        required: false
    guaranteed_bandwidth:
        description: Specify guaranteed bandwidth (minimum) for 'Committed' type and 'Total' strategy (KB).
        type: int
        required: false
    burstable_bandwidth:
        description: Specify burstable bandwidth (maximum) for 'Committed' type and 'Total' strategy (KB).
        type: int
        required: false
    upload_bandwidth:
        description: Specify upload bandwidth for 'Individual' strategy and 'Strict' type (KB).
        type: int
        required: false
    download_bandwidth:
        description: Specify download bandwidth for 'Individual' strategy and 'Strict' type (KB).
        type: int
        required: false
    guaranteed_upload_bandwidth:
        description: Specify guaranteed upload bandwidth (minimum) for 'Committed' type and 'Individual' strategy (KB).
        type: int
        required: false
    burstable_upload_bandwidth:
        description: Specify burstable (maximum) upload bandwidth for 'Committed' type and 'Individual' strategy (KB).
        type: int
        required: false
    guaranteed_download_bandwidth:
        description: Specify guaranteed download bandwidth (minimum) for 'Committed' type and 'Individual' strategy (KB).
        type: int
        required: false
    burstable_download_bandwidth:
        description: Specify burstable (maximum) download bandwidth for 'Committed' type and 'Individual' strategy (KB).
        type: int
        required: false
    description:
        description: Specify policy description.
        type: str
        required: false
    schedule_based_rules:
        description: Specify schedule-wise QoS policy details.
        type: list
        elements: dict
        required: false
        suboptions:
            detail_id:
                description: Detail ID for the schedule rule.
                type: str
                required: true
            policy_type:
                description: Policy type for this schedule rule.
                type: str
                choices: ["Strict", "Committed"]
                required: false
            total_bandwidth:
                description: Total bandwidth for this schedule rule (KB).
                type: int
                required: false
            guaranteed_bandwidth:
                description: Guaranteed bandwidth for this schedule rule (KB).
                type: int
                required: false
            burstable_bandwidth:
                description: Burstable bandwidth for this schedule rule (KB).
                type: int
                required: false
            upload_bandwidth:
                description: Upload bandwidth for this schedule rule (KB).
                type: int
                required: false
            download_bandwidth:
                description: Download bandwidth for this schedule rule (KB).
                type: int
                required: false
            guaranteed_upload_bandwidth:
                description: Guaranteed upload bandwidth for this schedule rule (KB).
                type: int
                required: false
            burstable_upload_bandwidth:
                description: Burstable upload bandwidth for this schedule rule (KB).
                type: int
                required: false
            guaranteed_download_bandwidth:
                description: Guaranteed download bandwidth for this schedule rule (KB).
                type: int
                required: false
            burstable_download_bandwidth:
                description: Burstable download bandwidth for this schedule rule (KB).
                type: int
                required: false
            schedule:
                description: Schedule name for this rule.
                type: str
                required: true
    state:
        description:
            - Use C(query) to retrieve, C(present) to create, C(updated) to modify, or C(absent) to remove
        choices: [present, updated, query, absent]
        type: str
        required: true

author:
    - Matt Mullen (@mamullen13316)
"""

EXAMPLES = r"""
- name: Create QoS Policy - Strict Total
  sophos.sophos_firewall.sfos_qos_policy:
    name: "Strict Total Policy"
    policy_type: "Strict"
    implementation_on: "Total"
    priority: "BusinessCritical"
    policy_based_on: "User"
    bandwidth_usage_type: "Shared"
    total_bandwidth: 1000
    description: "Strict policy with total bandwidth control"
    state: present

- name: Create QoS Policy - Committed Individual
  sophos.sophos_firewall.sfos_qos_policy:
    name: "Committed Individual Policy"
    policy_type: "Committed"
    implementation_on: "Individual"
    priority: "Normal2"
    policy_based_on: "Application"
    bandwidth_usage_type: "Individual"
    guaranteed_upload_bandwidth: 1000
    burstable_upload_bandwidth: 500
    guaranteed_download_bandwidth: 5000
    burstable_download_bandwidth: 2000
    description: "Committed policy with individual bandwidth limits"
    state: present

- name: Create QoS Policy with Schedule-based Rules
  sophos.sophos_firewall.sfos_qos_policy:
    name: "Schedule Based Policy"
    policy_type: "Strict"
    implementation_on: "Total"
    priority: "Normal3"
    policy_based_on: "Firewall"
    bandwidth_usage_type: "Shared"
    total_bandwidth: 2000
    description: "Policy with schedule-based bandwidth rules"
    schedule_based_rules:
      - detail_id: "BusinessHours"
        policy_type: "Strict"
        total_bandwidth: 1500
        schedule: "Business Hours"
      - detail_id: "OffHours"
        policy_type: "Committed"
        guaranteed_bandwidth: 500
        burstable_bandwidth: 1000
        schedule: "Off Hours"
    state: present

- name: Query QoS Policy
  sophos.sophos_firewall.sfos_qos_policy:
    name: "Strict Total Policy"
    state: query

- name: Update QoS Policy
  sophos.sophos_firewall.sfos_qos_policy:
    name: "Strict Total Policy"
    total_bandwidth: 1500
    description: "Updated strict policy"
    state: updated

- name: Remove QoS Policy
  sophos.sophos_firewall.sfos_qos_policy:
    name: "Strict Total Policy"
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


def get_qos_policy(connection, module, result):
    """Get QoS Policy from Sophos Firewall

    Args:
        connection (Connection): Ansible Connection object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: Results of lookup operation
    """
    try:
        resp = connection.invoke_sdk("get_tag_with_filter", module_args={"xml_tag": "QoSPolicy",
                                                                         "key": "Name",
                                                                         "value": module.params.get("name"),
                                                                         "operator": "="})
    except (SophosFirewallAuthFailure, SophosFirewallAPIError, RequestException) as error:
        module.fail_json("An unexpected error occurred: {0}".format(error), **result)

    if resp["success"] and not resp["exists"]:
        return {"exists": False, "api_response": resp["response"]}

    if not resp["success"]:
        module.fail_json(msg="An error occurred: {0}".format(resp["response"]))

    return {"exists": True, "api_response": resp["response"]}


def create_qos_policy(connection, module, result):
    """Create QoS Policy on Sophos Firewall

    Args:
        connection (Connection): Ansible Connection object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: API response
    """
    payload = """
        <QoSPolicy>
            <Name>{{ name }}</Name>
            {% if policy_based_on %}
            <PolicyBasedOn>{{ policy_based_on }}</PolicyBasedOn>
            {% endif %}
            {% if policy_type %}
            <PolicyType>{{ policy_type }}</PolicyType>
            {% endif %}
            {% if implementation_on %}
            <ImplementationOn>{{ implementation_on }}</ImplementationOn>
            {% endif %}
            <Priority>{{ priority }}</Priority>
            {% if bandwidth_usage_type %}
            <BandwidthUsageType>{{ bandwidth_usage_type }}</BandwidthUsageType>
            {% endif %}
            {% if total_bandwidth %}
            <TotalBandwidth>{{ total_bandwidth }}</TotalBandwidth>
            {% endif %}
            {% if guaranteed_bandwidth %}
            <GuaranteedBandwidth>{{ guaranteed_bandwidth }}</GuaranteedBandwidth>
            {% endif %}
            {% if burstable_bandwidth %}
            <BurstableBandwidth>{{ burstable_bandwidth }}</BurstableBandwidth>
            {% endif %}
            {% if upload_bandwidth %}
            <UploadBandwidth>{{ upload_bandwidth }}</UploadBandwidth>
            {% endif %}
            {% if download_bandwidth %}
            <DownloadBandwidth>{{ download_bandwidth }}</DownloadBandwidth>
            {% endif %}
            {% if guaranteed_upload_bandwidth %}
            <GuaranteedUploadBandwidth>{{ guaranteed_upload_bandwidth }}</GuaranteedUploadBandwidth>
            {% endif %}
            {% if burstable_upload_bandwidth %}
            <BurstableUploadBandwidth>{{ burstable_upload_bandwidth }}</BurstableUploadBandwidth>
            {% endif %}
            {% if guaranteed_download_bandwidth %}
            <GuaranteedDownloadBandwidth>{{ guaranteed_download_bandwidth }}</GuaranteedDownloadBandwidth>
            {% endif %}
            {% if burstable_download_bandwidth %}
            <BurstableDownloadBandwidth>{{ burstable_download_bandwidth }}</BurstableDownloadBandwidth>
            {% endif %}
            {% if description %}
            <Description>{{ description }}</Description>
            {% endif %}
            {% if schedule_based_rules %}
            <SchedulebasedPolicyRuleList>
                {% for rule in schedule_based_rules %}
                <Rule>
                    <DetailId>{{ rule.detail_id }}</DetailId>
                    {% if rule.policy_type %}
                    <PolicyType>{{ rule.policy_type }}</PolicyType>
                    {% endif %}
                    {% if rule.total_bandwidth %}
                    <TotalBandwidth>{{ rule.total_bandwidth }}</TotalBandwidth>
                    {% endif %}
                    {% if rule.guaranteed_bandwidth %}
                    <GuaranteedBandwidth>{{ rule.guaranteed_bandwidth }}</GuaranteedBandwidth>
                    {% endif %}
                    {% if rule.burstable_bandwidth %}
                    <BurstableBandwidth>{{ rule.burstable_bandwidth }}</BurstableBandwidth>
                    {% endif %}
                    {% if rule.upload_bandwidth %}
                    <UploadBandwidth>{{ rule.upload_bandwidth }}</UploadBandwidth>
                    {% endif %}
                    {% if rule.download_bandwidth %}
                    <DownloadBandwidth>{{ rule.download_bandwidth }}</DownloadBandwidth>
                    {% endif %}
                    {% if rule.guaranteed_upload_bandwidth %}
                    <GuaranteedUploadBandwidth>{{ rule.guaranteed_upload_bandwidth }}</GuaranteedUploadBandwidth>
                    {% endif %}
                    {% if rule.burstable_upload_bandwidth %}
                    <BurstableUploadBandwidth>{{ rule.burstable_upload_bandwidth }}</BurstableUploadBandwidth>
                    {% endif %}
                    {% if rule.guaranteed_download_bandwidth %}
                    <GuaranteedDownloadBandwidth>{{ rule.guaranteed_download_bandwidth }}</GuaranteedDownloadBandwidth>
                    {% endif %}
                    {% if rule.burstable_download_bandwidth %}
                    <BurstableDownloadBandwidth>{{ rule.burstable_download_bandwidth }}</BurstableDownloadBandwidth>
                    {% endif %}
                    <Schedule>{{ rule.schedule }}</Schedule>
                </Rule>
                {% endfor %}
            </SchedulebasedPolicyRuleList>
            {% endif %}
        </QoSPolicy>
    """
    
    template_vars = {
        "name": module.params.get("name"),
        "policy_based_on": module.params.get("policy_based_on"),
        "policy_type": module.params.get("policy_type"),
        "implementation_on": module.params.get("implementation_on"),
        "priority": module.params.get("priority"),
        "bandwidth_usage_type": module.params.get("bandwidth_usage_type"),
        "total_bandwidth": module.params.get("total_bandwidth"),
        "guaranteed_bandwidth": module.params.get("guaranteed_bandwidth"),
        "burstable_bandwidth": module.params.get("burstable_bandwidth"),
        "upload_bandwidth": module.params.get("upload_bandwidth"),
        "download_bandwidth": module.params.get("download_bandwidth"),
        "guaranteed_upload_bandwidth": module.params.get("guaranteed_upload_bandwidth"),
        "burstable_upload_bandwidth": module.params.get("burstable_upload_bandwidth"),
        "guaranteed_download_bandwidth": module.params.get("guaranteed_download_bandwidth"),
        "burstable_download_bandwidth": module.params.get("burstable_download_bandwidth"),
        "description": module.params.get("description"),
        "schedule_based_rules": module.params.get("schedule_based_rules")
    }
    
    try:
        with contextlib.redirect_stdout(output_buffer):
            resp = connection.invoke_sdk("submit_xml", module_args={
                "template_data": payload,
                "template_vars": template_vars,
                "timeout": 90,
                "debug": True
                }
            )
    except (SophosFirewallAuthFailure, SophosFirewallAPIError, RequestException) as error:
        module.fail_json("An unexpected error occurred: {0}".format(error), **result)

    if not resp["success"]:
        module.fail_json(msg="An error occurred: {0}".format(resp["response"]))

    return resp["response"]


def update_qos_policy(connection, exist_settings, module, result):
    """Update QoS Policy configuration on Sophos Firewall

    Args:
        connection (Connection): Ansible Connection object
        exist_settings (dict): API response containing existing QoS Policy
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: API response
    """
    update_params = {}
    existing_policy = exist_settings["api_response"]["Response"]["QoSPolicy"]
    
    update_params["Name"] = module.params.get("name")

    # Use provided values if given, otherwise use existing values
    update_params["PolicyBasedOn"] = (module.params.get("policy_based_on") 
                                    if module.params.get("policy_based_on") is not None 
                                    else existing_policy.get("PolicyBasedOn"))

    update_params["PolicyType"] = (module.params.get("policy_type") 
                                 if module.params.get("policy_type") is not None 
                                 else existing_policy.get("PolicyType"))

    update_params["ImplementationOn"] = (module.params.get("implementation_on") 
                                       if module.params.get("implementation_on") is not None 
                                       else existing_policy.get("ImplementationOn"))

    update_params["Priority"] = (module.params.get("priority") 
                               if module.params.get("priority") is not None 
                               else existing_policy.get("Priority"))

    update_params["BandwidthUsageType"] = (module.params.get("bandwidth_usage_type") 
                                         if module.params.get("bandwidth_usage_type") is not None 
                                         else existing_policy.get("BandwidthUsageType"))

    # Bandwidth parameters
    if module.params.get("total_bandwidth") is not None:
        update_params["TotalBandwidth"] = module.params.get("total_bandwidth")
    elif existing_policy.get("TotalBandwidth"):
        update_params["TotalBandwidth"] = existing_policy.get("TotalBandwidth")

    if module.params.get("guaranteed_bandwidth") is not None:
        update_params["GuaranteedBandwidth"] = module.params.get("guaranteed_bandwidth")
    elif existing_policy.get("GuaranteedBandwidth"):
        update_params["GuaranteedBandwidth"] = existing_policy.get("GuaranteedBandwidth")

    if module.params.get("burstable_bandwidth") is not None:
        update_params["BurstableBandwidth"] = module.params.get("burstable_bandwidth")
    elif existing_policy.get("BurstableBandwidth"):
        update_params["BurstableBandwidth"] = existing_policy.get("BurstableBandwidth")

    if module.params.get("upload_bandwidth") is not None:
        update_params["UploadBandwidth"] = module.params.get("upload_bandwidth")
    elif existing_policy.get("UploadBandwidth"):
        update_params["UploadBandwidth"] = existing_policy.get("UploadBandwidth")

    if module.params.get("download_bandwidth") is not None:
        update_params["DownloadBandwidth"] = module.params.get("download_bandwidth")
    elif existing_policy.get("DownloadBandwidth"):
        update_params["DownloadBandwidth"] = existing_policy.get("DownloadBandwidth")

    if module.params.get("guaranteed_upload_bandwidth") is not None:
        update_params["GuaranteedUploadBandwidth"] = module.params.get("guaranteed_upload_bandwidth")
    elif existing_policy.get("GuaranteedUploadBandwidth"):
        update_params["GuaranteedUploadBandwidth"] = existing_policy.get("GuaranteedUploadBandwidth")

    if module.params.get("burstable_upload_bandwidth") is not None:
        update_params["BurstableUploadBandwidth"] = module.params.get("burstable_upload_bandwidth")
    elif existing_policy.get("BurstableUploadBandwidth"):
        update_params["BurstableUploadBandwidth"] = existing_policy.get("BurstableUploadBandwidth")

    if module.params.get("guaranteed_download_bandwidth") is not None:
        update_params["GuaranteedDownloadBandwidth"] = module.params.get("guaranteed_download_bandwidth")
    elif existing_policy.get("GuaranteedDownloadBandwidth"):
        update_params["GuaranteedDownloadBandwidth"] = existing_policy.get("GuaranteedDownloadBandwidth")

    if module.params.get("burstable_download_bandwidth") is not None:
        update_params["BurstableDownloadBandwidth"] = module.params.get("burstable_download_bandwidth")
    elif existing_policy.get("BurstableDownloadBandwidth"):
        update_params["BurstableDownloadBandwidth"] = existing_policy.get("BurstableDownloadBandwidth")

    if module.params.get("description") is not None:
        update_params["Description"] = module.params.get("description")
    elif existing_policy.get("Description"):
        update_params["Description"] = existing_policy.get("Description")

    # Handle schedule-based rules if provided
    if module.params.get("schedule_based_rules") is not None:
        update_params["SchedulebasedPolicyRuleList"] = []
        for rule in module.params.get("schedule_based_rules"):
            rule_params = {
                "DetailId": rule.get("detail_id"),
                "Schedule": rule.get("schedule")
            }
            
            if rule.get("policy_type"):
                rule_params["PolicyType"] = rule.get("policy_type")
            if rule.get("total_bandwidth"):
                rule_params["TotalBandwidth"] = rule.get("total_bandwidth")
            if rule.get("guaranteed_bandwidth"):
                rule_params["GuaranteedBandwidth"] = rule.get("guaranteed_bandwidth")
            if rule.get("burstable_bandwidth"):
                rule_params["BurstableBandwidth"] = rule.get("burstable_bandwidth")
            if rule.get("upload_bandwidth"):
                rule_params["UploadBandwidth"] = rule.get("upload_bandwidth")
            if rule.get("download_bandwidth"):
                rule_params["DownloadBandwidth"] = rule.get("download_bandwidth")
            if rule.get("guaranteed_upload_bandwidth"):
                rule_params["GuaranteedUploadBandwidth"] = rule.get("guaranteed_upload_bandwidth")
            if rule.get("burstable_upload_bandwidth"):
                rule_params["BurstableUploadBandwidth"] = rule.get("burstable_upload_bandwidth")
            if rule.get("guaranteed_download_bandwidth"):
                rule_params["GuaranteedDownloadBandwidth"] = rule.get("guaranteed_download_bandwidth")
            if rule.get("burstable_download_bandwidth"):
                rule_params["BurstableDownloadBandwidth"] = rule.get("burstable_download_bandwidth")
            
            update_params["SchedulebasedPolicyRuleList"].append({"Rule": rule_params})
    elif existing_policy.get("SchedulebasedPolicyRuleList"):
        # Preserve existing schedule rules if none provided
        update_params["SchedulebasedPolicyRuleList"] = existing_policy.get("SchedulebasedPolicyRuleList")

    try:
        with contextlib.redirect_stdout(output_buffer):
            resp = connection.invoke_sdk("update", module_args={
                "xml_tag": "QoSPolicy",
                "update_params": update_params,
                "name": module.params.get("name"),
                "lookup_key": "Name",
                "timeout": 90,
                "debug": True
            })
    except (SophosFirewallAuthFailure, SophosFirewallAPIError, RequestException) as error:
        module.fail_json("An unexpected error occurred: {0}".format(error), **result)

    if not resp["success"]:
        module.fail_json(msg="An error occurred: {0}".format(resp["response"]))

    return resp["response"]


def remove_qos_policy(connection, module, result):
    """Remove QoS Policy from Sophos Firewall

    Args:
        connection (Connection): Ansible Connection object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: API response
    """
    try:
        resp = connection.invoke_sdk("remove", module_args={"xml_tag": "QoSPolicy", "name": module.params.get("name")})
    except (SophosFirewallAuthFailure, SophosFirewallAPIError, RequestException) as error:
        module.fail_json("An unexpected error occurred: {0}".format(error), **result)

    if not resp["success"]:
        module.fail_json(msg="An error occurred: {0}".format(resp["response"]))

    return resp["response"]


def eval_changed(module, exist_settings):
    """Evaluate the provided arguments against existing settings.

    Args:
        module (AnsibleModule): AnsibleModule object
        exist_settings (dict): Response from the 'get' operation

    Returns:
        bool: Return true if the two do not match
    """
    exist_policy = exist_settings["api_response"]["Response"]["QoSPolicy"]
    
    # Check basic parameters
    if module.params.get("policy_type") and module.params.get("policy_type") != exist_policy.get("PolicyType"):
        return True
    
    if module.params.get("implementation_on") and module.params.get("implementation_on") != exist_policy.get("ImplementationOn"):
        return True
    
    if module.params.get("priority") and module.params.get("priority") != exist_policy.get("Priority"):
        return True
    
    if module.params.get("policy_based_on") and module.params.get("policy_based_on") != exist_policy.get("PolicyBasedOn"):
        return True
    
    if module.params.get("bandwidth_usage_type") and module.params.get("bandwidth_usage_type") != exist_policy.get("BandwidthUsageType"):
        return True
    
    if module.params.get("description") and module.params.get("description") != exist_policy.get("Description"):
        return True

    # Check bandwidth parameters
    bandwidth_params = [
        ("total_bandwidth", "TotalBandwidth"),
        ("guaranteed_bandwidth", "GuaranteedBandwidth"),
        ("burstable_bandwidth", "BurstableBandwidth"),
        ("upload_bandwidth", "UploadBandwidth"),
        ("download_bandwidth", "DownloadBandwidth"),
        ("guaranteed_upload_bandwidth", "GuaranteedUploadBandwidth"),
        ("burstable_upload_bandwidth", "BurstableUploadBandwidth"),
        ("guaranteed_download_bandwidth", "GuaranteedDownloadBandwidth"),
        ("burstable_download_bandwidth", "BurstableDownloadBandwidth")
    ]
    
    for param_name, api_key in bandwidth_params:
        if (module.params.get(param_name) is not None and 
            module.params.get(param_name) != exist_policy.get(api_key)):
            return True
    
    # Check schedule-based rules if provided
    if module.params.get("schedule_based_rules") is not None:
        # For simplicity, consider rules changed if they are provided
        return True

    return False


def validate_parameters(module, result):
    """Validate module parameters.
    
    Args:
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console
        
    Returns:
        bool: True if validation passes, False otherwise
    """
    # Validate name length
    if len(module.params.get("name")) > 50:
        module.fail_json(
            msg="Name must be 50 characters or less",
            **result
        )
    
    # Validate description length if provided
    if module.params.get("description") and len(module.params.get("description")) > 255:
        module.fail_json(
            msg="Description must be 255 characters or less",
            **result
        )
    
    # Validate bandwidth ranges (2-10240000 KB)
    bandwidth_params = [
        "total_bandwidth", "guaranteed_bandwidth", "burstable_bandwidth",
        "upload_bandwidth", "download_bandwidth", "guaranteed_upload_bandwidth",
        "burstable_upload_bandwidth", "guaranteed_download_bandwidth", 
        "burstable_download_bandwidth"
    ]
    
    for param in bandwidth_params:
        value = module.params.get(param)
        if value is not None and not (2 <= value <= 10240000):
            module.fail_json(
                msg=f"{param} must be between 2 and 10240000 KB",
                **result
            )
    
    # Validate that burstable bandwidth is greater than guaranteed bandwidth
    if (module.params.get("guaranteed_bandwidth") is not None and 
        module.params.get("burstable_bandwidth") is not None):
        if module.params.get("burstable_bandwidth") <= module.params.get("guaranteed_bandwidth"):
            module.fail_json(
                msg="Burstable bandwidth must be greater than guaranteed bandwidth",
                **result
            )
    
    if (module.params.get("guaranteed_upload_bandwidth") is not None and 
        module.params.get("burstable_upload_bandwidth") is not None):
        if module.params.get("burstable_upload_bandwidth") <= module.params.get("guaranteed_upload_bandwidth"):
            module.fail_json(
                msg="Burstable upload bandwidth must be greater than guaranteed upload bandwidth",
                **result
            )
    
    if (module.params.get("guaranteed_download_bandwidth") is not None and 
        module.params.get("burstable_download_bandwidth") is not None):
        if module.params.get("burstable_download_bandwidth") <= module.params.get("guaranteed_download_bandwidth"):
            module.fail_json(
                msg="Burstable download bandwidth must be greater than guaranteed download bandwidth",
                **result
            )
    
    # Policy-specific parameter requirements
    policy_type = module.params.get("policy_type")
    implementation_on = module.params.get("implementation_on")
    
    # Only validate these requirements for 'present' state
    if module.params.get("state") == "present":
        # Strict + Total: total_bandwidth is required
        if policy_type == "Strict" and implementation_on == "Total":
            if module.params.get("total_bandwidth") is None:
                module.fail_json(
                    msg="total_bandwidth is required when policy_type=Strict and implementation_on=Total",
                    **result
                )
        
        # Strict + Individual: upload_bandwidth and download_bandwidth are required
        if policy_type == "Strict" and implementation_on == "Individual":
            if module.params.get("upload_bandwidth") is None:
                module.fail_json(
                    msg="upload_bandwidth is required when policy_type=Strict and implementation_on=Individual",
                    **result
                )
            if module.params.get("download_bandwidth") is None:
                module.fail_json(
                    msg="download_bandwidth is required when policy_type=Strict and implementation_on=Individual",
                    **result
                )
        
        # Committed + Total: guaranteed_bandwidth and burstable_bandwidth are required
        if policy_type == "Committed" and implementation_on == "Total":
            if module.params.get("guaranteed_bandwidth") is None:
                module.fail_json(
                    msg="guaranteed_bandwidth is required when policy_type=Committed and implementation_on=Total",
                    **result
                )
            if module.params.get("burstable_bandwidth") is None:
                module.fail_json(
                    msg="burstable_bandwidth is required when policy_type=Committed and implementation_on=Total",
                    **result
                )
        
        # Committed + Individual: all four individual committed parameters are required
        if policy_type == "Committed" and implementation_on == "Individual":
            required_params = [
                ("guaranteed_upload_bandwidth", "guaranteed_upload_bandwidth is required when policy_type=Committed and implementation_on=Individual"),
                ("burstable_upload_bandwidth", "burstable_upload_bandwidth is required when policy_type=Committed and implementation_on=Individual"),
                ("guaranteed_download_bandwidth", "guaranteed_download_bandwidth is required when policy_type=Committed and implementation_on=Individual"),
                ("burstable_download_bandwidth", "burstable_download_bandwidth is required when policy_type=Committed and implementation_on=Individual")
            ]
            
            for param_name, error_msg in required_params:
                if module.params.get(param_name) is None:
                    module.fail_json(msg=error_msg, **result)
    
    return True


def main():
    """Code executed at run time."""
    argument_spec = {
        "name": {"type": "str", "required": True},
        "policy_type": {"type": "str", "choices": ["Strict", "Committed"], "required": False},
        "implementation_on": {"type": "str", "choices": ["Total", "Individual"], "required": False},
        "priority": {"type": "str", "choices": ["RealTime", "BusinessCritical", "Normal2", "Normal3", "Normal4", "Normal5", "BulkyFTP", "BestEffort"], "required": False},
        "policy_based_on": {"type": "str", "choices": ["User", "Firewall", "Application", "WebCategory"], "required": False},
        "bandwidth_usage_type": {"type": "str", "choices": ["Individual", "Shared"], "required": False},
        "total_bandwidth": {"type": "int", "required": False},
        "guaranteed_bandwidth": {"type": "int", "required": False},
        "burstable_bandwidth": {"type": "int", "required": False},
        "upload_bandwidth": {"type": "int", "required": False},
        "download_bandwidth": {"type": "int", "required": False},
        "guaranteed_upload_bandwidth": {"type": "int", "required": False},
        "burstable_upload_bandwidth": {"type": "int", "required": False},
        "guaranteed_download_bandwidth": {"type": "int", "required": False},
        "burstable_download_bandwidth": {"type": "int", "required": False},
        "description": {"type": "str", "required": False},
        "schedule_based_rules": {
            "type": "list", 
            "elements": "dict", 
            "required": False,
            "options": {
                "detail_id": {"type": "str", "required": True},
                "policy_type": {"type": "str", "choices": ["Strict", "Committed"], "required": False},
                "total_bandwidth": {"type": "int", "required": False},
                "guaranteed_bandwidth": {"type": "int", "required": False},
                "burstable_bandwidth": {"type": "int", "required": False},
                "upload_bandwidth": {"type": "int", "required": False},
                "download_bandwidth": {"type": "int", "required": False},
                "guaranteed_upload_bandwidth": {"type": "int", "required": False},
                "burstable_upload_bandwidth": {"type": "int", "required": False},
                "guaranteed_download_bandwidth": {"type": "int", "required": False},
                "burstable_download_bandwidth": {"type": "int", "required": False},
                "schedule": {"type": "str", "required": True}
            }
        },
        "state": {"type": "str", "required": True, "choices": ["present", "updated", "query", "absent"]},
    }

    required_if = [
        (
            "state",
            "present",
            [
                "name",
                "priority"
            ],
            False,
        ),
        (
            "state",
            "updated",
            [
                "name"
            ],
            False,
        ),
        (
            "state",
            "query",
            [
                "name"
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
    
    # Validate parameters
    if module.params.get("state") in ["present", "updated"]:
        validate_parameters(module, result)

    state = module.params.get("state")

    try:
        # pylint: disable=protected-access
        connection = Connection(module._socket_path)
    except AssertionError:
        module.fail_json(msg="Connection error: Ensure you are targeting a remote host and not using 'delegate_to: localhost'.")

    if not hasattr(connection, "httpapi"):
        module.fail_json(msg="HTTPAPI plugin is not initialized. Ensure the connection is set to 'httpapi'.")

    exist_settings = get_qos_policy(connection, module, result)
    result["api_response"] = exist_settings["api_response"]

    if state == "query":
        module.exit_json(**result)

    if module.check_mode:
        result["check_mode"] = True
        module.exit_json(**result)

    if state == "present" and not exist_settings["exists"]:
        api_response = create_qos_policy(connection, module, result)

        if (
            "Configuration applied successfully" in api_response["Response"]["QoSPolicy"]["Status"]["#text"]
        ) or ("Unable to get status message" in api_response["Response"]["QoSPolicy"]["Status"]["#text"]) or (
            api_response["Response"]["QoSPolicy"]["Status"]["@code"] in ["200", "217"]
        ):
            result["changed"] = True
            result["api_response"] = api_response

    elif state == "present" and exist_settings["exists"]:
        result["changed"] = False

    elif state == "absent" and exist_settings["exists"]:
        api_response = remove_qos_policy(connection, module, result)
        if (
            "Configuration applied successfully" in api_response["Response"]["QoSPolicy"]["Status"]["#text"]
        ) or (
            api_response["Response"]["QoSPolicy"]["Status"]["@code"] in ["200", "217"]
        ):
            result["changed"] = True
        result["api_response"] = api_response

    elif state == "absent" and not exist_settings["exists"]:
        result["changed"] = False

    elif state == "updated" and exist_settings["exists"]:
        if eval_changed(module, exist_settings):
            api_response = update_qos_policy(connection, exist_settings, module, result)

            if api_response:
                result["api_response"] = api_response
                if (
                    "Configuration applied successfully" in api_response["Response"]["QoSPolicy"]["Status"]["#text"]
                ) or (
                    api_response["Response"]["QoSPolicy"]["Status"]["@code"] in ["200", "217"]
                ):
                    result["changed"] = True
    
    elif state == "updated" and not exist_settings["exists"]:
        result["changed"] = False
        module.fail_json(exist_settings["api_response"], **result)

    module.exit_json(**result)


if __name__ == "__main__":
    main()
