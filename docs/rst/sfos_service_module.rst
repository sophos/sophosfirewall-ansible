.. Document meta

:orphan:

.. |antsibull-internal-nbsp| unicode:: 0xA0
    :trim:

.. meta::
  :antsibull-docs: 2.14.0

.. Anchors

.. _ansible_collections.sophos.sophos_firewall.sfos_service_module:

.. Anchors: short name for ansible.builtin

.. Title

sophos.sophos_firewall.sfos_service module -- Manage Service (System \> Hosts and services \> Services)
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. Collection note

.. note::
    This module is part of the `sophos.sophos_firewall collection <https://galaxy.ansible.com/ui/repo/published/sophos/sophos_firewall/>`_ (version 1.2.0).

    It is not included in ``ansible-core``.
    To check whether it is installed, run :code:`ansible-galaxy collection list`.

    To install it, use: :code:`ansible-galaxy collection install sophos.sophos\_firewall`.
    You need further requirements to be able to use this module,
    see :ref:`Requirements <ansible_collections.sophos.sophos_firewall.sfos_service_module_requirements>` for details.

    To use it in a playbook, specify: :code:`sophos.sophos_firewall.sfos_service`.

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

- Creates, updates or removes a Service (System \> Hosts and services \> Services) on Sophos Firewall


.. Aliases


.. Requirements

.. _ansible_collections.sophos.sophos_firewall.sfos_service_module_requirements:

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
        <div class="ansibleOptionAnchor" id="parameter-action"></div>

      .. _ansible_collections.sophos.sophos_firewall.sfos_service_module__parameter-action:

      .. rst-class:: ansible-option-title

      **action**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-action" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      When performing an update, use to add or remove services from the list, or replace the list entirely


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"add"`
      - :ansible-option-choices-entry:`"remove"`
      - :ansible-option-choices-entry-default:`"replace"` :ansible-option-choices-default-mark:`← (default)`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-hostname"></div>

      .. _ansible_collections.sophos.sophos_firewall.sfos_service_module__parameter-hostname:

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
        <div class="ansibleOptionAnchor" id="parameter-name"></div>

      .. _ansible_collections.sophos.sophos_firewall.sfos_service_module__parameter-name:

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

      Name of the Service object to create, update, or delete


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-password"></div>

      .. _ansible_collections.sophos.sophos_firewall.sfos_service_module__parameter-password:

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

      .. _ansible_collections.sophos.sophos_firewall.sfos_service_module__parameter-port:

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
        <div class="ansibleOptionAnchor" id="parameter-service_list"></div>

      .. _ansible_collections.sophos.sophos_firewall.sfos_service_module__parameter-service_list:

      .. rst-class:: ansible-option-title

      **service_list**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-service_list" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`list` / :ansible-option-elements:`elements=dictionary`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      A list of ports/protocols to be included in the service definition.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-service_list/dst_port"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.sophos.sophos_firewall.sfos_service_module__parameter-service_list/dst_port:

      .. rst-class:: ansible-option-title

      **dst_port**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-service_list/dst_port" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Destination TCP or UDP port.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-service_list/icmp_code"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.sophos.sophos_firewall.sfos_service_module__parameter-service_list/icmp_code:

      .. rst-class:: ansible-option-title

      **icmp_code**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-service_list/icmp_code" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      ICMP code in numeric format.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-service_list/icmp_type"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.sophos.sophos_firewall.sfos_service_module__parameter-service_list/icmp_type:

      .. rst-class:: ansible-option-title

      **icmp_type**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-service_list/icmp_type" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      ICMP type in numeric format.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-service_list/protocol"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.sophos.sophos_firewall.sfos_service_module__parameter-service_list/protocol:

      .. rst-class:: ansible-option-title

      **protocol**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-service_list/protocol" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      TCP, UDP, or IP protocol number


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-service_list/src_port"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.sophos.sophos_firewall.sfos_service_module__parameter-service_list/src_port:

      .. rst-class:: ansible-option-title

      **src_port**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-service_list/src_port" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Source TCP or UDP port.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`"1:65535"`

      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-state"></div>

      .. _ansible_collections.sophos.sophos_firewall.sfos_service_module__parameter-state:

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
        <div class="ansibleOptionAnchor" id="parameter-type"></div>

      .. _ansible_collections.sophos.sophos_firewall.sfos_service_module__parameter-type:

      .. rst-class:: ansible-option-title

      **type**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-type" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Type of service object.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"tcporudp"`
      - :ansible-option-choices-entry:`"ip"`
      - :ansible-option-choices-entry:`"icmp"`
      - :ansible-option-choices-entry:`"icmpv6"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-username"></div>

      .. _ansible_collections.sophos.sophos_firewall.sfos_service_module__parameter-username:

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

      .. _ansible_collections.sophos.sophos_firewall.sfos_service_module__parameter-verify:

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

    - name: Retrieve Service
      sophos.sophos_firewall.sfos_service:
        username: "{{ username }}"
        password: "{{ password }}"
        hostname: myfirewallhostname.sophos.net
        port: 4444
        verify: false
        name: TESTSERVICE
        state: query
      delegate_to: localhost

    - name: Create Service
      sophos.sophos_firewall.sfos_service:
        username: "{{ username }}"
        password: "{{ password }}"
        hostname: myfirewallhostname.sophos.net
        port: 4444
        verify: false
        name: TESTSERVICEWEB
        type: tcporudp
        service_list:
          - protocol: tcp
            src_port: 1:65535
            dst_port: 80
          - protocol: tcp
            src_port: 1:65535
            dst_port: 443
        state: present
      delegate_to: localhost

    - name: Add service to service list
      sophos.sophos_firewall.sfos_service:
        username: "{{ username }}"
        password: "{{ password }}"
        hostname: myfirewallhostname.sophos.net
        port: 4444
        verify: false
        name: TESTSERVICEWEB
        service_list:
          - protocol: tcp
            src_port: 1:65535
            dst_port: 8888
        action: add
        state: updated
      delegate_to: localhost

    - name: Add ICMP service
      sophos.sophos_firewall.sfos_service:
        username: "{{ username }}"
        password: "{{ password }}"
        hostname: myfirewallhostname.sophos.net
        port: 4444
        verify: false
        name: TESTICMP
        type: icmp
        service_list:
        - icmp_type: "Echo Reply"
          icmp_code: "Any Code"
        state: present
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

      .. _ansible_collections.sophos.sophos_firewall.sfos_service_module__return-api_response:

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
