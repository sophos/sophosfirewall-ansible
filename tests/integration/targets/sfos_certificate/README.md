# sfos_certificate Integration Tests

This directory contains integration tests for the `sfos_certificate` module.

## Test Structure

- `aliases` - Test configuration for Ansible test runner
- `tasks/main.yml` - Main test orchestration file
- `tasks/upload_certificate.yml` - Tests for certificate upload functionality
- `tasks/selfsigned_certificate.yml` - Tests for self-signed certificate generation
- `tasks/csr_certificate.yml` - Tests for Certificate Signing Request generation
- `tasks/letsencrypt_certificate.yml` - Tests for Let's Encrypt certificate validation (error cases only)
- `tasks/edge_cases.yml` - Tests for edge cases and error conditions
- `files/test_certificate.pem` - Test certificate for upload tests
- `files/test_certificate.key` - Test private key for upload tests

## Test Coverage

### Upload Certificate Tests
- Upload certificate with private key
- Upload certificate without private key
- Error handling for missing certificate files
- Validation of required parameters

### Self-Signed Certificate Tests
- Basic self-signed certificate generation
- Advanced parameters (SANs, validity dates, etc.)
- Elliptic curve certificates
- RSA certificates with various key lengths
- Different hash algorithms

### Certificate Signing Request Tests
- Basic CSR generation
- Advanced CSR parameters
- Elliptic curve CSR
- RSA CSR with various configurations

### Let's Encrypt Tests
- Parameter validation (email, common name requirements)
- Email format validation
- Note: Actual Let's Encrypt requests are commented out as they require valid domains

### Edge Cases and Error Conditions
- Missing required parameters
- Invalid parameter values
- Minimal valid configurations
- Special characters in certificate names

## Prerequisites

Before running these tests, ensure you have:

1. A working Sophos Firewall accessible for testing
2. Proper authentication credentials configured
3. The integration test configuration file set up

## Running the Tests

The tests follow the standard Ansible integration test structure and can be run using:

```bash
ansible-test integration sfos_certificate
```

Or as part of the full test suite:

```bash
ansible-test integration
```

## Test Certificates

The test directory includes pre-generated self-signed certificates for testing the upload functionality:

- **Subject**: C=US, ST=California, L=San Francisco, O=Test Organization, OU=Test Unit, CN=test.example.com
- **Validity**: 365 days from generation
- **Key**: 2048-bit RSA
- **Format**: PEM

These certificates are safe to use for testing as they are self-signed and contain only test data.

## Notes

- Let's Encrypt tests only validate parameter requirements and don't make actual certificate requests
- Upload tests use relative paths to the test certificate files
- All test certificate names are prefixed with `IGT_` (Integration Test) for easy identification
- Tests include both positive (success) and negative (failure) test cases