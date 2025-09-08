#!/usr/bin/python

# Copyright 2024 Sophos Ltd.  All rights reserved.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: sfos_web_policy

short_description: Manage Web Filter Policies (Protect > Web > Policies)

version_added: "2.3.0"

description: Manage Web Filter Policies (Protect > Web > Policies) on Sophos Firewall

extends_documentation_fragment:
  - sophos.sophos_firewall.fragments.base

options:
    name:
        description: Specify a name for the Web Filter Policy.
        type: str
        required: true
    default_action:
        description: Default action of the policy.
        type: str
        choices: ["Allow", "Deny"]
        required: true
    download_file_size_restriction:
        description: Specify maximum allowed file download size in MB (0-1536).
        type: int
        required: false
        default: 0
    enable_reporting:
        description: Select to enable reporting of policy.
        type: str
        choices: ["Enable", "Disable"]
        required: false
        default: "Enable"
    download_file_size_restriction_enabled:
        description: Enable or disable checking for maximum allowed file download size.
        type: bool
        required: false
    goog_app_domain_list:
        description: Comma-separated list of domains allowed to access Google services. Max 256 chars.
        type: str
        required: false
    goog_app_domain_list_enabled:
        description: Enable or disable specifying domains for Google services.
        type: bool
        required: false
    youtube_filter_is_strict:
        description: Adjust the policy used for YouTube Restricted Mode (true for strict, false for moderate).
        type: bool
        required: false
    youtube_filter_enabled:
        description: Enable or disable YouTube Restricted Mode.
        type: bool
        required: false
    enforce_safe_search:
        description: Enable or disable blocking of pornography and explicit content in search results.
        type: bool
        required: false
    enforce_image_licensing:
        description: Enable or disable limiting search results to Creative Commons licensed images.
        type: bool
        required: false
    xff_enabled:
        description: Enable or disable X-Forwarded-For header.
        type: bool
        required: false
    office_365_tenants_list:
        description: Comma-separated list of domain names and domain IDs allowed to access Microsoft 365. Max 4096 chars.
        type: str
        required: false
    office_365_directory_id:
        description: Domain ID allowed to access the Microsoft 365 service. Max 50 chars.
        type: str
        required: false
    office_365_enabled:
        description: Turn on or off specifying domains/IDs for Microsoft 365.
        type: bool
        required: false
    quota_limit:
        description: Maximum allowed time (1-1440 minutes) for browsing restricted web content under quota policy action.
        type: int
        required: false
        default: 60
    description:
        description: Specify Policy description. Max 255 chars.
        type: str
        required: false
    rules:
        description: Specify the rules contained in this policy.
        type: list
        elements: dict
        required: false
        suboptions:
            categories:
                description: List of rule categories.
                type: list
                elements: dict
                required: true
                suboptions:
                    id:
                        description: Category Name.
                        type: str
                        required: true
                    type:
                        description: Category type.
                        type: str
                        choices: ["WebCategory", "FileType", "URLGroup", "UserActivity"]
                        required: true
            http_action:
                description: HTTP action.
                type: str
                choices: ["Allow", "Deny"]
                required: false
                default: "Deny"
            https_action:
                description: HTTPS action.
                type: str
                choices: ["Allow", "Deny"]
                required: false
                default: "Deny"
            follow_http_action:
                description: Enable or disable following HTTP action.
                type: bool
                required: false
                default: true
            schedule:
                description: Schedule name.
                type: str
                required: false
                default: "All The Time"
            policy_rule_enabled:
                description: Enable or disable the policy rule.
                type: bool
                required: false
                default: true
            user_list:
                description: List of users to which the policy applies.
                type: list
                elements: str
                required: false
                default: []
            ccl_rule_enabled:
                description: Enable or disable CCL rule.
                type: bool
                required: false
                default: false
    rule_action:
        description: Action for rules when updating policies ('add' or 'replace'). To remove rules, use 'replace' with the new complete list.
        type: str
        choices: ["add", "replace"]
        required: false
        default: "add"
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
- name: Create Web Filter Policy with basic settings
  sophos.sophos_firewall.sfos_web_policy:
    name: "Corporate Policy"
    default_action: "Allow"
    enable_reporting: "Enable"
    description: "Corporate web filtering policy"
    state: present

- name: Create Web Filter Policy with file size restriction
  sophos.sophos_firewall.sfos_web_policy:
    name: "Corporate Policy with Size Limit"
    default_action: "Allow"
    download_file_size_restriction: 100
    enable_reporting: "Enable"
    description: "Corporate web filtering policy with 100MB file size limit"
    state: present

- name: Create Web Filter Policy with advanced settings
  sophos.sophos_firewall.sfos_web_policy:
    name: "Strict Policy"
    default_action: "Deny"
    download_file_size_restriction: 50
    enable_reporting: "Enable"
    download_file_size_restriction_enabled: true
    youtube_filter_enabled: true
    youtube_filter_is_strict: true
    enforce_safe_search: true
    enforce_image_licensing: true
    quota_limit: 30
    description: "Strict web filtering policy with content restrictions"
    state: present

- name: Create Web Filter Policy with rules
  sophos.sophos_firewall.sfos_web_policy:
    name: "Business Policy"
    default_action: "Allow"
    download_file_size_restriction: 200
    enable_reporting: "Enable"
    description: "Business policy with category rules"
    rules:
      - categories:
          - id: "Social Networking"
            type: "WebCategory"
          - id: "Gaming"
            type: "WebCategory"
        http_action: "Deny"
        https_action: "Deny"
        schedule: "Business Hours"
        policy_rule_enabled: true
        user_list:
          - "Guest Group"
          - "Unknown Users"
      - categories:
          - id: "Document Files"
            type: "FileType"
        http_action: "Allow"
        https_action: "Allow"
        policy_rule_enabled: true
    state: present

- name: Create Web Filter Policy with Office 365 and Google settings
  sophos.sophos_firewall.sfos_web_policy:
    name: "Cloud Services Policy"
    default_action: "Allow"
    download_file_size_restriction: 500
    enable_reporting: "Enable"
    goog_app_domain_list: "example.com,test.org"
    goog_app_domain_list_enabled: true
    office_365_tenants_list: "tenant1.onmicrosoft.com,tenant2.onmicrosoft.com"
    office_365_directory_id: "12345678-1234-1234-1234-123456789012"
    office_365_enabled: true
    xff_enabled: true
    description: "Policy for cloud services access"
    state: present

- name: Query Web Filter Policy
  sophos.sophos_firewall.sfos_web_policy:
    name: "Corporate Policy"
    state: query

- name: Update Web Filter Policy
  sophos.sophos_firewall.sfos_web_policy:
    name: "Corporate Policy"
    default_action: "Deny"
    download_file_size_restriction: 75
    description: "Updated corporate policy"
    state: updated

- name: Update Web Filter Policy and replace all rules
  sophos.sophos_firewall.sfos_web_policy:
    name: "Business Policy"
    description: "Updated business policy with new rules"
    rules:
      - categories:
          - id: "Entertainment"
            type: "WebCategory"
        http_action: "Deny"
        https_action: "Deny"
        policy_rule_enabled: true
    rule_action: "replace"
    state: updated

- name: Update Web Filter Policy and add additional rules
  sophos.sophos_firewall.sfos_web_policy:
    name: "Business Policy"
    description: "Business policy with additional rules"
    rules:
      - categories:
          - id: "Video Files"
            type: "FileType"
        http_action: "Allow"
        https_action: "Allow"
        policy_rule_enabled: true
    rule_action: "add"
    state: updated

- name: Remove Web Filter Policy
  sophos.sophos_firewall.sfos_web_policy:
    name: "Corporate Policy"
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


def bool_to_str(value):
    """Convert boolean value to string representation for API calls.
    
    Args:
        value (bool or None): Boolean value to convert
        
    Returns:
        str or None: "1" for True, "0" for False, None for None
    """
    if value is True:
        return "1"
    elif value is False:
        return "0"
    else:
        return None


def get_web_policy(connection, module, result):
    """Get Web Filter Policy from Sophos Firewall

    Args:
        connection (Connection): Ansible Connection object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: Results of lookup operation
    """
    try:
        resp = connection.invoke_sdk("get_webfilterpolicy", module_args={"name": module.params.get("name")})
    except (SophosFirewallAuthFailure, SophosFirewallAPIError, RequestException) as error:
        module.fail_json("An unexpected error occurred: {0}".format(error), **result)

    if resp["success"] and not resp["exists"]:
        return {"exists": False, "api_response": resp["response"]}

    if not resp["success"]:
        module.fail_json(msg="An error occurred: {0}".format(resp["response"]))

    return {"exists": True, "api_response": resp["response"]}


def create_web_policy(connection, module, result):
    """Create Web Filter Policy on Sophos Firewall

    Args:
        connection (Connection): Ansible Connection object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: API response
    """
    # Prepare the arguments for the SDK method
    create_args = {
        "name": module.params.get("name"),
        "default_action": module.params.get("default_action"),
        "download_file_size_restriction": str(module.params.get("download_file_size_restriction"))
    }

    # Add optional parameters if provided
    if module.params.get("enable_reporting") is not None:
        create_args["enable_reporting"] = module.params.get("enable_reporting")
    
    if module.params.get("download_file_size_restriction_enabled") is not None:
        create_args["download_file_size_restriction_enabled"] = bool_to_str(module.params.get("download_file_size_restriction_enabled"))
    
    if module.params.get("goog_app_domain_list") is not None:
        create_args["goog_app_domain_list"] = module.params.get("goog_app_domain_list")
    
    if module.params.get("goog_app_domain_list_enabled") is not None:
        create_args["goog_app_domain_list_enabled"] = bool_to_str(module.params.get("goog_app_domain_list_enabled"))
    
    if module.params.get("youtube_filter_is_strict") is not None:
        create_args["youtube_filter_is_strict"] = bool_to_str(module.params.get("youtube_filter_is_strict"))
    
    if module.params.get("youtube_filter_enabled") is not None:
        create_args["youtube_filter_enabled"] = bool_to_str(module.params.get("youtube_filter_enabled"))
    
    if module.params.get("enforce_safe_search") is not None:
        create_args["enforce_safe_search"] = bool_to_str(module.params.get("enforce_safe_search"))
    
    if module.params.get("enforce_image_licensing") is not None:
        create_args["enforce_image_licensing"] = bool_to_str(module.params.get("enforce_image_licensing"))
    
    if module.params.get("xff_enabled") is not None:
        create_args["xff_enabled"] = bool_to_str(module.params.get("xff_enabled"))
    
    if module.params.get("office_365_tenants_list") is not None:
        create_args["office_365_tenants_list"] = module.params.get("office_365_tenants_list")
    
    if module.params.get("office_365_directory_id") is not None:
        create_args["office_365_directory_id"] = module.params.get("office_365_directory_id")
    
    if module.params.get("office_365_enabled") is not None:
        create_args["office_365_enabled"] = bool_to_str(module.params.get("office_365_enabled"))
    
    if module.params.get("quota_limit") is not None:
        create_args["quota_limit"] = module.params.get("quota_limit")
    
    if module.params.get("description") is not None:
        create_args["description"] = module.params.get("description")
    
    if module.params.get("rules") is not None:
        # Convert boolean values in rules to string format
        processed_rules = []
        for rule in module.params.get("rules"):
            processed_rule = rule.copy()
            if "follow_http_action" in processed_rule:
                processed_rule["follow_http_action"] = bool_to_str(processed_rule["follow_http_action"])
            if "policy_rule_enabled" in processed_rule:
                processed_rule["policy_rule_enabled"] = bool_to_str(processed_rule["policy_rule_enabled"])
            if "ccl_rule_enabled" in processed_rule:
                processed_rule["ccl_rule_enabled"] = bool_to_str(processed_rule["ccl_rule_enabled"])
            processed_rules.append(processed_rule)
        create_args["rules"] = processed_rules

    try:
        with contextlib.redirect_stdout(output_buffer):
            resp = connection.invoke_sdk("create_webfilterpolicy", module_args=create_args)
    except (SophosFirewallAuthFailure, SophosFirewallAPIError, RequestException) as error:
        module.fail_json("An unexpected error occurred: {0}".format(error), **result)

    if not resp["success"]:
        module.fail_json(msg="An error occurred: {0}".format(resp["response"]))

    return resp["response"]


def update_web_policy(connection, exist_settings, module, result):
    """Update Web Filter Policy configuration on Sophos Firewall

    Args:
        connection (Connection): Ansible Connection object
        exist_settings (dict): API response containing existing Web Filter Policy
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: API response
    """

    # Use exist_settings for reference and add to update args if not provided
    existing_policy = exist_settings["Response"]["WebFilterPolicy"]
    
    # Prepare the arguments for the SDK method
    update_args = {
        "name": module.params.get("name")
    }

    # Add parameters that need to be updated, using existing values as fallback
    if module.params.get("default_action") is not None:
        update_args["default_action"] = module.params.get("default_action")
    elif existing_policy.get("DefaultAction"):
        update_args["default_action"] = existing_policy.get("DefaultAction")
    
    if module.params.get("download_file_size_restriction") is not None:
        update_args["download_file_size_restriction"] = str(module.params.get("download_file_size_restriction"))
    elif existing_policy.get("DownloadFileSizeRestriction"):
        update_args["download_file_size_restriction"] = existing_policy.get("DownloadFileSizeRestriction")
    
    if module.params.get("enable_reporting") is not None:
        update_args["enable_reporting"] = module.params.get("enable_reporting")
    
    if module.params.get("download_file_size_restriction_enabled") is not None:
        update_args["download_file_size_restriction_enabled"] = bool_to_str(module.params.get("download_file_size_restriction_enabled"))
    
    if module.params.get("goog_app_domain_list") is not None:
        update_args["goog_app_domain_list"] = module.params.get("goog_app_domain_list")
    
    if module.params.get("goog_app_domain_list_enabled") is not None:
        update_args["goog_app_domain_list_enabled"] = bool_to_str(module.params.get("goog_app_domain_list_enabled"))
    
    if module.params.get("youtube_filter_is_strict") is not None:
        update_args["youtube_filter_is_strict"] = bool_to_str(module.params.get("youtube_filter_is_strict"))
    
    if module.params.get("youtube_filter_enabled") is not None:
        update_args["youtube_filter_enabled"] = bool_to_str(module.params.get("youtube_filter_enabled"))
    
    if module.params.get("enforce_safe_search") is not None:
        update_args["enforce_safe_search"] = bool_to_str(module.params.get("enforce_safe_search"))
    
    if module.params.get("enforce_image_licensing") is not None:
        update_args["enforce_image_licensing"] = bool_to_str(module.params.get("enforce_image_licensing"))
    
    if module.params.get("xff_enabled") is not None:
        update_args["xff_enabled"] = bool_to_str(module.params.get("xff_enabled"))
    
    if module.params.get("office_365_tenants_list") is not None:
        update_args["office_365_tenants_list"] = module.params.get("office_365_tenants_list")
    
    if module.params.get("office_365_directory_id") is not None:
        update_args["office_365_directory_id"] = module.params.get("office_365_directory_id")
    
    if module.params.get("office_365_enabled") is not None:
        update_args["office_365_enabled"] = bool_to_str(module.params.get("office_365_enabled"))
    
    if module.params.get("quota_limit") is not None:
        update_args["quota_limit"] = module.params.get("quota_limit")
    
    if module.params.get("description") is not None:
        update_args["description"] = module.params.get("description")
    
    if module.params.get("rules") is not None:
        # Convert boolean values in rules to string format
        processed_rules = []
        for rule in module.params.get("rules"):
            processed_rule = rule.copy()
            if "follow_http_action" in processed_rule:
                processed_rule["follow_http_action"] = bool_to_str(processed_rule["follow_http_action"])
            if "policy_rule_enabled" in processed_rule:
                processed_rule["policy_rule_enabled"] = bool_to_str(processed_rule["policy_rule_enabled"])
            if "ccl_rule_enabled" in processed_rule:
                processed_rule["ccl_rule_enabled"] = bool_to_str(processed_rule["ccl_rule_enabled"])
            processed_rules.append(processed_rule)
        update_args["rules"] = processed_rules
        
        # Add rule_action parameter when rules are provided
        if module.params.get("rule_action") is not None:
            update_args["rule_action"] = module.params.get("rule_action")

    try:
        with contextlib.redirect_stdout(output_buffer):
            resp = connection.invoke_sdk("update_webfilterpolicy", module_args=update_args)
    except (SophosFirewallAuthFailure, SophosFirewallAPIError, RequestException) as error:
        module.fail_json("An unexpected error occurred: {0}".format(error), **result)

    if not resp["success"]:
        module.fail_json(msg="An error occurred: {0}".format(resp["response"]))

    return resp["response"]


def remove_web_policy(connection, module, result):
    """Remove Web Filter Policy from Sophos Firewall

    Args:
        connection (Connection): Ansible Connection object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: API response
    """
    try:
        with contextlib.redirect_stdout(output_buffer):
            resp = connection.invoke_sdk("remove", module_args={"xml_tag": "WebFilterPolicy", "name": module.params.get("name")})
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
    exist_policy = exist_settings["api_response"]["Response"]["WebFilterPolicy"]
    
    # Check if any of the parameters have changed
    if module.params.get("default_action") and module.params.get("default_action") != exist_policy.get("DefaultAction"):
        return True
    
    if (module.params.get("download_file_size_restriction") is not None and 
        module.params.get("download_file_size_restriction") != exist_policy.get("DownloadFileSizeRestriction")):
        return True
    
    if (module.params.get("enable_reporting") and 
        module.params.get("enable_reporting") != exist_policy.get("EnableReporting")):
        return True
    
    if (module.params.get("description") and 
        module.params.get("description") != exist_policy.get("Description")):
        return True
    
    if (module.params.get("quota_limit") is not None and 
        module.params.get("quota_limit") != exist_policy.get("QuotaLimit")):
        return True

    # Check other optional parameters
    optional_params = [
        ("download_file_size_restriction_enabled", "DownloadFileSizeRestrictionEnabled"),
        ("goog_app_domain_list", "GoogAppDomainList"),
        ("goog_app_domain_list_enabled", "GoogAppDomainListEnabled"),
        ("youtube_filter_is_strict", "YoutubeFilterIsStrict"),
        ("youtube_filter_enabled", "YoutubeFilterEnabled"),
        ("enforce_safe_search", "EnforceSafeSearch"),
        ("enforce_image_licensing", "EnforceImageLicensing"),
        ("xff_enabled", "XffEnabled"),
        ("office_365_tenants_list", "Office365TenantsList"),
        ("office_365_directory_id", "Office365DirectoryId"),
        ("office_365_enabled", "Office365Enabled")
    ]
    
    for param_name, api_key in optional_params:
        if (module.params.get(param_name) is not None and 
            module.params.get(param_name) != exist_policy.get(api_key)):
            return True
    
    # Check rules if provided
    if module.params.get("rules") is not None:
        # Always consider rules changed if they are provided since rule_action
        # determines whether to 'add' or 'replace' rules
        # In a more sophisticated implementation, you could compare the actual rule structures
        # and consider the rule_action parameter
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
    
    # Validate download file size restriction range
    if (module.params.get("download_file_size_restriction") is not None and 
        not (0 <= module.params.get("download_file_size_restriction") <= 1536)):
        module.fail_json(
            msg="Download file size restriction must be between 0 and 1536 MB",
            **result
        )
    
    # Validate quota limit range
    if (module.params.get("quota_limit") is not None and 
        not (1 <= module.params.get("quota_limit") <= 1440)):
        module.fail_json(
            msg="Quota limit must be between 1 and 1440 minutes",
            **result
        )
    
    # Validate Google app domain list length
    if (module.params.get("goog_app_domain_list") and 
        len(module.params.get("goog_app_domain_list")) > 256):
        module.fail_json(
            msg="Google app domain list must be 256 characters or less",
            **result
        )
    
    # Validate Office 365 tenants list length
    if (module.params.get("office_365_tenants_list") and 
        len(module.params.get("office_365_tenants_list")) > 4096):
        module.fail_json(
            msg="Office 365 tenants list must be 4096 characters or less",
            **result
        )
    
    # Validate Office 365 directory ID length
    if (module.params.get("office_365_directory_id") and 
        len(module.params.get("office_365_directory_id")) > 50):
        module.fail_json(
            msg="Office 365 directory ID must be 50 characters or less",
            **result
        )
    
    return True


def main():
    """Code executed at run time."""
    argument_spec = {
        "name": {"type": "str", "required": True},
        "default_action": {"type": "str", "choices": ["Allow", "Deny"], "required": False},
        "download_file_size_restriction": {"type": "int", "required": False, "default": 0},
        "enable_reporting": {"type": "str", "choices": ["Enable", "Disable"], "required": False, "default": "Enable"},
        "download_file_size_restriction_enabled": {"type": "bool", "required": False},
        "goog_app_domain_list": {"type": "str", "required": False},
        "goog_app_domain_list_enabled": {"type": "bool", "required": False},
        "youtube_filter_is_strict": {"type": "bool", "required": False},
        "youtube_filter_enabled": {"type": "bool", "required": False},
        "enforce_safe_search": {"type": "bool", "required": False},
        "enforce_image_licensing": {"type": "bool", "required": False},
        "xff_enabled": {"type": "bool", "required": False},
        "office_365_tenants_list": {"type": "str", "required": False},
        "office_365_directory_id": {"type": "str", "required": False},
        "office_365_enabled": {"type": "bool", "required": False},
        "quota_limit": {"type": "int", "required": False, "default": 60},
        "description": {"type": "str", "required": False},
        "rules": {
            "type": "list", 
            "elements": "dict", 
            "required": False,
            "options": {
                "categories": {
                    "type": "list",
                    "elements": "dict",
                    "required": True,
                    "options": {
                        "id": {"type": "str", "required": True},
                        "type": {"type": "str", "choices": ["WebCategory", "FileType", "URLGroup", "UserActivity"], "required": True}
                    }
                },
                "http_action": {"type": "str", "choices": ["Allow", "Deny"], "required": False, "default": "Deny"},
                "https_action": {"type": "str", "choices": ["Allow", "Deny"], "required": False, "default": "Deny"},
                "follow_http_action": {"type": "bool", "required": False, "default": True},
                "schedule": {"type": "str", "required": False, "default": "All The Time"},
                "policy_rule_enabled": {"type": "bool", "required": False, "default": True},
                "user_list": {"type": "list", "elements": "str", "required": False, "default": []},
                "ccl_rule_enabled": {"type": "bool", "required": False, "default": False}
            }
        },
        "rule_action": {"type": "str", "choices": ["add", "replace"], "required": False, "default": "add"},
        "state": {"type": "str", "required": True, "choices": ["present", "updated", "query", "absent"]},
    }

    required_if = [
        (
            "state",
            "present",
            [
                "name",
                "default_action"
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

    exist_settings = get_web_policy(connection, module, result)
    result["api_response"] = exist_settings["api_response"]

    if state == "query":
        module.exit_json(**result)

    if module.check_mode:
        result["check_mode"] = True
        module.exit_json(**result)

    if state == "present" and not exist_settings["exists"]:
        api_response = create_web_policy(connection, module, result)

        if (
            "Configuration applied successfully" in api_response["Response"]["WebFilterPolicy"]["Status"]["#text"]
        ):
            result["changed"] = True
            result["api_response"] = api_response

    elif state == "present" and exist_settings["exists"]:
        result["changed"] = False

    elif state == "absent" and exist_settings["exists"]:
        api_response = remove_web_policy(connection, module, result)
        if (
            "Configuration applied successfully" in api_response["Response"]["WebFilterPolicy"]["Status"]["#text"]
        ):
            result["changed"] = True
        result["api_response"] = api_response

    elif state == "absent" and not exist_settings["exists"]:
        result["changed"] = False

    elif state == "updated" and exist_settings["exists"]:
        if eval_changed(module, exist_settings):
            api_response = update_web_policy(connection, exist_settings["api_response"], module, result)

            if api_response:
                result["api_response"] = api_response
                if (
                    "Configuration applied successfully" in api_response["Response"]["WebFilterPolicy"]["Status"]["#text"]
                ):
                    result["changed"] = True
    
    elif state == "updated" and not exist_settings["exists"]:
        result["changed"] = False
        module.fail_json(exist_settings["api_response"], **result)

    module.exit_json(**result)


if __name__ == "__main__":
    main()
