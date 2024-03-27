# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://www.mozilla.org/en-US/MPL/2.0/.

import pytest

pytest_plugins = "pytester",


class TestLoop:

   pytest_plugins = ("pytester",)


def test_help_message(testdir):
    result = testdir.runpytest("--help")
    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines(
        [
            "loop:",
            "*--delay=DELAY*The amount of time to wait between each test loop.",
            "*--hours=HOURS*The number of hours to loop the tests for.",
            "*--minutes=MINUTES*The number of minutes to loop the tests for.",
            "*--seconds=SECONDS*The number of seconds to loop the tests for.",
            "*--loop=*The number of times to loop each test"
        ]
    )


def test_ini_file(testdir):
    testdir.makeini(
        """
        [pytest]
        addopts = --delay=0 --hours=0 --minutes=0 --seconds=0 --loop=2
    """
    )

    testdir.makepyfile(
        """
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
    """
    )

    result = testdir.runpytest("-v")

    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines(
        ["*::test_ini - run* PASSED*", ] #TODO: Get [] to work
    )

    # Make sure that that we get a '0' exit code for the testsuite
    assert result.ret == 0