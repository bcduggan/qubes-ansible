# Ansible Connection and Module for QubesOS

This project provides an Ansible connection plugin to interact with [Qubes OS](https://qubes-os.org) virtual machines called `qubes` and an Ansible module to manage the state of your qubes.

## Setup

To use this project, you must install both Ansible and the project itself in **dom0**.
This project should also work from a management qube.
However, this functionality has not yet been fully tested.
The project consists of two primary components:

- The **qubes** connection plugin
- The **qubesos** module

### Clone the project

On a qube, say `work-qubesos`, clone the repository using the following command:

```bash
git clone https://github.com/fepitre/qubes-ansible
```

### Install Ansible

On Qubes 4.2+ you can install Ansible with:

```bash
sudo qubes-dom0-update ansible
```

### Copy the `ansible_module` directory to dom0

Assuming you have checked out the repository in `/home/user/qubes_ansible` on the VM named *work-qubesos*, copy the module files to `/usr/share/ansible_module/` in **dom0** using these commands:

```bash
sudo su -
mkdir -p /usr/share/ansible_module/conns
qvm-run -p work-qubesos 'cat /home/user/qubes_ansible/ansible_module/qubesos.py' > /usr/share/ansible_module/qubesos.py
qvm-run -p work-qubesos 'cat /home/user/qubes_ansible/ansible_module/conns/qubes.py' > /usr/share/ansible_module/conns/qubes.py
```

### Configure Ansible

Update your `/etc/ansible/ansible.cfg` file by adding these lines so that Ansible can locate the module and connection plugin:

```ini
[defaults]
library = /usr/share/ansible_module/
connection_plugins = /usr/share/ansible_module/conns/
```

## Writing playbooks and roles

- When creating or destroying qubes, use a **local** connection with the `qubesos` module.
- For tasks executed on qubes, use the **qubes** connection along with standard Ansible playbooks.

## Examples

See the [examples](EXAMPLES.md) for sample playbooks and role tasks demonstrating common usage scenarios.

## Development status

This project is still in its early stages. The `qubesos` module is under active development, so the syntax and keywords may change in future releases.

## License

This project is licensed under the GPLv3+ license. Please see the [LICENSE](LICENSE) file for the full license text.
