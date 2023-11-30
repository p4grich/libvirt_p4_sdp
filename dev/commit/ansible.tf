resource "ansible_vault" "secrets" {
  vault_file          = "vault.yml"
  vault_password_file = ".vaultpass"
}

locals {
  decoded_vault_yaml = yamldecode(ansible_vault.secrets.yaml)
}

resource "ansible_host" "host" {
  name   = local.fqdn
  groups = ["sdp"]
  variables = {
    sdp_commit_nfs_host = var.sdp_commit_nfs_host
    sdp_role = var.sdp_role
    sdp_green_field_installer = var.sdp_green_field_installer
    perforce_release = var.perforce_release
    perforce_arch = var.perforce_arch
    # using jsonencode() here is needed to stringify 
    # a list that looks like: [ element_1, element_2, ..., element_N ]
    # yaml_list = jsonencode(local.decoded_vault_yaml.a_list)
  }
}

resource "ansible_group" "group" {
  name     = "sdp"
  children = ["sdp_p4d_servers"]
  variables = {
    ansible_user = local.decoded_vault_yaml.ansible_user
    sdp_release_version = var.sdp_release_version
    sdp_platform = var.sdp_platform
    sdp_archive = var.sdp_archive
    sdp_release_branch = var.sdp_release_branch
  }
}

resource "ansible_playbook" "playbook" {
  playbook                = "playbook.yml"
  name                    = local.fqdn
  replayable              = true
  check_mode              = false
  ignore_playbook_failure = true
  verbosity               = 6
  extra_vars = {
    sdp_role = var.sdp_role
    network_cidr = var.network_cidr
    ansible_user = local.decoded_vault_yaml.ansible_user
  }
}
