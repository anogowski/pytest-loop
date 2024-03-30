# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://www.mozilla.org/en-US/MPL/2.0/.

import pytest

pytest_plugins = "pytester",


class Test_Loop:

	def test_no_loop(self, testdir):
		testdir.makepyfile("""
            def test_no_loop(request):
                fixtures = request.fixturenames
                assert "__pytest_loop_step_number" not in fixtures
        """)
		result = testdir.runpytest('-v', '--loop', '1')
		result.stdout.fnmatch_lines([
		    '*test_no_loop.py::test_no_loop PASSED*',
		    '*1 passed*',
		])
		assert result.ret == 0

	def test_can_loop(self, testdir):
		testdir.makepyfile("""
            def test_loop():
                pass
        """)
		result = testdir.runpytest('--loop', '2')
		result.stdout.fnmatch_lines(['*2 passed*'])
		assert result.ret == 0

	def test_mark_loop_decorator_is_registered(self, testdir):
		result = testdir.runpytest('--markers')
		result.stdout.fnmatch_lines(['@pytest.mark.loop(n): run the given test function `n` times.'])
		assert result.ret == 0

	def test_mark_loop_decorator(self, testdir):
		testdir.makepyfile("""
            import pytest
            @pytest.mark.loop(3)
            def test_mark_loop_decorator():
                pass
        """)
		result = testdir.runpytest()
		result.stdout.fnmatch_lines(['*3 passed*'])
		assert result.ret == 0

	def test_mark_loop_decorator_loop_once(self, testdir):
		testdir.makepyfile("""
            import pytest
            @pytest.mark.loop(1)
            def test_mark_loop_decorator_loop_once():
                pass
        """)
		result = testdir.runpytest('--loop', '10')
		result.stdout.fnmatch_lines(['*1 passed*'])
		assert result.ret == 0

	def test_parametrize(self, testdir):
		testdir.makepyfile("""
            import pytest
            @pytest.mark.parametrize('x', ['a', 'b', 'c'])
            def test_loop(x):
                pass
        """)
		result = testdir.runpytest('-v', '--loop', '2')
		result.stdout.fnmatch_lines([
		    '*test_parametrize.py::test_loop[ 1 / 6 ]  PASSED*',
		    '*test_parametrize.py::test_loop[ 2 / 6 ]  PASSED*',
		    '*test_parametrize.py::test_loop[ 3 / 6 ]  PASSED*',
		    '*test_parametrize.py::test_loop[ 4 / 6 ]  PASSED*',
		    '*test_parametrize.py::test_loop[ 5 / 6 ]  PASSED*',
		    '*test_parametrize.py::test_loop[ 6 / 6 ]  PASSED*',
		    '*6 passed*',
		])
		assert result.ret == 0

	def test_parametrized_fixture(self, testdir):
		testdir.makepyfile("""
            import pytest
            @pytest.fixture(params=['a', 'b', 'c'])
            def parametrized_fixture(request):
                return request.param

            def test_loop(parametrized_fixture):
                pass
        """)
		result = testdir.runpytest('--loop', '2')
		result.stdout.fnmatch_lines(['*6 passed*'])
		assert result.ret == 0

	def test_step_number(self, testdir):
		testdir.makepyfile("""
            import pytest
            expected_steps = iter(range(5))
            def test_loop(__pytest_loop_step_number):
                assert next(expected_steps) == __pytest_loop_step_number
                if __pytest_loop_step_number == 4:
                    assert not list(expected_steps)
        """)
		result = testdir.runpytest('-v', '--loop', '5')
		result.stdout.fnmatch_lines([
		    '*test_step_number.py::test_loop[ 1 / 5 ] PASSED*',
		    '*test_step_number.py::test_loop[ 2 / 5 ] PASSED*',
		    '*test_step_number.py::test_loop[ 3 / 5 ] PASSED*',
		    '*test_step_number.py::test_loop[ 4 / 5 ] PASSED*',
		    '*test_step_number.py::test_loop[ 5 / 5 ] PASSED*',
		    '*5 passed*',
		])
		assert result.ret == 0

	def test_invalid_option(self, testdir):
		testdir.makepyfile("""
            def test_loop():
                pass
        """)
		result = testdir.runpytest('--loop', 'a')
		assert result.ret == 4

	def test_unittest_test(self, testdir):
		testdir.makepyfile("""
            from unittest import TestCase

            class ClassStyleTest(TestCase):
                def test_this(self):
                    assert 1
        """)
		result = testdir.runpytest('-v', '--loop', '2')
		result.stdout.fnmatch_lines([
		    '*test_unittest_test.py::ClassStyleTest::test_this PASSED*',
		    '*1 passed*',
		])

	def test_ini_file(self, testdir):
		testdir.makeini("""
            [pytest]
            addopts = --delay=0 --hours=0 --minutes=0 --seconds=0 --loop=2
        """)

		testdir.makepyfile("""
            import pytest
            @pytest.fixture
            def addopts(request):
                return request.config.getini('addopts')
            def test_ini(addopts):
                assert addopts[0] == "--delay=0"
                assert addopts[1] == "--hours=0"
                assert addopts[2] == "--minutes=0"
                assert addopts[3] == "--seconds=0"
                assert addopts[4] == "--loop=0"
        """)

		result = testdir.runpytest("-v")

		# fnmatch_lines does an assertion internally
		result.stdout.fnmatch_lines([
		    "*::test_ini - run* PASSED*",
		]  #TODO: Get [] to work
		                           )

		# Make sure that that we get a '0' exit code for the testsuite
		assert result.ret == 0
