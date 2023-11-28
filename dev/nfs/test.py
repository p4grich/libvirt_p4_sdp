import pytest
import testinfra
import json

@pytest.fixture
def ansible_vars(host):
    a_vars = host.ansible.get_variables()
    return a_vars

@pytest.fixture
def ansible_magic_vars(host):
    f = open('dump_facts.json')
    a_magic_vars = json.load(f)
    f.close()
    return a_magic_vars

def test_os_release(host, ansible_vars, ansible_magic_vars):
    print("Distribution:", ansible_vars['distribution'])
    assert host.file("/etc/os-release").contains(ansible_magic_vars['ansible_distribution'])

def test_ssh_service(host, ansible_magic_vars):
      assert host.service("sshd").is_running is True
      assert host.service("sshd").is_enabled is True
      assert host.service("sshd").is_valid is True

def test_user_perforce(host, ansible_vars):
    assert host.user("perforce").exists is True
    assert host.user("perforce").uid == 9004
    assert host.user("perforce").gid == 9004

def test_no_sudo_perforce(host):
    assert host.file("/etc/sudoers.d/perforce").is_file is False

def test_dir_hxdepots(host):
      assert host.file("/nfs/hxdepots").is_directory is True
      assert host.file("/nfs/hxdepots").uid == 9004 
      assert host.file("/nfs/hxdepots").gid == 9004 

def test_file_export_commit(host, ansible_vars):
    print("Network: ", ansible_vars['network_cidr'])
    assert host.file("/etc/exports").content_string.splitlines()[0] == '/nfs/hxdepots ' + ansible_vars['network_cidr'] + '(rw,sync,subtree_check,no_root_squash)'

def test_idmap_domain(host, ansible_magic_vars):
    print("Domain: ", ansible_magic_vars['ansible_domain'])
    assert host.file("/etc/idmapd.conf").is_file is True
    assert host.file("/etc/idmapd.conf").content_string.splitlines()[4] == 'Domain = ' + ansible_magic_vars['ansible_domain']

def test_service_nfs_server(host):
    assert host.service("nfs-server").is_enabled is True
    assert host.service("nfs-server").is_running is True

def test_service_rpcbind_server(host):
    assert host.service("rpcbind").is_enabled is True
    assert host.service("rpcbind").is_running is True
