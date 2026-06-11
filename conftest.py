import json
import os
from pathlib import Path

from dotenv import load_dotenv

from helpers.config import SessionConfig

_INTERNAL_FIXTURES = frozenset({
    "_session_faker", "pytestconfig", "browser_type_launch_args", "base_url",
    "delete_output_dir", "_verify_url", "playwright", "connect_options",
    "launch_browser", "browser_type", "browser", "browser_context_args",
    "output_path", "_artifacts_recorder", "_pw_artifacts_folder",
    "new_context", "context", "page", "browser_name",
})


def pytest_configure():
    load_dotenv()
    SessionConfig.base_url = os.getenv("UI_URL")
    SessionConfig.faker_location = os.getenv("FAKER_LOCALE")


def pytest_sessionfinish(session, exitstatus):
    allure_dir = session.config.option.allure_report_dir
    if not allure_dir:
        return
    allure_path = Path(allure_dir)
    if not allure_path.exists():
        return

    for container_file in allure_path.glob("*-container.json"):
        try:
            data = json.loads(container_file.read_text(encoding="utf-8"))
            names = {b.get("name", "").split("::")[0] for b in data.get("befores", [])}
            names |= {a.get("name", "").split("::")[0] for a in data.get("afters", [])}
            if names and names <= _INTERNAL_FIXTURES:
                container_file.unlink()
        except Exception:
            pass
