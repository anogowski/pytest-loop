pytest-loop
===========

pytest-loop is a plugin for `pytest <https://docs.pytest.org>`_ that makes it
easy to loop a single test, or multiple tests, a specific number of times or for a certain duration of time.
This plugin merges pytest-repeat and pytest-stress with a fix for test results.

.. image:: https://img.shields.io/badge/license-MPL%202.0-blue.svg
   :target: https://github.com/anogowski/pytest-loop/blob/master/LICENSE
   :alt: License
.. image:: https://img.shields.io/pypi/v/pytest-loop.svg
   :target: https://pypi.python.org/pypi/pytest-loop/
   :alt: PyPI
.. image:: https://img.shields.io/pypi/pyversions/pytest-loop.svg
   :target: https://pypi.org/project/pytest-loop/
   :alt: Python versions
.. image:: https://github.com/anogowski/pytest-loop/actions/workflows/test.yml/badge.svg
    :target: https://github.com/anogowski/pytest-cov/actions
    :alt: See Build Status on GitHub Actions
.. image:: https://img.shields.io/github/issues-raw/anogowski/pytest-loop.svg
   :target: https://github.com/anogowski/pytest-loop/issues
   :alt: Issues
.. image:: https://img.shields.io/requires/github/anogowski/pytest-loop.svg
   :target: https://requires.io/github/anogowski/pytest-loop/requirements/?branch=master
   :alt: Requirements

Requirements
------------

You will need the following prerequisites in order to use pytest-loop:
- Python 3.7+ or PyPy
- pytest 7 or newer

Installation
------------

To install pytest-loop:

.. code-block:: bash

  $ pip install pytest-loop

Usage
-----

Iterative Loop:
^^^^^^^^^^^^^^^
Use the :code:`--loop` command line option to specify how many times you want
your test, or tests, to be run:

.. code-block:: bash

  $ pytest --loop=10 test_file.py

Each test collected by pytest will be run :code:`n` times.

If you want to mark a test in your code to be looped a number of times, you
can use the :code:`@pytest.mark.loop(n)` decorator:

.. code-block:: python

   import pytest


   @pytest.mark.loop(3)
   def test_loop_decorator():
       pass



Time based loop:
^^^^^^^^^^^^^^^^

Loop tests for 30 seconds::

    $ pytest --seconds 30

Loop tests for 45 minutes::

    $ pytest --minutes 45

Loop tests for 8 hours::

    $ pytest --hours 8

Loop tests for 1 hour 8 minutes and 9 seconds::

    $ pytest --hours 1 --minutes 8 --seconds 9

Need to wait some time after each test loop?::

    $ pytest --delay 5 --hours 4 --minutes 30

You can also add these values to config files::

    [pytest]
    addopts = --hours 1 --minutes 30

Note: These loop times include setup and teardown operations as well. So if you have a test setup that takes 5
seconds, your actual tests will run for 5 seconds less than your desired time.

looping a test until failure:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you are trying to diagnose an intermittent failure, it can be useful to run the same
test over and over again until it fails. You can use pytest's :code:`-x` option in
conjunction with pytest-loop to force the test runner to stop at the first failure.
For example:

.. code-block:: bash

  $ pytest --loop=1000 -x test_file.py

This will attempt to run test_file.py 1000 times, but will stop as soon as a failure
occurs.

.. code-block:: bash

  $ pytest --hours 10 -x test_file.

This will attempt to run test_file.py for 10 hours, but will stop as soon as a failure
occurs.

UnitTest Style Tests
--------------------

Unfortunately pytest-loop is not able to work with unittest.TestCase test classes.
These tests will simply always run once, regardless of :code:`--loop`, and show a warning.

Resources
---------

- `Release Notes <https://github.com/anogowski/pytest-loop/blob/master/CHANGES.rst>`_
- `Issue Tracker <https://github.com/anogowski/pytest-loop/issues>`_
- `Code <https://github.com/anogowski/pytest-loop/>`_