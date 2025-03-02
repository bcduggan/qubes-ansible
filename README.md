# Ansible Connection and Module for QubesOS

This project provides an Ansible connection plugin to interact with [Qubes OS](https://qubes-os.org) virtual machines called `qubes` and an Ansible module to manage the state of your qubes.

## Documentation

For comprehensive usage instructions, advanced commands, and setup details, please refer to the full documentation available [online](https://qubes-ansible.readthedocs.io/en/latest/).

## Setup

### Module installation

1. Copy the `ansible_module` directory to a known location on your system. For example, you can place it in:
   ```
   /usr/share/ansible_module
   ```

2. This project is designed to run from **dom0** or from any qube with required RPC policies.

> FIXME: Provide RPC policies.

### Ansible installation and Module/Connection configuration

1. Install Ansible:
   ```bash
   sudo qubes-dom0-update ansible
   ```

2. Modify your `/etc/ansible/ansible.cfg` file to include the following lines:
   ```ini
   [defaults]
   library = /usr/share/ansible_module/
   connection_plugins = /usr/share/ansible_module/conns/
   ```

## Writing playbooks and roles

- When creating or destroying qubes, use a **local** connection with the `qubesos` module.
- For tasks executed on qubes, use the **qubes** connection along with standard Ansible playbooks.

## Examples

See the [examples](examples/) directory for sample playbooks and role tasks demonstrating common usage scenarios.

## Development status

This project is still in its early stages. The `qubesos` module is under active development, so the syntax and keywords may change in future releases.

## License

This project is licensed under the GPLv3+ license. Please see the [LICENSE](LICENSE) file for the full license text.
