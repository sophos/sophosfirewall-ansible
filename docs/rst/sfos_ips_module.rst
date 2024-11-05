.. Document meta

:orphan:

.. |antsibull-internal-nbsp| unicode:: 0xA0
    :trim:

.. meta::
  :antsibull-docs: 2.14.0

.. Anchors

.. _ansible_collections.sophos.sophos_firewall.sfos_ips_module:

.. Anchors: short name for ansible.builtin

.. Title

sophos.sophos_firewall.sfos_ips module -- Manage IPS protection (Protect \> Intrusion Protection \> IPS policies)
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. Collection note

.. note::
    This module is part of the `sophos.sophos_firewall collection <https://galaxy.ansible.com/ui/repo/published/sophos/sophos_firewall/>`_ (version 1.2.0).

    It is not included in ``ansible-core``.
    To check whether it is installed, run :code:`ansible-galaxy collection list`.

    To install it, use: :code:`ansible-galaxy collection install sophos.sophos\_firewall`.
    You need further requirements to be able to use this module,
    see :ref:`Requirements <ansible_collections.sophos.sophos_firewall.sfos_ips_module_requirements>` for details.

    To use it in a playbook, specify: :code:`sophos.sophos_firewall.sfos_ips`.

.. version_added

.. rst-class:: ansible-version-added

New in sophos.sophos\_firewall 1.2.0

.. contents::
   :local:
   :depth: 1

.. Deprecated


Synopsis
--------

.. Description

- Manage IPS protection (Protect \> Intrusion Protection \> IPS policies) on Sophos Firewall


.. Aliases


.. Requirements

.. _ansible_collections.sophos.sophos_firewall.sfos_ips_module_requirements:

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
        <div class="ansibleOptionAnchor" id="parameter-enabled"></div>

      .. _ansible_collections.sophos.sophos_firewall.sfos_ips_module__parameter-enabled:

      .. rst-class:: ansible-option-title

      **enabled**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-enabled" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`boolean`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Enable (true) or disable (false) IPS protection


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`false`
      - :ansible-option-choices-entry:`true`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-hostname"></div>

      .. _ansible_collections.sophos.sophos_firewall.sfos_ips_module__parameter-hostname:

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
        <div class="ansibleOptionAnchor" id="parameter-password"></div>

      .. _ansible_collections.sophos.sophos_firewall.sfos_ips_module__parameter-password:

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

      .. _ansible_collections.sophos.sophos_firewall.sfos_ips_module__parameter-port:

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
        <div class="ansibleOptionAnchor" id="parameter-state"></div>

      .. _ansible_collections.sophos.sophos_firewall.sfos_ips_module__parameter-state:

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

      Use :literal:`query` to retrieve or :literal:`updated` to modify


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"updated"`
      - :ansible-option-choices-entry:`"query"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-username"></div>

      .. _ansible_collections.sophos.sophos_firewall.sfos_ips_module__parameter-username:

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

      .. _ansible_collections.sophos.sophos_firewall.sfos_ips_module__parameter-verify:

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

    - name: Enable IPS protection
      sophos.sophos_firewall.sfos_ips:
        username: "{{ username }}"
        password: "{{ password }}"
        hostname: "{{ inventory_hostname }}"
        port: 4444
        verify: false
        enabled: true
        state: updated
        delegate_to: localhost

    - name: Query IPS protection settings
      sophos.sophos_firewall.sfos_ips:
        username: "{{ username }}"
        password: "{{ password }}"
        hostname: "{{ inventory_hostname }}"
        port: 4444
        verify: false
        state: query
        delegate_to: localhost



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

      .. _ansible_collections.sophos.sophos_firewall.sfos_ips_module__return-api_response:

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
