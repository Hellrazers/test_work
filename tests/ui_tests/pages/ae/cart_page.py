import allure
from assertpy import assert_that
from playwright.sync_api import Page

from lib.models.cart_item import CartItem


class CartPage:
    URL = "/view_cart"

    def __init__(self, page: Page):
        self.page = page
        self._rows = page.locator("#cart_info_table tbody tr")
        self._proceed_btn = page.get_by_text("Proceed To Checkout")

    @allure.step("Navigate to cart page")
    def navigate(self):
        self.page.goto(self.URL)
        self.page.wait_for_load_state("domcontentloaded")

    @allure.step("Verify cart contains expected items with correct attributes")
    def verify_items(self, expected_items: list[CartItem]):
        self.page.wait_for_selector("#cart_info_table tbody tr", timeout=8_000)
        rows = self._rows.all()

        actual: dict[str, dict] = {}
        for row in rows:
            name = row.locator("td.cart_description h4 a").inner_text().strip()
            actual[name] = {
                "price": row.locator("td.cart_price p").inner_text().strip(),
                "quantity": row.locator("td.cart_quantity button").inner_text().strip(),
                "total": row.locator("td.cart_total p").inner_text().strip(),
            }

        for item in expected_items:
            with allure.step(f"Assert '{item.name}' is in cart"):
                assert_that(actual).contains_key(item.name)

            row_data = actual[item.name]

            with allure.step(f"Assert price — expected: {item.price}"):
                assert_that(row_data["price"]).is_equal_to(item.price)

            with allure.step(f"Assert quantity = 1"):
                assert_that(row_data["quantity"]).is_equal_to("1")

            with allure.step(f"Assert total — expected: {item.price}"):
                assert_that(row_data["total"]).is_equal_to(item.price)

    @allure.step("Proceed to checkout")
    def proceed_to_checkout(self):
        self._proceed_btn.click()
        self.page.wait_for_url("**/checkout", timeout=8_000)
