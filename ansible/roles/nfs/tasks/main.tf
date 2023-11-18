
- name: Add hxdepots path
  ansible.builtin.file:
    path: /nfs/hxdepots
    state: directory
    recurse: yes
    owner: nobody
    group: nobody

- name: Install NFS-utils rpm
  ansible.builtin.yum:
    name: nfs-utils
    state: present

- name: Add NFS Export for subnet
  ansible.builtin.lineinfile:
    path: /etc/exports
    state: present
    owner: root
    group: root
    mode: '0544'
    line: "/nfs/hxdepots {{ network_cidr }}(rw,sync,no_subtree_check)"

- name: Enable service rpcbind and start
  ansible.builtin.service:
    name: rpcbind
    enabled: yes
    state: started

- name: Enable service nfs-idmapd.service and start
  ansible.builtin.service:
    name: nfs-idmapd
    enabled: yes
    state: started

- name: Enable service nfs-server and start
  ansible.builtin.service:
    name: nfs-server
    enabled: yes
    state: started

