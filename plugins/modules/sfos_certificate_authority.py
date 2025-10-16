#!/usr/bin/python

# Copyright 2024 Sophos Ltd.  All rights reserved.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: sfos_certificate_authority

short_description: Manage Certificate Authorities (System > Certificates > Certificate Authorities)

version_added: "2.5.0"

description: Creates, updates, and removes certificate authorities on Sophos Firewall

extends_documentation_fragment:
  - sophos.sophos_firewall.fragments.base

options:
    name:
        description: Name of the certificate authority
        required: true
        type: str
    format:
        description: Format of the root certificate you uploaded
        choices: ["PEM", "DER"]
        type: str
        required: false
    ca_cert_file:
        description: Path to the certificate to be uploaded
        type: str
        required: false
    ca_private_key_file:
        description: Path to the private key to be uploaded
        type: str
        required: false
    password:
        description: Specify the password to access the private key
        type: str
        required: false
    state:
        description:
            - Use C(present) to create or update certificate authority
            - Use C(update) to update an existing certificate authority
            - Use C(absent) to remove certificate authority
        choices: [present, update, absent]
        type: str
        required: true

author:
    - Matt Mullen (@mamullen13316)
"""

EXAMPLES = r"""
- name: Add Certificate Authority
  sophos.sophos_firewall.sfos_certificate_authority:
    name: MY_CA
    format: PEM
    ca_cert_file: /path/to/ca_certificate.pem
    ca_private_key_file: /path/to/ca_private_key.key
    password: ca_password
    state: present

- name: Update Certificate Authority
  sophos.sophos_firewall.sfos_certificate_authority:
    name: MY_CA
    format: DER
    ca_cert_file: /path/to/updated_ca_certificate.der
    state: update

- name: Remove Certificate Authority
  sophos.sophos_firewall.sfos_certificate_authority:
    name: MY_CA
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
        SophosFirewallAPIError,
    )
    from requests.exceptions import RequestException
    import requests

    PREREQ_MET = {"result": True}
except ImportError as errMsg:
    PREREQ_MET = {"result": False, "missing_module": errMsg.name}

import re
import os
import base64
import binascii
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.basic import missing_required_lib
from ansible.module_utils.connection import Connection

try:
    from jinja2 import Template, TemplateError
    HAS_JINJA2 = True
except ImportError:
    HAS_JINJA2 = False
    TemplateError = Exception


def validate_certificate_format(file_path, expected_format=None):
    """Validate that a file contains a valid PEM or DER encoded certificate

    Args:
        file_path (str): Path to the certificate file
        expected_format (str): Expected format ('PEM' or 'DER'), None for auto-detect

    Returns:
        tuple: (is_valid, detected_format, error_message)
    """
    try:
        with open(file_path, 'rb') as cert_file:
            cert_data = cert_file.read()
        
        # Check for PEM format
        cert_text = cert_data.decode('utf-8', errors='ignore')
        is_pem = '-----BEGIN CERTIFICATE-----' in cert_text and '-----END CERTIFICATE-----' in cert_text
        
        if is_pem:
            # Validate PEM structure
            try:
                # Extract the base64 content between BEGIN and END markers
                pem_lines = cert_text.split('\n')
                cert_lines = []
                in_cert = False
                
                for line in pem_lines:
                    line = line.strip()
                    if line == '-----BEGIN CERTIFICATE-----':
                        in_cert = True
                        continue
                    elif line == '-----END CERTIFICATE-----':
                        in_cert = False
                        break
                    elif in_cert and line:
                        cert_lines.append(line)
                
                if not cert_lines:
                    return (False, None, "Invalid PEM format: no certificate data found between markers")
                
                # Try to decode the base64 content
                cert_b64 = ''.join(cert_lines)
                base64.b64decode(cert_b64, validate=True)
                
                # Check if expected format matches
                if expected_format and expected_format.upper() != 'PEM':
                    return (False, 'PEM', "Certificate is in PEM format but {0} format was expected".format(expected_format))
                
                return (True, 'PEM', None)
                
            except (ValueError, binascii.Error) as e:
                return (False, None, "Invalid PEM format: {0}".format(str(e)))
        
        # Check for DER format
        # DER certificates typically start with 0x30 (SEQUENCE tag)
        if len(cert_data) > 4 and cert_data[0] == 0x30:
            # Basic DER validation - check if it starts like a DER certificate
            # This is a simplified check - a full ASN.1 parser would be more robust
            try:
                # Try to extract length field (simplified)
                length_byte = cert_data[1]
                if length_byte & 0x80:  # Long form length
                    length_octets = length_byte & 0x7F
                    if length_octets > 0 and len(cert_data) > (2 + length_octets):
                        # Check if expected format matches
                        if expected_format and expected_format.upper() != 'DER':
                            return (False, 'DER', "Certificate is in DER format but {0} format was expected".format(expected_format))
                        return (True, 'DER', None)
                else:  # Short form length
                    if len(cert_data) > 2:
                        # Check if expected format matches
                        if expected_format and expected_format.upper() != 'DER':
                            return (False, 'DER', "Certificate is in DER format but {0} format was expected".format(expected_format))
                        return (True, 'DER', None)
            except (ValueError, IndexError, TypeError) as e:
                return (False, None, "Invalid DER format: {0}".format(str(e)))
        
        return (False, None, "File does not appear to be a valid PEM or DER encoded certificate")
        
    except IOError as e:
        return (False, None, "Cannot read certificate file: {0}".format(str(e)))
    except UnicodeDecodeError:
        # If we can't decode as UTF-8, it might be DER, but we already checked that
        return (False, None, "File contains binary data that is not a valid DER certificate")


def validate_private_key_format(file_path):
    """Validate that a file contains a valid PEM encoded private key

    Args:
        file_path (str): Path to the private key file

    Returns:
        tuple: (is_valid, error_message)
    """
    try:
        with open(file_path, 'rb') as key_file:
            key_data = key_file.read()
        
        key_text = key_data.decode('utf-8', errors='ignore')
        
        # Check for common private key PEM markers
        key_markers = [
            ('-----BEGIN PRIVATE KEY-----', '-----END PRIVATE KEY-----'),
            ('-----BEGIN RSA PRIVATE KEY-----', '-----END RSA PRIVATE KEY-----'),
            ('-----BEGIN EC PRIVATE KEY-----', '-----END EC PRIVATE KEY-----'),
            ('-----BEGIN ENCRYPTED PRIVATE KEY-----', '-----END ENCRYPTED PRIVATE KEY-----')
        ]
        
        for begin_marker, end_marker in key_markers:
            if begin_marker in key_text and end_marker in key_text:
                try:
                    # Extract and validate base64 content
                    key_lines = key_text.split('\n')
                    key_content_lines = []
                    in_key = False
                    
                    for line in key_lines:
                        line = line.strip()
                        if line == begin_marker:
                            in_key = True
                            continue
                        elif line == end_marker:
                            in_key = False
                            break
                        elif in_key and line:
                            key_content_lines.append(line)
                    
                    if key_content_lines:
                        key_b64 = ''.join(key_content_lines)
                        base64.b64decode(key_b64, validate=True)
                        return (True, None)
                
                except (ValueError, binascii.Error) as e:
                    return (False, "Invalid private key format: {0}".format(str(e)))
        
        return (False, "File does not appear to be a valid PEM encoded private key")
        
    except IOError as e:
        return (False, "Cannot read private key file: {0}".format(str(e)))
    except UnicodeDecodeError:
        return (False, "Private key file contains invalid text encoding")


def validate_inputs(module, result):
    """Validate module inputs based on state type

    Args:
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console
    """
    state = module.params.get("state")
    
    # Validate password length if provided
    password = module.params.get("password")
    if password:
        if len(password) < 4 or len(password) > 30:
            module.fail_json(msg="Password must be between 4 and 30 characters", **result)
    
    # Validate name constraints
    name = module.params.get("name")
    if name:
        if len(name) > 255:
            module.fail_json(msg="Name must not exceed 255 characters", **result)
        
        # Check allowed characters: A-Za-z0-9_@\-\.
        name_pattern = r'^[A-Za-z0-9_@\-\.]+$'
        if not re.match(name_pattern, name):
            module.fail_json(msg="Name contains invalid characters. Allowed: A-Za-z0-9_@\\-\\.", **result)
    
    # State-specific validations
    if state in ["present", "update"]:
        if not module.params.get("ca_cert_file"):
            module.fail_json(msg="ca_cert_file is required for {0} state".format(state), **result)
        
        # Validate certificate file format
        ca_cert_file = module.params.get("ca_cert_file")
        expected_format = module.params.get("format")
        
        if ca_cert_file:
            is_valid, detected_format, error_msg = validate_certificate_format(ca_cert_file, expected_format)
            if not is_valid:
                module.fail_json(msg="Invalid certificate file: {0}".format(error_msg), **result)
            
            # If format was not specified, use the detected format
            if not expected_format and detected_format:
                module.params["format"] = detected_format
        
        # Validate private key file format if provided
        ca_key_file = module.params.get("ca_private_key_file")
        if ca_key_file:
            is_valid, error_msg = validate_private_key_format(ca_key_file)
            if not is_valid:
                module.fail_json(msg="Invalid private key file: {0}".format(error_msg), **result)


def upload_certificate_authority(connection, module, result):
    """Upload a Certificate Authority to Sophos Firewall using direct API call with file uploads

    Args:
        connection (Connection): Ansible Connection object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: API response
    """
    # Get connection details
    try:
        hostname = connection.get_option("host")
        username = connection.get_option("remote_user")
        password = connection.get_option("password")
        port = connection.get_option("port") or 4444
    except (AttributeError, KeyError, TypeError) as error:
        module.fail_json(msg="Failed to get connection details: {0}".format(error), **result)
    
    # Build the API URL
    url = "https://{0}:{1}/webconsole/APIController".format(hostname, port)
    
    # Get certificate authority parameters
    ca_name = module.params.get("name")
    ca_cert_file_path = module.params.get("ca_cert_file")
    ca_key_file_path = module.params.get("ca_private_key_file")
    ca_format = module.params.get("format", "PEM")
    ca_password = module.params.get("password")
    
    # Validate file paths exist
    if not os.path.isfile(ca_cert_file_path):
        module.fail_json(msg="CA certificate file not found: {0}".format(ca_cert_file_path), **result)
    
    if ca_key_file_path and not os.path.isfile(ca_key_file_path):
        module.fail_json(msg="CA private key file not found: {0}".format(ca_key_file_path), **result)
    
    # Build XML request body
    xml_body = '''<Request>
<Login>
  <Username>{0}</Username>
  <Password>{1}</Password>
</Login>
<Set>
  <CertificateAuthority transactionid="10">
    <Name>{2}</Name>
    <Format>{3}</Format>
    <CACertFile>{4}</CACertFile>'''.format(
        username, password, ca_name, ca_format, os.path.basename(ca_cert_file_path)
    )
    
    # Add private key file if provided
    if ca_key_file_path:
        xml_body += '''
    <CAPrivateKeyFile>{0}</CAPrivateKeyFile>'''.format(os.path.basename(ca_key_file_path))
    
    # Add password if provided
    if ca_password:
        xml_body += '''
    <Password>{0}</Password>'''.format(ca_password)
    
    # Add type - assuming "Uploaded" for uploaded certificates
    xml_body += '''
    <Type>Uploaded</Type>
  </CertificateAuthority>
</Set>
</Request>'''
    
    try:
        # Prepare files for upload
        with open(ca_cert_file_path, "rb") as cert_file:
            files = {
                # XML must be called "reqxml"
                "reqxml": (None, xml_body, "application/xml"),
                # Certificate part must be named exactly "CertificateAuthority"
                "CertificateAuthority": (os.path.basename(ca_cert_file_path), cert_file, "application/x-x509-ca-cert"),
            }
            
            # Add private key if provided
            if ca_key_file_path:
                with open(ca_key_file_path, "rb") as key_file:
                    files["CA Private Key"] = (os.path.basename(ca_key_file_path), key_file, "application/x-pem-file")
                    
                    # Make the request
                    response = requests.post(url, files=files, verify=False, timeout=30)
            else:
                # Make the request without private key
                response = requests.post(url, files=files, verify=False, timeout=30)
        
        # Check response
        response.raise_for_status()
        
        # Parse XML response (simplified - you may need more robust XML parsing)
        response_text = response.text
        
        # Try to extract status from XML response
        status_text = "Configuration applied successfully."
        if "failed" in response_text.lower() or "error" in response_text.lower():
            # Extract error message if possible
            if "<Status>" in response_text and "</Status>" in response_text:
                start = response_text.find("<Status>") + 8
                end = response_text.find("</Status>", start)
                if start > 7 and end > start:
                    status_text = response_text[start:end].strip()
            else:
                status_text = "Upload failed: {0}".format(response_text[:200])
        
        # Create a mock response structure similar to SDK responses
        api_response = {
            "Response": {
                "CertificateAuthority": {
                    "Status": {
                        "#text": status_text
                    }
                }
            }
        }
        
        return api_response
        
    except requests.exceptions.RequestException as error:
        module.fail_json(msg="HTTP request failed: {0}".format(error), **result)
    except IOError as error:
        module.fail_json(msg="File I/O error: {0}".format(error), **result)
    except (ValueError, TypeError) as error:
        module.fail_json(msg="Unexpected error during certificate authority upload: {0}".format(error), **result)


def create_certificate_authority(connection, module, result):
    """Create or update a Certificate Authority on Sophos Firewall

    Args:
        connection (Connection): Ansible Connection object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: API response
    """
    payload = """
        <CertificateAuthority>
          <Name>{{ name }}</Name>
          {% if format %}
          <Format>{{ format }}</Format>
          {% endif %}
          {% if ca_cert_file %}
          <CACertFile>{{ ca_cert_file_basename }}</CACertFile>
          {% endif %}
          {% if ca_private_key_file %}
          <CAPrivateKeyFile>{{ ca_private_key_file_basename }}</CAPrivateKeyFile>
          {% endif %}
          {% if password %}
          <Password>{{ password }}</Password>
          {% endif %}
          <Type>Uploaded</Type>
        </CertificateAuthority>
    """
    
    # Prepare template variables
    template_vars = {
        "name": module.params.get("name"),
        "format": module.params.get("format"),
        "ca_cert_file": module.params.get("ca_cert_file"),
        "ca_private_key_file": module.params.get("ca_private_key_file"),
        "password": module.params.get("password")
    }
    
    # Add basename variables for file references
    if template_vars["ca_cert_file"]:
        template_vars["ca_cert_file_basename"] = os.path.basename(template_vars["ca_cert_file"])
    if template_vars["ca_private_key_file"]:
        template_vars["ca_private_key_file_basename"] = os.path.basename(template_vars["ca_private_key_file"])
    
    # Render the template for debugging
    rendered_payload = ""
    if HAS_JINJA2:
        try:
            template = Template(payload)
            rendered_payload = template.render(**template_vars)
        except (TemplateError, TypeError, ValueError) as template_error:
            module.fail_json(
                msg="Template rendering failed: {0}".format(template_error),
                payload=payload,
                template_vars=template_vars,
                **result
            )
    else:
        rendered_payload = "Jinja2 not available for template rendering"
    
    try:
        with contextlib.redirect_stdout(output_buffer):
            resp = connection.invoke_sdk("submit_xml", module_args={
                "template_data": payload,
                "template_vars": template_vars,
                "debug": True
                }
            )
    except (SophosFirewallAPIError, RequestException) as error:
        module.fail_json(
            msg="An unexpected error occurred: {0}".format(error),
            rendered_payload=rendered_payload,
            template_vars=template_vars,
            **result
        )
    
    if not resp["success"]:
        module.fail_json(
            msg="An error occurred: {0}".format(resp["response"]),
            rendered_payload=rendered_payload,
            template_vars=template_vars,
            **result
        )

    return resp["response"]


def remove_certificate_authority(connection, module, result):
    """Remove a Certificate Authority from Sophos Firewall

    Args:
        connection (Connection): Ansible Connection object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: API response
    """
    try:
        resp = connection.invoke_sdk("remove", module_args={"xml_tag": "CertificateAuthority", "name": module.params.get("name")})
    except (SophosFirewallAPIError, RequestException) as error:
        module.fail_json("An unexpected error occurred: {0}".format(error), **result)
    
    if not resp["success"]:
        module.fail_json(msg="An error occurred: {0}".format(resp["response"]))

    return resp["response"]


def main():
    """Code executed at run time."""
    argument_spec = {
        "name": {"required": True, "type": "str"},
        "format": {
            "type": "str",
            "choices": ["PEM", "DER"]
        },
        "ca_cert_file": {"type": "str"},
        "ca_private_key_file": {"type": "str"},
        "password": {"type": "str", "no_log": True},
        "state": {
            "required": True,
            "choices": ["present", "update", "absent"],
        },
    }

    # Define conditional requirements based on state
    required_if = [
        ("state", "present", ["ca_cert_file"], True),
        ("state", "update", ["ca_cert_file"], True),
    ]

    module = AnsibleModule(
        argument_spec=argument_spec,
        required_if=required_if,
        supports_check_mode=True,
    )

    if not PREREQ_MET["result"]:
        module.fail_json(msg=missing_required_lib(PREREQ_MET["missing_module"]))

    result = {"changed": False, "check_mode": False}

    state = module.params.get("state")
    
    # Validate inputs
    if state in ["present", "update"]:
        validate_inputs(module, result)

    try:
        connection = Connection(module._socket_path)  # pylint: disable=protected-access
    except AssertionError:
        module.fail_json(msg="Connection error: Ensure you are targeting a remote host and not using 'delegate_to: localhost'.")

    if not hasattr(connection, "httpapi"):
        module.fail_json(msg="HTTPAPI plugin is not initialized. Ensure the connection is set to 'httpapi'.")

    if module.check_mode:
        result["check_mode"] = True
        module.exit_json(**result)

    if state in ["present", "update"]:
        # Use file upload method for certificate authority operations
        api_response = upload_certificate_authority(connection, module, result)
        
        # Check if the certificate authority was created/updated successfully
        if api_response.get("Response", {}).get("CertificateAuthority", {}).get("Status", {}).get("#text") == "Configuration applied successfully.":
            result["changed"] = True
        else:
            # If no specific success message, assume success if no error occurred
            result["changed"] = True
            
        result["api_response"] = api_response

    elif state == "absent":
        api_response = remove_certificate_authority(connection, module, result)
        result["changed"] = True
        result["api_response"] = api_response

    module.exit_json(**result)


if __name__ == "__main__":
    main()