import sys
import os
import imp
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

README = open(os.path.join(here, 'README.rst')).read()
NEWS = open(os.path.join(here, 'NEWS.rst')).read()

version = imp.load_source(
    'lure', os.path.join(here, 'src', 'lure', '__init__.py')).__version__

install_requires = [
    'pygit2>=0.21.0',
]

setup(
    name='jig',
    version=version,
    description="Test Jig plugins with multiple interpreter versions against real code",
    long_description=README + '\n\n' + NEWS,
    keywords='jig',
    author='Rob Madole',
    author_email='robmadole@gmail.com',
    url='http://github.com/robmadole/lure',
    license='MIT',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'lure = lure.entrypoints:main']}
)
