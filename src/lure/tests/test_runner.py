# -*- coding: utf-8 -*-

from unittest.mock import patch

from lure.runner import languages


def test_lists_languages():
    with patch('lure.runner.log') as log:
        languages()

    assert log.info.called
