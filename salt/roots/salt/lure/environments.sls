/envs:
  file.directory:
    - user: vagrant
    - group: vagrant

libffi-dev:
  pkg.installed

{% for python in pillar['pythons'] %}
/envs/{{ python }}:
  virtualenv.managed:
    - user: vagrant
    - group: vagrant
    - python: /usr/bin/{{ python }}

cffi:
  pip.installed:
    - user: vagrant
    - group: vagrant
    - bin_env: /envs/{{ python }}

lure-requirements:
  pip.installed:
    - user: vagrant
    - group: vagrant
    - bin_env: /envs/{{ python }}
    - requirements: salt://lure/requirements.txt

lure:
  pip.installed:
    - user: vagrant
    - group: vagrant
    - bin_env: /envs/{{ python }}
    - editable:
      - /lure
{% endfor %}
