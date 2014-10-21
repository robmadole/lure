# -*- coding: utf-8 -*-

import pickle
import pkg_resources
from os import listdir
from os.path import splitext
from tempfile import mkdtemp
from functools import partial

import docker

from lure.config import (
    DOCKER_BASE_URL, DOCKER_CLIENT_VERSION, DOCKER_CLIENT_TIMEOUT, DOCKER_IMAGE, DOCKER_HELPERS_DIRECTORY)
from lure.logger import log


def _client():
    """
    Get a connection to Docker.

    :rtype: docker.Client
    """
    return docker.Client(
        base_url=DOCKER_BASE_URL,
        version=DOCKER_CLIENT_VERSION,
        timeout=DOCKER_CLIENT_TIMEOUT
    )


def _run_helper(helper_name):
    client = _client()

    output = mkdtemp()

    container = client.create_container(
        image=DOCKER_IMAGE,
        command='/sbin/my_init -- /lang/python/3.4.1/bin/python /helpers/{}.py'.format(helper_name),
        environment=[
            'OUTPUT_FILE=/output/result',
            'LANG_DIRECTORY=/lang'
        ],
        volumes=['/helpers', '/output']
    )

    container_id = container['Id']

    client.start(
        container_id,
        binds={DOCKER_HELPERS_DIRECTORY: '/helpers', output: '/output'}
    )

    client.wait(container_id)

    logs = client.logs(container_id).decode('utf8')

    client.remove_container(container_id)

    try:
        return pickle.load(open('{}/result'.format(output), 'rb'))
    except IOError:
        log.error("Failed to list languages\n" + logs)

        return None


def _load_helpers(cls):
    """
    Loads the helpers and makes them available on the given class.

    :param class cls:
    """
    for helper_filename in listdir(DOCKER_HELPERS_DIRECTORY):
        base_name, extension = splitext(helper_filename)

        setattr(cls, base_name, partial(_run_helper, base_name))


class helpers:

    """
    Dynamic group of helpers that will run inside of the Docker container.

    """
    pass

_load_helpers(helpers)
