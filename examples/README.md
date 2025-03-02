# How to try out the examples?

Ensure you have installed the required module and set up the connection as described in the main README.

## The inventory file

The inventory file can be provided in two formats: INI and YAML.

### INI format

```ini
[local]
localhost

[local:vars]
ansible_connection=local

[appvms]
testvm
xchat

[appvms:vars]
ansible_connection=qubes

[debian_templates]
debian-12-xfce
whonix-gateway-17
whonix-workstation-17

[debian_templates:vars]
ansible_connection=qubes

[fedora_templates]
fedora-41-xfce
fedora-41-minimal

[fedora_templates:vars]
ansible_connection=qubes
```

### YAML format

```yaml
local:
  hosts:
    localhost
  vars:
    ansible_connection: local

appvms:
  hosts:
    testvm
    xchat
  vars:
    ansible_connection: qubes

debian_templates:
  hosts:
    debian-12-xfce
    whonix-gateway-17
    whonix-workstation-17
  vars:
    ansible_connection: qubes

fedora_templates:
  hosts:
    fedora-41-xfce
    fedora-41-minimal
  vars:
    ansible_connection: qubes
```

## Running the playbooks from dom0

To create the qubes:
```bash
ansible-playbook-3 -i inventory create_vm.yaml
```

To delete one particular qube:
```bash
ansible-playbook-3 -i inventory undefine_vm.yaml
```

To install packages in the *xchat* qube:
```bash
ansible-playbook-3 -i inventory -b install_packages.yaml
```

To make sure that one vm (in this example, xchat) is in running state with particular details:
```bash
ansible-playbook-3 -i inventory presentstate.yaml
```

## Property values currently available

- autostart
- debug
- default_dispvm
- include_in_backups
- kernel
- label
- maxmem
- memory
- netvm
- provides_network
- template
- template_for_dispvms
- vcpus
- virt_mode
