.. Document meta

:orphan:

.. |antsibull-internal-nbsp| unicode:: 0xA0
    :trim:

.. meta::
  :antsibull-docs: 2.14.0

.. Anchors

.. _ansible_collections.sophos.sophos_firewall.sfos_user_module:

.. Anchors: short name for ansible.builtin

.. Title

sophos.sophos_firewall.sfos_user module -- Manage Users (Configure \> Authentication \> Users)
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. Collection note

.. note::
    This module is part of the `sophos.sophos_firewall collection <https://galaxy.ansible.com/ui/repo/published/sophos/sophos_firewall/>`_ (version 1.2.0).

    It is not included in ``ansible-core``.
    To check whether it is installed, run :code:`ansible-galaxy collection list`.

    To install it, use: :code:`ansible-galaxy collection install sophos.sophos\_firewall`.
    You need further requirements to be able to use this module,
    see :ref:`Requirements <ansible_collections.sophos.sophos_firewall.sfos_user_module_requirements>` for details.

    To use it in a playbook, specify: :code:`sophos.sophos_firewall.sfos_user`.

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

- Creates, updates or removes Users (Configure \> Authentication \> Users) on Sophos Firewall


.. Aliases


.. Requirements

.. _ansible_collections.sophos.sophos_firewall.sfos_user_module_requirements:

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
        <div class="ansibleOptionAnchor" id="parameter-access_time_policy"></div>

      .. _ansible_collections.sophos.sophos_firewall.sfos_user_module__parameter-access_time_policy:

      .. rst-class:: ansible-option-title

      **access_time_policy**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-access_time_policy" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Access time policy name.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`"Allowed all the time"`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-appliance_login_restriction"></div>

      .. _ansible_collections.sophos.sophos_firewall.sfos_user_module__parameter-appliance_login_restriction:

      .. rst-class:: ansible-option-title

      **appliance_login_restriction**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-appliance_login_restriction" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Login restriction for appliance.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`"AnyNode"`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-applianceaccess_schedule"></div>

      .. _ansible_collections.sophos.sophos_firewall.sfos_user_module__parameter-applianceaccess_schedule:

      .. rst-class:: ansible-option-title

      **applianceaccess_schedule**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-applianceaccess_schedule" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Name of appliance access schedule.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`"All The Time"`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-cisco"></div>

      .. _ansible_collections.sophos.sophos_firewall.sfos_user_module__parameter-cisco:

      .. rst-class:: ansible-option-title

      **cisco**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-cisco" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Enable/Disable Cisco.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"Enable"`
      - :ansible-option-choices-entry-default:`"Disable"` :ansible-option-choices-default-mark:`← (default)`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-clientless_policy"></div>

      .. _ansible_collections.sophos.sophos_firewall.sfos_user_module__parameter-clientless_policy:

      .. rst-class:: ansible-option-title

      **clientless_policy**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-clientless_policy" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Clientless VPN policy.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`"No Policy Applied"`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-description"></div>

      .. _ansible_collections.sophos.sophos_firewall.sfos_user_module__parameter-description:

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

      User description.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-email"></div>

      .. _ansible_collections.sophos.sophos_firewall.sfos_user_module__parameter-email:

      .. rst-class:: ansible-option-title

      **email**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-email" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      User email address.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-group"></div>

      .. _ansible_collections.sophos.sophos_firewall.sfos_user_module__parameter-group:

      .. rst-class:: ansible-option-title

      **group**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-group" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Group name.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-hostname"></div>

      .. _ansible_collections.sophos.sophos_firewall.sfos_user_module__parameter-hostname:

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
        <div class="ansibleOptionAnchor" id="parameter-isencryptcert"></div>

      .. _ansible_collections.sophos.sophos_firewall.sfos_user_module__parameter-isencryptcert:

      .. rst-class:: ansible-option-title

      **isencryptcert**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-isencryptcert" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Enable/Disable encrypted cert.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"Enable"`
      - :ansible-option-choices-entry-default:`"Disable"` :ansible-option-choices-default-mark:`← (default)`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-l2tp"></div>

      .. _ansible_collections.sophos.sophos_firewall.sfos_user_module__parameter-l2tp:

      .. rst-class:: ansible-option-title

      **l2tp**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-l2tp" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Enable/Disable l2tp.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"Enable"`
      - :ansible-option-choices-entry-default:`"Disable"` :ansible-option-choices-default-mark:`← (default)`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-login_restriction"></div>

      .. _ansible_collections.sophos.sophos_firewall.sfos_user_module__parameter-login_restriction:

      .. rst-class:: ansible-option-title

      **login_restriction**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-login_restriction" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Login Restriction for user.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`"UserGroupNode"`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-mac_binding"></div>

      .. _ansible_collections.sophos.sophos_firewall.sfos_user_module__parameter-mac_binding:

      .. rst-class:: ansible-option-title

      **mac_binding**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-mac_binding" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Enable/Disable MAC binding.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"Enable"`
      - :ansible-option-choices-entry-default:`"Disable"` :ansible-option-choices-default-mark:`← (default)`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-name"></div>

      .. _ansible_collections.sophos.sophos_firewall.sfos_user_module__parameter-name:

      .. rst-class:: ansible-option-title

      **name**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-name" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      User display name.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-password"></div>

      .. _ansible_collections.sophos.sophos_firewall.sfos_user_module__parameter-password:

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
        <div class="ansibleOptionAnchor" id="parameter-port"></div>

      .. _ansible_collections.sophos.sophos_firewall.sfos_user_module__parameter-port:

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
        <div class="ansibleOptionAnchor" id="parameter-pptp"></div>

      .. _ansible_collections.sophos.sophos_firewall.sfos_user_module__parameter-pptp:

      .. rst-class:: ansible-option-title

      **pptp**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-pptp" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Enable/Disable pptp.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"Enable"`
      - :ansible-option-choices-entry-default:`"Disable"` :ansible-option-choices-default-mark:`← (default)`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-profile"></div>

      .. _ansible_collections.sophos.sophos_firewall.sfos_user_module__parameter-profile:

      .. rst-class:: ansible-option-title

      **profile**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-profile" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Profile name.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-quarantine_digest"></div>

      .. _ansible_collections.sophos.sophos_firewall.sfos_user_module__parameter-quarantine_digest:

      .. rst-class:: ansible-option-title

      **quarantine_digest**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-quarantine_digest" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Enable/Disable Quarantine Digest.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"Enable"`
      - :ansible-option-choices-entry-default:`"Disable"` :ansible-option-choices-default-mark:`← (default)`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-simultaneous_logins"></div>

      .. _ansible_collections.sophos.sophos_firewall.sfos_user_module__parameter-simultaneous_logins:

      .. rst-class:: ansible-option-title

      **simultaneous_logins**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-simultaneous_logins" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Enable/Disable simultaneous logins


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"Enable"`
      - :ansible-option-choices-entry:`"Disable"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-sslvpn_policy"></div>

      .. _ansible_collections.sophos.sophos_firewall.sfos_user_module__parameter-sslvpn_policy:

      .. rst-class:: ansible-option-title

      **sslvpn_policy**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-sslvpn_policy" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      SSL VPN Policy name.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`"No Policy Applied"`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-state"></div>

      .. _ansible_collections.sophos.sophos_firewall.sfos_user_module__parameter-state:

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
        <div class="ansibleOptionAnchor" id="parameter-surfingquota_policy"></div>

      .. _ansible_collections.sophos.sophos_firewall.sfos_user_module__parameter-surfingquota_policy:

      .. rst-class:: ansible-option-title

      **surfingquota_policy**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-surfingquota_policy" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Surfing quota policy name.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`"Unlimited Internet Access"`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-user"></div>

      .. _ansible_collections.sophos.sophos_firewall.sfos_user_module__parameter-user:

      .. rst-class:: ansible-option-title

      **user**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-user" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string` / :ansible-option-required:`required`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Username to create, update, or delete.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-user_password"></div>

      .. _ansible_collections.sophos.sophos_firewall.sfos_user_module__parameter-user_password:

      .. rst-class:: ansible-option-title

      **user_password**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-user_password" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      User password.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-user_type"></div>

      .. _ansible_collections.sophos.sophos_firewall.sfos_user_module__parameter-user_type:

      .. rst-class:: ansible-option-title

      **user_type**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-user_type" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Type of user (Administrator/User).


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"Administrator"`
      - :ansible-option-choices-entry:`"User"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-username"></div>

      .. _ansible_collections.sophos.sophos_firewall.sfos_user_module__parameter-username:

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

      .. _ansible_collections.sophos.sophos_firewall.sfos_user_module__parameter-verify:

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


.. Attributes


.. Notes


.. Seealso


.. Examples

Examples
--------

.. code-block:: yaml+jinja

    - name: Create User
      sophos.sophos_firewall.sfos_user:
        username: "{{ username }}"
        password: "{{ password }}"
        hostname: myfirewallhostname.sophos.net
        port: 4444
        verify: false
        user: testuser
        name: Test User
        description: Testing user creation from Ansible
        user_password: Sup3rS3cr3tP@ssw0rd
        user_type: User
        group: Open Group
        email: test.user@sophos.com
        state: present



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

      .. _ansible_collections.sophos.sophos_firewall.sfos_user_module__return-api_response:

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
    url: "https://github.com/sophos/sophosfirewall-ansible/issues"
    external: true
  - title: "Repository (Sources)"
    url: "https://github.com/sophos/sophosfirewall-ansible"
    external: true


.. Parsing errors
