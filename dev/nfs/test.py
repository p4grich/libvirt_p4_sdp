import pytest
import testinfra
import json

@pytest.fixture
def ansible_vars(host):
  a_vars = host.ansible.get_variables()
  return a_vars

def test_os_release(host, ansible_vars):
    print("Distribution:", ansible_vars['distribution'])
    assert host.file("/etc/os-release").contains(ansible_vars['distribution'])

def test_sshd_inactive(host):
    assert host.service("sshd").is_running is True 

def test_user_perforce(host, ansible_vars):
    assert host.user("perforce").exists is True
    assert host.user("perforce").uid == 9004
    assert host.user("perforce").gid == 9004
    assert host.user("perforce").group == "perforce"
    assert host.user("perforce").home == "/home/perforce"
    assert host.user("perforce").shell == "/bin/bash"
    if ansible_vars['distribution'] == "Debian" or ansible_vars['distribution'] == "Ubuntu":
      assert host.user("perforce").password == "!"
    else:
      assert host.user("perforce").password == "!!"

def test_sudo_perforce(host):
    assert host.file("/etc/sudoers.d/perforce").is_file is True
    assert host.file("/etc/sudoers.d/perforce").user == 'root'
    assert host.file("/etc/sudoers.d/perforce").uid == 0
    assert host.file("/etc/sudoers.d/perforce").gid == 0
    assert host.file("/etc/sudoers.d/perforce").mode == 0o400
    assert host.file("/etc/sudoers.d/perforce").content_string.strip() == 'perforce ALL=(ALL) NOPASSWD:ALL'

def test_dir_hxdepots(host):
    assert host.file("/nfs/hxdepots").is_directory is True
    assert host.file("/nfs/hxdepots").uid == 65534
    assert host.file("/nfs/hxdepots").gid == 65534

def test_file_export_commit(host, ansible_vars):
    print("Network: ", ansible_vars['network_cidr'])
    assert host.file("/etc/exports").content_string.splitlines()[0] == '/nfs/hxdepots ' + ansible_vars['network_cidr'] + '(rw,sync,no_subtree_check)'

def test_idmap_domain(host, ansible_vars):
    print("Domain: ",ansible_vars['domain'])
    assert host.file("/etc/idmapd.conf").is_file is True
    assert host.file("/etc/idmapd.conf").content_string.splitlines()[4] == 'Domain = ' + ansible_vars['domain']

def test_service_nfs_server(host):
    assert host.service("nfs-server").is_enabled is True
    assert host.service("nfs-server").is_running is True

def test_service_rpcbind_server(host):
    assert host.service("rpcbind").is_enabled is True
    assert host.service("rpcbind").is_running is True
