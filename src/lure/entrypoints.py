# -*- coding: utf-8 -*-

from docopt import docopt


def main():
    """
    Lure - test Jig plugins with multiple interpreter versions against real codes

    Usage:
      lure <lurespec>
    """
    arguments = docopt(main.__doc__)

    spec_filename = arguments['<lurespec>']

    try:
        spec = load_spec(spec_filename)
    except SpecNotFound as snf:
        logger.error(snf)
