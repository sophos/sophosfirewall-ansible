#!/usr/bin/python

# Copyright 2024 Sophos Ltd.  All rights reserved.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: sfos_web_filetype

short_description: Manage Web File Types (Protect > Web > File Types)

version_added: "2.3.0"

description: Manage Web File Types (Protect > Web > File Types) on Sophos Firewall

extends_documentation_fragment:
  - sophos.sophos_firewall.fragments.base

options:
    name:
        description: Specify a name to identify the File Type Category.
        type: str
        required: true
    file_extension:
        description: Enter File Extensions to be included in the Category.
        type: list
        elements: str
        required: false
    mime_header:
        description: Enter MIME Header to be included in the Category.
        type: list
        elements: str
        required: false
    description:
        description: Specify File Type Category description.
        type: str
        required: false
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
- name: Create File Type Category with extensions and MIME headers
  sophos.sophos_firewall.sfos_web_filetype:
    name: "Custom File Type"
    description: "Custom file type category for document files"
    file_extension:
      - "pdf"
      - "doc"
      - "docx"
      - "txt"
    mime_header:
      - "application/pdf"
      - "application/msword"
      - "text/plain"
    state: present

- name: Create File Type Category with only extensions
  sophos.sophos_firewall.sfos_web_filetype:
    name: "Image Files"
    description: "Image file types"
    file_extension:
      - "jpg"
      - "jpeg"
      - "png"
      - "gif"
    state: present

- name: Query File Type Category
  sophos.sophos_firewall.sfos_web_filetype:
    name: "Custom File Type"
    state: query

- name: Update File Type Category
  sophos.sophos_firewall.sfos_web_filetype:
    name: "Custom File Type"
    description: "Updated description"
    file_extension:
      - "pdf"
      - "doc"
      - "docx"
      - "txt"
      - "rtf"
    state: updated

- name: Remove File Type Category
  sophos.sophos_firewall.sfos_web_filetype:
    name: "Custom File Type"
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


def get_web_filetype(connection, module, result):
    """Get Web File Type from Sophos Firewall

    Args:
        connection (Connection): Ansible Connection object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: Results of lookup
    """
    try:
        resp = connection.invoke_sdk("get_tag_with_filter", module_args={"xml_tag": "FileType",
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

def create_web_filetype(connection, module, result):
    """Create a Web File Type on Sophos Firewall

    Args:
        connection (Connection): Ansible Connection object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: API response
    """
    payload = """
        <FileType>
          <Name>{{ name }}</Name>
          <Template>Blank</Template>
          {% if file_extension %}
          <FileExtensionList>
            {% for extension in file_extension %}
            <FileExtension>{{ extension }}</FileExtension>
            {% endfor %}
          </FileExtensionList>
          {% endif %}
          {% if mime_header %}
          <MIMEHeaderList>
            {% for mime in mime_header %}
            <MIMEHeader>{{ mime }}</MIMEHeader>
            {% endfor %}
          </MIMEHeaderList>
          {% endif %}
          {% if description %}
          <Description>{{ description }}</Description>
          {% endif %}
        </FileType>
    """
    template_vars = {
        "name": module.params.get("name"),
        "file_extension": module.params.get("file_extension"),
        "mime_header": module.params.get("mime_header"),
        "description": module.params.get("description")
    }

    try:
        with contextlib.redirect_stdout(output_buffer):
            resp = connection.invoke_sdk("submit_xml", module_args={
                "template_data": payload,
                "template_vars": template_vars,
                "debug": True
                }
            )
    except (SophosFirewallAuthFailure, SophosFirewallAPIError, RequestException) as error:
        module.fail_json("An unexpected error occurred: {0}".format(error), **result)

    if not resp["success"]:
        module.fail_json(msg="An error occurred: {0}".format(resp["response"]))

    return resp["response"]

def update_web_filetype(connection, exist_settings, module, result):
    """Update Web File Type configuration on Sophos Firewall

    Args:
        connection (Connection): Ansible Connection object
        exist_settings (dict): API response containing existing Web File Type
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: API response
    """
    update_params = {}
    existing_filetype = exist_settings["Response"]["FileType"]
    
    update_params["Name"] = module.params.get("name")

    if module.params.get("description") is not None:
        update_params["Description"] = module.params.get("description")

    # Handle File Extension List
    if module.params.get("file_extension"):
        existing_extensions = []
        if "FileExtensionList" in existing_filetype and existing_filetype["FileExtensionList"]:
            extension_list = existing_filetype["FileExtensionList"]
            if isinstance(extension_list, dict) and "FileExtension" in extension_list:
                if isinstance(extension_list["FileExtension"], list):
                    existing_extensions = extension_list["FileExtension"]
                else:
                    existing_extensions = [extension_list["FileExtension"]]
        
        # Merge existing and new extensions
        all_extensions = list(set(existing_extensions + module.params.get("file_extension")))
        update_params["FileExtensionList"] = []
        for extension in all_extensions:
            update_params["FileExtensionList"].append({"FileExtension": extension})
    
    # Handle MIME Header List
    if module.params.get("mime_header"):
        existing_mimes = []
        if "MIMEHeaderList" in existing_filetype and existing_filetype["MIMEHeaderList"]:
            mime_list = existing_filetype["MIMEHeaderList"]
            if isinstance(mime_list, dict) and "MIMEHeader" in mime_list:
                if isinstance(mime_list["MIMEHeader"], list):
                    existing_mimes = mime_list["MIMEHeader"]
                else:
                    existing_mimes = [mime_list["MIMEHeader"]]
        
        # Merge existing and new MIME headers
        all_mimes = list(set(existing_mimes + module.params.get("mime_header")))
        update_params["MIMEHeaderList"] = []
        for mime in all_mimes:
            update_params["MIMEHeaderList"].append({"MIMEHeader": mime})

    try:
        with contextlib.redirect_stdout(output_buffer):
            resp = connection.invoke_sdk("update", module_args={"xml_tag": "FileType",
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
        exist_settings (dict): Response from the call to get_web_filetype()

    Returns:
        bool: Return true if any settings are different, otherwise return false
    """
    exist_settings = exist_settings["api_response"]["Response"]["FileType"]

    # Check description changes
    if (module.params.get("description") is not None and 
        module.params.get("description") != exist_settings.get("Description")):
        return True

    # Check file extensions
    if module.params.get("file_extension"):
        existing_extensions = []
        if "FileExtensionList" in exist_settings and exist_settings["FileExtensionList"]:
            extension_list = exist_settings["FileExtensionList"]
            if isinstance(extension_list, dict) and "FileExtension" in extension_list:
                if isinstance(extension_list["FileExtension"], list):
                    existing_extensions = extension_list["FileExtension"]
                else:
                    existing_extensions = [extension_list["FileExtension"]]
        
        if set(module.params.get("file_extension")) != set(existing_extensions):
            return True

    # Check MIME headers
    if module.params.get("mime_header"):
        existing_mimes = []
        if "MIMEHeaderList" in exist_settings and exist_settings["MIMEHeaderList"]:
            mime_list = exist_settings["MIMEHeaderList"]
            if isinstance(mime_list, dict) and "MIMEHeader" in mime_list:
                if isinstance(mime_list["MIMEHeader"], list):
                    existing_mimes = mime_list["MIMEHeader"]
                else:
                    existing_mimes = [mime_list["MIMEHeader"]]
        
        if set(module.params.get("mime_header")) != set(existing_mimes):
            return True

    return False

def remove_web_filetype(connection, module, result):
    """Remove a Web File Type from Sophos Firewall.

    Args:
        connection (Connection): Ansible Connection object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: API response
    """
    try:
        resp = connection.invoke_sdk("remove", module_args={"xml_tag": "FileType", "name": module.params.get("name")})
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
    
    if name:
        # Check for disallowed characters (comma)
        if "," in name:
            module.fail_json(
                msg=f"Name '{name}' contains disallowed characters. Commas are not allowed.",
                **result
            )
        
        # Check max length
        if len(name) > 50:
            module.fail_json(
                msg=f"Name '{name}' exceeds maximum length of 50 characters.",
                **result
            )
    
    return True

def validate_description(module, result):
    """Validate the description parameter according to constraints.
    
    Args:
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console
        
    Returns:
        bool: True if validation passes
    """
    description = module.params.get("description")
    
    if description and len(description) > 1000:
        module.fail_json(
            msg=f"Description exceeds maximum length of 1000 characters. Current length: {len(description)}",
            **result
        )
    
    return True

def main():
    """Code executed at run time."""
    argument_spec = {
        "name": {"type": "str", "required": True},
        "file_extension": {"type": "list", "elements": "str", "required": False},
        "mime_header": {"type": "list", "elements": "str", "required": False},
        "description": {"type": "str", "required": False},
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
        validate_description(module, result)

    state = module.params.get("state")

    try:
        connection = Connection(module._socket_path)
    except AssertionError:
        module.fail_json(msg="Connection error: Ensure you are targeting a remote host and not using 'delegate_to: localhost'.")

    if not hasattr(connection, "httpapi"):
        module.fail_json(msg="HTTPAPI plugin is not initialized. Ensure the connection is set to 'httpapi'.")

    exist_settings = get_web_filetype(connection, module, result)
    result["api_response"] = exist_settings["api_response"]

    if state == "query":
        module.exit_json(**result)

    if module.check_mode:
        result["check_mode"] = True
        module.exit_json(**result)

    if state == "present" and not exist_settings["exists"]:
        api_response = create_web_filetype(connection, module, result)
        if (
            "Configuration applied successfully" in api_response["Response"]["FileType"]["Status"]["#text"]
        ):
            result["changed"] = True
            result["api_response"] = api_response

    elif state == "present" and exist_settings["exists"]:
        result["changed"] = False

    elif state == "absent" and exist_settings["exists"]:
        api_response = remove_web_filetype(connection, module, result)
        if (
            "Configuration applied successfully" in api_response["Response"]["FileType"]["Status"]["#text"]
        ):
            result["changed"] = True
        result["api_response"] = api_response

    elif state == "absent" and not exist_settings["exists"]:
        result["changed"] = False

    elif state == "updated" and exist_settings["exists"]:
        if eval_changed(module, exist_settings):
            api_response = update_web_filetype(connection, exist_settings["api_response"], module, result)

            if api_response:
                result["api_response"] = api_response
                if (
                    "Configuration applied successfully" in api_response["Response"]["FileType"]["Status"]["#text"]
                ):
                    result["changed"] = True
    
    elif state == "updated" and not exist_settings["exists"]:
        result["changed"] = False
        module.fail_json(exist_settings["api_response"], **result)

    module.exit_json(**result)


if __name__ == "__main__":
    main()
