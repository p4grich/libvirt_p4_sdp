# libvirt_p4_sdp
Terraform deployment on libvirt/qemu for Perforce SDP testing.

This stake will deploy basic infrastructure for development and testing the Perforce SDP framework:
 https://swarm.workshop.perforce.com/projects/perforce-software-sdp

### Software dependencies:

 - Terraform
 - Terragrunt
 - Python >= 3.9.1
 - Pytest-testinfra
 - Ansible
 - Perforce p4/p4d
 - Perforce SDP
 - Libvirt 
 - Libvirt-nss
 - Qemu-kvm
 - Gnumake
  
### Makefile:

    install: Install needed dependencies and tools.
    test_runner: Run all tests.

    deploy_nfs: Run terrform deply tasks.
    test_nfs: Run tests on host.
    clean_nfs: Destory host, data, and logs.

    deploy_commit: Run terrform deply tasks.
    test_commit: Run tests on host.
    clean_commit: Destory host, data, and logs.
