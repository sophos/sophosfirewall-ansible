# Copyright 2024 Sophos Ltd.  All rights reserved.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


class ModuleDocFragment(object):
    BASE = r"""
requirements:
  - sophosfirewall-python

notes:
  - Beginning in version 1.5.0, this module requires use of an httpapi connection plugin.
  - Existing playbooks from versions prior to 1.5.0 will need to be updated, removing C(username), C(password), C(hostname), C(port) and C(verify) arguments from tasks.
  - These settings can now be configured as inventory, playbook, or task variables. Example inventory configuration::

      all:
        hosts:
          testfirewall:
            ansible_host: <firewall_ip_or_hostname>
        vars:
          ansible_user: <firewall_username>
          ansible_password: <firewall_password>
          ansible_connection: ansible.netcommon.httpapi
          ansible_httpapi_validate_certs: false
          ansible_httpapi_port: 4444
          ansible_network_os: sophos.sophos_firewall.sfos

  - The C(delegate_to) parameter is also no longer required, and should be removed as it will cause tasks to fail.
"""
