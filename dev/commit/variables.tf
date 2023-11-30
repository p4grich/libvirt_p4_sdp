variable "hostname" {
  type        = string
  description = "Set HOSTNAME of this system."
  default     = "commit"
}

variable "domain" {
  type        = string
  description = "Set DOMAIN of this system."
  default     = "local"
}

variable "ssh_user" {
  type        = string
  description = "Set SSH_USER for this system."
  default     = "root"
}

variable "sdp_role" {
  type        = string
  description = "Deploy Perforce server by role SDP_ROLE: commit, commit-standy, commit-nfs, edge, edge-nfs, replica, replica-nfs"
  default     = "commit"
}

variable "sdp_commit_nfs_host" {
  type        = string
  description = "Set hostname for commit server NFS Server"
  default     = "nfs.local"
}

variable "sdp_release_version" {
  type        = string
  description = "Perforce SDP Version: https://swarm.workshop.perforce.com/files/guest/perforce_software/sdp/downloads"
  default     = "2018.1.23504"
}

variable "sdp_platform" {
  type        = string
  description = "Perforce SDP Platform: Unix || Windows"
  default     = "Unix"
}

variable "sdp_archive" {
  type        = string
  description = "Perforce SDP Archive type: tgz || zip"
  default     = "tgz"
}
variable "perforce_arch" {
  type        = string
  description = "Perforce architecture type: linux26x86_64 || ntx64"
  default     = "linux26x86_64"
}

variable "perforce_release" {
  type        = string
  description = "Perforce release: r23.1 || r22.1 || etc..."
  default     = "r23.1"
}

variable "sdp_green_field_installer" {
  type        = string
  description = "Perforce SDP green field installer: yes || no"
  default     = "no"
}

variable "sdp_release_branch" {
  type        = string
  description = "Perforce SDP release branch or dev"
  default     = "yes"
}

variable "distribution" {
  type        = string
  description = "Set OS distribution and drive tests. AKA ansible_distribution"
  default     = "Rocky"
}

variable "os_family" {
  type        = string
  description = "Set OS distribution and drive tests. AKA ansible os_family"
  default     = "RedHat"
}

variable "image_qcow2" {
  type        = string
  description = "Get qcow2 image IMAGE_QCOW2: URL or local path"
  default     = "https://download.rockylinux.org/pub/rocky/8/images/x86_64/Rocky-8-EC2-LVM-8.8-20230518.0.x86_64.qcow2"
}

variable "network_cidr" {
  type        = string
  description = "Set network_cidr"
  default     = "192.168.168.0/24"
}

variable "vm_memory" {
  type        = number
  description = "Set VM Memory in MB"
  default     = "512"
}

variable "vm_vcpu" {
  type        = number
  description = "Set the number of VM vcpu's"
  default     = "1"
}

variable "vm_volsize" {
  type        = number
  description = "Set the volume size in bytes. default is 10GB"
  default     = "10000000000"
}
