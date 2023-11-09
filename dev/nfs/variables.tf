variable "hostname" {
  type    = string
  description = "Set HOSTNAME of this system."
}
variable "domain" {
  type    = string
  description = "Set DOMAIN of this system."
  default = "local"
}

variable "ssh_user" {
  type    = string
  description = "Set SSH_USER for this system."
  default = "root"
}


variable "sdp_role" {
  type    = string
  description = "Deploy Perforce server by role SDP_ROLE: commit, commit-standy, edge, replica"
  default = "commit"
}

variable "image_qcow2" {
  type    = string
  description = "Get qcow2 image IMAGE_QCOW2: URL or local path"
  default = "https://download.rockylinux.org/pub/rocky/8/images/x86_64/Rocky-8-EC2-LVM-8.8-20230518.0.x86_64.qcow2"
}
variable "vm_memory" {
  type    = number
  description = "Set VM Memory in MB"
  default = "512"
}
variable "vm_vcpu" {
  type    = number
  description = "Set the number of VM vcpu's"
  default = "1"
}
