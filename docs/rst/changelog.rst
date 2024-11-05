=====================================
Sophos.Sophos\_Firewall Release Notes
=====================================

.. contents:: Topics

v1.2.0
======

Release Summary
---------------

This release adds modules for working with IPS and Syslog settings

New Modules
-----------

- sophos.sophos_firewall.sfos_ips - Manage IPS protection (Protect > Intrusion Protection > IPS policies).
- sophos.sophos_firewall.sfos_syslog - Manage Syslog servers (Configure > System services > Log settings).

v1.1.0
======

Release Summary
---------------

This release contains new modules for working with the SNMP agent and SNMPv3 users on Sophos Firewall

New Modules
-----------

- sophos.sophos_firewall.sfos_snmp_agent - Manage SNMP Agent (System > Administration > SNMP).
- sophos.sophos_firewall.sfos_snmp_user - Manage SNMPv3 User (System > Administration > SNMP).

v1.0.0
======

Release Summary
---------------

This is the first proper release of the ``sophos.sophos_firewall`` collection.

New Modules
-----------

- sophos.sophos_firewall.sfos_admin_settings - Manage Admin and user settings (System > Administration).
- sophos.sophos_firewall.sfos_atp - Manage Active Threat Protection (Protect > Active threat response > Sophos X-Ops threat feeds).
- sophos.sophos_firewall.sfos_backup - Manage Backup settings (System > Backup & firmware).
- sophos.sophos_firewall.sfos_device_access_profile - Manage Device Access Profiles (System > Profiles > Device Access).
- sophos.sophos_firewall.sfos_dns - Manage DNS settings (Configure > Network > DNS).
- sophos.sophos_firewall.sfos_firewall_rule - Manage Firewall Rules (Protect > Rules & policies).
- sophos.sophos_firewall.sfos_fqdn_host - Manage FQDN hosts (System > Hosts & services > FQDN host).
- sophos.sophos_firewall.sfos_fqdn_hostgroup - Manage FQDN Host Groups (System > Hosts & services > FQDN host group).
- sophos.sophos_firewall.sfos_ip_host - Manage IP Host (System > Hosts & services > IP host).
- sophos.sophos_firewall.sfos_ip_hostgroup - Manage IP Hostgroup (System > Hosts & services > IP host group).
- sophos.sophos_firewall.sfos_malware_protection - Manage Malware Protection (Configure > System services > Malware protection).
- sophos.sophos_firewall.sfos_service - Manage Service (System > Hosts and services > Services).
- sophos.sophos_firewall.sfos_service_acl_exception - Manage Local Service Exception ACL Rules (System > Administration > Device Access).
- sophos.sophos_firewall.sfos_servicegroup - Manage Service Group (System > Hosts and services > Service Group).
- sophos.sophos_firewall.sfos_time - Manage Date and Time settings (System > Administration > Time).
- sophos.sophos_firewall.sfos_user - Manage Users (Configure > Authentication > Users).
- sophos.sophos_firewall.sfos_xmlapi - Use the XML API to get, create, update, or delete settings on Sophos Firewall.
- sophos.sophos_firewall.sfos_zone - Manage Zones (Configure > Network > Zones).
