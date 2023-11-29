"""Tests for Perforce NFS Server"""
import json
import pytest

@pytest.fixture(name="ansible_vars")
def fixture_ansible_vars(host):
    """Get vars from ansible"""
    a_vars = host.ansible.get_variables()
    return a_vars

@pytest.fixture(name="ansible_magic_vars")
def fixture_ansible_magic_vars():
    """Get magic vars from ansible"""
    with open('./dump_facts.json', 'r', encoding='utf-8') as dump_file:
        a_magic_vars = json.load(dump_file)
    return a_magic_vars

def test_os_release(host, ansible_magic_vars):
    """Test distribution match"""
    print("Distribution: ", ansible_magic_vars['ansible_distribution'])
    assert host.file("/etc/os-release").contains(ansible_magic_vars['ansible_distribution'])

def test_ssh_service(host):
    """Test ssh services"""
    assert host.service("sshd").is_running is True
    assert host.service("sshd").is_enabled is True
    assert host.service("sshd").is_valid is True

def test_user_perforce(host):
    """Test perforce user"""
    assert host.user("perforce").exists is True
    assert host.user("perforce").uid == 9004
    assert host.user("perforce").gid == 9004

def test_no_sudo_perforce(host):
    """Test perforce sudo"""
    assert host.file("/etc/sudoers.d/perforce").is_file is False

def test_dir_hxdepots(host):
    """Test NFS dir"""
    assert host.file("/nfs/hxdepots").is_directory is True
    assert host.file("/nfs/hxdepots").uid == 9004
    assert host.file("/nfs/hxdepots").gid == 9004

def test_file_export_commit(host, ansible_vars):
    """Test NFS export"""
    print("Network: ", ansible_vars['network_cidr'])
    assert host.file("/etc/exports").content_string.splitlines(
)[0] == '/nfs/hxdepots ' + ansible_vars['network_cidr'] + '(rw,sync,subtree_check,no_root_squash)'

def test_idmap_domain(host, ansible_magic_vars):
    """Test NFS idmap"""
    print("Domain: ", ansible_magic_vars['ansible_domain'])
    assert host.file("/etc/idmapd.conf").is_file is True
    assert host.file("/etc/idmapd.conf").content_string.splitlines(
)[4] == 'Domain = ' + ansible_magic_vars['ansible_domain']

def test_service_nfs_server(host):
    """Test NFS service"""
    assert host.service("nfs-server").is_enabled is True
    assert host.service("nfs-server").is_running is True

def test_service_rpcbind_server(host):
    """Test RPCBIND service"""
    assert host.service("rpcbind").is_enabled is True
    assert host.service("rpcbind").is_running is True
