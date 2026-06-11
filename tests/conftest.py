import logging

import pytest

logger = logging.getLogger("tests")
logger.setLevel(logging.INFO)


@pytest.hookimpl(tryfirst=True)
def pytest_sessionstart(session):
    logger.info("═" * 50)
    logger.info("TEST SESSION STARTED")
    logger.info("═" * 50)


@pytest.hookimpl(trylast=True)
def pytest_sessionfinish(session, exitstatus):
    logger.info("═" * 50)
    logger.info("TEST SESSION FINISHED")
    logger.info("═" * 50)


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_logstart(nodeid, location):
    test_name = nodeid.split("::")[-1]
    logger.info("══════════════════════════════════════")
    logger.info(f"TEST START: {test_name}")
    logger.info("══════════════════════════════════════")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_logreport(report):
    yield
    if report.when == "call":
        test_name = report.nodeid.split("::")[-1]
        if report.passed:
            logger.info(f"TEST PASSED: {test_name}")
        elif report.failed:
            logger.info(f"TEST FAILED: {test_name}")
        elif report.skipped:
            logger.info(f"TEST SKIPPED: {test_name}")
