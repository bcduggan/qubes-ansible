import os
import subprocess
import uuid
from typing import List

import pytest
from pathlib import Path

PLUGIN_PATH = Path(__file__).parent / "plugins" / "modules"


@pytest.fixture
def run_playbook(tmp_path):
    """
    Helper to write a playbook and execute it with ansible-playbook.
    """

    def _run(playbook_content: List[dict], vms: List[str] = []):
        # Create playbook file
        pb_file = tmp_path / "playbook.yml"
        import yaml

        pb_file.write_text(yaml.dump(playbook_content))
        # Run ansible-playbook
        cmd = [
            "ansible-playbook",
            "-vvv",
            "-i",
            f"localhost,{','.join(vms)}",
            "-c",
            "local",
            "-M",
            str(PLUGIN_PATH),
            str(pb_file),
        ]
        result = subprocess.run(
            cmd, cwd=tmp_path, capture_output=True, text=True
        )
        return result

    return _run


def test_create_and_destroy_vm(run_playbook, request):
    name = f"test-vm-{uuid.uuid4().hex[:6]}"
    request.node.mark_vm_created(name)

    playbook = [
        {
            "hosts": "localhost",
            "tasks": [
                {
                    "name": "Create AppVM",
                    "qubesos": {
                        "name": name,
                        "command": "create",
                        "vmtype": "AppVM",
                    },
                },
                {
                    "name": "Start AppVM",
                    "qubesos": {
                        "name": name,
                        "command": "start",
                    },
                },
                {
                    "name": "Destroy AppVM",
                    "qubesos": {"name": name, "command": "destroy"},
                },
                {
                    "name": "Remove AppVM",
                    "qubesos": {"name": name, "command": "remove"},
                },
            ],
        }
    ]
    result = run_playbook(playbook)
    # Playbook should run successfully
    assert result.returncode == 0, result.stderr


def test_properties_and_tags_playbook(run_playbook, request):
    name = f"test-vm-{uuid.uuid4().hex[:6]}"
    request.node.mark_vm_created(name)

    playbook = [
        {
            "hosts": "localhost",
            "tasks": [
                {
                    "name": "Create VM with properties",
                    "qubesos": {
                        "name": name,
                        "state": "present",
                        "properties": {"autostart": True, "memory": 128},
                        "tags": ["tag1", "tag2"],
                    },
                },
                {
                    "name": "Validate VM state",
                    "qubesos": {"name": name, "command": "status"},
                },
                {
                    "name": "Cleanup",
                    "qubesos": {"name": name, "state": "absent"},
                },
            ],
        }
    ]
    result = run_playbook(playbook)
    assert result.returncode == 0, result.stderr

    # Ensure properties and tags were applied
    assert "changed=" in result.stdout
    assert "tag1" in result.stdout and "tag2" in result.stdout


def test_inventory_playbook(run_playbook, tmp_path, qubes):
    # Generate inventory via playbook
    playbook = [
        {
            "hosts": "localhost",
            "tasks": [
                {
                    "name": "Create inventory",
                    "qubesos": {"command": "createinventory"},
                }
            ],
        }
    ]
    result = run_playbook(playbook)
    assert result.returncode == 0, result.stderr

    # Check inventory file exists
    inv_file = tmp_path / "inventory"
    assert inv_file.exists()
    content = inv_file.read_text()

    # Should contain at least one VM entry under [appvms]
    assert "[appvms]" in content

    # Compare with qubes.domains data
    for vm in qubes.domains.values():
        if vm.name != "dom0" and vm.klass == "AppVM":
            assert vm.name in content


def test_vm_connection(vm, run_playbook):
    play_attrs = {
        "hosts": vm.name,
        "gather_facts": False,
        "connection": "qubes",
    }
    playbook = [
        {
            **play_attrs,
            "tasks": [
                {
                    "name": "Default VM user is 'user'",
                    "ansible.builtin.command": "whoami",
                    "register": "default_result",
                    "failed_when": "default_result.stdout != 'user'",
                },
            ],
        },
        {
            **play_attrs,
            "remote_user": "user",
            "tasks": [
                {
                    "name": "VM user with 'remote_user: user' is 'user'",
                    "ansible.builtin.command": "whoami",
                    "register": "user_result",
                    "failed_when": "user_result.stdout != 'user'",
                },
            ],
        },
        {
            **play_attrs,
            "remote_user": "root",
            "tasks": [
                {
                    "name": "VM user with 'remote_user: root' is 'root'",
                    "ansible.builtin.command": "whoami",
                    "register": "root_result",
                    "failed_when": "root_result.stdout != 'root'",
                },
            ],
        },
        {
            **play_attrs,
            "become": True,
            "tasks": [
                {
                    "name": "VM user with 'become: true' is 'root'",
                    "ansible.builtin.command": "whoami",
                    "register": "become_result",
                    "failed_when": "become_result.stdout != 'root'",
                },
            ],
        },
    ]
    result = run_playbook(playbook, vms=[vm.name])
    # Playbook should run successfully
    assert result.returncode == 0, result.stderr

    invalid_user_playbook = [
        {
            **play_attrs,
            "remote_user": "invalid_user",
            "tasks": [
                {
                    "name": "No-op",
                    "ansible.builtin.command": "true",
                },
            ],
        },
    ]
    invalid_user_result = run_playbook(invalid_user_playbook, vms=[vm.name])
    # Playbook should fail because connection module only supports remote users in ["root", "user"].
    # Only needs to be tested once.
    assert invalid_user_result.returncode == 2, invalid_user_result.stderr


def test_minimalvm_connection(minimalvm, run_playbook):
    play_attrs = {
        "hosts": minimalvm.name,
        "gather_facts": False,
        "connection": "qubes",
    }
    playbook = [
        {
            **play_attrs,
            "tasks": [
                {
                    "name": "Default minimal VM user is 'user'",
                    "ansible.builtin.command": "whoami",
                    "register": "default_result",
                    "failed_when": "default_result.stdout != 'user'",
                },
            ],
        },
        {
            **play_attrs,
            "remote_user": "user",
            "tasks": [
                {
                    "name": "Minimal VM user with 'remote_user: user' is 'user'",
                    "ansible.builtin.command": "whoami",
                    "register": "user_result",
                    "failed_when": "user_result.stdout != 'user'",
                },
            ],
        },
        {
            **play_attrs,
            "remote_user": "root",
            "tasks": [
                {
                    "name": "Minimal VM user with 'remote_user: root' is 'root'",
                    "ansible.builtin.command": "whoami",
                    "register": "root_result",
                    "failed_when": "root_result.stdout != 'root'",
                },
            ],
        },
    ]
    result = run_playbook(playbook, vms=[minimalvm.name])
    # Playbook should run successfully
    assert result.returncode == 0, result.stderr

    become_playbook = [
        {
            **play_attrs,
            "become": True,
            "tasks": [
                {
                    "name": "No-op",
                    "ansible.builtin.command": "true",
                },
            ],
        },
    ]
    become_result = run_playbook(become_playbook, vms=[minimalvm.name])
    # Playbook should fail because "become" isn't possibile on unmodified minimal vms.
    assert become_result.returncode == 2, become_result.stderr
