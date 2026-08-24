from src.main.ui.steps.catalog_steps import CatalogSteps
from src.main.ui.steps.checkout_steps import CheckoutSteps
from src.main.ui.steps.basket_steps import BasketSteps


def test_add_item_and_check_in_cart(page):
    catalog = CatalogSteps(page)
    basket = BasketSteps(page)

    catalog.login("standard_user", "secret_sauce")
    catalog.add_to_cart("Sauce Labs Backpack")

    basket.open_cart()
    basket.expect_item_in_cart("Sauce Labs Backpack")


def test_add_items_and_check_in_cart(page):
    catalog = CatalogSteps(page)
    basket = BasketSteps(page)

    catalog.login("standard_user", "secret_sauce")
    catalog.add_to_cart("Sauce Labs Fleece Jacket")
    catalog.add_to_cart("Sauce Labs Bolt T-Shirt")

    basket.open_cart()
    basket.expect_item_in_cart("Sauce Labs Fleece Jacket")
    basket.expect_item_in_cart("Sauce Labs Bolt T-Shirt")


def test_remove_item_from_cart(page):
    catalog = CatalogSteps(page)
    basket = BasketSteps(page)

    catalog.login("standard_user", "secret_sauce")
    catalog.add_to_cart("Sauce Labs Fleece Jacket")

    basket.open_cart()
    basket.expect_item_in_cart("Sauce Labs Fleece Jacket")
    basket.remove_item("Sauce Labs Fleece Jacket")
    basket.expect_item_not_in_cart("Sauce Labs Fleece Jacket")


def test_remove_items_from_cart(page):
    catalog = CatalogSteps(page)
    basket = BasketSteps(page)

    catalog.login("standard_user", "secret_sauce")
    catalog.add_to_cart("Sauce Labs Backpack")
    catalog.add_to_cart("Test.allTheThings() T-Shirt (Red)")

    basket.open_cart()
    basket.expect_item_in_cart("Sauce Labs Backpack")
    basket.expect_item_in_cart("Test.allTheThings() T-Shirt (Red)")

    basket.remove_item("Sauce Labs Backpack")
    basket.remove_item("Test.allTheThings() T-Shirt (Red)")
    basket.expect_item_not_in_cart("Sauce Labs Backpack")
    basket.expect_item_not_in_cart("Test.allTheThings() T-Shirt (Red)")


def test_checkout_multiple_items(page):
    catalog = CatalogSteps(page)
    basket = BasketSteps(page)
    checkout = CheckoutSteps(page)

    catalog.login("standard_user", "secret_sauce")
    catalog.add_to_cart("Sauce Labs Fleece Jacket")
    catalog.add_to_cart("Sauce Labs Bolt T-Shirt")

    basket.open_cart()
    basket.expect_item_in_cart("Sauce Labs Fleece Jacket")
    basket.expect_item_in_cart("Sauce Labs Bolt T-Shirt")
    basket_total = basket.get_items_total_price()

    basket.checkout()
    checkout.start_checkout(first_name="Test", last_name="User", postal_code="12345")
    checkout_total = checkout.get_item_total_after_continue()
    assert checkout_total == basket_total, "Сумма товаров в Checkout не совпадает с корзиной"


def test_checkout_without_items(page):
    catalog = CatalogSteps(page)
    basket = BasketSteps(page)
    checkout = CheckoutSteps(page)

    catalog.login("standard_user", "secret_sauce")

    basket.open_cart()
    items = basket.get_item_names()
    assert len(items) == 0, "Корзина не пуста"

    basket.checkout()
    checkout.start_checkout(first_name="NewUser", last_name="Nrk", postal_code="")
    error_text = checkout.get_error_text()
    assert error_text != "", "Ожидалась ошибка при оформлении пустой корзины"
