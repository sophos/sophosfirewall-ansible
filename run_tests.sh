#!/bin/bash

# Sophos Firewall Integration Test Runner Script
# This script provides easy ways to run different categories of integration tests

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLAYBOOK="${SCRIPT_DIR}/run_integration_tests.yml"

show_usage() {
    cat << EOF
Usage: $0 [OPTIONS] [TAG_FILTER]

Run Sophos Firewall integration tests with ansible-test integration commands.

OPTIONS:
    -h, --help              Show this help message
    -l, --list              List available test categories and tags
    -a, --all               Run all integration tests
    -v, --verbose           Run with verbose output
    -c, --check             Run in check mode (dry-run)
    -t, --tags TAGS         Run only tests with specified tags (comma-separated)
    -s, --skip-tags TAGS    Skip tests with specified tags (comma-separated)

EXAMPLES:
    $0 --all                           # Run all tests
    $0 --tags "firewall,security"      # Run only firewall and security tests
    $0 --tags "core,admin"             # Run core and admin tests
    $0 --skip-tags "auth,slow"         # Skip authentication and slow tests
    $0 --tags "network" --verbose      # Run network tests with verbose output

AVAILABLE TEST CATEGORIES:
    Core:         admin, core, dns, xmlapi, zone
    Security:     firewall, security, ips, atp, malware
    Authentication: auth, authentication, ad, azure, ldap, radius, tacacs
    Network:      network, objects, host, hostgroup, service, servicegroup
    Monitoring:   monitoring, snmp, syslog, logging, netflow, notification
    Web Security: web, filtering, policy, category, filetype, useractivity
    VPN:          vpn, ipsec, connection
    Certificates: certificate, cert, ca, crypto
    Other:        backup, maintenance, time, ntp, qos, traffic

EOF
}

list_tags() {
    echo "Available Tags by Category:"
    echo
    echo "Core System:"
    echo "  admin, admin_settings, core, dns, xmlapi, zone, network, interfaces"
    echo
    echo "Security & Protection:"
    echo "  firewall, rule, rulegroup, security, policy, ips, atp, protection"
    echo "  malware, web, filtering, category, filetype, useractivity"
    echo
    echo "Authentication:"
    echo "  auth, authentication, ad, activedirectory, azure, cloud"
    echo "  edirectory, novell, ldap, radius, tacacs, user"
    echo
    echo "Network Objects:"
    echo "  objects, host, hostgroup, ip, fqdn, service, servicegroup"
    echo "  urlgroup, qos, traffic"
    echo
    echo "Monitoring & Logging:"
    echo "  monitoring, snmp, agent, syslog, logging, netflow"
    echo "  notification, email, alerts"
    echo
    echo "VPN & Connectivity:"
    echo "  vpn, ipsec, connection"
    echo
    echo "Certificates & Crypto:"
    echo "  certificate, cert, ca, crypto"
    echo
    echo "Administration:"
    echo "  backup, maintenance, time, ntp, system, device, access, profile"
    echo "  webadmin, acl, exception"
    echo
}

# Default options
VERBOSE=""
CHECK_MODE=""
TAGS=""
SKIP_TAGS=""
RUN_ALL=false

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_usage
            exit 0
            ;;
        -l|--list)
            list_tags
            exit 0
            ;;
        -a|--all)
            RUN_ALL=true
            shift
            ;;
        -v|--verbose)
            VERBOSE="--verbose"
            shift
            ;;
        -c|--check)
            CHECK_MODE="--check"
            shift
            ;;
        -t|--tags)
            TAGS="$2"
            shift 2
            ;;
        -s|--skip-tags)
            SKIP_TAGS="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            show_usage
            exit 1
            ;;
    esac
done

# Check if we're in the collection directory
if [ ! -f "${SCRIPT_DIR}/galaxy.yml" ]; then
    echo "ERROR: This script must be run from the collection root directory."
    echo "Current directory: ${SCRIPT_DIR}"
    echo "Expected to find: galaxy.yml"
    echo
    echo "Please run from: /path/to/collections/ansible_collections/sophos/sophos_firewall/"
    exit 1
fi

# Build ansible-playbook command
CMD="ansible-playbook"

if [ -n "$VERBOSE" ]; then
    CMD="$CMD -v"
fi

if [ -n "$CHECK_MODE" ]; then
    CMD="$CMD --check"
fi

if [ -n "$TAGS" ]; then
    CMD="$CMD --tags \"$TAGS\""
fi

if [ -n "$SKIP_TAGS" ]; then
    CMD="$CMD --skip-tags \"$SKIP_TAGS\""
fi

CMD="$CMD \"$PLAYBOOK\""

# Display what will be run
echo "=========================================="
echo "Sophos Firewall Integration Test Runner"
echo "=========================================="
echo "Command: $CMD"
echo

if [ "$RUN_ALL" = true ]; then
    echo "Running ALL integration tests..."
elif [ -n "$TAGS" ]; then
    echo "Running tests with tags: $TAGS"
elif [ -n "$SKIP_TAGS" ]; then
    echo "Running all tests except: $SKIP_TAGS"
else
    echo "Running all tests (no filters specified)"
fi

echo "=========================================="
echo

# Execute the command
eval $CMD

exit_code=$?

echo
echo "=========================================="
if [ $exit_code -eq 0 ]; then
    echo "Integration tests completed successfully!"
else
    echo "Integration tests failed with exit code: $exit_code"
    echo "Check the output above for details."
fi
echo "=========================================="

exit $exit_code