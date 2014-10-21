import os
import pkg_resources
import tempfile

DOCKER_BASE_URL = 'unix://var/run/docker.sock'

DOCKER_CLIENT_VERSION = '1.12'

DOCKER_CLIENT_TIMEOUT = 10

DOCKER_IMAGE = 'robmadole/lure:with-jig'

DOCKER_HELPERS_DIRECTORY = pkg_resources.resource_filename(__name__, 'resources/dockerhelpers')

CLONE_ROOT = os.path.join(tempfile.gettempdir(), '.lure')

JIG_SCRIPT = '/envs/jig/bin/jig'

JIG_INIT_DIRECTORY = '.jig'

JIG_PLUGINS_DIRECTORY = 'plugins'
