"""ansible tests for basic SDP system dependency"""

def test_os_release(host):
    """Test OS release"""
    assert host.file("/etc/os-release").contains("Rocky")

def test_sshd_inactive(host):
    """Test SSH service"""
    assert host.service("sshd").is_running is True

def test_perforce_user(host):
    """Test Perforce user"""
    assert host.user("perforce").exists is True
    assert host.user("perforce").uid == 9004
    assert host.user("perforce").gid == 9004
    assert host.user("perforce").group == "perforce"
    assert host.user("perforce").home == "/home/perforce"
    assert host.user("perforce").shell == "/bin/bash"
    assert host.user("perforce").password == "!!"

def test_nfs_hxdepots_mount(host):
    """Test SDP base dir/mount"""
    assert host.file("/hxdepots").exists is True
    assert host.file("/hxdepots").uid == 9004
    assert host.file("/hxdepots").gid == 9004
    assert host.mount_point("/hxdepots").exists is True

def test_dir_hxlogs(host):
    """Test SDP logs dir"""
    assert host.file("/hxlogs").exists is True
    assert host.file("/hxlogs").uid == 9004
    assert host.file("/hxlogs").gid == 9004
    assert host.mount_point("/hxlogs").exists is False

def test_dir_hxmetadata(host):
    """Test SDP metadata dir"""
    assert host.file("/hxmetadata").exists is True
    assert host.file("/hxmetadata").uid == 9004
    assert host.file("/hxmetadata").gid == 9004
    assert host.mount_point("/hxmetadata").exists is False

def test_package_install(host):
    """Test SDP software deps"""
    assert host.package("unzip").is_installed
    assert host.package("bind-utils").is_installed
    assert host.package("unzip").is_installed
    assert host.package("bc").is_installed
    assert host.package("cronie").is_installed
    assert host.package("curl").is_installed
    assert host.package("gcc").is_installed
    assert host.package("gcc-c++").is_installed
    assert host.package("mailx").is_installed
    assert host.package("make").is_installed
    assert host.package("openssl").is_installed
    assert host.package("openssl-devel").is_installed
    assert host.package("rsync").is_installed
    assert host.package("tar").is_installed
    assert host.package("wget").is_installed
    assert host.package("which").is_installed
    assert host.package("zlib").is_installed
    assert host.package("zlib-devel").is_installed
    assert host.package("policycoreutils-python-utils").is_installed
