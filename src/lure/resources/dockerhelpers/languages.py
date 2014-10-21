import os
import pickle
from collections import OrderedDict
from functools import partial
from os.path import join

LANG_DIRECTORY = os.environ['LANG_DIRECTORY']

list_languages = partial(sorted, os.listdir(LANG_DIRECTORY))
list_versions = lambda x: sorted(os.listdir(join(LANG_DIRECTORY, x)))

language_and_version = OrderedDict([(k, list_versions(k)) for k in list_languages()])

pickle.dump(language_and_version, open(os.environ['OUTPUT_FILE'], 'wb'))
