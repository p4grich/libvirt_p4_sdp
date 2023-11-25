locals {
  fqdn = "${var.hostname}.${var.domain}"
}

data "template_file" "sshpubkey" {
  template = "${file("../../perforce.pub")}"
}

resource "libvirt_pool" "libvirt-pool" {
  name = "${local.fqdn}-pool"
  type = "dir"
  path = "/tmp/terraform-provider-libvirt-pool-${local.fqdn}"
}

# We fetch the latest rocky release image from their mirrors
resource "libvirt_volume" "libvirt-qcow2" {
  name = "${local.fqdn}-qcow2"
  pool   = libvirt_pool.libvirt-pool.name
  source = var.image_qcow2
  format = "qcow2"
}

data "template_file" "user_data" {
  template = file("${path.module}/cloud_init.cfg")
  vars= {
    domain = var.domain
    fqdn = local.fqdn
    hostname = var.hostname
    ssh_user = var.ssh_user
    ssh_pubkey =  "${data.template_file.sshpubkey.rendered}"
  }
}

data "template_file" "network_config" {
  template = file("${path.module}/network_config.cfg")
}

# for more info about paramater check this out
# https://github.com/dmacvicar/terraform-provider-libvirt/blob/master/website/docs/r/cloudinit.html.markdown
# Use CloudInit to add our ssh-key to the instance
# you can add also meta_data field
resource "libvirt_cloudinit_disk" "commoninit" {
  name           = "commoninit.iso"
  user_data      = data.template_file.user_data.rendered
  network_config = data.template_file.network_config.rendered
  pool           = libvirt_pool.libvirt-pool.name
}

# Create the machine
resource "libvirt_domain" "libvirt-domain" {
  name   = local.fqdn
  memory = var.vm_memory
  vcpu   = var.vm_vcpu

  cloudinit = libvirt_cloudinit_disk.commoninit.id

  network_interface {
    network_name = "sdp_network"
    wait_for_lease = true
  }

  # IMPORTANT: this is a known bug on cloud images, since they expect a console
  # we need to pass it
  # https://bugs.launchpad.net/cloud-images/+bug/1573095
  console {
    type        = "pty"
    target_port = "0"
    target_type = "serial"
  }

  console {
    type        = "pty"
    target_type = "virtio"
    target_port = "1"
  }

  disk {
    volume_id = libvirt_volume.libvirt-qcow2.id
  }

  graphics {
    type        = "spice"
    listen_type = "address"
    autoport    = true
  }
}
