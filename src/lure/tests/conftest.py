import tempfile

from pytest import fixture, mark

from lure import config


@fixture
def empty_clone_root(request):
    original_clone_root = config.CLONE_ROOT

    config.CLONE_ROOT = tempfile.mkdtemp()

    def restore_clone_root():
        config.CLONE_ROOT = original_clone_root

    request.addfinalizer(restore_clone_root)
