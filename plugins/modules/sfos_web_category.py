#!/usr/bin/python

# Copyright 2024 Sophos Ltd.  All rights reserved.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: sfos_web_category

short_description: Manage Web Categories (Protect > Web > Web Categories)

version_added: "2.3.0"

description: Manage Web Categories (Protect > Web > Web Categories) on Sophos Firewall

extends_documentation_fragment:
  - sophos.sophos_firewall.fragments.base

options:
    name:
        description: Specify name of the Web Category.
        type: str
        required: true
    classification:
        description: Select classification.
        type: str
        choices: ["Productive", "Unproductive", "Acceptable", "Objectionable"]
        required: false
    qospolicy:
        description: Select the QoS Policy for bandwidth restriction purposes.
        type: str
        required: false
        default: "None"
    description:
        description: Category description.
        type: str
        required: false
    defaultdeniedmessage:
        description: Message (in HTML) to display when denied by default.
        type: str
        required: false
    domain_url:
        description: 
            - Domains or URLs included in the category.
            - For External configuration, URLs must start with 'http://' or 'ftp://' (https:// is not supported).
            - For Local configuration, domain names should be provided without protocol.
        type: list
        elements: str
        required: false
    keyword:
        description: Keywords included in the category.
        type: list
        elements: str
        required: false
    configurecategory:
        description: Content type configuration.
        type: str
        choices: ["0", "Local", "External"]
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
- name: Create Web Category with Local configuration
  sophos.sophos_firewall.sfos_web_category:
    name: "Custom Category"
    classification: "Productive"
    qospolicy: "Default"
    description: "Custom web category for internal use"
    configurecategory: "Local"
    domain_url:
      - "example.com"
      - "test.org"
    keyword:
      - "productivity"
      - "business"
    state: present

- name: Create Web Category with External configuration
  sophos.sophos_firewall.sfos_web_category:
    name: "External Category"
    classification: "Unproductive"
    qospolicy: "Low Priority"
    configurecategory: "External"
    domain_url:
      - "http://custom.com"
      - "ftp://custom1.com"
    state: present

- name: Query Web Category
  sophos.sophos_firewall.sfos_web_category:
    name: "Custom Category"
    state: query

- name: Update Web Category
  sophos.sophos_firewall.sfos_web_category:
    name: "Custom Category"
    classification: "Acceptable"
    description: "Updated description"
    state: updated

- name: Remove Web Category
  sophos.sophos_firewall.sfos_web_category:
    name: "Custom Category"
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


def get_web_category(connection, module, result):
    """Get Web Category from Sophos Firewall

    Args:
        connection (Connection): Ansible Connection object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: Results of lookup
    """
    try:
        resp = connection.invoke_sdk("get_tag_with_filter", module_args={"xml_tag": "WebFilterCategory",
                                                                         "key": "Name",
                                                                         "value": module.params.get("name")})
    except (SophosFirewallAuthFailure, SophosFirewallAPIError, RequestException) as error:
        module.fail_json("An unexpected error occurred: {0}".format(error), **result)

    if resp["success"] and not resp["exists"]:
        return {"exists": False, "api_response": resp["response"]}

    if not resp["success"]:
        module.fail_json(msg="An error occurred: {0}".format(resp["response"]))

    return {"exists": True, "api_response": resp["response"]}

def create_web_category(connection, module, result):
    """Create a Web Category on Sophos Firewall

    Args:
        connection (Connection): Ansible Connection object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: API response
    """
    payload = """
        <WebFilterCategory>
          <Name>{{ name }}</Name>
          {% if classification %}
          <Classification>{{ classification }}</Classification>
          {% endif %}
          <QoSPolicy>{{ qospolicy }}</QoSPolicy>
          <ConfigureCategory>{{ configurecategory }}</ConfigureCategory>
          {% if configurecategory == 'Local' %}
          {% if domain_url %}
          <DomainList>
            {% for domain in domain_url %}
            <Domain>{{ domain }}</Domain>
            {% endfor %}
          </DomainList>
          {% endif %}
          {% if keyword %}
          <KeywordList>
            {% for kw in keyword %}
            <Keyword>{{ kw }}</Keyword>
            {% endfor %}
          </KeywordList>
          {% endif %}
          {% elif configurecategory == 'External' %}
          {% if domain_url %}
          <URLList>
            {% for url in domain_url %}
            <URL>{{ url }}</URL>
            {% endfor %}
          </URLList>
          {% endif %}
          {% endif %}
          {% if description %}
          <Description>{{ description }}</Description>
          {% endif %}
          {% if defaultdeniedmessage %}
          <OverrideDefaultDeniedMessage>Enable</OverrideDefaultDeniedMessage>
          <DefaultDeniedMessage>{{ defaultdeniedmessage }}</DefaultDeniedMessage>
          {% else %}
          <OverrideDefaultDeniedMessage>Disable</OverrideDefaultDeniedMessage>
          <DefaultDeniedMessage>Default</DefaultDeniedMessage>
          {% endif %}
        </WebFilterCategory>
    """
    template_vars = {
        "name": module.params.get("name"),
        "classification": module.params.get("classification"),
        "qospolicy": module.params.get("qospolicy"),
        "configurecategory": module.params.get("configurecategory"),
        "domain_url": module.params.get("domain_url"),
        "keyword": module.params.get("keyword"),
        "description": module.params.get("description"),
        "defaultdeniedmessage": module.params.get("defaultdeniedmessage")
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

def update_web_category(connection, exist_settings, module, result):
    """Update Web Category configuration on Sophos Firewall

    Args:
        connection (Connection): Ansible Connection object
        exist_settings (dict): API response containing existing Web Category
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: API response
    """
    update_params = {}
    existing_category = exist_settings["Response"]["WebFilterCategory"]
    
    update_params["Name"] = module.params.get("name")

    if module.params.get("classification"):
        update_params["Classification"] = module.params.get("classification")

    if module.params.get("qospolicy"):
        update_params["QoSPolicy"] = module.params.get("qospolicy")

    if module.params.get("configurecategory"):
        update_params["ConfigureCategory"] = module.params.get("configurecategory")

    if module.params.get("description"):
        update_params["Description"] = module.params.get("description")

    if module.params.get("defaultdeniedmessage"):
        update_params["OverrideDefaultDeniedMessage"] = "Enable"
        update_params["DefaultDeniedMessage"] = module.params.get("defaultdeniedmessage")
    else:
        update_params["OverrideDefaultDeniedMessage"] = "Disable"
        update_params["DefaultDeniedMessage"] = "Default"

    # Handle domain/URL configuration based on category type
    if module.params.get("configurecategory") == "Local":
        if module.params.get("domain_url"):
            # For Local configuration, domains go in DomainList
            existing_domains = []
            if "DomainList" in existing_category and existing_category["DomainList"]:
                domain_list = existing_category["DomainList"]
                if isinstance(domain_list, dict) and "Domain" in domain_list:
                    if isinstance(domain_list["Domain"], list):
                        existing_domains = domain_list["Domain"]
                    else:
                        existing_domains = [domain_list["Domain"]]
            
            # Merge existing and new domains
            all_domains = list(set(existing_domains + module.params.get("domain_url")))
            update_params["DomainList"] = []
            for domain in all_domains:
                update_params["DomainList"].append({"Domain": domain})
        
        if module.params.get("keyword"):
            existing_keywords = []
            if "KeywordList" in existing_category and existing_category["KeywordList"]:
                keyword_list = existing_category["KeywordList"]
                if isinstance(keyword_list, dict) and "Keyword" in keyword_list:
                    if isinstance(keyword_list["Keyword"], list):
                        existing_keywords = keyword_list["Keyword"]
                    else:
                        existing_keywords = [keyword_list["Keyword"]]
            
            # Merge existing and new keywords
            all_keywords = list(set(existing_keywords + module.params.get("keyword")))
            update_params["KeywordList"] = []
            for kw in all_keywords:
                update_params["KeywordList"].append({"Keyword": kw})
    
    elif module.params.get("configurecategory") == "External":
        if module.params.get("domain_url"):
            # For External configuration, URLs go in URLList
            existing_urls = []
            if "URLList" in existing_category and existing_category["URLList"]:
                url_list = existing_category["URLList"]
                if isinstance(url_list, dict) and "URL" in url_list:
                    if isinstance(url_list["URL"], list):
                        existing_urls = url_list["URL"]
                    else:
                        existing_urls = [url_list["URL"]]
            
            # Merge existing and new URLs
            all_urls = list(set(existing_urls + module.params.get("domain_url")))
            update_params["URLList"] = []
            for url in all_urls:
                update_params["URLList"].append({"URL": url})

    try:
        with contextlib.redirect_stdout(output_buffer):
            resp = connection.invoke_sdk("update", module_args={"xml_tag": "WebFilterCategory",
                                 "update_params": update_params,
                                 "name": module.params.get("name"),
                                 "lookup_key": "Name",
                                 "timeout": 90,
                                 "debug": True})
    except (SophosFirewallAuthFailure, SophosFirewallAPIError, RequestException) as error:
        module.fail_json("An unexpected error occurred: {0}".format(error), **result)

    if not resp["success"]:
        module.fail_json(msg="An error occurred: {0}".format(resp["response"]))

    return resp["response"]

def eval_changed(module, exist_settings):
    """Evaluate the provided arguments against existing settings.

    Args:
        module (AnsibleModule): AnsibleModule object
        exist_settings (dict): Response from the call to get_web_category()

    Returns:
        bool: Return true if any settings are different, otherwise return false
    """
    exist_settings = exist_settings["api_response"]["Response"]["WebFilterCategory"]

    if (module.params.get("classification") and not module.params.get("classification") == exist_settings.get("Classification") or
        module.params.get("qospolicy") and not module.params.get("qospolicy") == exist_settings.get("QoSPolicy") or
        module.params.get("configurecategory") and not module.params.get("configurecategory") == exist_settings.get("ConfigureCategory") or
        module.params.get("description") and not module.params.get("description") == exist_settings.get("Description")
        ):
        return True

    # Check for changes in defaultdeniedmessage
    if module.params.get("defaultdeniedmessage"):
        if (exist_settings.get("OverrideDefaultDeniedMessage") != "Enable" or
            exist_settings.get("DefaultDeniedMessage") != module.params.get("defaultdeniedmessage")):
            return True
    elif exist_settings.get("OverrideDefaultDeniedMessage") == "Enable":
        return True

    # Check domain/URL lists based on configuration type
    if module.params.get("configurecategory") == "Local" and module.params.get("domain_url"):
        existing_domains = []
        if "DomainList" in exist_settings and exist_settings["DomainList"]:
            domain_list = exist_settings["DomainList"]
            if isinstance(domain_list, dict) and "Domain" in domain_list:
                if isinstance(domain_list["Domain"], list):
                    existing_domains = domain_list["Domain"]
                else:
                    existing_domains = [domain_list["Domain"]]
        
        if set(module.params.get("domain_url")) != set(existing_domains):
            return True

    if module.params.get("configurecategory") == "Local" and module.params.get("keyword"):
        existing_keywords = []
        if "KeywordList" in exist_settings and exist_settings["KeywordList"]:
            keyword_list = exist_settings["KeywordList"]
            if isinstance(keyword_list, dict) and "Keyword" in keyword_list:
                if isinstance(keyword_list["Keyword"], list):
                    existing_keywords = keyword_list["Keyword"]
                else:
                    existing_keywords = [keyword_list["Keyword"]]
        
        if set(module.params.get("keyword")) != set(existing_keywords):
            return True

    if module.params.get("configurecategory") == "External" and module.params.get("domain_url"):
        existing_urls = []
        if "URLList" in exist_settings and exist_settings["URLList"]:
            url_list = exist_settings["URLList"]
            if isinstance(url_list, dict) and "URL" in url_list:
                if isinstance(url_list["URL"], list):
                    existing_urls = url_list["URL"]
                else:
                    existing_urls = [url_list["URL"]]
        
        if set(module.params.get("domain_url")) != set(existing_urls):
            return True

    return False

def remove_web_category(connection, module, result):
    """Remove a Web Category from Sophos Firewall.

    Args:
        connection (Connection): Ansible Connection object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: API response
    """
    try:
        resp = connection.invoke_sdk("remove", module_args={"xml_tag": "WebFilterCategory", "name": module.params.get("name")})
    except (SophosFirewallAuthFailure, SophosFirewallAPIError, RequestException) as error:
        module.fail_json("An unexpected error occurred: {0}".format(error), **result)

    if not resp["success"]:
        module.fail_json(msg="An error occurred: {0}".format(resp["response"]))

    return resp["response"]

def validate_domain_urls(module, result):
    """Validate domain URLs for External configuration.
    
    For External configuration, URLs must contain http:// or ftp:// prefix and should not use https://.
    
    Args:
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console
        
    Returns:
        bool: True if validation passes, False otherwise
    """
    if (module.params.get("configurecategory") == "External" and 
        module.params.get("domain_url")):
        
        allowed_protocols = ["http://", "ftp://"]
        
        for url in module.params.get("domain_url"):
            if not any(url.startswith(protocol) for protocol in allowed_protocols):
                if url.startswith("https://"):
                    module.fail_json(
                        msg=f"URL '{url}' uses https:// which is not supported. External URLs must use http:// or ftp:// protocol.",
                        **result
                    )
                else:
                    module.fail_json(
                        msg=f"URL '{url}' does not have a valid protocol. External URLs must use http:// or ftp:// protocol.",
                        **result
                    )
    
    return True

def main():
    """Code executed at run time."""
    argument_spec = {
        "name": {"type": "str", "required": True},
        "classification": {"type": "str", "choices": ["Productive", "Unproductive", "Acceptable", "Objectionable"], "required": False},
        "qospolicy": {"type": "str", "required": False, "default": "None"},
        "description": {"type": "str", "required": False},
        "defaultdeniedmessage": {"type": "str", "required": False},
        "domain_url": {"type": "list", "elements": "str", "required": False},
        "keyword": {"type": "list", "elements": "str", "required": False},
        "configurecategory": {"type": "str", "choices": ["0", "Local", "External"], "required": False, "default": "Local"},
        "state": {"type": "str", "required": True, "choices": ["present", "updated", "query", "absent"]},
    }

    required_if = [
        (
            "state",
            "present",
            [
                "name",
                "qospolicy",
                "configurecategory"
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
    
    # Validate domain_url entries for External configuration
    if module.params.get("state") in ["present", "updated"]:
        validate_domain_urls(module, result)

    state = module.params.get("state")

    try:
        connection = Connection(module._socket_path)
    except AssertionError:
        module.fail_json(msg="Connection error: Ensure you are targeting a remote host and not using 'delegate_to: localhost'.")

    if not hasattr(connection, "httpapi"):
        module.fail_json(msg="HTTPAPI plugin is not initialized. Ensure the connection is set to 'httpapi'.")

    exist_settings = get_web_category(connection, module, result)
    result["api_response"] = exist_settings["api_response"]

    if state == "query":
        module.exit_json(**result)

    if module.check_mode:
        result["check_mode"] = True
        module.exit_json(**result)

    if state == "present" and not exist_settings["exists"]:
        api_response = create_web_category(connection, module, result)

        if (
            "Configuration applied successfully" in api_response["Response"]["WebFilterCategory"]["Status"]["#text"]
        ) or ("Unable to get status message" in api_response["Response"]["WebFilterCategory"]["Status"]["#text"]):
            result["changed"] = True
            result["api_response"] = api_response

    elif state == "present" and exist_settings["exists"]:
        result["changed"] = False

    elif state == "absent" and exist_settings["exists"]:
        api_response = remove_web_category(connection, module, result)
        if (
            "Configuration applied successfully" in api_response["Response"]["WebFilterCategory"]["Status"]["#text"]
        ):
            result["changed"] = True
        result["api_response"] = api_response

    elif state == "absent" and not exist_settings["exists"]:
        result["changed"] = False

    elif state == "updated" and exist_settings["exists"]:
        if eval_changed(module, exist_settings):
            api_response = update_web_category(connection, exist_settings["api_response"], module, result)

            if api_response:
                result["api_response"] = api_response
                if (
                    "Configuration applied successfully" in api_response["Response"]["WebFilterCategory"]["Status"]["#text"]
                ):
                    result["changed"] = True
    
    elif state == "updated" and not exist_settings["exists"]:
        result["changed"] = False
        module.fail_json(exist_settings["api_response"], **result)

    module.exit_json(**result)


if __name__ == "__main__":
    main()
