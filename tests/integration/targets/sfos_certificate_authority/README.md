# sfos_certificate_authority Integration Tests

This directory contains integration tests for the `sfos_certificate_authority` module.

## Test Structure

- `aliases` - Test configuration for Ansible test runner
- `tasks/main.yml` - Main test orchestration file
- `tasks/upload_ca.yml` - Tests for certificate authority upload functionality
- `tasks/edge_cases.yml` - Tests for edge cases and error conditions
- `tasks/removal_tests.yml` - Tests for certificate authority removal functionality
- `tasks/cleanup_cas.yml` - Cleanup tasks to remove test certificate authorities
- `files/test_ca_certificate.pem` - Test CA certificate for upload tests
- `files/test_ca_certificate.key` - Test CA private key for upload tests

## Test Coverage

### Upload Certificate Authority Tests
- Upload CA certificate with private key
- Upload CA certificate without private key
- Upload CA with PEM format
- Upload CA with DER format
- Upload CA with password protection
- Error handling for missing certificate files
- Validation of required parameters

### Update Certificate Authority Tests
- Update existing CA certificate
- Update CA format
- Update with new certificate file

### Edge Cases and Error Conditions
- Missing required parameters
- Invalid parameter values
- Invalid name characters
- Invalid password length
- Missing certificate files
- Minimal valid configurations

### Removal Tests
- Remove single certificate authority
- Remove multiple certificate authorities
- Handle removal of non-existent CAs

## Prerequisites

- Integration configuration must be set up in `tests/integration/integration_config.yml`
- Required variables:
  - `ansible_user`
  - `ansible_host` 
  - `ansible_password`
  - `ansible_connection` (must be `ansible.netcommon.httpapi`)
  - `ansible_httpapi_validate_certs`
  - `ansible_httpapi_port`
  - `ansible_network_os` (must be `sophos.sophos_firewall.sfos`)

## Running Tests

```bash
ansible-test integration sfos_certificate_authority
```

## Test Files

The test certificate and key files are minimal test certificates suitable for testing certificate authority upload functionality. They should not be used in production environments.

## Notes

- Tests create temporary certificate authorities with predictable names for testing
- All test certificate authorities are cleaned up after tests complete
- Tests include both positive and negative test cases
- Error conditions are validated to ensure proper error handling