.. _ansible_collections.sophos.sophos_firewall.docsite.httpapi_example:

New in version 2.0: HttpApi Plugin
==================================
Beginning in version 2.0.0, this module requires use of the httpapi connection plugin. 
The connection settings must now be configured as inventory, playbook, or task variables. For example:

.. code-block:: yaml

    # inventory.yml
    all:
      hosts:
        testfirewall:
          ansible_host: [firewall_ip_or_hostname]
      vars:
        ansible_user: [firewall_username]
        ansible_password: [firewall_password]
        ansible_connection: ansible.netcommon.httpapi
        ansible_httpapi_validate_certs: false
        ansible_httpapi_port: 4444
        ansible_network_os: sophos.sophos_firewall.sfos
  
With the connection parameters now being supplied as variables, the below task arguments are no longer valid
and must be removed from any existing playbook tasks:

* username
* password
* hostname
* port
* verify
  
In addition, it is no longer necessary or supported to use the **delegate_to** option for tasks.
Below is an example of a task definition where the connection parameters are being supplied as 
inventory variables. 

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

            