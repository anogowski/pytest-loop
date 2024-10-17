# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://www.mozilla.org/en-US/MPL/2.0/.

from typing import Final
import pytest
from pytest import Pytester, RunResult

pytest_plugins = "pytester",


class Test_Loop:

	def test_no_loop(self, testdir: Pytester):
		testdir.makepyfile("""
            def test_no_loop(request):
                fixtures = request.fixturenames
                assert "__pytest_loop_step_number" not in fixtures
        """)
		result: RunResult = testdir.runpytest('-v', '--loop', '1')
		result.stdout.fnmatch_lines([
		    '*test_no_loop.py::test_no_loop PASSED*',
		    '*1 passed*',
		])
		assert result.ret == 0

	def test_can_loop(self, testdir: Pytester):
		testdir.makepyfile("""
            def test_loop():
                pass
        """)
		result: RunResult = testdir.runpytest('--loop', '2')
		result.stdout.fnmatch_lines(['*2 passed*'])
		assert result.ret == 0

	def test_mark_loop_decorator_is_registered(self, testdir: Pytester):
		result: RunResult = testdir.runpytest('--markers')
		result.stdout.fnmatch_lines(['@pytest.mark.loop(n): run the given test function `n` times.'])
		assert result.ret == 0

	def test_mark_loop_decorator(self, testdir: Pytester):
		testdir.makepyfile("""
            import pytest
            @pytest.mark.loop(3)
            def test_mark_loop_decorator():
                pass
        """)
		result: RunResult = testdir.runpytest()
		result.stdout.fnmatch_lines(['*3 passed*'])
		assert result.ret == 0

	def test_mark_loop_decorator_loop_once(self, testdir: Pytester):
		testdir.makepyfile("""
            import pytest
            @pytest.mark.loop(1)
            def test_mark_loop_decorator_loop_once():
                pass
        """)
		result: RunResult = testdir.runpytest('--loop', '10')
		result.stdout.fnmatch_lines(['*1 passed*'])
		assert result.ret == 0

	def test_parametrize(self, testdir: Pytester):
		RGX_1: Final[str] = r".+test_loop\[\w\- 1 / 2 \] PASSED"
		RGX_2: Final[str] = r".+test_loop\[\w\- 2 / 2 \] PASSED"
		testdir.makepyfile("""
            import pytest
            @pytest.mark.parametrize('x', ['a', 'b', 'c'])
            def test_loop(x):
                pass
        """)
		result: RunResult = testdir.runpytest('-v', '--loop', '2')
		result.stdout.re_match_lines([RGX_1, RGX_2, RGX_1, RGX_2, RGX_1, RGX_2], consecutive=True)
		result.assert_outcomes(passed=6)
		assert result.ret == 0

	def test_parametrized_fixture(self, testdir: Pytester):
		testdir.makepyfile("""
            import pytest
            @pytest.fixture(params=['a', 'b', 'c'])
            def parametrized_fixture(request):
                return request.param

            def test_loop(parametrized_fixture):
                pass
        """)
		result: RunResult = testdir.runpytest('--loop', '2')
		result.assert_outcomes(passed=6)
		assert result.ret == 0

	def test_step_number(self, testdir: Pytester):
		RGX: Final[str] = r".+test_loop\[ \d / 5 \] PASSED"
		testdir.makepyfile("""
            import pytest
            expected_steps = iter(range(5))
            def test_loop(__pytest_loop_step_number):
                assert next(expected_steps) == __pytest_loop_step_number
                if __pytest_loop_step_number == 4:
                    assert not list(expected_steps)
        """)
		result: RunResult = testdir.runpytest('-v', '--loop', '5')
		result.assert_outcomes(passed=5)
		result.stdout.re_match_lines([RGX, RGX, RGX, RGX, RGX, RGX], consecutive=True)
		assert result.ret == 0

	def test_invalid_option(self, testdir: Pytester):
		testdir.makepyfile("""
            def test_loop():
                pass
        """)
		result: RunResult = testdir.runpytest('--loop', 'a')
		assert result.ret == 4

	def test_unittest_test(self, testdir: Pytester):
		testdir.makepyfile("""
            from unittest import TestCase

            class ClassStyleTest(TestCase):
                def test_this(self):
                    assert 1
        """)
		result: RunResult = testdir.runpytest('-v', '--loop', '2')
		result.stdout.fnmatch_lines([
		    '*test_unittest_test.py::ClassStyleTest::test_this PASSED*',
		    '*1 passed*',
		])

	def test_ini_file(self, testdir: Pytester):
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
                assert addopts[4] == "--loop=2"
        """)

		result: RunResult = testdir.runpytest("-v")

		# fnmatch_lines does an assertion internally
		# result.stdout.fnmatch_lines([
		#     "*::test_ini[ 1 / 2 ] PASSED*",
		#     "*::test_ini[ 2 / 2 ] PASSED*",
		# ])

		# Make sure that that we get a '0' exit code for the testsuite
		assert result.ret == 0
