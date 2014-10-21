from pytest import raises, fixture, mark
from pygit2 import Repository, GitError

from lure.git import clone, _simple_location_name


@fixture
def public_url():
    return 'https://github.com/robmadole/jig-plugins.git'


@fixture
def private_url():
    return 'git@github.com:robmadole/jig-plugins.git'


@mark.usefixtures('empty_clone_root')
def test_simple_location_name(public_url):
    assert _simple_location_name(public_url) == 'a77f6bdd8026'


@mark.usefixtures('empty_clone_root')
def test_clone_public(public_url):
    assert isinstance(clone(public_url), Repository)


@mark.usefixtures('empty_clone_root')
def test_clone_public_already_exists(public_url):
    clone(public_url)

    assert isinstance(clone(public_url), Repository)


@mark.usefixtures('empty_clone_root')
def test_clone_private(private_url):
    with raises(GitError):
        clone(private_url)
