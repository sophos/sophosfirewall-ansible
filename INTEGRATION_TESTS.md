# Sophos Firewall Integration Test Automation

This directory contains automation tools for running all Sophos Firewall collection integration tests using `ansible-test integration` commands.

## Files Created

- `run_integration_tests.yml` - Main Ansible playbook that runs all integration tests
- `run_tests.sh` - Bash script wrapper for easier test execution
- `integration_test_results_*.md` - Generated test result reports

## Usage

### Using the Ansible Playbook Directly

**IMPORTANT:** The playbook must be run from the collection root directory.

```bash
# Navigate to collection directory first
cd /path/to/collections/ansible_collections/sophos/sophos_firewall/

# Run all tests
ansible-playbook run_integration_tests.yml

# Run specific test categories using tags
ansible-playbook run_integration_tests.yml --tags "firewall,security"
ansible-playbook run_integration_tests.yml --tags "core,admin"
ansible-playbook run_integration_tests.yml --tags "network,objects"

# Skip certain test categories
ansible-playbook run_integration_tests.yml --skip-tags "auth,slow"

# Run with verbose output
ansible-playbook run_integration_tests.yml -v

# Run in check mode (dry-run)
ansible-playbook run_integration_tests.yml --check
```

### Using the Shell Script Wrapper

```bash
# Make executable (if needed)
chmod +x run_tests.sh

# Run all tests
./run_tests.sh --all

# Run specific categories
./run_tests.sh --tags "firewall,security"
./run_tests.sh --tags "core,admin" --verbose

# Skip categories
./run_tests.sh --skip-tags "auth"

# List available tags
./run_tests.sh --list

# Get help
./run_tests.sh --help
```

## Available Test Categories and Tags

### Core System
- **Tags:** `admin`, `admin_settings`, `core`, `dns`, `xmlapi`, `zone`, `network`, `interfaces`
- **Tests:** sfos_admin_settings, sfos_dns, sfos_xmlapi, sfos_zone

### Security & Protection  
- **Tags:** `firewall`, `rule`, `rulegroup`, `security`, `policy`, `ips`, `atp`, `protection`, `malware`
- **Tests:** sfos_firewall_rule, sfos_firewall_rulegroup, sfos_ips, sfos_atp, sfos_malware_protection

### Authentication
- **Tags:** `auth`, `authentication`, `ad`, `azure`, `ldap`, `radius`, `tacacs`, `user`
- **Tests:** sfos_authentication_*, sfos_user

### Network Objects
- **Tags:** `objects`, `host`, `hostgroup`, `ip`, `fqdn`, `service`, `servicegroup`
- **Tests:** sfos_ip_host, sfos_fqdn_host, sfos_service, sfos_servicegroup, etc.

### Monitoring & Logging
- **Tags:** `monitoring`, `snmp`, `syslog`, `logging`, `netflow`, `notification`, `email`, `alerts`
- **Tests:** sfos_snmp_agent, sfos_syslog, sfos_netflow, sfos_notification_target

### Web Security
- **Tags:** `web`, `filtering`, `policy`, `category`, `filetype`, `useractivity`
- **Tests:** sfos_web_policy, sfos_web_category, sfos_web_filetype, sfos_web_useractivity

### VPN & Connectivity
- **Tags:** `vpn`, `ipsec`, `connection`  
- **Tests:** sfos_ipsec_connection

### Certificates & Crypto
- **Tags:** `certificate`, `cert`, `ca`, `crypto`
- **Tests:** sfos_certificate, sfos_certificate_authority

### Administration
- **Tags:** `backup`, `maintenance`, `time`, `ntp`, `system`, `device`, `access`, `profile`
- **Tests:** sfos_backup, sfos_time, sfos_device_access_profile

## Test Results

After running tests, the playbook generates:
- Console summary with pass/fail counts
- Detailed markdown report: `integration_test_results_[timestamp].md`
- Failed test list for easy identification

## Example Usage Scenarios

```bash
# Test core firewall functionality
./run_tests.sh --tags "firewall,rule,rulegroup,security"

# Test network configuration
./run_tests.sh --tags "network,objects,dns,zone"

# Test monitoring and logging
./run_tests.sh --tags "monitoring,logging,snmp,syslog"

# Test everything except authentication (faster for development)
./run_tests.sh --skip-tags "auth,authentication"

# Test specific modules for debugging
ansible-playbook run_integration_tests.yml --tags "notification,admin"
```

## Prerequisites

1. Ensure `ansible-test` is available in your PATH
2. Configure your integration test environment (firewall access, credentials)
3. Set up proper `tests/integration/integration_config.yml` if required

## Notes

- Each test runs with `ansible-test integration [module_name] -v`
- Tests run with `ignore_errors: true` to continue on failures
- Final task fails if any tests failed, providing clear exit status
- All test results are collected and summarized at the end
- Tests are tagged for flexible execution based on functional areas