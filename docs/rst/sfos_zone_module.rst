.. Document meta

:orphan:

.. |antsibull-internal-nbsp| unicode:: 0xA0
    :trim:

.. meta::
  :antsibull-docs: 2.14.0

.. Anchors

.. _ansible_collections.sophos.sophos_firewall.sfos_zone_module:

.. Anchors: short name for ansible.builtin

.. Title

sophos.sophos_firewall.sfos_zone module -- Manage Zones on Sophos Firewall
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. Collection note

.. note::
    This module is part of the `sophos.sophos_firewall collection <https://galaxy.ansible.com/ui/repo/published/sophos/sophos_firewall/>`_ (version 1.0.0).

    It is not included in ``ansible-core``.
    To check whether it is installed, run :code:`ansible-galaxy collection list`.

    To install it, use: :code:`ansible-galaxy collection install sophos.sophos\_firewall`.
    You need further requirements to be able to use this module,
    see :ref:`Requirements <ansible_collections.sophos.sophos_firewall.sfos_zone_module_requirements>` for details.

    To use it in a playbook, specify: :code:`sophos.sophos_firewall.sfos_zone`.

.. version_added

.. rst-class:: ansible-version-added

New in sophos.sophos\_firewall 1.0.0

.. contents::
   :local:
   :depth: 1

.. Deprecated


Synopsis
--------

.. Description

- Creates, updates or removes firewall zones on Sophos Firewall


.. Aliases


.. Requirements

.. _ansible_collections.sophos.sophos_firewall.sfos_zone_module_requirements:

Requirements
------------
The below requirements are needed on the host that executes this module.

- sophosfirewall-python






.. Options

Parameters
----------

.. tabularcolumns:: \X{1}{3}\X{2}{3}

.. list-table::
  :width: 100%
  :widths: auto
  :header-rows: 1
  :class: longtable ansible-option-table

  * - Parameter
    - Comments

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-ad_sso"></div>

      .. _ansible_collections.sophos.sophos_firewall.sfos_zone_module__parameter-ad_sso:

      .. rst-class:: ansible-option-title

      **ad_sso**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-ad_sso" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Enable/Disable SSO with Active Directory


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"Enable"`
      - :ansible-option-choices-entry:`"Disable"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-captive_portal"></div>

      .. _ansible_collections.sophos.sophos_firewall.sfos_zone_module__parameter-captive_portal:

      .. rst-class:: ansible-option-title

      **captive_portal**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-captive_portal" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Enable/Disable captive portal


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"Enable"`
      - :ansible-option-choices-entry:`"Disable"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-chromebook_sso"></div>

      .. _ansible_collections.sophos.sophos_firewall.sfos_zone_module__parameter-chromebook_sso:

      .. rst-class:: ansible-option-title

      **chromebook_sso**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-chromebook_sso" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Enable/Disable Chromebook SSO


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"Enable"`
      - :ansible-option-choices-entry:`"Disable"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-client_authen"></div>

      .. _ansible_collections.sophos.sophos_firewall.sfos_zone_module__parameter-client_authen:

      .. rst-class:: ansible-option-title

      **client_authen**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-client_authen" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Enable/Disable client authentication service


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"Enable"`
      - :ansible-option-choices-entry:`"Disable"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-description"></div>

      .. _ansible_collections.sophos.sophos_firewall.sfos_zone_module__parameter-description:

      .. rst-class:: ansible-option-title

      **description**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-description" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Description for the zone


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-dns"></div>

      .. _ansible_collections.sophos.sophos_firewall.sfos_zone_module__parameter-dns:

      .. rst-class:: ansible-option-title

      **dns**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-dns" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Enable/Disable DNS network service


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"Enable"`
      - :ansible-option-choices-entry:`"Disable"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-dynamic_routing"></div>

      .. _ansible_collections.sophos.sophos_firewall.sfos_zone_module__parameter-dynamic_routing:

      .. rst-class:: ansible-option-title

      **dynamic_routing**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-dynamic_routing" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Enable/Disable Dynamic Routing


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"Enable"`
      - :ansible-option-choices-entry:`"Disable"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-hostname"></div>

      .. _ansible_collections.sophos.sophos_firewall.sfos_zone_module__parameter-hostname:

      .. rst-class:: ansible-option-title

      **hostname**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-hostname" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string` / :ansible-option-required:`required`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Firewall hostname


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-https"></div>

      .. _ansible_collections.sophos.sophos_firewall.sfos_zone_module__parameter-https:

      .. rst-class:: ansible-option-title

      **https**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-https" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Enable/Disable HTTPS administrative service


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"Enable"`
      - :ansible-option-choices-entry:`"Disable"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-ipsec"></div>

      .. _ansible_collections.sophos.sophos_firewall.sfos_zone_module__parameter-ipsec:

      .. rst-class:: ansible-option-title

      **ipsec**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-ipsec" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Enable/Disable IPSec VPN service


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"Enable"`
      - :ansible-option-choices-entry:`"Disable"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-name"></div>

      .. _ansible_collections.sophos.sophos_firewall.sfos_zone_module__parameter-name:

      .. rst-class:: ansible-option-title

      **name**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-name" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string` / :ansible-option-required:`required`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Name of the zone to create, update, or delete


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-password"></div>

      .. _ansible_collections.sophos.sophos_firewall.sfos_zone_module__parameter-password:

      .. rst-class:: ansible-option-title

      **password**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-password" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string` / :ansible-option-required:`required`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Firewall Password


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-ping"></div>

      .. _ansible_collections.sophos.sophos_firewall.sfos_zone_module__parameter-ping:

      .. rst-class:: ansible-option-title

      **ping**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-ping" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Enable/Disable Ping network service


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"Enable"`
      - :ansible-option-choices-entry:`"Disable"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-port"></div>

      .. _ansible_collections.sophos.sophos_firewall.sfos_zone_module__parameter-port:

      .. rst-class:: ansible-option-title

      **port**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-port" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`integer`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Firewall HTTP Port


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`4444`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-radius_sso"></div>

      .. _ansible_collections.sophos.sophos_firewall.sfos_zone_module__parameter-radius_sso:

      .. rst-class:: ansible-option-title

      **radius_sso**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-radius_sso" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Enable/Disable SSO with Radius


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"Enable"`
      - :ansible-option-choices-entry:`"Disable"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-red"></div>

      .. _ansible_collections.sophos.sophos_firewall.sfos_zone_module__parameter-red:

      .. rst-class:: ansible-option-title

      **red**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-red" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Enable/Disable RED service


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"Enable"`
      - :ansible-option-choices-entry:`"Disable"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-smtp_relay"></div>

      .. _ansible_collections.sophos.sophos_firewall.sfos_zone_module__parameter-smtp_relay:

      .. rst-class:: ansible-option-title

      **smtp_relay**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-smtp_relay" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Enable/Disable SMTP Relay


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"Enable"`
      - :ansible-option-choices-entry:`"Disable"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-snmp"></div>

      .. _ansible_collections.sophos.sophos_firewall.sfos_zone_module__parameter-snmp:

      .. rst-class:: ansible-option-title

      **snmp**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-snmp" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Enable/Disable SNMP


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"Enable"`
      - :ansible-option-choices-entry:`"Disable"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-ssh"></div>

      .. _ansible_collections.sophos.sophos_firewall.sfos_zone_module__parameter-ssh:

      .. rst-class:: ansible-option-title

      **ssh**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-ssh" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Enable/Disable SSH administrative service


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"Enable"`
      - :ansible-option-choices-entry:`"Disable"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-sslvpn"></div>

      .. _ansible_collections.sophos.sophos_firewall.sfos_zone_module__parameter-sslvpn:

      .. rst-class:: ansible-option-title

      **sslvpn**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-sslvpn" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Enable/Disable SSLVPN service


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"Enable"`
      - :ansible-option-choices-entry:`"Disable"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-state"></div>

      .. _ansible_collections.sophos.sophos_firewall.sfos_zone_module__parameter-state:

      .. rst-class:: ansible-option-title

      **state**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-state" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string` / :ansible-option-required:`required`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Use :literal:`query` to retrieve, :literal:`present` to create, :literal:`absent` to remove, or :literal:`updated` to modify


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"present"`
      - :ansible-option-choices-entry:`"absent"`
      - :ansible-option-choices-entry:`"updated"`
      - :ansible-option-choices-entry:`"query"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-user_portal"></div>

      .. _ansible_collections.sophos.sophos_firewall.sfos_zone_module__parameter-user_portal:

      .. rst-class:: ansible-option-title

      **user_portal**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-user_portal" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Enable/Disable user portal


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"Enable"`
      - :ansible-option-choices-entry:`"Disable"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-username"></div>

      .. _ansible_collections.sophos.sophos_firewall.sfos_zone_module__parameter-username:

      .. rst-class:: ansible-option-title

      **username**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-username" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string` / :ansible-option-required:`required`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Firewall Username


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-verify"></div>

      .. _ansible_collections.sophos.sophos_firewall.sfos_zone_module__parameter-verify:

      .. rst-class:: ansible-option-title

      **verify**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-verify" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`boolean`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Perform certificate verification


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`false`
      - :ansible-option-choices-entry-default:`true` :ansible-option-choices-default-mark:`← (default)`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-vpn_portal"></div>

      .. _ansible_collections.sophos.sophos_firewall.sfos_zone_module__parameter-vpn_portal:

      .. rst-class:: ansible-option-title

      **vpn_portal**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-vpn_portal" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Enable/Disable VPN Portal


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"Enable"`
      - :ansible-option-choices-entry:`"Disable"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-web_proxy"></div>

      .. _ansible_collections.sophos.sophos_firewall.sfos_zone_module__parameter-web_proxy:

      .. rst-class:: ansible-option-title

      **web_proxy**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-web_proxy" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Enable/Disable Web Proxy


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"Enable"`
      - :ansible-option-choices-entry:`"Disable"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-wireless_protection"></div>

      .. _ansible_collections.sophos.sophos_firewall.sfos_zone_module__parameter-wireless_protection:

      .. rst-class:: ansible-option-title

      **wireless_protection**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-wireless_protection" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Enable/Disable Wireless Protection


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"Enable"`
      - :ansible-option-choices-entry:`"Disable"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-zone_type"></div>

      .. _ansible_collections.sophos.sophos_firewall.sfos_zone_module__parameter-zone_type:

      .. rst-class:: ansible-option-title

      **zone_type**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-zone_type" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Type of zone to create (LAN/DMZ)


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"LAN"`
      - :ansible-option-choices-entry:`"DMZ"`


      .. raw:: html

        </div>


.. Attributes


.. Notes


.. Seealso


.. Examples

Examples
--------

.. code-block:: yaml+jinja

    - name: Create Zone
      sophos.sophos_firewall.sfos_firewall_rule:
        username: "{{ username }}"
        password: "{{ password }}"
        hostname: myfirewallhostname.sophos.net
        port: 4444
        verify: false
        name: TESTZONE
        description: Zone created by Ansible
        zone_type: LAN
        state: present

    - name: Display Existing Zone
      sophos.sophos_firewall.sfos_firewall_rule:
        username: "{{ username }}"
        password: "{{ password }}"
        hostname: myfirewallhostname.sophos.net
        port: 4444
        verify: false
        name: TESTZONE
        state: query

    - name: Update Zone Admin Services
      sophos.sophos_firewall.sfos_firewall_rule:
        username: "{{ username }}"
        password: "{{ password }}"
        hostname: myfirewallhostname.sophos.net
        port: 4444
        verify: false
        name: TESTZONE
        https: Enable
        ssh: Enable
        state: updated

    - name: Remove Zone
      sophos.sophos_firewall.sfos_firewall_rule:
        username: "{{ username }}"
        password: "{{ password }}"
        hostname: myfirewallhostname.sophos.net
        port: 4444
        verify: false
        name: TESTZONE
        state: absent



.. Facts


.. Return values

Return Values
-------------
Common return values are documented :ref:`here <common_return_values>`, the following are the fields unique to this module:

.. tabularcolumns:: \X{1}{3}\X{2}{3}

.. list-table::
  :width: 100%
  :widths: auto
  :header-rows: 1
  :class: longtable ansible-option-table

  * - Key
    - Description

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-api_response"></div>

      .. _ansible_collections.sophos.sophos_firewall.sfos_zone_module__return-api_response:

      .. rst-class:: ansible-option-title

      **api_response**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-api_response" title="Permalink to this return value"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`dictionary`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Serialized object containing the API response.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` always


      .. raw:: html

        </div>



..  Status (Presently only deprecated)


.. Authors

Authors
~~~~~~~

- Matt Mullen (@mamullen13316)



.. Extra links

Collection links
~~~~~~~~~~~~~~~~

.. ansible-links::

  - title: "Issue Tracker"
    url: "http://example.com/issue/tracker"
    external: true
  - title: "Homepage"
    url: "http://example.com"
    external: true
  - title: "Repository (Sources)"
    url: "http://example.com/repository"
    external: true


.. Parsing errors
