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
    assert host.file("/hxdepots").uid == 9004
    assert host.file("/hxdepots").gid == 9004
    assert host.mount_point("/hxdepots").exists is True

def test_dir_hxlogs(host):
    assert host.file("/hxlogs").exists is True
    assert host.file("/hxlogs").uid == 9004
    assert host.file("/hxlogs").gid == 9004
    assert host.mount_point("/hxlogs").exists is False

def test_dir_hxmetadata(host):
    assert host.file("/hxmetadata").exists is True
    assert host.file("/hxmetadata").uid == 9004
    assert host.file("/hxmetadata").gid == 9004
    assert host.mount_point("/hxmetadata").exists is False
