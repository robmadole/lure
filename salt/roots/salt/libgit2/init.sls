cmake:
  pkg.installed

libssl-dev:
  pkg.installed

libssh2-1-dev:
  pkg.installed

libgit2:
  cmd.script:
    - source: salt://libgit2/install.sh
    - unless: test -f /usr/local/lib/libgit2.so.0.21.0

ldconfig:
  cmd.wait:
    - watch:
      - cmd: libgit2
