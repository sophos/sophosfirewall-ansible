#!/usr/bin/python

# Copyright 2024 Sophos Ltd.  All rights reserved.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: sfos_web_useractivity

short_description: Manage Web User Activities (Protect > Web > User Activities)

version_added: "2.3.0"

description: Manage Web User Activities (Protect > Web > User Activities) on Sophos Firewall

extends_documentation_fragment:
  - sophos.sophos_firewall.fragments.base

options:
    name:
        description: Specify a name for the User Activity.
        type: str
        required: true
        constraints:
            - Maximum 50 characters
    description:
        description: Specify a description for the User Activity.
        type: str
        required: false
    category_list:
        description: List of categories to apply to this User Activity.
        type: list
        elements: dict
        required: false
        suboptions:
            id:
                description: Category Name
                type: str
                required: true
            type:
                description: Category type
                type: str
                choices: ["web category", "file type", "url group"]
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
- name: Create User Activity with web categories
  sophos.sophos_firewall.sfos_web_useractivity:
    name: "Social Media Activity"
    description: "User activity for social media monitoring"
    category_list:
      - id: "Social Networking"
        type: "web category"
      - id: "Entertainment"
        type: "web category"
    state: present

- name: Create User Activity with mixed categories
  sophos.sophos_firewall.sfos_web_useractivity:
    name: "Document Management"
    description: "User activity for document handling"
    category_list:
      - id: "Business"
        type: "web category"
      - id: "Document Files"
        type: "file type"
      - id: "Corporate URLs"
        type: "url group"
    state: present

- name: Create User Activity with only description
  sophos.sophos_firewall.sfos_web_useractivity:
    name: "Basic Activity"
    description: "Basic user activity without categories"
    state: present

- name: Query User Activity
  sophos.sophos_firewall.sfos_web_useractivity:
    name: "Social Media Activity"
    state: query

- name: Update User Activity
  sophos.sophos_firewall.sfos_web_useractivity:
    name: "Social Media Activity"
    description: "Updated social media monitoring activity"
    category_list:
      - id: "Social Networking"
        type: "web category"
      - id: "Entertainment"
        type: "web category"
      - id: "Gaming"
        type: "web category"
    state: updated

- name: Remove User Activity
  sophos.sophos_firewall.sfos_web_useractivity:
    name: "Social Media Activity"
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


def get_web_useractivity(connection, module, result):
    """Get Web User Activity from Sophos Firewall

    Args:
        connection (Connection): Ansible Connection object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: Results of lookup
    """
    try:
        resp = connection.invoke_sdk("get_tag_with_filter", module_args={"xml_tag": "UserActivity",
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

def create_web_useractivity(connection, module, result):
    """Create a Web User Activity on Sophos Firewall

    Args:
        connection (Connection): Ansible Connection object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: API response
    """
    try:
        with contextlib.redirect_stdout(output_buffer):
            resp = connection.invoke_sdk("create_useractivity", module_args={
                "name": module.params.get("name"),
                "description": module.params.get("description"),
                "category_list": module.params.get("category_list"),
                "debug": True
                }
            )
    except (SophosFirewallAuthFailure, SophosFirewallAPIError, RequestException) as error:
        module.fail_json("An unexpected error occurred: {0}".format(error), **result)

    if not resp["success"]:
        module.fail_json(msg="An error occurred: {0}".format(resp["response"]))

    return resp["response"]

def update_web_useractivity(connection, exist_settings, module, result):
    """Update Web User Activity configuration on Sophos Firewall

    Args:
        connection (Connection): Ansible Connection object
        exist_settings (dict): API response containing existing Web User Activity
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: API response
    """
    update_params = {}
    existing_useractivity = exist_settings["Response"]["UserActivity"]
    
    update_params["Name"] = module.params.get("name")

    if module.params.get("description") is not None:
        update_params["Desc"] = module.params.get("description")

    # Handle Category List
    if module.params.get("category_list"):
        existing_categories = []
        if "CategoryList" in existing_useractivity and existing_useractivity["CategoryList"]:
            category_list = existing_useractivity["CategoryList"]
            if isinstance(category_list, dict) and "Category" in category_list:
                if isinstance(category_list["Category"], list):
                    existing_categories = category_list["Category"]
                else:
                    existing_categories = [category_list["Category"]]
        
        # Convert module categories to the expected format
        new_categories = []
        for category in module.params.get("category_list"):
            new_categories.append({
                "ID": category["id"],
                "type": category["type"]
            })
        
        # Merge existing and new categories (remove duplicates based on Name and Type)
        all_categories = existing_categories.copy()
        for new_cat in new_categories:
            # Check if this category already exists
            exists = False
            for existing_cat in all_categories:
                if (existing_cat.get("ID") == new_cat["ID"] and 
                    existing_cat.get("type") == new_cat["type"]):
                    exists = True
                    break
            if not exists:
                all_categories.append(new_cat)

        update_params["CategoryList"] = {}
        update_params["CategoryList"]["Category"] = []
        for category in all_categories:
            update_params["CategoryList"]["Category"].append({
                "ID": category.get("ID"),
                "type": category.get("type")
                }
            )

    try:
        with contextlib.redirect_stdout(output_buffer):
            resp = connection.invoke_sdk("update", module_args={"xml_tag": "UserActivity",
                                 "update_params": update_params,
                                 "name": module.params.get("name"),
                                 "lookup_key": "Name",
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
        exist_settings (dict): Response from the call to get_web_useractivity()

    Returns:
        bool: Return true if any settings are different, otherwise return false
    """
    exist_settings = exist_settings["api_response"]["Response"]["UserActivity"]

    # Check description changes
    if (module.params.get("description") is not None and 
        module.params.get("description") != exist_settings.get("Desc")):
        return True

    # Check category list changes
    if module.params.get("category_list"):
        existing_categories = []
        if "CategoryList" in exist_settings and exist_settings["CategoryList"]:
            category_list = exist_settings["CategoryList"]
            if isinstance(category_list, dict) and "Category" in category_list:
                if isinstance(category_list["Category"], list):
                    for cat in category_list["Category"]:
                        existing_categories.append({
                            "ID": cat.get("ID"),
                            "type": cat.get("type")
                        })
                else:
                    cat = category_list["Category"]
                    existing_categories.append({
                        "ID": cat.get("ID"),
                        "type": cat.get("type")
                    })
        
        # Convert sets for comparison
        existing_cat_set = set((cat["ID"], cat["type"]) for cat in existing_categories)
        new_cat_set = set((cat["id"], cat["type"]) for cat in module.params.get("category_list"))

        if new_cat_set != existing_cat_set:
            return True

    return False

def remove_web_useractivity(connection, module, result):
    """Remove a Web User Activity from Sophos Firewall.

    Args:
        connection (Connection): Ansible Connection object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: API response
    """
    try:
        resp = connection.invoke_sdk("remove", module_args={"xml_tag": "UserActivity", "name": module.params.get("name")})
    except (SophosFirewallAuthFailure, SophosFirewallAPIError, RequestException) as error:
        module.fail_json("An unexpected error occurred: {0}".format(error), **result)

    if not resp["success"]:
        module.fail_json(msg="An error occurred: {0}".format(resp["response"]))

    return resp["response"]

def validate_name(module, result):
    """Validate the name parameter according to constraints.
    
    Args:
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console
        
    Returns:
        bool: True if validation passes
    """
    name = module.params.get("name")
    
    if name and len(name) > 50:
        module.fail_json(
            msg=f"Name '{name}' exceeds maximum length of 50 characters.",
            **result
        )
    
    return True

def validate_category_list(module, result):
    """Validate the category_list parameter.
    
    Args:
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console
        
    Returns:
        bool: True if validation passes
    """
    category_list = module.params.get("category_list")
    
    if category_list:
        valid_types = ["web category", "file type", "url group"]
        for i, category in enumerate(category_list):
            if "id" not in category or not category["id"]:
                module.fail_json(
                    msg=f"Category at index {i} is missing required 'id' field.",
                    **result
                )
            if "type" not in category or category["type"] not in valid_types:
                module.fail_json(
                    msg=f"Category at index {i} has invalid 'type'. Must be one of: {valid_types}",
                    **result
                )
    
    return True

def main():
    """Code executed at run time."""
    argument_spec = {
        "name": {"type": "str", "required": True},
        "description": {"type": "str", "required": False},
        "category_list": {
            "type": "list",
            "elements": "dict",
            "required": False,
            "options": {
                "id": {"type": "str", "required": True},
                "type": {"type": "str", "required": True, "choices": ["web category", "file type", "url group"]}
            }
        },
        "state": {"type": "str", "required": True, "choices": ["present", "updated", "query", "absent"]},
    }

    required_if = [
        (
            "state",
            "present",
            [
                "name"
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
    
    # Validate input parameters
    if module.params.get("state") in ["present", "updated"]:
        validate_name(module, result)
        validate_category_list(module, result)

    state = module.params.get("state")

    try:
        connection = Connection(module._socket_path)
    except AssertionError:
        module.fail_json(msg="Connection error: Ensure you are targeting a remote host and not using 'delegate_to: localhost'.")

    if not hasattr(connection, "httpapi"):
        module.fail_json(msg="HTTPAPI plugin is not initialized. Ensure the connection is set to 'httpapi'.")

    exist_settings = get_web_useractivity(connection, module, result)
    result["api_response"] = exist_settings["api_response"]

    if state == "query":
        module.exit_json(**result)

    if module.check_mode:
        result["check_mode"] = True
        module.exit_json(**result)

    if state == "present" and not exist_settings["exists"]:
        api_response = create_web_useractivity(connection, module, result)
        if (
            "Configuration applied successfully" in api_response["Response"]["UserActivity"]["Status"]["#text"]
        ):
            result["changed"] = True
            result["api_response"] = api_response

    elif state == "present" and exist_settings["exists"]:
        result["changed"] = False

    elif state == "absent" and exist_settings["exists"]:
        api_response = remove_web_useractivity(connection, module, result)
        if (
            "Configuration applied successfully" in api_response["Response"]["UserActivity"]["Status"]["#text"]
        ):
            result["changed"] = True
        result["api_response"] = api_response

    elif state == "absent" and not exist_settings["exists"]:
        result["changed"] = False

    elif state == "updated" and exist_settings["exists"]:
        if eval_changed(module, exist_settings):
            api_response = update_web_useractivity(connection, exist_settings["api_response"], module, result)

            if api_response:
                result["api_response"] = api_response
                if (
                    "Configuration applied successfully" in api_response["Response"]["UserActivity"]["Status"]["#text"]
                ):
                    result["changed"] = True
    
    elif state == "updated" and not exist_settings["exists"]:
        result["changed"] = False
        module.fail_json(exist_settings["api_response"], **result)

    module.exit_json(**result)


if __name__ == "__main__":
    main()
