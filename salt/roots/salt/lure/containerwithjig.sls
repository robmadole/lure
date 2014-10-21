{% set base_image_id = '{}:{}'.format(pillar['lure']['docker_container'], pillar['lure']['docker_tag']) %}
{% set with_jig_image_id = pillar['lure']['docker_container'] + ':with-jig' %}

docker-py:
  pip.installed

pull_container:
  docker.pulled:
    - name: "{{ pillar['lure']['docker_container'] }}:{{ pillar['lure']['docker_tag'] }}"

/tmp/containerwithjig/Dockerfile:
  file.managed:
    - makedirs: true
    - source: salt://lure/containerwithjig.Dockerfile
    - template: jinja
    - defaults:
      dockerfile:
        from: "{{ base_image_id }}"
      jig:
        rev: develop

"{{ with_jig_image_id }}":
  docker.built:
    - path: /tmp/containerwithjig
