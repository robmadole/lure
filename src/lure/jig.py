import shlex
from os import walk
from os.path import isdir, join
from subprocess import check_output, CalledProcessError, STDOUT

from lure import config
from lure.logger import log, block_format

SHEBANG_FORMAT = '/lang/{language}/{version}/bin/{language}'


def install_jig_plugin(repository, plugin):
    """
    Initialize a repository for Jig and install a single plugin.

    :param pygit2.Repository repository: the Git repository
    :param str plugin: the URL to a Jig plugin that will be passed to ``jig
        plugin add``
    """
    log.info('Initialize repository to use Jig')
    try:
        check_output(
            [config.JIG_SCRIPT, 'init', repository.workdir],
            stderr=STDOUT
        )
    except CalledProcessError as cpe:
        if not isdir(join(repository.workdir, config.JIG_INIT_DIRECTORY)):
            log.error(block_format(
                'Unable to init repository for use with Jig',
                cpe.output.decode('utf8')
            ))

    log.info('Installing Jig plugin {}'.format(plugin))
    try:
        check_output(
            [config.JIG_SCRIPT, 'plugin', 'add', '-r', repository.workdir, plugin],
            stderr=STDOUT
        )
    except CalledProcessError as cpe:
        if not 'already installed' in cpe.output.decode('utf8'):
            log.error(block_format(
                'Unable to install the plugin in {}'.format(repository.workdir),
                cpe.output.decode('utf8')
            ))
            return False

    return True


def find_plugin_pre_commit_script(repository):
    """
    Locates the pre-commit script for the installed Jig plugin in a repository.

    :param pygit2.Repository repository: the Git repository
    """
    plugins_directory = join(
        repository.workdir,
        config.JIG_INIT_DIRECTORY,
        config.JIG_PLUGINS_DIRECTORY
    )

    if not isdir(plugins_directory):
        return None

    for dirpath, dirnames, filenames in walk(plugins_directory):
        if 'pre-commit' in filenames:
            return join(dirpath, 'pre-commit')

    return None


def _replace_command(shebang_line, command):
    """
    Replaces the command in a shebang with a new command.

    This function has special handling that understands the use of ``env`` and will
    replace that command and the first argument given.

    :param str shebang_line:
    :param str command:
    """
    parts = shlex.split(shebang_line.strip('#!'))

    try:
        if '/env' in parts[0]:
            parts = parts[1:]

        parts[0] = command
    except IndexError:
        raise ValueError('No shebang command found in {}'.format(shebang_line))

    return '#!{}'.format(' '.join(parts))


def change_shebang(lines, command):
    """
    Replaces the shebang in the list of lines with a different command.

    :param list lines:
    :param str command:
    """
    changed = lines[:]

    changed[0] = '{}\n'.format(
        _replace_command(lines[0].strip(), command)
    )

    return changed


def shebang_editor(spec, script, shebang_format=SHEBANG_FORMAT):
    """
    Changes the script's shebang to use a spec's list of versions.

    This is a generator. Each time this function yields it will have changed
    the shebang of the script to a version and language listed in the Lure spec
    object.

    :param lure.specs.Spec spec: a Lure spec that describes what versions and
        language to use
    :param str script: location of a file that should be edited every time this
        function yields
    :param str shebang_format: the Python string formatting
        used to change the shebang
    """
    with open(script) as fh:
        lines = fh.readlines()

    if not lines or '#!' not in lines[0]:
        raise ValueError('No shebang line found in {}'.format(script))

    original_shebang = lambda: lines[0].strip() if lines else None

    yield original_shebang()

    try:
        for language, version in spec:
            with open(script, 'w') as fh:
                fh.writelines(
                    change_shebang(
                        lines,
                        shebang_format.format(language=language, version=version)
                    )
                )

            yield (language, version)
    finally:
        # Restore the file to its original state
        with open(script, 'w') as fh:
            fh.writelines(lines)
