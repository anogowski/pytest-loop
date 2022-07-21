pytest-loop
===================

pytest-loop is a plugin for `pytest <https://docs.pytest.org>`_ that makes it
easy to loop a single test, or multiple tests, a specific number of times or for a certain duration of time.
This plugin merges pytest-repeat and pytest-stress with a fix for test results.

.. image:: https://img.shields.io/badge/license-MPL%202.0-blue.svg
   :target: https://github.com/pytest-dev/pytest-loop/blob/master/LICENSE
   :alt: License
.. image:: https://img.shields.io/pypi/v/pytest-loop.svg
   :target: https://pypi.python.org/pypi/pytest-loop/
   :alt: PyPI
.. image:: https://img.shields.io/pypi/pyversions/pytest-loop.svg
   :target: https://pypi.org/project/pytest-loop/
   :alt: Python versions
.. image:: https://img.shields.io/travis/pytest-dev/pytest-loop.svg
   :target: https://travis-ci.org/pytest-dev/pytest-loop/
   :alt: Travis
.. image:: https://img.shields.io/github/issues-raw/pytest-dev/pytest-loop.svg
   :target: https://github.com/pytest-dev/pytest-loop/issues
   :alt: Issues
.. image:: https://img.shields.io/requires/github/pytest-dev/pytest-loop.svg
   :target: https://requires.io/github/pytest-dev/pytest-loop/requirements/?branch=master
   :alt: Requirements

Requirements
------------

You will need the following prerequisites in order to use pytest-loop:

- pytest 6 or newer

Installation
------------
To install pytest-loop:

.. code-block:: bash

  $ pip install pytest-loop

looping a test
----------------

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

looping a test until failure
------------------------------

If you are trying to diagnose an intermittent failure, it can be useful to run the same
test over and over again until it fails. You can use pytest's :code:`-x` option in
conjunction with pytest-loop to force the test runner to stop at the first failure.
For example:

.. code-block:: bash

  $ pytest --loop=1000 -x test_file.py

This will attempt to run test_file.py 1000 times, but will stop as soon as a failure
occurs.


Resources
---------

- `Release Notes <https://github.com/pytest-dev/pytest-loop/blob/master/CHANGES.rst>`_
- `Issue Tracker <https://github.com/pytest-dev/pytest-loop/issues>`_
- `Code <https://github.com/pytest-dev/pytest-loop/>`_
