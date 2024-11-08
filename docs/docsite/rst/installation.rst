.. _ansible_collections.sophos.sophos_firewall.docsite.installation:

Installation
============
  
Prerequisites
-------------
The following must be installed prior to installing the module:

* Python 3.11+
* Ansible 2.16+
* sophosfirewall-python 0.1.56+
  
With Python installed on the system, Ansible and the sophosfirewall-python module can be installed with ``pip``:
  
.. code-block:: bash

    $ pip install ansible
    $ pip install sophosfirewall-python

Install
-------
The Sophos Firewall Ansible Collection can be installed using the ``ansible-galaxy`` utility which is included with Ansible:
  
.. code-block:: bash

    $ ansible-galaxy collection install sophos.sophos_firewall



