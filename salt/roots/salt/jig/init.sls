https://github.com/robmadole/jig.git:
  git.latest:
    - target: /opt/jig
    - rev: {{ pillar['jig']['rev'] }}

jig-virtualenv:
  virtualenv.managed:
    - name: /envs/jig
    - user: vagrant
    - group: vagrant
    - python: /usr/bin/python2.7

jig-editable:
  pip.installed:
    - bin_env: /envs/jig
    - editable:
      - /opt/jig
