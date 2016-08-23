sudo_group:
  group.present:
    - name: {{pillar['sudo_groupname']}}
    - gid: {{pillar['sudo_group_gid']}}


/etc/sudoers:
  file.blockreplace:
    - marker_start: "# START managed zone sudo group"
    - marker_end: "# END managed zone sudo group"
    - content: "%{{pillar['sudo_groupname']}}   ALL=(ALL)       NOPASSWD:ALL"
    - append_if_not_found: True


regular_user:
  group.present:
    - name: {{pillar['regular_username']}}
    - gid: {{pillar['regular_user_gid']}}
  user.present:
    - name: {{pillar['regular_username']}}
    - fullname: Regular User
    - shell: /bin/bash
    - home: /home/{{pillar['regular_username']}}
    - uid: {{pillar['regular_user_gid']}}
    - gid: {{pillar['regular_user_gid']}}
    - require:
      - group: regular_user


sudo_user:
  group.present:
    - name: {{pillar['sudo_username']}}
    - gid: {{pillar['sudo_user_gid']}}
  user.present:
    - name: {{pillar['sudo_username']}}
    - fullname: Sudo User
    - shell: /bin/bash
    - home: /home/{{pillar['sudo_username']}}
    - uid: {{pillar['sudo_user_gid']}}
    - gid: {{pillar['sudo_user_gid']}}
    - groups:
      - {{pillar['sudo_groupname']}}
    - require:
      - group: sudo_user
      - group: sudo_group
