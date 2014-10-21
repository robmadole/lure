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


@fixture
def spec_raw_object():
    return {
        'repository': 'http://github.com/repository',
        'plugin': 'http://github.com/plugin',
        'versions': {
            'lang': 'python',
            'using': [
                '2.7',
                '3.4'
            ]
        }
    }


def test_spec_repr():
    spec = Spec('r', 'p')

    assert repr(spec) == "<Spec 'r', 'p'>"


def test_spec_versions(spec_raw_object):
    spec = Spec.from_object(spec_raw_object)

    assert list(spec) == [
        ('python', '2.7'),
        ('python', '3.4')
    ]


def test_load_from_file_not_found():
    with raises(SpecNotFound):
        spec = load_from_file('/tmp/not-a-filename')


def test_load_from_file_bad_syntax(bad_spec):
    with raises(BadSpecSyntax):
        spec = load_from_file(bad_spec)


def test_load_from_file_is_spec(example_spec):
    spec = load_from_file(example_spec)

    assert isinstance(spec, Spec)
