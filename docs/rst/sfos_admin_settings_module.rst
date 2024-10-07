.. Document meta

:orphan:

.. |antsibull-internal-nbsp| unicode:: 0xA0
    :trim:

.. meta::
  :antsibull-docs: 2.14.0

.. Anchors

.. _ansible_collections.sophos.sophos_firewall.sfos_admin_settings_module:

.. Anchors: short name for ansible.builtin

.. Title

sophos.sophos_firewall.sfos_admin_settings module -- Manage Admin and user settings (System \> Administration)
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. Collection note

.. note::
    This module is part of the `sophos.sophos_firewall collection <https://galaxy.ansible.com/ui/repo/published/sophos/sophos_firewall/>`_ (version 1.0.0).

    It is not included in ``ansible-core``.
    To check whether it is installed, run :code:`ansible-galaxy collection list`.

    To install it, use: :code:`ansible-galaxy collection install sophos.sophos\_firewall`.
    You need further requirements to be able to use this module,
    see :ref:`Requirements <ansible_collections.sophos.sophos_firewall.sfos_admin_settings_module_requirements>` for details.

    To use it in a playbook, specify: :code:`sophos.sophos_firewall.sfos_admin_settings`.

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

- Manage settings under System \> Administration \> Admin and user settings


.. Aliases


.. Requirements

.. _ansible_collections.sophos.sophos_firewall.sfos_admin_settings_module_requirements:

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
        <div class="ansibleOptionAnchor" id="parameter-hostname"></div>

      .. _ansible_collections.sophos.sophos_firewall.sfos_admin_settings_module__parameter-hostname:

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
        <div class="ansibleOptionAnchor" id="parameter-hostname_settings"></div>

      .. _ansible_collections.sophos.sophos_firewall.sfos_admin_settings_module__parameter-hostname_settings:

      .. rst-class:: ansible-option-title

      **hostname_settings**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-hostname_settings" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`dictionary`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Hostname settings.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-hostname_settings/description"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.sophos.sophos_firewall.sfos_admin_settings_module__parameter-hostname_settings/description:

      .. rst-class:: ansible-option-title

      **description**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-hostname_settings/description" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Description field in the hostname settings


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-hostname_settings/hostname"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.sophos.sophos_firewall.sfos_admin_settings_module__parameter-hostname_settings/hostname:

      .. rst-class:: ansible-option-title

      **hostname**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-hostname_settings/hostname" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Hostname of the firewall


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-login_disclaimer"></div>

      .. _ansible_collections.sophos.sophos_firewall.sfos_admin_settings_module__parameter-login_disclaimer:

      .. rst-class:: ansible-option-title

      **login_disclaimer**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-login_disclaimer" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Enable/Disable the login disclaimer


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"Enable"`
      - :ansible-option-choices-entry:`"Disable"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-login_security"></div>

      .. _ansible_collections.sophos.sophos_firewall.sfos_admin_settings_module__parameter-login_security:

      .. rst-class:: ansible-option-title

      **login_security**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-login_security" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`dictionary`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Login security settings


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-login_security/block_login"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.sophos.sophos_firewall.sfos_admin_settings_module__parameter-login_security/block_login:

      .. rst-class:: ansible-option-title

      **block_login**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-login_security/block_login" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Enable to block Admin login after configured number of failed attempts within configured time span.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"Enable"`
      - :ansible-option-choices-entry:`"Disable"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-login_security/duration"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.sophos.sophos_firewall.sfos_admin_settings_module__parameter-login_security/duration:

      .. rst-class:: ansible-option-title

      **duration**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-login_security/duration" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Time span within which if Admin Login attempts exceed configured Unsuccessful Attempts, then Admin Login gets blocked. (1-120 seconds).


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-login_security/logout_session"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.sophos.sophos_firewall.sfos_admin_settings_module__parameter-login_security/logout_session:

      .. rst-class:: ansible-option-title

      **logout_session**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-login_security/logout_session" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Enable to logout Admin Session after configured timeout. Specify number of minutes to enable (1-120)


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-login_security/minutes"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.sophos.sophos_firewall.sfos_admin_settings_module__parameter-login_security/minutes:

      .. rst-class:: ansible-option-title

      **minutes**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-login_security/minutes" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Time interval for which Admin Login is blocked (1-60 minutes)


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-login_security/unsuccessful_attempt"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.sophos.sophos_firewall.sfos_admin_settings_module__parameter-login_security/unsuccessful_attempt:

      .. rst-class:: ansible-option-title

      **unsuccessful_attempt**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-login_security/unsuccessful_attempt" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Number of unsuccessful attempts


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-password"></div>

      .. _ansible_collections.sophos.sophos_firewall.sfos_admin_settings_module__parameter-password:

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
        <div class="ansibleOptionAnchor" id="parameter-password_complexity"></div>

      .. _ansible_collections.sophos.sophos_firewall.sfos_admin_settings_module__parameter-password_complexity:

      .. rst-class:: ansible-option-title

      **password_complexity**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-password_complexity" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`dictionary`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Password complexity settings


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-password_complexity/complexity_check"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.sophos.sophos_firewall.sfos_admin_settings_module__parameter-password_complexity/complexity_check:

      .. rst-class:: ansible-option-title

      **complexity_check**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-password_complexity/complexity_check" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Enable/Disable complexity check


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"Enable"`
      - :ansible-option-choices-entry:`"Disable"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-password_complexity/enforce_min_length"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.sophos.sophos_firewall.sfos_admin_settings_module__parameter-password_complexity/enforce_min_length:

      .. rst-class:: ansible-option-title

      **enforce_min_length**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-password_complexity/enforce_min_length" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Enable/Disable enforcement of minimum password length


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"Enable"`
      - :ansible-option-choices-entry:`"Disable"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-password_complexity/include_alpha"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.sophos.sophos_firewall.sfos_admin_settings_module__parameter-password_complexity/include_alpha:

      .. rst-class:: ansible-option-title

      **include_alpha**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-password_complexity/include_alpha" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Enable/Disable special character requirement


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"Enable"`
      - :ansible-option-choices-entry:`"Disable"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-password_complexity/include_numeric"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.sophos.sophos_firewall.sfos_admin_settings_module__parameter-password_complexity/include_numeric:

      .. rst-class:: ansible-option-title

      **include_numeric**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-password_complexity/include_numeric" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Enable/Disable special character requirement


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"Enable"`
      - :ansible-option-choices-entry:`"Disable"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-password_complexity/include_special"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.sophos.sophos_firewall.sfos_admin_settings_module__parameter-password_complexity/include_special:

      .. rst-class:: ansible-option-title

      **include_special**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-password_complexity/include_special" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Enable/Disable special character requirement


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"Enable"`
      - :ansible-option-choices-entry:`"Disable"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-password_complexity/min_length"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.sophos.sophos_firewall.sfos_admin_settings_module__parameter-password_complexity/min_length:

      .. rst-class:: ansible-option-title

      **min_length**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-password_complexity/min_length" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Minimum password length


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-port"></div>

      .. _ansible_collections.sophos.sophos_firewall.sfos_admin_settings_module__parameter-port:

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

      .. _ansible_collections.sophos.sophos_firewall.sfos_admin_settings_module__parameter-state:

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

      .. _ansible_collections.sophos.sophos_firewall.sfos_admin_settings_module__parameter-username:

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

      .. _ansible_collections.sophos.sophos_firewall.sfos_admin_settings_module__parameter-verify:

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
        <div class="ansibleOptionAnchor" id="parameter-webadmin_settings"></div>

      .. _ansible_collections.sophos.sophos_firewall.sfos_admin_settings_module__parameter-webadmin_settings:

      .. rst-class:: ansible-option-title

      **webadmin_settings**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-webadmin_settings" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`dictionary`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Web admin settings


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-webadmin_settings/certificate"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.sophos.sophos_firewall.sfos_admin_settings_module__parameter-webadmin_settings/certificate:

      .. rst-class:: ansible-option-title

      **certificate**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-webadmin_settings/certificate" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Certificate used for the admin interface


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-webadmin_settings/https_port"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.sophos.sophos_firewall.sfos_admin_settings_module__parameter-webadmin_settings/https_port:

      .. rst-class:: ansible-option-title

      **https_port**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-webadmin_settings/https_port" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      HTTPS port for the administrative interface


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-webadmin_settings/portal_custom_hostname"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.sophos.sophos_firewall.sfos_admin_settings_module__parameter-webadmin_settings/portal_custom_hostname:

      .. rst-class:: ansible-option-title

      **portal_custom_hostname**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-webadmin_settings/portal_custom_hostname" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Custom portal hostname


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-webadmin_settings/portal_redirect_mode"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.sophos.sophos_firewall.sfos_admin_settings_module__parameter-webadmin_settings/portal_redirect_mode:

      .. rst-class:: ansible-option-title

      **portal_redirect_mode**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-webadmin_settings/portal_redirect_mode" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Redirect mode


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`"ip"`


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-webadmin_settings/userportal_https_port"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.sophos.sophos_firewall.sfos_admin_settings_module__parameter-webadmin_settings/userportal_https_port:

      .. rst-class:: ansible-option-title

      **userportal_https_port**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-webadmin_settings/userportal_https_port" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      HTTPS port for the user portal


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-webadmin_settings/vpnportal_https_port"></div>

      .. raw:: latex

        \hspace{0.02\textwidth}\begin{minipage}[t]{0.3\textwidth}

      .. _ansible_collections.sophos.sophos_firewall.sfos_admin_settings_module__parameter-webadmin_settings/vpnportal_https_port:

      .. rst-class:: ansible-option-title

      **vpnportal_https_port**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-webadmin_settings/vpnportal_https_port" title="Permalink to this option"></a>

      .. ansible-option-type-line::

        :ansible-option-type:`string`

      .. raw:: html

        </div>

      .. raw:: latex

        \end{minipage}

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      HTTPS port for the VPN portal


      .. raw:: html

        </div>



.. Attributes


.. Notes


.. Seealso


.. Examples

Examples
--------

.. code-block:: yaml+jinja

    - name: Update hostname settings
      sophos.sophos_firewall.sfos_admin_settings:
        username: "{{ username }}"
        password: "{{ password }}"
        hostname: "{{ inventory_hostname }}"
        port: 4444
        verify: false
        hostname_settings:
            hostname: sophos-firewall-dev1
            description: Automation Testing 1
        state: updated
        delegate_to: localhost

    - name: Update webadmin settings
      sophos.sophos_firewall.sfos_admin_settings:
        username: "{{ username }}"
        password: "{{ password }}"
        hostname: "{{ inventory_hostname }}"
        port: 4444
        verify: false
        webadmin_settings:
            vpnportal_https_port: 444
            userportal_https_port: 4445
        state: updated
        delegate_to: localhost

    - name: Update loginsecurity settings
      sophos.sophos_firewall.sfos_admin_settings:
        username: "{{ username }}"
        password: "{{ password }}"
        hostname: "{{ inventory_hostname }}"
        port: 4444
        verify: false
        login_security:
            logout_session: 120
            block_login: Enable
            unsuccessful_attempt: 3
            duration: 30
            minutes: 1
        state: updated
        delegate_to: localhost

    - name: Update administrator password complexity settings
      sophos.sophos_firewall.sfos_admin_settings:
        username: "{{ username }}"
        password: "{{ password }}"
        hostname: "{{ inventory_hostname }}"
        port: 4444
        verify: false
        password_complexity:
            complexity_check: Enable
            enforce_min_length: Enable
            include_alpha: Enable
            include_numeric: Enable
            include_special: Enable
            min_length: 10
        state: updated
        delegate_to: localhost

    - name: Update login disclaimer
      sophos.sophos_firewall.sfos_admin_settings:
        username: "{{ username }}"
        password: "{{ password }}"
        hostname: "{{ inventory_hostname }}"
        port: 4444
        verify: false
        login_disclaimer: Enable
        state: updated
        delegate_to: localhost

    - name: Query admin settings
      sophos.sophos_firewall.sfos_admin_settings:
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

      .. _ansible_collections.sophos.sophos_firewall.sfos_admin_settings_module__return-api_response:

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
