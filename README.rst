Lure
====

Lure is a testing tool that integrates with Jig_ to make sure Jig plugins are running as expected.

Even though Jig offers a way of testing plugins its not easy to test with
different versions of an interpreter. The tests that Jig performs are also more
Unit Test than integration tests. This means they don't test against real code.

How Lure helps
--------------

Multiple versions of the scripting language
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you write a Python plugin you will normally see this as the first line:

::

    #!/usr/bin/env python

This shebang - the ``#!`` - uses ``/usr/bin/env`` to find a Python interpreter
to execute the rest of the script with.

It's not always predictable what version a user will have on their system. It
may be Python 2.6. It could be Python 3.4. So a plugin that was carefully tested with one
Python version may behave differently or be broken with another.

To address this issue Lure will execute the plugins using different
versions of the interpreter. It does this by utilizing Linux Containers via
Docker_. The included Docker image has multiple versions of popular scripting
languages like Python, Ruby, and Node.js.

Testing against real code
~~~~~~~~~~~~~~~~~~~~~~~~~

Another feature of Lure is that not only will it run the normal Unit Tests that
a plugin was developed with it will also clone one or more repositories and
execute the plugin against the real commits of the project.

For example if the plugin checked Python code for adherence to the PEP8 style
guide you can ask Lure to clone a popular Python project like Django_ and run
the plugin against that code.

Running Lure
------------

TODO

.. _Jig: http://pythonhosted.org/jig
.. _Docker: http://docker.com
.. _Django: https://www.djangoproject.com
