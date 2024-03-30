# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://www.mozilla.org/en-US/MPL/2.0/.

# System Imports
import re
import shutil
import time

# PyTest Imports
import pytest
from pluggy import HookspecMarker
from _pytest.main import Session
from _pytest.config import Config

SECONDS_IN_HOUR: float = 3600
SECONDS_IN_MINUTE: float = 60
SHORTEST_AMOUNT_OF_TIME: float = 0
hookspec = HookspecMarker("pytest")


class InvalidTimeParameterError(Exception):
	pass


def pytest_configure(config: Config):
	config.addinivalue_line('markers', 'loop(n): run the given test function `n` times.')


def pytest_addoption(parser):
	"""
	Add our command line options.
	"""
	pytest_loop = parser.getgroup("loop")
	pytest_loop.addoption(
	    "--delay",
	    action="store",
	    default=0,
	    type=float,
	    help="The amount of time to wait between each test loop.",
	)
	pytest_loop.addoption(
	    "--hours",
	    action="store",
	    default=0,
	    type=float,
	    help="The number of hours to loop the tests for.",
	)
	pytest_loop.addoption(
	    "--minutes",
	    action="store",
	    default=0,
	    type=float,
	    help="The number of minutes to loop the tests for.",
	)
	pytest_loop.addoption(
	    "--seconds",
	    action="store",
	    default=0,
	    type=float,
	    help="The number of seconds to loop the tests for.",
	)

	pytest_loop.addoption(
	    '--loop',
	    action='store',
	    default=1,
	    type=int,
	    help='The number of times to loop each test',
	)


@hookspec(firstresult=True)
def pytest_runtestloop(session: Session) -> bool:
	"""
	Reimplement the test loop but loop for the user defined amount of time or iterations.
	"""
	if session.testsfailed and not session.config.option.continue_on_collection_errors:
		raise session.Interrupted("%d error%s during collection" % (session.testsfailed, "s" if session.testsfailed != 1 else ""))

	if session.config.option.collectonly:
		return True

	start_time: float = time.time()
	total_time: float = 0

	iterations = session.config.option.loop
	m = session.get_closest_marker('loop')

	if m is not None:
		iterations = int(m.args[0])

	count: int = 0
	pattern: str = ""

	while total_time >= SHORTEST_AMOUNT_OF_TIME or count <= iterations:  # need to run at least one for normal tests
		count += 1
		total_time = _get_total_time(session)

		_print_loop_count(count, iterations)
		for index, item in enumerate(session.items):
			item: pytest.Item = item
			item._report_sections.clear()  #clear reports for new test

			if total_time > SHORTEST_AMOUNT_OF_TIME:
				pattern = " - run\[\d+\]"
				run_str: str = f" - run[{count}]"
				item._nodeid = _set_nodeid(item._nodeid, pattern, run_str)

			elif count < iterations:
				pattern = " - run\[\d+ / d+\]"
				run_str: str = f" - run[{count} / {iterations}]"
				item._nodeid = _set_nodeid(item._nodeid, pattern, run_str)

			next_item: pytest.Item = session.items[index + 1] if index + 1 < len(session.items) else None
			item.config.hook.pytest_runtest_protocol(item=item, nextitem=next_item)
			if session.shouldfail:
				raise session.Failed(session.shouldfail)
			if session.shouldstop:
				raise session.Interrupted(session.shouldstop)
		if _timed_out(session, start_time) and count >= iterations:
			break  # exit loop
		time.sleep(_get_delay_time(session))
	return True


def _set_nodeid(nodeid: str, pattern: str, run_str: str) -> str:
	if re.search(pattern, nodeid):
		nodeid = re.sub(pattern, run_str, nodeid)
	else:
		nodeid = nodeid + run_str
	return nodeid


def _get_delay_time(session: Session) -> float:
	"""
	Helper function to extract the delay time from the session.

	:param session: Pytest session object.
	:return: Returns the delay time for each test loop.
	"""
	return session.config.option.delay


def _get_total_time(session: Session) -> float:
	"""
	Takes all the user available time options, adds them and returns it in seconds.

	:param session: Pytest session object.
	:return: Returns total amount of time in seconds.
	"""
	hours_in_seconds = session.config.option.hours * SECONDS_IN_HOUR
	minutes_in_seconds = session.config.option.minutes * SECONDS_IN_MINUTE
	seconds = session.config.option.seconds
	total_time = hours_in_seconds + minutes_in_seconds + seconds
	if total_time < SHORTEST_AMOUNT_OF_TIME:
		raise InvalidTimeParameterError("Total time cannot be less than: {}!".format(SHORTEST_AMOUNT_OF_TIME))
	return total_time


def _timed_out(session: Session, start_time: float) -> bool:
	"""
	Helper function to check if the user specified amount of time has lapsed.

	:param session: Pytest session object.
	:return: Returns True if the timeout has expired, False otherwise.
	"""
	return time.time() - start_time > _get_total_time(session)


def _print_loop_count(count: int, iterations: int):
	"""
	Helper function to simply print out what loop number we're on.

	:param count: The number to print.
	:return: None.
	"""
	column_length = shutil.get_terminal_size().columns
	print("\n")
	if iterations > 1:
		print(f" Loop # {count}/{iterations} ".center(column_length, "="))
	else:
		print(f" Loop # {count} ".center(column_length, "="))
	print("\n")
