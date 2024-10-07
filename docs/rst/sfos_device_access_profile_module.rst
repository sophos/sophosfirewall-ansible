.. Document meta

:orphan:

.. |antsibull-internal-nbsp| unicode:: 0xA0
    :trim:

.. meta::
  :antsibull-docs: 2.14.0

.. Anchors

.. _ansible_collections.sophos.sophos_firewall.sfos_device_access_profile_module:

.. Anchors: short name for ansible.builtin

.. Title

sophos.sophos_firewall.sfos_device_access_profile module -- Manage Device Access Profiles
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. Collection note

.. note::
    This module is part of the `sophos.sophos_firewall collection <https://galaxy.ansible.com/ui/repo/published/sophos/sophos_firewall/>`_ (version 1.0.0).

    It is not included in ``ansible-core``.
    To check whether it is installed, run :code:`ansible-galaxy collection list`.

    To install it, use: :code:`ansible-galaxy collection install sophos.sophos\_firewall`.
    You need further requirements to be able to use this module,
    see :ref:`Requirements <ansible_collections.sophos.sophos_firewall.sfos_device_access_profile_module_requirements>` for details.

    To use it in a playbook, specify: :code:`sophos.sophos_firewall.sfos_device_access_profile`.

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

- Manage Device Access Profiles on Sophos Firewall (System \> Profiles \> Device Access)


.. Aliases


.. Requirements

.. _ansible_collections.sophos.sophos_firewall.sfos_device_access_profile_module_requirements:

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
        <div class="ansibleOptionAnchor" id="parameter-application_filter"></div>

      .. _ansible_collections.sophos.sophos_firewall.sfos_device_access_profile_module__parameter-application_filter:

      .. rst-class:: ansible-option-title

      **application_filter**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-application_filter" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Application Filter permissions.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"Read-Write"`
      - :ansible-option-choices-entry:`"Read-Only"`
      - :ansible-option-choices-entry:`"None"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-cloud_application_dashboard"></div>

      .. _ansible_collections.sophos.sophos_firewall.sfos_device_access_profile_module__parameter-cloud_application_dashboard:

      .. rst-class:: ansible-option-title

      **cloud_application_dashboard**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-cloud_application_dashboard" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Cloud Application Dashboard permissions.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"Read-Write"`
      - :ansible-option-choices-entry:`"Read-Only"`
      - :ansible-option-choices-entry:`"None"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-dashboard"></div>

      .. _ansible_collections.sophos.sophos_firewall.sfos_device_access_profile_module__parameter-dashboard:

      .. rst-class:: ansible-option-title

      **dashboard**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-dashboard" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Dashboard permissions.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"Read-Write"`
      - :ansible-option-choices-entry:`"Read-Only"`
      - :ansible-option-choices-entry:`"None"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-default_permission"></div>

      .. _ansible_collections.sophos.sophos_firewall.sfos_device_access_profile_module__parameter-default_permission:

      .. rst-class:: ansible-option-title

      **default_permission**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-default_permission" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Default permission to use for unspecified arguments when creating profile.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"Read-Write"`
      - :ansible-option-choices-entry:`"Read-Only"`
      - :ansible-option-choices-entry:`"None"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-email_protection"></div>

      .. _ansible_collections.sophos.sophos_firewall.sfos_device_access_profile_module__parameter-email_protection:

      .. rst-class:: ansible-option-title

      **email_protection**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-email_protection" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Email Protection permissions.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"Read-Write"`
      - :ansible-option-choices-entry:`"Read-Only"`
      - :ansible-option-choices-entry:`"None"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-firewall"></div>

      .. _ansible_collections.sophos.sophos_firewall.sfos_device_access_profile_module__parameter-firewall:

      .. rst-class:: ansible-option-title

      **firewall**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-firewall" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Firewall permissions.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"Read-Write"`
      - :ansible-option-choices-entry:`"Read-Only"`
      - :ansible-option-choices-entry:`"None"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-hostname"></div>

      .. _ansible_collections.sophos.sophos_firewall.sfos_device_access_profile_module__parameter-hostname:

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
        <div class="ansibleOptionAnchor" id="parameter-identity"></div>

      .. _ansible_collections.sophos.sophos_firewall.sfos_device_access_profile_module__parameter-identity:

      .. rst-class:: ansible-option-title

      **identity**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-identity" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`dictionary`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Identity permissions group.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-identity/authentication"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.sophos.sophos_firewall.sfos_device_access_profile_module__parameter-identity/authentication:

      .. rst-class:: ansible-option-title

      **authentication**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-identity/authentication" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Authentication permissions.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"Read-Write"`
      - :ansible-option-choices-entry:`"Read-Only"`
      - :ansible-option-choices-entry:`"None"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-identity/disconnect_live_user"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.sophos.sophos_firewall.sfos_device_access_profile_module__parameter-identity/disconnect_live_user:

      .. rst-class:: ansible-option-title

      **disconnect_live_user**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-identity/disconnect_live_user" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Disconnect live user permissions.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"Read-Write"`
      - :ansible-option-choices-entry:`"Read-Only"`
      - :ansible-option-choices-entry:`"None"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-identity/groups"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.sophos.sophos_firewall.sfos_device_access_profile_module__parameter-identity/groups:

      .. rst-class:: ansible-option-title

      **groups**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-identity/groups" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Groups permissions.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"Read-Write"`
      - :ansible-option-choices-entry:`"Read-Only"`
      - :ansible-option-choices-entry:`"None"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-identity/guest_user_management"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.sophos.sophos_firewall.sfos_device_access_profile_module__parameter-identity/guest_user_management:

      .. rst-class:: ansible-option-title

      **guest_user_management**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-identity/guest_user_management" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Guest user management permissions.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"Read-Write"`
      - :ansible-option-choices-entry:`"Read-Only"`
      - :ansible-option-choices-entry:`"None"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-identity/policy"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.sophos.sophos_firewall.sfos_device_access_profile_module__parameter-identity/policy:

      .. rst-class:: ansible-option-title

      **policy**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-identity/policy" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Policy permissions.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"Read-Write"`
      - :ansible-option-choices-entry:`"Read-Only"`
      - :ansible-option-choices-entry:`"None"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-identity/test_external_server_connectivity"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.sophos.sophos_firewall.sfos_device_access_profile_module__parameter-identity/test_external_server_connectivity:

      .. rst-class:: ansible-option-title

      **test_external_server_connectivity**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-identity/test_external_server_connectivity" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Test external server connectivity permissions.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"Read-Write"`
      - :ansible-option-choices-entry:`"Read-Only"`
      - :ansible-option-choices-entry:`"None"`


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-ips"></div>

      .. _ansible_collections.sophos.sophos_firewall.sfos_device_access_profile_module__parameter-ips:

      .. rst-class:: ansible-option-title

      **ips**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-ips" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      IPS permissions.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"Read-Write"`
      - :ansible-option-choices-entry:`"Read-Only"`
      - :ansible-option-choices-entry:`"None"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-logs_reports"></div>

      .. _ansible_collections.sophos.sophos_firewall.sfos_device_access_profile_module__parameter-logs_reports:

      .. rst-class:: ansible-option-title

      **logs_reports**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-logs_reports" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`dictionary`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Logs/Reports permissions group


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-logs_reports/configuration"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.sophos.sophos_firewall.sfos_device_access_profile_module__parameter-logs_reports/configuration:

      .. rst-class:: ansible-option-title

      **configuration**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-logs_reports/configuration" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Configuration permissions.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"Read-Write"`
      - :ansible-option-choices-entry:`"Read-Only"`
      - :ansible-option-choices-entry:`"None"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-logs_reports/de_anonymization"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.sophos.sophos_firewall.sfos_device_access_profile_module__parameter-logs_reports/de_anonymization:

      .. rst-class:: ansible-option-title

      **de_anonymization**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-logs_reports/de_anonymization" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      De-anonymization permissions.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"Read-Write"`
      - :ansible-option-choices-entry:`"Read-Only"`
      - :ansible-option-choices-entry:`"None"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-logs_reports/four_eye_authentication_settings"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.sophos.sophos_firewall.sfos_device_access_profile_module__parameter-logs_reports/four_eye_authentication_settings:

      .. rst-class:: ansible-option-title

      **four_eye_authentication_settings**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-logs_reports/four_eye_authentication_settings" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Four Eye authentication settings permissions.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"Read-Write"`
      - :ansible-option-choices-entry:`"Read-Only"`
      - :ansible-option-choices-entry:`"None"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-logs_reports/log_viewer"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.sophos.sophos_firewall.sfos_device_access_profile_module__parameter-logs_reports/log_viewer:

      .. rst-class:: ansible-option-title

      **log_viewer**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-logs_reports/log_viewer" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Log viewer permissions.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"Read-Write"`
      - :ansible-option-choices-entry:`"Read-Only"`
      - :ansible-option-choices-entry:`"None"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-logs_reports/reports_access"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.sophos.sophos_firewall.sfos_device_access_profile_module__parameter-logs_reports/reports_access:

      .. rst-class:: ansible-option-title

      **reports_access**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-logs_reports/reports_access" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Reports access permissions.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"Read-Write"`
      - :ansible-option-choices-entry:`"Read-Only"`
      - :ansible-option-choices-entry:`"None"`


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-name"></div>

      .. _ansible_collections.sophos.sophos_firewall.sfos_device_access_profile_module__parameter-name:

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

      Name of the profile.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-network"></div>

      .. _ansible_collections.sophos.sophos_firewall.sfos_device_access_profile_module__parameter-network:

      .. rst-class:: ansible-option-title

      **network**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-network" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Network permissions.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"Read-Write"`
      - :ansible-option-choices-entry:`"Read-Only"`
      - :ansible-option-choices-entry:`"None"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-objects"></div>

      .. _ansible_collections.sophos.sophos_firewall.sfos_device_access_profile_module__parameter-objects:

      .. rst-class:: ansible-option-title

      **objects**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-objects" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Objects permissions.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"Read-Write"`
      - :ansible-option-choices-entry:`"Read-Only"`
      - :ansible-option-choices-entry:`"None"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-password"></div>

      .. _ansible_collections.sophos.sophos_firewall.sfos_device_access_profile_module__parameter-password:

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

      .. _ansible_collections.sophos.sophos_firewall.sfos_device_access_profile_module__parameter-port:

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
        <div class="ansibleOptionAnchor" id="parameter-qos"></div>

      .. _ansible_collections.sophos.sophos_firewall.sfos_device_access_profile_module__parameter-qos:

      .. rst-class:: ansible-option-title

      **qos**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-qos" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      QoS permissions.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"Read-Write"`
      - :ansible-option-choices-entry:`"Read-Only"`
      - :ansible-option-choices-entry:`"None"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-state"></div>

      .. _ansible_collections.sophos.sophos_firewall.sfos_device_access_profile_module__parameter-state:

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

      - :ansible-option-choices-entry:`"present"`
      - :ansible-option-choices-entry:`"absent"`
      - :ansible-option-choices-entry:`"updated"`
      - :ansible-option-choices-entry:`"query"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-system"></div>

      .. _ansible_collections.sophos.sophos_firewall.sfos_device_access_profile_module__parameter-system:

      .. rst-class:: ansible-option-title

      **system**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-system" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`dictionary`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      System permissions group.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-system/backup"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.sophos.sophos_firewall.sfos_device_access_profile_module__parameter-system/backup:

      .. rst-class:: ansible-option-title

      **backup**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-system/backup" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Backup permissions.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"Read-Write"`
      - :ansible-option-choices-entry:`"Read-Only"`
      - :ansible-option-choices-entry:`"None"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-system/central_management"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.sophos.sophos_firewall.sfos_device_access_profile_module__parameter-system/central_management:

      .. rst-class:: ansible-option-title

      **central_management**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-system/central_management" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Central Management permissions.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"Read-Write"`
      - :ansible-option-choices-entry:`"Read-Only"`
      - :ansible-option-choices-entry:`"None"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-system/download_certificates"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.sophos.sophos_firewall.sfos_device_access_profile_module__parameter-system/download_certificates:

      .. rst-class:: ansible-option-title

      **download_certificates**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-system/download_certificates" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Restore permissions.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"Read-Write"`
      - :ansible-option-choices-entry:`"Read-Only"`
      - :ansible-option-choices-entry:`"None"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-system/firmware"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.sophos.sophos_firewall.sfos_device_access_profile_module__parameter-system/firmware:

      .. rst-class:: ansible-option-title

      **firmware**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-system/firmware" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Firmware permissions.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"Read-Write"`
      - :ansible-option-choices-entry:`"Read-Only"`
      - :ansible-option-choices-entry:`"None"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-system/ha"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.sophos.sophos_firewall.sfos_device_access_profile_module__parameter-system/ha:

      .. rst-class:: ansible-option-title

      **ha**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-system/ha" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      HA permissions.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"Read-Write"`
      - :ansible-option-choices-entry:`"Read-Only"`
      - :ansible-option-choices-entry:`"None"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-system/licensing"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.sophos.sophos_firewall.sfos_device_access_profile_module__parameter-system/licensing:

      .. rst-class:: ansible-option-title

      **licensing**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-system/licensing" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Licensing permissions.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"Read-Write"`
      - :ansible-option-choices-entry:`"Read-Only"`
      - :ansible-option-choices-entry:`"None"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-system/other_certificate_configuration"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.sophos.sophos_firewall.sfos_device_access_profile_module__parameter-system/other_certificate_configuration:

      .. rst-class:: ansible-option-title

      **other_certificate_configuration**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-system/other_certificate_configuration" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Other certificate configuration permissions.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"Read-Write"`
      - :ansible-option-choices-entry:`"Read-Only"`
      - :ansible-option-choices-entry:`"None"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-system/profile"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.sophos.sophos_firewall.sfos_device_access_profile_module__parameter-system/profile:

      .. rst-class:: ansible-option-title

      **profile**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-system/profile" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Profile permissions.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"Read-Write"`
      - :ansible-option-choices-entry:`"Read-Only"`
      - :ansible-option-choices-entry:`"None"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-system/reboot_shutdown"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.sophos.sophos_firewall.sfos_device_access_profile_module__parameter-system/reboot_shutdown:

      .. rst-class:: ansible-option-title

      **reboot_shutdown**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-system/reboot_shutdown" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Reboot/Shutdown permissions.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"Read-Write"`
      - :ansible-option-choices-entry:`"Read-Only"`
      - :ansible-option-choices-entry:`"None"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-system/restore"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.sophos.sophos_firewall.sfos_device_access_profile_module__parameter-system/restore:

      .. rst-class:: ansible-option-title

      **restore**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-system/restore" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Restore permissions.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"Read-Write"`
      - :ansible-option-choices-entry:`"Read-Only"`
      - :ansible-option-choices-entry:`"None"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-system/services"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.sophos.sophos_firewall.sfos_device_access_profile_module__parameter-system/services:

      .. rst-class:: ansible-option-title

      **services**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-system/services" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Services permissions.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"Read-Write"`
      - :ansible-option-choices-entry:`"Read-Only"`
      - :ansible-option-choices-entry:`"None"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-system/system_password"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.sophos.sophos_firewall.sfos_device_access_profile_module__parameter-system/system_password:

      .. rst-class:: ansible-option-title

      **system_password**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-system/system_password" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Manage system password


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"Read-Write"`
      - :ansible-option-choices-entry:`"Read-Only"`
      - :ansible-option-choices-entry:`"None"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-system/updates"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.sophos.sophos_firewall.sfos_device_access_profile_module__parameter-system/updates:

      .. rst-class:: ansible-option-title

      **updates**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-system/updates" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Updates permissions.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"Read-Write"`
      - :ansible-option-choices-entry:`"Read-Only"`
      - :ansible-option-choices-entry:`"None"`


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-traffic_discovery"></div>

      .. _ansible_collections.sophos.sophos_firewall.sfos_device_access_profile_module__parameter-traffic_discovery:

      .. rst-class:: ansible-option-title

      **traffic_discovery**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-traffic_discovery" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Traffic Discovery permissions.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"Read-Write"`
      - :ansible-option-choices-entry:`"Read-Only"`
      - :ansible-option-choices-entry:`"None"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-username"></div>

      .. _ansible_collections.sophos.sophos_firewall.sfos_device_access_profile_module__parameter-username:

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

      .. _ansible_collections.sophos.sophos_firewall.sfos_device_access_profile_module__parameter-verify:

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
        <div class="ansibleOptionAnchor" id="parameter-vpn"></div>

      .. _ansible_collections.sophos.sophos_firewall.sfos_device_access_profile_module__parameter-vpn:

      .. rst-class:: ansible-option-title

      **vpn**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-vpn" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`dictionary`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      VPN permissions group


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-vpn/connect_tunnel"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.sophos.sophos_firewall.sfos_device_access_profile_module__parameter-vpn/connect_tunnel:

      .. rst-class:: ansible-option-title

      **connect_tunnel**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-vpn/connect_tunnel" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Connect tunnel permissions.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"Read-Write"`
      - :ansible-option-choices-entry:`"Read-Only"`
      - :ansible-option-choices-entry:`"None"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-vpn/other_vpn_configurations"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.sophos.sophos_firewall.sfos_device_access_profile_module__parameter-vpn/other_vpn_configurations:

      .. rst-class:: ansible-option-title

      **other_vpn_configurations**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-vpn/other_vpn_configurations" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Other VPN configurations permissions.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"Read-Write"`
      - :ansible-option-choices-entry:`"Read-Only"`
      - :ansible-option-choices-entry:`"None"`


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-waf"></div>

      .. _ansible_collections.sophos.sophos_firewall.sfos_device_access_profile_module__parameter-waf:

      .. rst-class:: ansible-option-title

      **waf**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-waf" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`dictionary`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      WAF permissions group


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-waf/alerts"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.sophos.sophos_firewall.sfos_device_access_profile_module__parameter-waf/alerts:

      .. rst-class:: ansible-option-title

      **alerts**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-waf/alerts" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Alerts permissions.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"Read-Write"`
      - :ansible-option-choices-entry:`"Read-Only"`
      - :ansible-option-choices-entry:`"None"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-waf/other_waf_configuration"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.sophos.sophos_firewall.sfos_device_access_profile_module__parameter-waf/other_waf_configuration:

      .. rst-class:: ansible-option-title

      **other_waf_configuration**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-waf/other_waf_configuration" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Other WAF configuration permissions.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"Read-Write"`
      - :ansible-option-choices-entry:`"Read-Only"`
      - :ansible-option-choices-entry:`"None"`


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-web_filter"></div>

      .. _ansible_collections.sophos.sophos_firewall.sfos_device_access_profile_module__parameter-web_filter:

      .. rst-class:: ansible-option-title

      **web_filter**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-web_filter" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Web Filter permissions.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"Read-Write"`
      - :ansible-option-choices-entry:`"Read-Only"`
      - :ansible-option-choices-entry:`"None"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-wireless_protection"></div>

      .. _ansible_collections.sophos.sophos_firewall.sfos_device_access_profile_module__parameter-wireless_protection:

      .. rst-class:: ansible-option-title

      **wireless_protection**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-wireless_protection" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`dictionary`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Wireless protection permissions group


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-wireless_protection/wireless_protection_access_point"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.sophos.sophos_firewall.sfos_device_access_profile_module__parameter-wireless_protection/wireless_protection_access_point:

      .. rst-class:: ansible-option-title

      **wireless_protection_access_point**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-wireless_protection/wireless_protection_access_point" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Wireless protection access point permissions.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"Read-Write"`
      - :ansible-option-choices-entry:`"Read-Only"`
      - :ansible-option-choices-entry:`"None"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-wireless_protection/wireless_protection_mesh"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.sophos.sophos_firewall.sfos_device_access_profile_module__parameter-wireless_protection/wireless_protection_mesh:

      .. rst-class:: ansible-option-title

      **wireless_protection_mesh**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-wireless_protection/wireless_protection_mesh" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Wireless protection mesh permissions.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"Read-Write"`
      - :ansible-option-choices-entry:`"Read-Only"`
      - :ansible-option-choices-entry:`"None"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-wireless_protection/wireless_protection_network"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.sophos.sophos_firewall.sfos_device_access_profile_module__parameter-wireless_protection/wireless_protection_network:

      .. rst-class:: ansible-option-title

      **wireless_protection_network**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-wireless_protection/wireless_protection_network" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Wireless protection network permissions.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"Read-Write"`
      - :ansible-option-choices-entry:`"Read-Only"`
      - :ansible-option-choices-entry:`"None"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-wireless_protection/wireless_protection_overview"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.sophos.sophos_firewall.sfos_device_access_profile_module__parameter-wireless_protection/wireless_protection_overview:

      .. rst-class:: ansible-option-title

      **wireless_protection_overview**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-wireless_protection/wireless_protection_overview" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Wireless protection overview permissions.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"Read-Write"`
      - :ansible-option-choices-entry:`"Read-Only"`
      - :ansible-option-choices-entry:`"None"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-wireless_protection/wireless_protection_settings"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.sophos.sophos_firewall.sfos_device_access_profile_module__parameter-wireless_protection/wireless_protection_settings:

      .. rst-class:: ansible-option-title

      **wireless_protection_settings**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-wireless_protection/wireless_protection_settings" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Wireless protection permissions.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"Read-Write"`
      - :ansible-option-choices-entry:`"Read-Only"`
      - :ansible-option-choices-entry:`"None"`


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-wizard"></div>

      .. _ansible_collections.sophos.sophos_firewall.sfos_device_access_profile_module__parameter-wizard:

      .. rst-class:: ansible-option-title

      **wizard**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-wizard" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Wizard permissions.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"Read-Write"`
      - :ansible-option-choices-entry:`"Read-Only"`
      - :ansible-option-choices-entry:`"None"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-zero_day_protection"></div>

      .. _ansible_collections.sophos.sophos_firewall.sfos_device_access_profile_module__parameter-zero_day_protection:

      .. rst-class:: ansible-option-title

      **zero_day_protection**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-zero_day_protection" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Zero day protection permissions.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"Read-Write"`
      - :ansible-option-choices-entry:`"Read-Only"`
      - :ansible-option-choices-entry:`"None"`


      .. raw:: html

        </div>


.. Attributes


.. Notes


.. Seealso


.. Examples

Examples
--------

.. code-block:: yaml+jinja

    - name: CREATE A READ-ONLY PROFILE
      sophos.sophos_firewall.sfos_device_access_profile:
        username: "{{ username }}"
        password: "{{ password }}"
        hostname: "{{ inventory_hostname }}"
        port: 4444
        verify: false
        name: ReadOnlyAll
        default_permission: Read-Only
        state: present
        delegate_to: localhost

    - name: CREATE A WIRELESS ADMIN PROFILE
      sophos.sophos_firewall.sfos_admin_settings:
        username: "{{ username }}"
        password: "{{ password }}"
        hostname: "{{ inventory_hostname }}"
        port: 4444
        verify: false
        name: WirelessAdmin
        default_permission: Read-Only
        wireless_protection:
            wireless_protection_overview: Read-Write
            wireless_protection_settings: Read-Write
            wireless_protection_network: Read-Write
            wireless_protection_access_point: Read-Write
            wireless_protection_mesh: Read-Write
        state: present
        delegate_to: localhost

    - name: UPDATE PROFILE PERMISSIONS
      sophos.sophos_firewall.sfos_admin_settings:
        username: "{{ username }}"
        password: "{{ password }}"
        hostname: "{{ inventory_hostname }}"
        port: 4444
        verify: false
        name: ExampleProfile
        system:
            central_management: Read-Only
        logs_reports:
            log_viewer: Read-Write
            reports_access: Read-Write
        state: updated
        delegate_to: localhost

    - name: RETRIEVE PROFILE
      sophos.sophos_firewall.sfos_admin_settings:
        username: "{{ username }}"
        password: "{{ password }}"
        hostname: "{{ inventory_hostname }}"
        port: 4444
        verify: false
        name: ExampleProfile
        state: query
        delegate_to: localhost

    - name: DELETE PROFILE
      sophos.sophos_firewall.sfos_admin_settings:
        username: "{{ username }}"
        password: "{{ password }}"
        hostname: "{{ inventory_hostname }}"
        port: 4444
        verify: false
        name: ExampleProfile
        state: absent
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

      .. _ansible_collections.sophos.sophos_firewall.sfos_device_access_profile_module__return-api_response:

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
