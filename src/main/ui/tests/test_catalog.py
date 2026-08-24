from playwright.sync_api import expect
from src.main.ui.pages.catalog_page import CatalogPage
from src.main.ui.steps.catalog_steps import CatalogSteps
from src.main.ui.steps.login_steps import LoginSteps


def test_count_catalog(page):
    catalog = CatalogPage(page)
    catalog.login("standard_user", "secret_sauce")
    assert catalog.get_products_count() == 6


def test_sorted_by_name(page):
    catalog = CatalogPage(page)
    catalog.login("standard_user", "secret_sauce")

    catalog.sort_items("az")
    assert catalog.get_product_names() == sorted(catalog.get_product_names())

    catalog.sort_items("za")
    assert catalog.get_product_names() == sorted(catalog.get_product_names(), reverse=True)


def test_sort_by_price(page):
    catalog = CatalogPage(page)
    catalog.login("standard_user", "secret_sauce")

    catalog.sort_items("lohi")
    assert catalog.get_product_prices() == sorted(catalog.get_product_prices())

    catalog.sort_items("hilo")
    assert catalog.get_product_prices() == sorted(catalog.get_product_prices(), reverse=True)


def test_add_to_cart(page):
    catalog = CatalogPage(page)
    catalog.login("standard_user", "secret_sauce")

    button = catalog.add_to_cart("Sauce Labs Bike Light")
    expect(button).to_have_text("Remove")
    assert catalog.get_cart_count() == 1


def test_add_and_remove_onesie(page):
    catalog = CatalogPage(page)
    catalog.login("standard_user", "secret_sauce")

    catalog.add_to_cart("Sauce Labs Onesie")
    assert catalog.get_cart_count() == 1

    catalog.remove_from_cart("Sauce Labs Onesie")
    assert catalog.get_cart_count() == 0


def test_product_details_onesie(page):
    catalog = CatalogPage(page)
    catalog.login("standard_user", "secret_sauce")

    name, price, detail_name, detail_price = catalog.open_product_details("Sauce Labs Onesie")
    assert name == detail_name
    assert price == detail_price


def test_product_details_fleece_jacket(page):
    catalog = CatalogPage(page)
    catalog.login("standard_user", "secret_sauce")

    name, price, detail_name, detail_price = catalog.open_product_details("Sauce Labs Fleece Jacket")
    assert name == detail_name
    assert price == detail_price


def test_remove_item_from_catalog(page):
    catalog = CatalogPage(page)
    catalog.login("standard_user", "secret_sauce")

    remove_button = catalog.remove_from_cart("Test.allTheThings() T-Shirt (Red)")

    expect(remove_button).to_have_text("Add to cart")
