# -*- coding: utf-8 -*-

import sys
from textwrap import dedent

from docopt import docopt

from lure.specs import load_from_file, SpecNotFound, BadSpecSyntax
from lure.logger import log
from lure.runner import run_spec, languages


def _run(arguments):
    spec_filename = arguments['<lurespec>']

    try:
        log.info('Loading the specifications file')
        spec = load_from_file(spec_filename)
    except SpecNotFound as snf:
        log.critical(snf)
        return
    except BadSpecSyntax as bss:
        log.critical(bss)
        return
    else:
        run_spec(spec)


def _list(arguments):
    available = languages()


def main(argv=sys.argv):
    """
    Lure - test Jig plugins with multiple interpreter versions against real codes

    Usage:
      lure run <lurespec>
      lure list
    """
    arguments = docopt(dedent(main.__doc__))

    if arguments['list']:
        _list(arguments)

    if arguments['run']:
        _run(arguments)
