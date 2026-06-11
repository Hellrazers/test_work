import logging
import os
from pathlib import Path

import pytest
from allure_commons.types import AttachmentType
from allure_commons._allure import attach
from playwright.sync_api import Page

logger = logging.getLogger(__name__)

TRACES_DIR = Path(__file__).parent.parent.parent / "traces"


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    return {
        **browser_type_launch_args,
        "headless": True,
        "args": ["--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu"],
    }


@pytest.fixture(scope="function")
def ui_test_fixture(page: Page, request) -> Page:
    test_name = request.node.name
    safe_name = "".join(c if c.isalnum() or c in "-_" else "_" for c in test_name)
    console_logs = []

    page.on("console", lambda msg: console_logs.append(msg))
    page.context.tracing.start(screenshots=True, snapshots=True, sources=True)

    yield page

    try:
        test_failed = hasattr(request.node, "rep_call") and request.node.rep_call.failed

        if test_failed:
            log_text = "\n".join(f"{m.type.upper()} - {m.text}" for m in console_logs)
            if log_text:
                attach(log_text, name="Browser Console Log", attachment_type=AttachmentType.TEXT)
            attach(page.screenshot(full_page=True), name=f"{safe_name}_screenshot", attachment_type=AttachmentType.PNG)

        TRACES_DIR.mkdir(parents=True, exist_ok=True)
        trace_path = TRACES_DIR / f"{safe_name}.zip"
        page.context.tracing.stop(path=str(trace_path))

        with open(trace_path, "rb") as f:
            attach(f.read(), name=f"{safe_name}_trace.zip", attachment_type="application/zip")

        logger.info(f"Trace saved: {trace_path.resolve()}")
    except Exception as e:
        logger.warning(f"Error while capturing diagnostics: {e}")
