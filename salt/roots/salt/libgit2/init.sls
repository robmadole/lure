cmake:
  pkg.installed

libgit2:
  cmd.script:
    - source: salt://libgit2/install.sh
    - unless: test -f /usr/local/lib/libgit2.so.0.21.0
