# -*- coding: utf-8 -*-

from lure.exc import SpecNotFound, BadSpecSyntax


def test_spec_not_found():
    exception = SpecNotFound('/file')

    assert str(exception) == \
        'Could not find a Lure spec file /file'


def test_bad_spec_syntax():
    exception = BadSpecSyntax(ValueError('Invalid syntax line 1, character 1'))

    assert str(exception) == \
        'Bad syntax in Lure spec file: Invalid syntax line 1, character 1'
