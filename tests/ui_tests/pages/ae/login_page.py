import allure
from playwright.sync_api import Page


class LoginPage:
    URL = "/login"

    def __init__(self, page: Page):
        self.page = page
        self._email = page.locator('input[data-qa="login-email"]')
        self._password = page.locator('input[data-qa="login-password"]')
        self._submit = page.locator('button[data-qa="login-button"]')

    @allure.step("Navigate to login page")
    def navigate(self):
        self.page.goto(self.URL)
        self.page.wait_for_load_state("networkidle")

    @allure.step("Login with email={email}")
    def login(self, email: str, password: str):
        self.page.evaluate("document.querySelectorAll('iframe').forEach(el => el.remove())")
        self._email.fill(email)
        self._password.fill(password)
        self._submit.click()
        self.page.wait_for_url(lambda url: "/login" not in url, timeout=15_000)

    def is_logged_in(self) -> bool:
        return self.page.locator('a[href="/logout"]').is_visible()
