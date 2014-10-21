python-tools:
  pkg.installed:
    - pkgs:
      - python-software-properties
      - python-dev
      - python-pip

old-python-versions:
  pkgrepo.managed:
    - ppa: fkrull/deadsnakes
  pkg.latest:
    - pkgs:
      - python3.4-dev

virtualenv:
  pip.installed
