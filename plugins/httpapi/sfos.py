# Copyright 2024 Sophos Ltd.  All rights reserved.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = """
---
module: sfos
short_description: HTTPAPI plugin for Sophos Firewall (SFOS)
description:
  - This plugin enables communication with a Sophos Firewall (SFOS)
version_added: "2.0.0"
author: "Matt Mullen (@mamullen13316)"
"""

from ansible_collections.ansible.netcommon.plugins.plugin_utils.httpapi_base import HttpApiBase
from sophosfirewall_python.firewallapi import SophosFirewall, SophosFirewallAuthFailure, SophosFirewallAPIError, SophosFirewallZeroRecords
from requests.exceptions import RequestException
import sys

# sys.stderr.write("SophosFirewall HTTPAPI Plugin is being loaded...\n")

class HttpApi(HttpApiBase):
    """Ansible HTTPAPI plugin for Sophos Firewall"""

    def send_request(self, data=None, headers=None):
        """Required method, even if not used"""
        raise NotImplementedError("send_request() is not yet implemented.")

    def invoke_sdk(self, method_name, module_args=None):
        """Send request to the firewall using sophosfirewall-python SDK.

        Args:
            method_name (function): The SDK method to call.
            module_args (dict): Arguments to pass to the SophosFirewall object method.
        """
        client = SophosFirewall(self.connection.get_option('remote_user'),
                                self.connection.get_option('password'),
                                self.connection.get_option('host'),
                                self.connection.get_option('port'),
                                self.connection.get_option('validate_certs'))
        method = getattr(client, method_name)

        try:
            resp = method(**module_args)
        except SophosFirewallZeroRecords as error:
            return {"success": True, "exists": False, "response": str(error)}
        except SophosFirewallAuthFailure as error:
            return {"success": False, "response": str(error)}
        except SophosFirewallAPIError as error:
            return {"success": False, "response": str(error)}
        except RequestException as error:
            return {"success": False, "response": str(error)}
        
        return {"success": True, "exists": True, "response": resp}
    
