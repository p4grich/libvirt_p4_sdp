import pytest
import subprocess
import testinfra

def test_os_release(host):
    assert host.file("/etc/os-release").contains("Rocky")

def test_sshd_inactive(host):
    assert host.service("sshd").is_running is True 

def test_perforce_user(host):
    assert host.user("perforce").exists is True
    assert host.user("perforce").uid == 9004
    assert host.user("perforce").gid == 9004
    assert host.user("perforce").group == "perforce"
    assert host.user("perforce").home == "/home/perforce"
    assert host.user("perforce").shell == "/bin/bash"
    assert host.user("perforce").password == "!!"

def test_nfs_hxdepots_mount(host):
    assert host.file("/hxdepots").exists is True
    assert host.mount_point("/hxdepots").exists is True

def test_nfs_hxlogs_mount(host):
    assert host.file("/hxlogs").exists is True

def test_nfs_hxmetadata_mount(host):
    assert host.file("/hxmetadata").exists is True
