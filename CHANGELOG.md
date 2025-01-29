# Sophos Firewall Ansible Collection Release Notes

**Topics**

- <a href="#v1-4-1">v1\.4\.1</a>
    - <a href="#bugfixes">Bugfixes</a>
- <a href="#v1-4-0">v1\.4\.0</a>
    - <a href="#release-summary">Release Summary</a>
    - <a href="#new-modules">New Modules</a>
- <a href="#v1-3-0">v1\.3\.0</a>
    - <a href="#release-summary-1">Release Summary</a>
    - <a href="#new-modules-1">New Modules</a>
- <a href="#v1-2-1">v1\.2\.1</a>
    - <a href="#release-summary-2">Release Summary</a>
    - <a href="#bugfixes-1">Bugfixes</a>
- <a href="#v1-2-0">v1\.2\.0</a>
    - <a href="#release-summary-3">Release Summary</a>
    - <a href="#new-modules-2">New Modules</a>
- <a href="#v1-1-0">v1\.1\.0</a>
    - <a href="#release-summary-4">Release Summary</a>
    - <a href="#new-modules-3">New Modules</a>
- <a href="#v1-0-0">v1\.0\.0</a>
    - <a href="#release-summary-5">Release Summary</a>
    - <a href="#new-modules-4">New Modules</a>

<a id="v1-4-1"></a>
## v1\.4\.1

<a id="bugfixes"></a>
### Bugfixes

* Correct test files

<a id="v1-4-0"></a>
## v1\.4\.0

<a id="release-summary"></a>
### Release Summary

This release introduces a new module for working with firewall rule groups\.

<a id="new-modules"></a>
### New Modules

* sophos\.sophos\_firewall\.sfos\_firewall\_rulegroup \- Manage Firewall Rules \(Protect \> Rules \& policies\)\.

<a id="v1-3-0"></a>
## v1\.3\.0

<a id="release-summary-1"></a>
### Release Summary

This release adds modules for working with authentication servers

<a id="new-modules-1"></a>
### New Modules

* sophos\.sophos\_firewall\.sfos\_authentication\_ad \- Manage Authentication settings Active Directory\.
* sophos\.sophos\_firewall\.sfos\_authentication\_azure \- Manage Authentication settings AzureADSSO\.
* sophos\.sophos\_firewall\.sfos\_authentication\_edirectory \- Manage Authentication settings eDirectory\.
* sophos\.sophos\_firewall\.sfos\_authentication\_ldap \- Manage Authentication settings LDAP\.
* sophos\.sophos\_firewall\.sfos\_authentication\_radius \- Manage Authentication settings Radius\.
* sophos\.sophos\_firewall\.sfos\_authentication\_tacacs \- Manage Authentication settings Tacacs\.

<a id="v1-2-1"></a>
## v1\.2\.1

<a id="release-summary-2"></a>
### Release Summary

Minor bug fixes

<a id="bugfixes-1"></a>
### Bugfixes

* Allow use of \'any\' keyword for src/dst networks and services for sfos\_firewall\_rule module
* Fixed documentation error in examples for sfos\_zone

<a id="v1-2-0"></a>
## v1\.2\.0

<a id="release-summary-3"></a>
### Release Summary

This release adds modules for working with IPS and Syslog settings

<a id="new-modules-2"></a>
### New Modules

* sophos\.sophos\_firewall\.sfos\_ips \- Manage IPS protection \(Protect \> Intrusion Protection \> IPS policies\)\.
* sophos\.sophos\_firewall\.sfos\_syslog \- Manage Syslog servers \(Configure \> System services \> Log settings\)\.

<a id="v1-1-0"></a>
## v1\.1\.0

<a id="release-summary-4"></a>
### Release Summary

This release contains new modules for working with the SNMP agent and SNMPv3 users on Sophos Firewall

<a id="new-modules-3"></a>
### New Modules

* sophos\.sophos\_firewall\.sfos\_snmp\_agent \- Manage SNMP Agent \(System \> Administration \> SNMP\)\.
* sophos\.sophos\_firewall\.sfos\_snmp\_user \- Manage SNMPv3 User \(System \> Administration \> SNMP\)\.

<a id="v1-0-0"></a>
## v1\.0\.0

<a id="release-summary-5"></a>
### Release Summary

This is the first proper release of the <code>sophos\.sophos\_firewall</code> collection\.

<a id="new-modules-4"></a>
### New Modules

* sophos\.sophos\_firewall\.sfos\_admin\_settings \- Manage Admin and user settings \(System \> Administration\)\.
* sophos\.sophos\_firewall\.sfos\_atp \- Manage Active Threat Protection \(Protect \> Active threat response \> Sophos X\-Ops threat feeds\)\.
* sophos\.sophos\_firewall\.sfos\_backup \- Manage Backup settings \(System \> Backup \& firmware\)\.
* sophos\.sophos\_firewall\.sfos\_device\_access\_profile \- Manage Device Access Profiles \(System \> Profiles \> Device Access\)\.
* sophos\.sophos\_firewall\.sfos\_dns \- Manage DNS settings \(Configure \> Network \> DNS\)\.
* sophos\.sophos\_firewall\.sfos\_firewall\_rule \- Manage Firewall Rules \(Protect \> Rules \& policies\)\.
* sophos\.sophos\_firewall\.sfos\_fqdn\_host \- Manage FQDN hosts \(System \> Hosts \& services \> FQDN host\)\.
* sophos\.sophos\_firewall\.sfos\_fqdn\_hostgroup \- Manage FQDN Host Groups \(System \> Hosts \& services \> FQDN host group\)\.
* sophos\.sophos\_firewall\.sfos\_ip\_host \- Manage IP Host \(System \> Hosts \& services \> IP host\)\.
* sophos\.sophos\_firewall\.sfos\_ip\_hostgroup \- Manage IP Hostgroup \(System \> Hosts \& services \> IP host group\)\.
* sophos\.sophos\_firewall\.sfos\_malware\_protection \- Manage Malware Protection \(Configure \> System services \> Malware protection\)\.
* sophos\.sophos\_firewall\.sfos\_service \- Manage Service \(System \> Hosts and services \> Services\)\.
* sophos\.sophos\_firewall\.sfos\_service\_acl\_exception \- Manage Local Service Exception ACL Rules \(System \> Administration \> Device Access\)\.
* sophos\.sophos\_firewall\.sfos\_servicegroup \- Manage Service Group \(System \> Hosts and services \> Service Group\)\.
* sophos\.sophos\_firewall\.sfos\_time \- Manage Date and Time settings \(System \> Administration \> Time\)\.
* sophos\.sophos\_firewall\.sfos\_user \- Manage Users \(Configure \> Authentication \> Users\)\.
* sophos\.sophos\_firewall\.sfos\_xmlapi \- Use the XML API to get\, create\, update\, or delete settings on Sophos Firewall\.
* sophos\.sophos\_firewall\.sfos\_zone \- Manage Zones \(Configure \> Network \> Zones\)\.