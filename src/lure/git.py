import hashlib
from os.path import join

from pygit2 import clone_repository, discover_repository, Repository

from lure import config
from lure.logger import log


def _simple_location_name(location):
    """
    Make a predictable name that can be used to create a directory on the file system.

    :param str location:
    :returns: a hex value based on location
    :rtype: str
    """
    hash = hashlib.sha256()
    hash.update(location.encode('utf8'))

    return hash.hexdigest()[:12]


def clone(location):
    """
    Clone a Git repository if it doesn't exist into a temporary directory.

    :param str location: the Git URL to clone
    :rtype: pygit2.Repository
    """
    path = join(config.CLONE_ROOT, _simple_location_name(location))

    log.info('Cloning to path {}'.format(path))

    try:
        log.info('Looking for existing repository')
        repository_path = discover_repository(path)
    except KeyError:
        log.info('No existing repository found, cloning fresh')
        return clone_repository(location, path)
    else:
        log.info('Repository already exists at {}'.format(repository_path))
        repository = Repository(repository_path)

        remote = repository.remotes[0]
        remote.sideband_progress = log.info

        log.info('Fetching to get the latest objects from remote')
        remote.fetch()

        return repository


def update():
    pass
