import tempfile
from functools import partial
from os.path import join, isfile

from pytest import fixture, raises
from pygit2 import init_repository, Signature

from lure.jig import (
    install_jig_plugin, shebang_editor, change_shebang,
    _replace_command, find_plugin_pre_commit_script)
from lure.specs import Spec

SHEBANG = '#!/bin/bash'


def _spec(lang, versions):
    spec_fixture = Spec('git://repository', 'git://plugin')

    spec_fixture.lang = lang

    list(map(spec_fixture.add_version, versions))

    return spec_fixture


@fixture
def repository():
    repo = init_repository(tempfile.mkdtemp())

    with open(join(repo.workdir, 'README.txt'), 'w') as fh:
        fh.write('Initial file')

    signature = Signature('Lure tests', 'noreply@nodomain')

    repo.index.add('README.txt')
    tree = repo.index.write_tree()

    repo.create_commit(
        'refs/heads/master',
        signature,
        signature,
        'Initial commit',
        tree,
        []
    )

    return repo


@fixture
def plugin():
    return 'http://github.com/robmadole/jig-plugins@chucknorris'


@fixture
def spec_one_version():
    return _spec('fake', ['1.0'])


@fixture
def script():
    fn, path = tempfile.mkstemp()

    with open(path, 'w') as fh:
        fh.write('{}\necho "fake script"\n'.format(SHEBANG))

    return path


def assert_shebang_is(script, shebang):
    with open(script) as fh:
        first_line = fh.readline()

    assert shebang.strip() == first_line.strip()


def test_install_jig_plugin(repository, plugin):
    assert install_jig_plugin(repository, plugin)


def test_install_jig_plugin_twice(repository, plugin):
    bound = partial(install_jig_plugin, repository, plugin)

    # Call it once
    bound()

    # And again
    assert bound()


def test_find_plugin_pre_commit_script(repository, plugin):
    install_jig_plugin(repository, plugin)

    script = find_plugin_pre_commit_script(repository)

    assert script.endswith('pre-commit')
    assert isfile(script)


def test_replace_command_not_found():
    with raises(ValueError):
        _replace_command('#!', '/usr/bin/fake')


def test_replace_command():
    assert _replace_command(
        '#!/bin/bash', '/usr/bin/fake'
    ) == '#!/usr/bin/fake'


def test_replace_command_keeps_args():
    assert _replace_command(
        '#!/bin/bash -a -b --ccc', '/usr/bin/fake'
    ) == '#!/usr/bin/fake -a -b --ccc'


def test_replace_command_drops_env_usage():
    assert _replace_command(
        '#!/usr/bin/env bash -a -b --ccc', '/usr/bin/fake'
    ) == '#!/usr/bin/fake -a -b --ccc'


def test_change_shebang():
    lines = ['#!/bin/bash\n', 'echo "test"\n']

    assert change_shebang(lines, '/usr/bin/fake') == \
        ['#!/usr/bin/fake\n', 'echo "test"\n']


def test_shebang_editor_yields_original_shebang(spec_one_version, script):
    editor = shebang_editor(spec_one_version, script)

    original_shebang = next(editor)

    assert original_shebang == SHEBANG


def test_shebang_editor_yields_language_version(spec_one_version, script):
    editor = shebang_editor(spec_one_version, script)

    # Original shebang
    next(editor)

    assert next(editor) == ('fake', '1.0')


def test_shebang_editor_changes_shebang(spec_one_version, script):
    editor = shebang_editor(spec_one_version, script)

    # Original shebang
    next(editor)

    language, version = next(editor)

    assert_shebang_is(script, '#!/lang/fake/1.0/bin/fake')


def test_shebang_editor_restores_at_the_end(spec_one_version, script):
    editor = shebang_editor(spec_one_version, script, shebang_format='{language}-{version}')

    # Original shebang
    next(editor)

    # Edit the shebang to be our new command
    next(editor)

    with raises(StopIteration):
        next(editor)

    assert_shebang_is(script, '#!/bin/bash')
