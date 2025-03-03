How to install the project in dom0?
====================================

**dom0** is the privileged VM that holds administrative rights over the entire [QubesOS](https://qubes-os.org) system.
To use this project, you must install both Ansible and the project itself in **dom0**.

What about an admin qube?
--------------------------------

This project should also work from an administrative **domU** AppVM. However, this functionality has not yet been fully tested. The project consists of two primary components:

- The **qubes** connection plugin
- The **qubesos** module

Clone the project
-----------------

On a Qube (we assume the VM's name is ``work-qubesos``), clone the repository using the following command:

.. code-block:: bash

    git clone https://github.com/fepitre/qubes-ansible

Install Ansible
---------------

On Qubes 4.2+ you can install Ansible with:

.. code-block:: bash

    sudo qubes-dom0-update ansible

Copy the ``ansible_module`` directory to dom0
---------------------------------------------

Assuming you have checked out the repository in ``/home/user/qubes_ansible`` on the VM named *work-qubesos*, copy the module files to ``/usr/share/ansible_module/`` in **dom0** using these commands:

.. code-block:: bash

    sudo su -
    mkdir -p /usr/share/ansible_module/conns
    qvm-run -p work-qubesos 'cat /home/user/qubes_ansible/ansible_module/qubesos.py' > /usr/share/ansible_module/qubesos.py
    qvm-run -p work-qubesos 'cat /home/user/qubes_ansible/ansible_module/conns/qubes.py' > /usr/share/ansible_module/conns/qubes.py

Configure Ansible
-----------------

Update your ``/etc/ansible/ansible.cfg`` file by adding these lines so that Ansible can locate the module and connection plugin:

.. code-block:: ini

    [defaults]
    library = /usr/share/ansible_module/
    connection_plugins = /usr/share/ansible_module/conns/
