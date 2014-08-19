# -*- coding: utf-8 -*-

from os.path import dirname, join

from pytest import raises, fixture

from lure.exc import SpecNotFound, BadSpecSyntax
from lure.specs import load_from_file, Spec


@fixture
def bad_spec():
    return join(dirname(__file__), 'fixtures', 'bad_spec.json')


@fixture
def example_spec():
    return join(dirname(__file__), 'fixtures', 'example_spec.json')


def test_load_from_file_not_found():
    with raises(SpecNotFound):
        spec = load_from_file('/tmp/not-a-filename')


def test_load_from_file_bad_syntax(bad_spec):
    with raises(BadSpecSyntax):
        spec = load_from_file(bad_spec)


def test_load_from_file_is_spec(example_spec):
    spec = load_from_file(example_spec)

    assert isinstance(spec, Spec)
