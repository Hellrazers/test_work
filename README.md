# Hybrid QA Automation — automationexercise.com

![CI](https://github.com/Hellrazers/test_work/actions/workflows/run-tests.yml/badge.svg)

Hybrid E2E test suite: API pre-condition → UI test → API teardown.

**Stack:** Python 3.10+ · Playwright · Pytest · Allure Report

**[Allure Report](https://hellrazers.github.io/test_work/)** — auto-updated on every push to `main`.

---

## Setup

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
playwright install chromium
```

## Configuration

```bash
cp .env.example .env
```

`.env`:
```
UI_URL=https://automationexercise.com/
FAKER_LOCALE=en_US
```

---

## Run

**Hybrid E2E test:**
```bash
pytest tests/ui_tests/tests/test_hybrid_flow.py -v --alluredir=allure-results
```

**API smoke test:**
```bash
pytest tests/api_tests/test_create.py -v --alluredir=allure-results
```

**All tests:**
```bash
pytest -v --alluredir=allure-results
```

**Allure report:**
```bash
allure serve allure-results
```

**View Playwright trace (local CLI):**
```bash
playwright show-trace traces/<test_name>.zip
```

**View Playwright trace (online):**
Upload the `.zip` file from `traces/` to [https://trace.playwright.dev](https://trace.playwright.dev) — no installation needed, works in any browser.

---

## Test flow

```
PRE-CONDITION  (API)
  POST /api/createAccount — registers a unique user via Faker-generated data

UI STEPS
  1. /login      — log in via the UI form using API-created credentials
  2. /products   — add 2 random products to the cart
  3. /view_cart  — verify both items are present, click Proceed To Checkout
  4. /checkout   — parse the Delivery Address block and assert it matches registration data

POST-CONDITION (API)
  DELETE /api/deleteAccount — deletes the user (runs even if the test fails)
```

---

## Artifacts

| Artifact | When | Where |
|---|---|---|
| Playwright trace `.zip` | always | `traces/` + Allure |
| Screenshot | on failure only | Allure |
| Browser console log | on failure only | Allure |
| HTTP request / response | every API call | Allure |
