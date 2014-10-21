# -*- coding: utf-8 -*-

import logging

from colorlog import ColoredFormatter

log = logging.getLogger('lure')
log.setLevel(logging.DEBUG)

formatter = ColoredFormatter(
   "%(log_color)s%(levelname)8s%(reset)s"
   " %(message)s"
)

handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)

log.addHandler(handler)


def block_format(heading, output):
    """
    Format a block of text that will print nicely with our logger.

    :param str output:
    :rtype: str
    """
    indent = ' ' * 9
    indented = '\n'.join(map(lambda x: '{}{}'.format(indent, x), output.splitlines()))
    return '{}\n{}'.format(heading, indented)
