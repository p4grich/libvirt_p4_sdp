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
    #network_cidr = var.network_cidr
    #hostname  = var.hostname
    #domain  = var.domain
    #fqdn  = local.fqdn
    #distribution = var.distribution
    sdp_commit_nfs_host = var.sdp_commit_nfs_host
    sdp_role = var.sdp_role
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
