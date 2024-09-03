# Copyright 2023 Sophos Ltd.  All rights reserved.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


class ModuleDocFragment(object):
    BASE = r"""
requirements:
  - sophosfirewall-python
options:
  username:
    description:
      - "Firewall Username"
    required: true
    type: str
  password:
    description:
      - "Firewall Password"
    required: true
    type: str
  hostname:
    description:
      - "Firewall hostname"
    type: str
    required: true
  port:
    description:
      - "Firewall HTTP Port"
    default: 4444
    required: false
    type: int
  verify:
    description:
      - "Perform certificate verification"
    required: false
    default: true
    type: bool
"""
