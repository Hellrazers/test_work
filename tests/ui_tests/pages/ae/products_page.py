import random

import allure
from playwright.sync_api import Page

from lib.models.cart_item import CartItem


class ProductsPage:
    URL = "/products"

    def __init__(self, page: Page):
        self.page = page
        self._continue_btn = page.locator("#cartModal").get_by_text("Continue Shopping")
        self._modal = page.locator("#cartModal")

    @allure.step("Navigate to products page")
    def navigate(self):
        self.page.goto(self.URL)
        self.page.wait_for_load_state("networkidle")

    @allure.step("Add {count} random products to cart")
    def add_random_products_to_cart(self, count: int = 2) -> list[CartItem]:
        products = self.page.locator(".features_items .col-sm-4").all()
        assert len(products) >= count, f"Not enough products on page: found {len(products)}"

        selected = random.sample(products, count)
        added_items: list[CartItem] = []

        for product in selected:
            name = product.locator(".productinfo p").inner_text().strip()
            price = product.locator(".productinfo h2").inner_text().strip()
            with allure.step(f"Add to cart: {name} ({price})"):
                product.locator(".productinfo .add-to-cart").click()
                self._modal.wait_for(state="visible", timeout=5_000)
                added_items.append(CartItem(name=name, price=price))

                self._continue_btn.click()
                self._modal.wait_for(state="hidden", timeout=5_000)

        return added_items
