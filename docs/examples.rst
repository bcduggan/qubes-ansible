Example tasks
=============

The **qubesos** module is under active development, and its syntax and available options may evolve.
Refer to the examples below to learn more about managing Qubes OS qubes.

Example inventory file
-----------------------

An inventory file that automatically includes all qubes in a Qubes OS environment can be created.
Re-run the following command after adding new qubes. Note that the command will rewrite the existing inventory file.

.. warning:: The following command overwrites the current inventory file.

::

    ansible localhost -m qubesos -a 'command=createinventory'

Once the inventory file is created, playbooks can be executed as follows:

::

    ansible-playbook -i inventory my_playbook.yaml

If the **[standalonevms]** section is empty in the ``inventory`` file, delete that section along with its connection details.

Ensuring a qube is present
---------------------------

This is the preferred method to create (or define) a new qube if it is not already present.

::

    ---
    - hosts: local
      connection: local
      tasks:
          - name: Create a test qube
            qubesos:
              guest: supansible
              label: blue
              state: present
              template: "debian-9"

Note: Only the *guest* parameter is mandatory. By default, the module uses the system default template and netvm, and the default label color is **red**.

Creating multiple qubes with custom properties and tags
---------------------------------------------------------

The following example demonstrates creating multiple qubes with specific labels, templates, properties, and a policy file for inter-qube communication.

::

    ---
    - hosts: local
      connection: local
      tasks:
          - name: Create vault-demo with custom properties
            qubesos:
              guest: vault-demo
              label: black
              state: present
              template: "fedora-41-xfce"
              properties:
                memory: 600
                maxmem: 800
                netvm: ""

          - name: Create work-demo qube using a template
            qubesos:
              guest: work-demo
              label: blue
              state: present
              template: "fedora-41-xfce"

          - name: Create project-demo qube using a template
            qubesos:
              guest: project-demo
              label: orange
              state: present
              template: "fedora-41-xfce"

          - name: Create policy file for qube communications
            copy:
              dest: /etc/qubes/policy.d/10-demo.policy
              content: |
                qubes.Gpg * work-demo vault-demo allow
                project.Service1 * work-demo @default allow target=project-demo
              mode: '0755'

Setting different property values for a qube
---------------------------------------------

Properties can be applied during qube creation or to an existing (but shut down) qube.
The following example sets various properties such as memory, maximum memory, netvm, and default_dispvm.

::

    ---
    - hosts: local
      connection: local
      tasks:
          - name: Set properties for social qube
            qubesos:
              guest: social
              state: present
              properties:
                memory: 1200
                maxmem: 2400
                netvm: 'sys-whonix'
                default_dispvm: 'fedora-41-dvm'
                label: "yellow"

          - name: Ensure the social qube is defined
            qubesos:
              guest: social
              state: present

          - name: Start the social qube
            qubesos:
              guest: social
              state: running

.. note:: Change the state to ``running`` to power on the qube.

Resizing a qube's volume
------------------------

A qube's volume can be resized using the *volume* property.
For App qubes, set the "private" volume size; for Standalone or Template qubes, set the "root" volume size.
The size must be specified in bytes.

::

    ---
    - hosts: local
      connection: local
      tasks:
          - name: Resize volume for social qube
            qubesos:
              guest: social
              state: present
              properties:
                memory: 1200
                maxmem: 2400
                netvm: 'sys-whonix'
                label: "yellow"
                volume:
                  name: "private"
                  size: "5368709120"

Available properties
--------------------

The following properties and their types are supported:

- **autostart**: bool
- **debug**: bool
- **include_in_backups**: bool
- **kernel**: str
- **label**: str
- **maxmem**: int
- **memory**: int
- **provides_network**: bool
- **template**: str
- **template_for_dispvms**: bool
- **vcpus**: int
- **virt_mode**: str
- **default_dispvm**: str
- **netvm**: str
- **features**: dict[str, str]
- **volume**: dict[str, str]

To modify an existing qube's properties, first shut it down and then apply the new properties with state ``present``.
Features can be added, updated, or removed via properties:

::

    ---
    - hosts: local
      connection: local
      tasks:
          - name: Configure features for social qube
            qubesos:
              guest: social
              state: present
              properties:
                memory: 1200
                maxmem: 2400
                netvm: 'sys-whonix'
                default_dispvm: 'fedora-41-dvm'
                label: "yellow"
                features:
                  life: "better"
                  can_fix_world_problem: False
                  news: "good"

To remove a feature, set its value to **"None"**; to clear a feature (i.e. set to an empty string), use **""**:

::

    features:
      life: "None"
      news: ""

Adding tags to a qube
---------------------

Tags (a list of strings) can be assigned to a qube for categorization.

::

    ---
    - hosts: local
      connection: local
      tasks:
          - name: Assign tags to social qube
            qubesos:
              guest: social
              state: present
              tags:
                - "Linux"
                - "IRC"
                - "Chat"

Different available states
--------------------------

The module supports the following states:

- **destroyed**
- **pause**
- **running**
- **shutdown**
- **undefine**
- **present**

.. warning:: The **undefine** state will remove the qube and all associated data. Use with caution.

Different available commands
-----------------------------

The module also supports several non-idempotent commands:

**shutdown**
++++++++++++

Gracefully shut down the qube.

::

    ansible localhost -m qubesos -a 'guest=social command=shutdown'

**destroy**
+++++++++++

Forcefully shut down the qube immediately.

::

    ansible localhost -m qubesos -a 'guest=social command=destroy'

.. note:: It is recommended to use the **destroyed** state for proper qube destruction.

**removetags**
++++++++++++++

Remove specified tags from a qube.

::

    ---
    - hosts: local
      connection: local
      tasks:
          - name: Remove tags from social qube
            qubesos:
              guest: social
              command: removetags
              tags:
                - "Linux"
                - "IRC"
                - "Chat"

Find qubes by state
-------------------

List all qubes with a particular state (for example, running):

::

    ansible localhost -m qubesos -a 'state=running command=list_vms'

Queries can similarly be performed for qubes with states such as *shutdown* or *paused*.

Installing packages, copying files, and fetching files
-------------------------------------------------------

The following example playbook (``install_packages.yaml``) installs a package, copies a configuration file to a qube, and fetches a file from a qube:

::

    ---
    - hosts: social
      tasks:
        - name: Ensure sl is installed at the latest version
          ansible.builtin.package:
            name: sl
            state: latest
          become: true
        - name: Copy configuration file to the qube
          copy:
            src: foo.conf
            dest: /etc/foo.conf
        - name: Fetch OS release information from the qube
          fetch:
            src: /etc/os-release
            dest: /tmp/fetched

Run a command in every running qube
------------------------------------

After creating the inventory file using the ``createinventory`` command, a playbook can be used to execute a command (e.g. ``hostname``) on every running qube:

::

    ---
    - hosts: localhost
      connection: local
      tasks:
          - name: Retrieve list of running qubes
            qubesos:
              command: list_vms
              state: running
            register: rhosts

    - hosts: "{{ hostvars['localhost']['rhosts']['list_vms'] }}"
      connection: qubes
      tasks:
          - name: Get hostname of each qube
            command: hostname

Run a command in every running qube except system qubes
-------------------------------------------------------

Exclude system qubes (those whose names start with ``sys-``):

::

    ---
    - hosts: localhost
      connection: local
      tasks:
          - name: Retrieve running qubes
            qubesos:
              command: list_vms
              state: running
            register: rhosts

          - name: Filter out system qubes
            set_fact:
              myvms: "{% for name in rhosts.list_vms if not name.startswith('sys-') %}{{ name }},{% endfor %}"

    - hosts: "{{ hostvars['localhost']['myvms'] }}"
      connection: qubes
      tasks:
          - name: Get hostname of each non-system qube
            command: hostname

Shutdown all qubes except system qubes
--------------------------------------

Shut down all running qubes except those whose names start with ``sys-``:

::

    ---
    - hosts: localhost
      connection: local
      tasks:
          - name: Retrieve running qubes
            qubesos:
              command: list_vms
              state: running
            register: rhosts

          - debug: var=rhosts

          - name: Shutdown each non-system qube
            qubesos:
              command: destroy
              guest: "{{ item }}"
            with_items: "{{ rhosts.list_vms }}"
            when: not item.startswith("sys-")

The above playbook (e.g. ``shutdown_all.yaml``) can be executed using:

::

    ansible-playbook -i inventory -b shutdown_all.yaml
