import allure
import pytest
from playwright.sync_api import Page

from lib.models.registration.registration_request_model import RegistrationRequestPost
from tests.ui_tests.pages.ae.cart_page import CartPage
from tests.ui_tests.pages.ae.checkout_page import CheckoutPage
from tests.ui_tests.pages.ae.login_page import LoginPage
from tests.ui_tests.pages.ae.products_page import ProductsPage


@pytest.mark.hybrid_e2e
@allure.feature("Hybrid E2E")
@allure.story("Register via API → UI checkout → verify delivery address → delete via API")
@allure.title("Hybrid: API registration + UI checkout address validation")
@allure.description(
    "End-to-end hybrid test covering the full user journey across API and UI layers.\n\n"
    "Pre-condition (API): registers a unique user via POST /api/createAccount using Faker-generated data.\n\n"
    "UI steps:\n"
    "1. /login — authenticates with the API-created credentials.\n"
    "2. /products — adds 2 randomly selected products to the cart.\n"
    "3. /view_cart — verifies both items are present with correct attributes (name, price, quantity=1, total) and proceeds to checkout.\n"
    "4. /checkout — parses the Delivery Address block and asserts every field "
    "(name, company, address, city, state, zip, country, phone) matches the registration payload.\n\n"
    "Post-condition (API): deletes the user via DELETE /api/deleteAccount regardless of test outcome."
)
def test_hybrid_checkout_address(ui_test_fixture: Page, registered_user: RegistrationRequestPost):
    page = ui_test_fixture
    user = registered_user

    with allure.step("Step 1 — Login via UI with API-created credentials"):
        login = LoginPage(page)
        login.navigate()
        login.login(email=str(user.email), password=user.password)
        assert login.is_logged_in(), "Login failed — logout link not visible after login"

    with allure.step("Step 2 — Navigate to Products and add 2 random items to cart"):
        products = ProductsPage(page)
        products.navigate()
        added_items = products.add_random_products_to_cart(count=2)

    with allure.step("Step 3 — Open cart, verify both items, proceed to checkout"):
        cart = CartPage(page)
        cart.navigate()
        cart.verify_items(added_items)
        cart.proceed_to_checkout()

    with allure.step("Step 4 — Verify delivery address matches registration data"):
        checkout = CheckoutPage(page)
        checkout.verify_delivery_address(user)
