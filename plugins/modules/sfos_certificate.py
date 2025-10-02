#!/usr/bin/python

# Copyright 2024 Sophos Ltd.  All rights reserved.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: sfos_certificate

short_description: Manage Certificates (System > Certificates)

version_added: "1.2.0"

description: Creates certificates on Sophos Firewall, including uploaded certificates, self-signed certificates, certificate signing requests, and Let's Encrypt certificates

extends_documentation_fragment:
  - sophos.sophos_firewall.fragments.base

options:
    action:
        description: 
            - Select an option for certificate management
        choices: ["UploadCertificate", "GenerateSelfSignedCertificate", "GenerateCertificateSigningRequest", "UploadRemoteCertificate", "RequestLetsEncryptCertificate", "LetsEncryptCertificate"]
        type: str
        required: false
    name:
        description: Name of the Certificate
        required: true
        type: str
    certificate_file:
        description: Certificate file to be uploaded (PEM, DER, CER, P7B, PFX, P12 formats)
        type: str
        required: false
    private_key_file:
        description: Private key file to be uploaded (KEY format)
        type: str
        required: false
    password:
        description: Password for the Certificate used for authentication
        type: str
        required: false
        no_log: true
    valid_from:
        description: Date from which the Certificate is valid. Required when action is GenerateSelfSignedCertificate.
        type: str
        required: false
    valid_upto:
        description: Date upto which the Certificate is valid. Required when action is GenerateSelfSignedCertificate.
        type: str
        required: false
    key_type:
        description: Key type - RSA or elliptic curve
        choices: ["RSA", "Elliptic Curve"]
        type: str
        default: RSA
        required: false
    key_length:
        description: Key length - number of bits used to construct the key
        choices: [1024, 1536, 2048, 4096]
        type: int
        default: 2048
        required: false
    curve_name:
        description: Curve name for elliptic curve keys
        choices: ["secp256r1", "secp384r1", "secp521r1"]
        type: str
        default: secp256r1
        required: false
    secure_hash:
        description: Secure hash algorithm
        choices: ["SHA - 256", "SHA - 384", "SHA - 512"]
        type: str
        default: "SHA - 256"
        required: false
    key_encryption:
        description: Enable Key encryption
        choices: ["y", "Y", "n", "N"]
        type: str
        default: n
        required: false
    certificate_id_type:
        description: Certificate ID type
        type: str
        required: false
    certificate_id:
        description: Value corresponding to the Certificate ID selected
        type: str
        required: false
    country_name:
        description: Country code (2-letter ISO code)
        type: str
        required: false
    organization_name:
        description: Organization name
        type: str
        required: false
    organization_unit_name:
        description: Department name
        type: str
        required: false
    state_province_name:
        description: State within the country
        type: str
        required: false
    locality_name:
        description: Name of the locality
        type: str
        required: false
    common_name:
        description: Common name comprising of host and domain name
        type: str
        required: false
    email_address:
        description: Email Address for communication
        type: str
        required: false
    hosted_address:
        description: Interface for Let's Encrypt challenge
        type: str
        required: false
    certificate_format:
        description: Format of Certificate file
        choices: ["pem", "der", "cer", "pkcs7", "pkcs12", "p7b"]
        type: str
        default: pem
        required: false
    dns_name:
        description: List of DNS Subject Alternative Names (SANs)
        type: list
        elements: str
        required: false
    ip_address:
        description: List of IP address Subject Alternative Names (SANs)
        type: list
        elements: str
        required: false
    certname:
        description: Certificate name
        type: str
        required: false
    state:
        description:
            - Use C(present) to create certificate
            - Use C(absent) to remove certificate
        choices: [present, absent]
        type: str
        required: true

author:
    - Matt Mullen (@mamullen13316)
"""

EXAMPLES = r"""
- name: Upload Certificate
  sophos.sophos_firewall.sfos_certificate:
    name: UPLOADED_CERT
    action: UploadCertificate
    certificate_file: /path/to/certificate.pem
    private_key_file: /path/to/private_key.key
    password: certpassword
    common_name: example.com
    state: present

- name: Generate Self-Signed Certificate
  sophos.sophos_firewall.sfos_certificate:
    name: SELFSIGNED_CERT
    action: GenerateSelfSignedCertificate
    common_name: internal.example.com
    organization_name: Example Organization
    country_name: US
    state_province_name: California
    locality_name: San Francisco
    email_address: admin@example.com
    key_type: RSA
    key_length: 2048
    secure_hash: "SHA - 256"
    valid_from: "2024-01-01"
    valid_upto: "2025-01-01"
    dns_name:
      - internal.example.com
      - www.internal.example.com
    state: present

- name: Generate Certificate Signing Request
  sophos.sophos_firewall.sfos_certificate:
    name: CSR_CERT
    action: GenerateCertificateSigningRequest
    common_name: csr.example.com
    organization_name: Example Organization
    country_name: US
    key_type: RSA
    key_length: 2048
    state: present

- name: Request Let's Encrypt Certificate
  sophos.sophos_firewall.sfos_certificate:
    name: LETSENCRYPT_CERT
    action: RequestLetsEncryptCertificate
    common_name: public.example.com
    email_address: admin@example.com
    hosted_address: 192.168.1.1
    dns_name:
      - public.example.com
      - www.public.example.com
    state: present

- name: Remove Certificate
  sophos.sophos_firewall.sfos_certificate:
    name: CERTIFICATE_TO_REMOVE
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
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.basic import missing_required_lib
from ansible.module_utils.connection import Connection

try:
    from jinja2 import Template, TemplateError
    HAS_JINJA2 = True
except ImportError:
    HAS_JINJA2 = False
    TemplateError = Exception


def validate_inputs(module, result):
    """Validate module inputs based on action type

    Args:
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console
    """
    action = module.params.get("action")
    
    # Validate email format if provided
    email = module.params.get("email_address")
    if email:
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            module.fail_json(msg="Invalid email address format", **result)
    
    # Validate country code if provided
    country = module.params.get("country_name")
    if country and len(country) != 2:
        module.fail_json(msg="Country name must be a 2-letter ISO code", **result)
    
    # Action-specific validations
    if action == "UploadCertificate":
        if not module.params.get("certificate_file"):
            module.fail_json(msg="certificate_file is required for UploadCertificate action", **result)
    
    elif action == "GenerateSelfSignedCertificate":
        required_fields = ["common_name", "valid_from", "valid_upto"]
        for field in required_fields:
            if not module.params.get(field):
                module.fail_json(msg="{0} is required for {1} action".format(field, action), **result)
    
    elif action == "GenerateCertificateSigningRequest":
        required_fields = ["common_name"]
        for field in required_fields:
            if not module.params.get(field):
                module.fail_json(msg="{0} is required for {1} action".format(field, action), **result)
    
    elif action in ["RequestLetsEncryptCertificate", "LetsEncryptCertificate"]:
        required_fields = ["common_name", "email_address"]
        for field in required_fields:
            if not module.params.get(field):
                module.fail_json(msg="{0} is required for {1} action".format(field, action), **result)


def upload_certificate(connection, module, result):
    """Upload a Certificate to Sophos Firewall using direct API call with file uploads

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
    
    # Get certificate parameters
    cert_name = module.params.get("name")
    cert_file_path = module.params.get("certificate_file")
    key_file_path = module.params.get("private_key_file")
    cert_format = module.params.get("certificate_format", "pem")
    
    # Validate file paths exist
    if not os.path.isfile(cert_file_path):
        module.fail_json(msg="Certificate file not found: {0}".format(cert_file_path), **result)
    
    if key_file_path and not os.path.isfile(key_file_path):
        module.fail_json(msg="Private key file not found: {0}".format(key_file_path), **result)
    
    # Build XML request body
    xml_body = '''<Request>
<Login>
  <Username>{0}</Username>
  <Password>{1}</Password>
</Login>
<Set>
  <Certificate transactionid="10">
    <Name>{2}</Name>
    <Action>UploadCertificate</Action>
    <CertificateFormat>{3}</CertificateFormat>
    <CertificateFile>{4}</CertificateFile>'''.format(
        username, password, cert_name, cert_format, os.path.basename(cert_file_path)
    )
    
    # Add private key file if provided
    if key_file_path:
        xml_body += '''
    <PrivateKeyFile>{0}</PrivateKeyFile>'''.format(os.path.basename(key_file_path))
    
    # Add password if provided
    if module.params.get("password"):
        xml_body += '''
    <Password>{0}</Password>'''.format(module.params.get("password"))
    
    xml_body += '''
  </Certificate>
</Set>
</Request>'''
    
    try:
        # Prepare files for upload
        with open(cert_file_path, "rb") as cert_file:
            files = {
                # XML must be called "reqxml"
                "reqxml": (None, xml_body, "application/xml"),
                # Certificate part must be named exactly "Certificate"
                "Certificate": (os.path.basename(cert_file_path), cert_file, "application/x-x509-ca-cert"),
            }
            
            # Add private key if provided
            if key_file_path:
                with open(key_file_path, "rb") as key_file:
                    files["Private Key"] = (os.path.basename(key_file_path), key_file, "application/x-pem-file")
                    
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
                "Certificate": {
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
        module.fail_json(msg="Unexpected error during certificate upload: {0}".format(error), **result)


def create_certificate(connection, module, result):
    """Create a Certificate on Sophos Firewall

    Args:
        connection (Connection): Ansible Connection object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: API response
    """
    payload = """
        <Certificate>
          <Action>{{ action }}</Action>
          <Name>{{ name }}</Name>
          {% if action in ['GenerateSelfSignedCertificate', 'GenerateCertificateSigningRequest'] %}
          {% if valid_from %}
          <ValidFrom>{{ valid_from }}</ValidFrom>
          {% endif %}
          {% if valid_upto %}
          <ValidUpto>{{ valid_upto }}</ValidUpto>
          {% endif %}
          <KeyType>{{ key_type }}</KeyType>
          {% if key_type == 'RSA' %}
          <KeyLength>{{ key_length }}</KeyLength>
          {% elif key_type == 'Elliptic Curve' %}
          <CurveName>{{ curve_name }}</CurveName>
          {% endif %}
          <SecureHash>{{ secure_hash }}</SecureHash>
          {% if key_encryption %}
          <KeyEncryption>{{ key_encryption }}</KeyEncryption>
          {% endif %}
          {% if country_name %}
          <CountryName>{{ country_name }}</CountryName>
          {% endif %}
          {% if state_province_name %}
          <StateProvinceName>{{ state_province_name }}</StateProvinceName>
          {% endif %}
          {% if locality_name %}
          <LocalityName>{{ locality_name }}</LocalityName>
          {% endif %}
          {% if organization_name %}
          <OrganizationName>{{ organization_name }}</OrganizationName>
          {% endif %}
          {% if organization_unit_name %}
          <OrganizationUnitName>{{ organization_unit_name }}</OrganizationUnitName>
          {% endif %}
          <CommonName>{{ common_name }}</CommonName>
          {% if email_address %}
          <EmailAddress>{{ email_address }}</EmailAddress>
          {% endif %}
          {% if dns_name %}
          <DNSSubjectAltNames>
            {% for dns in dns_name %}
            <DNSName>{{ dns }}</DNSName>
            {% endfor %}
          </DNSSubjectAltNames>
          {% endif %}
          {% if ip_address %}
          <IPAddressSubjectAltNames>
            {% for ip in ip_address %}
            <IPAddress>{{ ip }}</IPAddress>
            {% endfor %}
          </IPAddressSubjectAltNames>
          {% endif %}
          {% if certificate_id_type %}
          <CertificateIDType>{{ certificate_id_type }}</CertificateIDType>
          {% endif %}
          {% if certificate_id %}
          <CertificateID>{{ certificate_id }}</CertificateID>
          {% endif %}
          {% endif %}
          {% if action in ['RequestLetsEncryptCertificate', 'LetsEncryptCertificate'] %}
          <CommonName>{{ common_name }}</CommonName>
          {% if email_address %}
          <EmailAddress>{{ email_address }}</EmailAddress>
          {% endif %}
          {% if hosted_address %}
          <HostedAddress>{{ hosted_address }}</HostedAddress>
          {% endif %}
          {% if dns_name %}
          <DNSSubjectAltNames>
            {% for dns in dns_name %}
            <DNSName>{{ dns }}</DNSName>
            {% endfor %}
          </DNSSubjectAltNames>
          {% endif %}
          {% if ip_address %}
          <IPAddressSubjectAltNames>
            {% for ip in ip_address %}
            <IPAddress>{{ ip }}</IPAddress>
            {% endfor %}
          </IPAddressSubjectAltNames>
          {% endif %}
          {% endif %}
        </Certificate>
    """
    
    template_vars = {
        "action": module.params.get("action"),
        "name": module.params.get("name"),
        "valid_from": module.params.get("valid_from"),
        "valid_upto": module.params.get("valid_upto"),
        "key_type": module.params.get("key_type"),
        "key_length": module.params.get("key_length"),
        "curve_name": module.params.get("curve_name"),
        "secure_hash": module.params.get("secure_hash"),
        "key_encryption": module.params.get("key_encryption"),
        "country_name": module.params.get("country_name"),
        "state_province_name": module.params.get("state_province_name"),
        "locality_name": module.params.get("locality_name"),
        "organization_name": module.params.get("organization_name"),
        "organization_unit_name": module.params.get("organization_unit_name"),
        "common_name": module.params.get("common_name"),
        "email_address": module.params.get("email_address"),
        "dns_name": module.params.get("dns_name"),
        "ip_address": module.params.get("ip_address"),
        "certificate_id_type": module.params.get("certificate_id_type"),
        "certificate_id": module.params.get("certificate_id"),
        "hosted_address": module.params.get("hosted_address"),
        "certname": module.params.get("certname")
    }
    
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


def remove_certificate(connection, module, result):
    """Remove a Certificate from Sophos Firewall

    Args:
        connection (Connection): Ansible Connection object
        module (AnsibleModule): AnsibleModule object
        result (dict): Result output to be sent to the console

    Returns:
        dict: API response
    """
    try:
        resp = connection.invoke_sdk("remove", module_args={"xml_tag": "Certificate", "name": module.params.get("name")})
    except Exception as error:
        module.fail_json("An unexpected error occurred: {0}".format(error), **result)
    
    if not resp["success"]:
        module.fail_json(msg="An error occurred: {0}".format(resp["response"]))

    return resp["response"]


def main():
    """Code executed at run time."""
    argument_spec = {
        "action": {
            "type": "str",
            "choices": [
                "UploadCertificate",
                "GenerateSelfSignedCertificate", 
                "GenerateCertificateSigningRequest",
                "UploadRemoteCertificate",
                "RequestLetsEncryptCertificate",
                "LetsEncryptCertificate"
            ]
        },
        "name": {"required": True, "type": "str"},
        "certificate_file": {"type": "str"},
        "private_key_file": {"type": "str"},
        "password": {"type": "str", "no_log": True},
        "valid_from": {"type": "str"},
        "valid_upto": {"type": "str"},
        "key_type": {
            "type": "str",
            "choices": ["RSA", "Elliptic Curve"],
            "default": "RSA"
        },
        "key_length": {
            "type": "int",
            "choices": [1024, 1536, 2048, 4096],
            "default": 2048
        },
        "curve_name": {
            "type": "str",
            "choices": ["secp256r1", "secp384r1", "secp521r1"],
            "default": "secp256r1"
        },
        "secure_hash": {
            "type": "str",
            "choices": ["SHA - 256", "SHA - 384", "SHA - 512"],
            "default": "SHA - 256"
        },
        "key_encryption": {
            "type": "str",
            "choices": ["y", "Y", "n", "N"],
            "default": "n"
        },
        "certificate_id_type": {"type": "str"},
        "certificate_id": {"type": "str"},
        "country_name": {"type": "str"},
        "organization_name": {"type": "str"},
        "organization_unit_name": {"type": "str"},
        "state_province_name": {"type": "str"},
        "locality_name": {"type": "str"},
        "common_name": {"type": "str"},
        "email_address": {"type": "str"},
        "hosted_address": {"type": "str"},
        "certificate_format": {
            "type": "str",
            "choices": ["pem", "der", "cer", "pkcs7", "pkcs12", "p7b"]
        },
        "dns_name": {"type": "list", "elements": "str"},
        "ip_address": {"type": "list", "elements": "str"},
        "certname": {"type": "str"},
        "state": {
            "required": True,
            "choices": ["present", "absent"],
        },
    }

    # Define conditional requirements based on state and action
    required_if = [
        ("state", "present", ["action", "common_name"], True),
        ("action", "GenerateSelfSignedCertificate", ["valid_from", "valid_upto"], True),
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
    if state == "present":
        validate_inputs(module, result)

    try:
        connection = Connection(module._socket_path)
    except AssertionError:
        module.fail_json(msg="Connection error: Ensure you are targeting a remote host and not using 'delegate_to: localhost'.")

    if not hasattr(connection, "httpapi"):
        module.fail_json(msg="HTTPAPI plugin is not initialized. Ensure the connection is set to 'httpapi'.")

    if module.check_mode:
        result["check_mode"] = True
        module.exit_json(**result)

    if state == "present":
        # Use different methods based on action type
        action = module.params.get("action")
        
        if action == "UploadCertificate":
            api_response = upload_certificate(connection, module, result)
        else:
            api_response = create_certificate(connection, module, result)
        
        # Check if the certificate was created successfully
        # Note: The exact response structure may vary based on the actual API
        if api_response.get("Response", {}).get("Certificate", {}).get("Status", {}).get("#text") == "Configuration applied successfully.":
            result["changed"] = True
        else:
            # If no specific success message, assume success if no error occurred
            result["changed"] = True
            
        result["api_response"] = api_response

    elif state == "absent":
        api_response = remove_certificate(connection, module, result)
        result["changed"] = True
        result["api_response"] = api_response

    module.exit_json(**result)


if __name__ == "__main__":
    main()