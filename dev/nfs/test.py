import pytest
import subprocess
import testinfra
import json

@pytest.fixture
def get_ansible_vars(host):
  global ansible_user, network_cidr, domain, hostname, fqdn
  a_vars = host.ansible.get_variables()
  for k, v in a_vars.items():
    if k == "network_cidr":
      network_cidr = v
    if k == "hostname":
      hostname = v
    if k == "ansible_user":
      ansible_user = v
    if k == "domain":
      domain = v
    if k == "fqdn":
      fqdn = v
    a_json=json.dumps(a_vars)
  return ansible_user, network_cidr, domain, hostname, fqdn

def test_os_release(host):
    assert host.file("/etc/os-release").contains("Rocky")

def test_sshd_inactive(host):
    assert host.service("sshd").is_running is True 

def test_user_perforce(host):
    assert host.user("perforce").exists is True
    assert host.user("perforce").uid == 9004
    assert host.user("perforce").gid == 9004
    assert host.user("perforce").group == "perforce"
    assert host.user("perforce").home == "/home/perforce"
    assert host.user("perforce").shell == "/bin/bash"
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

def test_file_export_commit(host, get_ansible_vars):
    assert host.file("/etc/exports").content_string.splitlines()[0] == '/nfs/hxdepots ' + network_cidr +'(rw,sync,no_subtree_check)'

def test_idmap_domain(host, get_ansible_vars):
    assert host.file("/etc/idmapd.conf").is_file is True
    assert host.file("/etc/idmapd.conf").content_string.splitlines()[4] == 'Domain = ' + domain

def test_service_nfs_server(host):
    assert host.service("nfs-server").is_enabled is True
    assert host.service("nfs-server").is_running is True

def test_service_rpcbind_server(host):
    assert host.service("rpcbind").is_enabled is True
    assert host.service("rpcbind").is_running is True

