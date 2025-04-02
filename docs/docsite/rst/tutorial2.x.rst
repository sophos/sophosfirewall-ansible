.. _ansible_collections.sophos.sophos_firewall.docsite.usage:

.. note::

   This tutorial uses the syntax required as of version 2.0. Please see the `HTTPAPI Plugin example <https://sophosfirewall-ansible.readthedocs.io/en/latest/docsite/httpapi_example.html>`_ for details.

Tutorial v2.x
===============
This section is intended to help users who may be new to Ansible get up and running with their first playbook using the Sophos Firewall Ansible Collection.
Experienced Ansible users may want to skip this section and review the documentation for the individual `modules <../index.html#modules>`_.
  
Ansible requires two main components to operate; an `inventory <https://docs.ansible.com/ansible/latest/inventory_guide/index.html>`_ 
and a `playbook <https://docs.ansible.com/ansible/latest/playbook_guide/index.html>`_. An inventory file specifies what firewall(s) the Ansible playbook should operate on. It can also include variable
definitions that can be referenced in the playbook. 

Inventory
---------
Below is an inventory file containing a single firewall with
variable definitions needed for connectivity. The ``ansible_httpapi_validate_certs: false`` setting turns off 
certificate checking. This should be set to **true** if the firewall has a valid SSL certificate installed.

.. code-block:: yaml

    # inventory.yml
    all:
      hosts:
        testfirewall:
          ansible_host: [firewall_ip_or_hostname]
      vars:
        ansible_user: "{{ firewall_username }}"
        ansible_password: "{{ firewall_password }}"
        ansible_connection: ansible.netcommon.httpapi
        ansible_httpapi_validate_certs: false
        ansible_httpapi_port: 4444
        ansible_network_os: sophos.sophos_firewall.sfos

Credentials
~~~~~~~~~~~
The ``ansible_user`` and ``ansible_password`` arguments require special consideration to ensure the credentials are stored securely. While the credentials could be entered 
directly in the inventory, doing so is highly discouraged because these files are often 
checked into a source control repository such as Github where they can be easily read by anyone. There are many options to 
supply credentials securely to Ansible. One of the built-in options is using `Ansible Vault <https://docs.ansible.com/ansible/latest/vault_guide/index.html>`_. Ansible Vault can be used to encrypt the credentials in a file, and decrypt
the file at run time to retrieve the variables.  Other options include using a secrets manager, such as `Hashicorp Vault <https://docs.ansible.com/ansible/latest/collections/index_module.html#community-hashi-vault>`_. 
For this guide, we'll use Ansible Vault. 

First, create a YAML file containing the username and password variables. 

.. code-block:: yaml
    
    # credentials.yml
    firewall_username: <your firewall username>
    firewall_password: <your firewall password>

Create a directory ``group_vars`` and within that a subdirectory ``all``. Save the file as ``group_vars/all/credentials.yml``. Next, use the ``ansible-vault`` command to encrypt the file with AES 256-bit encryption:

.. code-block:: bash

    $ ansible-vault encrypt group_vars/all/credentials.yml

The above command will prompt for creation of an encryption password. This password will be entered at the command line to decrypt the credentials when running the playbook.
  
Now when we run the playbook, Ansible will replace the ``{{ firewall_username }}`` and ``{{ firewall_password }}`` in the inventory file with the values from ``credentials.yml``.

Playbook
--------

A playbook file contains tasks that will be executed against the firewall(s) in the inventory file. At the top of the file, the 
inventory group is specified. In this case, **all** is used to specify operation on all hosts in the inventory. 
The ``gather_facts: false`` command disables Ansible from gathering details about the system that it is working on because it is not
necessary for this collection and would make the playbook run more slowly.

In the **tasks** section of the playbook, a module is referenced using the format **{namespace}.{collection}.{module}**. In the below example, the module
``sophos.sophos_firewall.sfos_ip_host`` will be used to create an IP Host on Sophos firewall. 

.. code-block:: yaml

    # playbook.yml
    ---
    - name: SOPHOS FIREWALL ANSIBLE PLAYBOOK
      hosts: all
      gather_facts: false

      tasks:
        - name: ADD IP HOST
          sophos.sophos_firewall.sfos_ip_host:
            name: testhost1
            ip_address: 1.1.1.1
            state: present

In the above task, underneath the module name ``sophos.sophos_firewall.sfos_ip_host`` are the arguments needed to configure the IP host. 
For each module, there will be arguments that are specific to the module, such as ``name`` and ``ip_address`` in the above example.
  
Refer to the individual `module <../index.html#modules>`_ documentation for the available arguments for each module. 
The ``state`` argument indicates the operation to be performed. Modules support the following values for the ``state`` argument:

  * **present**: Create if not existing
  * **absent**: Delete if exists
  * **updated**: Update existing
  * **query**: Retrieve the existing

To run the playbook, use the ``ansible-playbook`` command as shown below:

.. code-block:: bash

    $ ansible-playbook -i inventory.yml playbook.yml --ask-vault-pass -v

When prompted, enter the encryption password created when executing the ``ansible-vault`` command above. Output should look similar to the following:

.. code-block:: bash
    
    $ ansible-playbook -i inventory.yml test.yml --ask-vault-pass -v
    No config file found; using defaults
    Vault password:

    PLAY [SOPHOS FIREWALL ANSIBLE PLAYBOOK] *********************************************************************************************************

    TASK [ADD IP HOST] ************************************************************************************************************************************
    changed: [testfirewall.sophos.com -> localhost] => {"api_response": {"Response": {"@APIVersion": "2000.2", "@IPS_CAT_VER": "1", "@IS_WIFI6": "0", "IPHost": {"@transactionid": "", "Status": {"#text": "Configuration applied successfully.", "@code": "200"}}, "Login": {"status": "Authentication Successful"}}}, "changed": true, "check_mode": false}

    PLAY RECAP ********************************************************************************************************************************************
    testfirewall.sophos.com              : ok=1    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

.. note::

  The modules in this collection are idempotent; they will not take any action if the configuration is already in the intended state. 
  Due to this, if you run the above task a second time, the response should indicate ``changed=0``.


To check that the host was created, you can check in the firewall dashboard under System > Hosts and services > IP host. To check using an Ansible task,
change the ``state`` argument to ``query``.

.. code-block:: yaml

    # playbook.yml
    ---
    - name: SOPHOS FIREWALL ANSIBLE PLAYBOOK
      hosts: all
      gather_facts: false

      tasks:
        - name: QUERY IP HOST
          sophos.sophos_firewall.sfos_ip_host:
            name: testhost
            state: query

The output should be similar to the following:

.. code-block:: bash

    $ ansible-playbook -i inventory.yml test.yml --ask-vault-pass -v
    No config file found; using defaults
    Vault password:

    PLAY [SOPHOS FIREWALL ANSIBLE PLAYBOOK] *********************************************************************************************************

    TASK [QUERY IP HOST] **********************************************************************************************************************************
    ok: [testhost.sophos.com -> localhost] => {"api_response": {"Response": {"@APIVersion": "2000.2", "@IPS_CAT_VER": "1", "@IS_WIFI6": "0", "IPHost": {"@transactionid": "", "Description": null, "HostType": "IP", "IPAddress": "1.1.1.1", "IPFamily": "IPv4", "Name": "testhost"}, "Login": {"status": "Authentication Successful"}}}, "changed": false, "check_mode": false}

    PLAY RECAP ********************************************************************************************************************************************
    testhost.sophos.com              : ok=1    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0  

To update the test host configuration, such as change the IP address, we can change the ``ip_address`` argument and set the 
``state`` field to ``updated``:

.. code-block:: yaml

    # playbook.yml
    ---
    - name: SOPHOS FIREWALL ANSIBLE PLAYBOOK
      hosts: all
      gather_facts: false

      tasks:
        - name: UPDATE IP HOST
          sophos.sophos_firewall.sfos_ip_host:
            name: testhost
            ip_address: 2.2.2.2
            state: updated

.. code-block:: bash

    $ ansible-playbook -i inventory.yml test.yml --ask-vault-pass -v
    No config file found; using defaults
    Vault password:

    PLAY [SOPHOS FIREWALL ANSIBLE MODULE TESTING] *********************************************************************************************************

    TASK [UPDATE IP HOST] *********************************************************************************************************************************
    changed: [testhost.sophos.com -> localhost] => {"api_response": {"Response": {"@APIVersion": "2000.2", "@IPS_CAT_VER": "1", "@IS_WIFI6": "0", "IPHost": {"@transactionid": "", "Status": {"#text": "Configuration applied successfully.", "@code": "200"}}, "Login": {"status": "Authentication Successful"}}}, "changed": true, "check_mode": false}

    PLAY RECAP ********************************************************************************************************************************************
    testhost.sophos.com              : ok=1    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

To see that the IP address has changed, we can change the state again to ``query``, and this time register a variable to store the result using the ``register`` module argument. 
Then a second task is added using the built-in debug module to display the ip address.

.. code-block:: yaml

    # playbook.yml
    ---
    - name: SOPHOS FIREWALL ANSIBLE PLAYBOOK
      hosts: all
      gather_facts: false

      tasks:
        - name: QUERY IP HOST
          sophos.sophos_firewall.sfos_ip_host:
            name: testhost
            state: query
          # Added a variable called query_host to store the results of the task
          register: query_host

        - name: DISPLAY IP ADDRESS
          ansible.builtin.debug:
            var: query_host.api_response.Response.IPHost.IPAddress

The output should look similar to the following:

.. code-block:: bash

    $ ansible-playbook -i inventory.yml test.yml --ask-vault-pass -v
    No config file found; using defaults
    Vault password:

    PLAY [SOPHOS FIREWALL ANSIBLE PLAYBOOK] *********************************************************************************************************

    TASK [UPDATE IP HOST] *********************************************************************************************************************************
    ok: [testhost.sophos.com -> localhost] => {"api_response": {"Response": {"@APIVersion": "2000.2", "@IPS_CAT_VER": "1", "@IS_WIFI6": "0", "IPHost": {"@transactionid": "", "Description": null, "HostType": "IP", "IPAddress": "2.2.2.2", "IPFamily": "IPv4", "Name": "testhost"}, "Login": {"status": "Authentication Successful"}}}, "changed": false, "check_mode": false}

    TASK [DISPLAY IP ADDRESS] *****************************************************************************************************************************
    ok: [testhost.sophos.com] => {
        "query_host.api_response.Response.IPHost.IPAddress": "2.2.2.2"
    \}

    PLAY RECAP ********************************************************************************************************************************************
    testhost.sophos.com              : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

Finally, if we want to delete the IP Host we can set the state to ``absent``.

.. code-block:: yaml

    # playbook.yml
    ---
    - name: SOPHOS FIREWALL ANSIBLE PLAYBOOK
      hosts: all
      gather_facts: false

      tasks:
        - name: REMOVE IP HOST
          sophos.sophos_firewall.sfos_ip_host:
            name: testhost
            state: absent

.. code-block:: bash

    $ ansible-playbook -i inventory.yml test.yml --ask-vault-pass -v
    No config file found; using defaults
    Vault password:

    PLAY [SOPHOS FIREWALL ANSIBLE PLAYBOOK] *********************************************************************************************************

    TASK [REMOVE IP HOST] *********************************************************************************************************************************
    changed: [testhost.sophos.com -> localhost] => {"api_response": {"Response": {"@APIVersion": "2000.2", "@IPS_CAT_VER": "1", "@IS_WIFI6": "0", "IPHost": {"@transactionid": "", "Status": {"#text": "Configuration applied successfully.", "@code": "200"}}, "Login": {"status": "Authentication Successful"}}}, "changed": true, "check_mode": false}

    PLAY RECAP ********************************************************************************************************************************************
    testhost.sophos.com              : ok=2    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

Now if we change the ``state`` argument back to ``query``, we should see a "No. of records Zero." response which confirms the IP Host was deleted.

.. code-block:: bash

    $ ansible-playbook -i inventory.yml test.yml --ask-vault-pass -v
    No config file found; using defaults
    Vault password:

    PLAY [SOPHOS FIREWALL ANSIBLE PLAYBOOK] *********************************************************************************************************

    TASK [QUERY IP HOST] **********************************************************************************************************************************
    ok: [testhost.sophos.com -> localhost] => {"api_response": "No. of records Zero.", "changed": false, "check_mode": false}

    PLAY RECAP ********************************************************************************************************************************************
    testhost.sophos.com              : ok=1    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0


For more playbook task examples, see the Examples section in each of the individual `modules <../index.html#modules>`_.  

