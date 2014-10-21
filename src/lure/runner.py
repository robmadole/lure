# -*- coding: utf-8 -*-

from lure.logger import log, block_format
from lure.docker import helpers
from lure.git import clone
from lure.jig import install_jig_plugin, find_plugin_pre_commit_script, shebang_editor


def run_spec(spec):
    repository = clone(spec.repository)

    install_jig_plugin(repository, spec.plugin)

    editor = shebang_editor(spec, find_plugin_pre_commit_script(repository))

    original_shebang = next(editor)

    log.info('Running automated tests that are bundled with the plugin')
    log.info('Original shebang on the plugin is {}'.format(original_shebang))

    for state in editor:
        log.info('Modifying the pre-commit to use {} {}'.format(*state))

    log.info('Restored plugin pre-commit script to the original state')


def languages():
    output = []
    for language, versions in helpers.languages().items():
        output.append('{!r}'.format(language))
        output.extend(['   {}'.format(i) for i in versions])

    log.info(block_format('Listing languages available', '\n'.join(output)))
