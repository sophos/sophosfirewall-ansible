.. _ansible_collections.sophos.sophos_firewall.docsite.setup:

Setup
=====
Prior to using the Ansible modules, the firewall must be set up to allow access to the API
from the IP address of the system running Ansible.
  
In the firewall dashboard, navigate to **Backup & firmware** and click on the **API** tab.
Check the box to enable API Configuration, and add the Ansible controller to the Allowed IP address field.
  
.. image:: ../../_static/images/setup.jpg
