# -*- coding: utf-8 -*-

import json

from lure.exc import SpecNotFound, BadSpecSyntax


def load_from_file(filename):
    """
    Loads a Lure spec definition from a file.

    :param str filename:
    """
    try:
        with open(filename) as fh:
            contents = fh.read()
    except FileNotFoundError:
        raise SpecNotFound(filename)

    try:
        raw_spec = json.loads(contents)
    except (TypeError, ValueError) as e:
        raise BadSpecSyntax(e)

    return Spec.from_object(raw_spec)


class Spec(object):

    """
    Definition of how a Lure test should be ran.

    """
    @classmethod
    def from_object(cls, raw_spec):
        spec = cls(raw_spec.get('repository'), raw_spec.get('plugin'))

        spec.lang = raw_spec['versions']['lang']

        for version in raw_spec['versions']['using']:
            spec.add_version(version)

        return spec

    def __repr__(self):
        return '<Spec {!r}, {!r}>'.format(self.repository, self.plugin)

    def __init__(self, repository, plugin):
        self._versions = []

        self.repository = repository
        self.plugin = plugin
        self.lang = None

    def add_version(self, version):
        self._versions.append(version)

    def __iter__(self):
        return iter([(self.lang, i) for i in self._versions])
