.. meta::
  :antsibull-docs: 2.14.0


.. _plugins_in_sophos.sophos_firewall:

Sophos.Sophos_Firewall
======================

Collection version 1.0.0

.. contents::
   :local:
   :depth: 1

Description
-----------

This Ansible collection contains modules for working with Sophos Firewall \<https://www.sophos.com/en-us/products/next-gen-firewall\>

**Author:**

* Matt Mullen (@mamullen13316)

**Supported ansible-core versions:**

* 2.9.10 or newer

.. ansible-links::

  - title: "Issue Tracker"
    url: "https://github.com/sophos/sophosfirewall-ansible/issues"
    external: true
  - title: "Homepage"
    url: "http://example.com"
    external: true
  - title: "Repository (Sources)"
    url: "https://github.com/sophos/sophosfirewall-ansible"
    external: true




.. toctree::
    :maxdepth: 1

Plugin Index
------------

These are the plugins in the sophos.sophos_firewall collection:


Modules
~~~~~~~

* :ansplugin:`sfos_admin_settings module <sophos.sophos_firewall.sfos_admin_settings#module>` -- Manage Admin and user settings (System \> Administration)
* :ansplugin:`sfos_atp module <sophos.sophos_firewall.sfos_atp#module>` -- Manage Active Threat Protection (Protect \> Active threat response \> Sophos X-Ops threat feeds)
* :ansplugin:`sfos_backup module <sophos.sophos_firewall.sfos_backup#module>` -- Manage Backup settings (System \> Backup & firmware)
* :ansplugin:`sfos_device_access_profile module <sophos.sophos_firewall.sfos_device_access_profile#module>` -- Manage Device Access Profiles (System \> Profiles \> Device Access)
* :ansplugin:`sfos_dns module <sophos.sophos_firewall.sfos_dns#module>` -- Manage DNS settings (Configure \> Network \> DNS)
* :ansplugin:`sfos_firewall_rule module <sophos.sophos_firewall.sfos_firewall_rule#module>` -- Manage Firewall Rules (Protect \> Rules & policies)
* :ansplugin:`sfos_fqdn_host module <sophos.sophos_firewall.sfos_fqdn_host#module>` -- Manage FQDN hosts (System \> Hosts & services \> FQDN host)
* :ansplugin:`sfos_fqdn_hostgroup module <sophos.sophos_firewall.sfos_fqdn_hostgroup#module>` -- Manage FQDN Host Groups (System \> Hosts & services \> FQDN host group)
* :ansplugin:`sfos_ip_host module <sophos.sophos_firewall.sfos_ip_host#module>` -- Manage IP Host (System \> Hosts & services \> IP host)
* :ansplugin:`sfos_ip_hostgroup module <sophos.sophos_firewall.sfos_ip_hostgroup#module>` -- Manage IP Hostgroup (System \> Hosts & services \> IP host group)
* :ansplugin:`sfos_ips module <sophos.sophos_firewall.sfos_ips#module>` -- Manage IPS protection (Protect \> Intrusion Protection \> IPS policies)
* :ansplugin:`sfos_malware_protection module <sophos.sophos_firewall.sfos_malware_protection#module>` -- Manage Malware Protection (Configure \> System services \> Malware protection)
* :ansplugin:`sfos_service module <sophos.sophos_firewall.sfos_service#module>` -- Manage Service (System \> Hosts and services \> Services)
* :ansplugin:`sfos_service_acl_exception module <sophos.sophos_firewall.sfos_service_acl_exception#module>` -- Manage Local Service Exception ACL Rules (System \> Administration \> Device Access)
* :ansplugin:`sfos_servicegroup module <sophos.sophos_firewall.sfos_servicegroup#module>` -- Manage Service Group (System \> Hosts and services \> Service Group)
* :ansplugin:`sfos_snmp_agent module <sophos.sophos_firewall.sfos_snmp_agent#module>` -- Manage SNMP Agent (System \> Administration \> SNMP)
* :ansplugin:`sfos_snmp_user module <sophos.sophos_firewall.sfos_snmp_user#module>` -- Manage SNMPv3 User (System \> Administration \> SNMP)
* :ansplugin:`sfos_syslog module <sophos.sophos_firewall.sfos_syslog#module>` -- Manage Syslog servers (Configure \> System services \> Log settings)
* :ansplugin:`sfos_time module <sophos.sophos_firewall.sfos_time#module>` -- Manage Date and Time settings (System \> Administration \> Time)
* :ansplugin:`sfos_user module <sophos.sophos_firewall.sfos_user#module>` -- Manage Users (Configure \> Authentication \> Users)
* :ansplugin:`sfos_xmlapi module <sophos.sophos_firewall.sfos_xmlapi#module>` -- Use the XML API to get, create, update, or delete settings on Sophos Firewall.
* :ansplugin:`sfos_zone module <sophos.sophos_firewall.sfos_zone#module>` -- Manage Zones (Configure \> Network \> Zones)

.. toctree::
    :maxdepth: 1
    :hidden:

    sfos_admin_settings_module
    sfos_atp_module
    sfos_backup_module
    sfos_device_access_profile_module
    sfos_dns_module
    sfos_firewall_rule_module
    sfos_fqdn_host_module
    sfos_fqdn_hostgroup_module
    sfos_ip_host_module
    sfos_ip_hostgroup_module
    sfos_ips_module
    sfos_malware_protection_module
    sfos_service_module
    sfos_service_acl_exception_module
    sfos_servicegroup_module
    sfos_snmp_agent_module
    sfos_snmp_user_module
    sfos_syslog_module
    sfos_time_module
    sfos_user_module
    sfos_xmlapi_module
    sfos_zone_module
