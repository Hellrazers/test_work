import allure
from assertpy import assert_that
from playwright.sync_api import Page

from lib.models.registration.registration_request_model import RegistrationRequestPost


class CheckoutPage:
    def __init__(self, page: Page):
        self.page = page
        self._delivery_block = page.locator("#address_delivery")

    def _get_address_lines(self) -> list[str]:
        all_li = self._delivery_block.locator("li").all()
        return [
            li.inner_text().strip()
            for li in all_li
            if li.locator("h3").count() == 0 and li.inner_text().strip()
        ]

    @allure.step("Verify delivery address matches registration data")
    def verify_delivery_address(self, user: RegistrationRequestPost):
        self._delivery_block.wait_for(state="visible", timeout=8_000)

        lines = self._get_address_lines()
        full_text = "\n".join(lines)

        with allure.step(f"Assert full name — expected: {user.title}. {user.firstname} {user.lastname}"):
            expected_name = f"{user.title}. {user.firstname} {user.lastname}"
            assert_that(lines[0]).is_equal_to(expected_name)

        with allure.step(f"Assert company '{user.company}' present in address block"):
            assert_that(full_text).contains(user.company)

        with allure.step(f"Assert address1 '{user.address1}' present"):
            assert_that(full_text).contains(user.address1)

        with allure.step(f"Assert city '{user.city}' present"):
            assert_that(full_text).contains(user.city)

        with allure.step(f"Assert state '{user.state}' present"):
            assert_that(full_text).contains(user.state)

        with allure.step(f"Assert zipcode '{user.zipcode}' present"):
            assert_that(full_text).contains(user.zipcode)

        with allure.step(f"Assert country '{user.country}' present"):
            assert_that(full_text).contains(user.country)

        with allure.step(f"Assert mobile '{user.mobile_number}' present"):
            assert_that(full_text).contains(user.mobile_number)
