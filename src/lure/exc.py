# -*- coding: utf-8 -*-


class SpecNotFound(Exception):

    """
    Raised when a spec file cannot be found.

    """
    def __init__(self, spec_filename):
        super().__init__(
            'Could not find a Lure spec file {}'.format(spec_filename)
        )


class BadSpecSyntax(Exception):

    """
    Raised when the JSON syntax is not valid enough for the parse to read it.

    """
    def __init__(self, exception):
        super().__init__(
            'Bad syntax in Lure spec file: {}'.format(exception)
        )
