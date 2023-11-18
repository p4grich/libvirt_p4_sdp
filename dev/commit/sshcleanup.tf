resource "null_resource" "ssh_knowhost_cleanup" {
  triggers = {
    fqdn_keyname = local.fqdn
  }
  depends_on = [ansible_host.host]

  provisioner "local-exec" {
    when    = destroy
    command = <<EOF
      ssh-keygen -f $HOME/.ssh/known_hosts -R "${self.triggers.fqdn_keyname}"
    EOF
  }
}
