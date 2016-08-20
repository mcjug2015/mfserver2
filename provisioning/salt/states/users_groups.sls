regular_user:
  group.present:
    - name: {{pillar['regular_username']}}
    - gid: {{pillar['regular_gid']}}
  user.present:
    - name: {{pillar['regular_username']}}
    - fullname: Regular User
    - shell: /bin/bash
    - home: /home/{{pillar['regular_username']}}
    - uid: {{pillar['regular_gid']}}
    - gid: {{pillar['regular_gid']}}
    - require:
      - group: regular_user