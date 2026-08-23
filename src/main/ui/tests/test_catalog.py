from playwright.sync_api import expect


def test_count_catalog(page):

    page.goto("https://www.saucedemo.com/")
    page.get_by_placeholder("Username").fill("standard_user")
    page.get_by_placeholder("Password").fill("secret_sauce")
    page.locator("#login-button").click()
    products = page.locator(".inventory_item")

    assert products.count() == 6


def test_sorted_by_name(page):

    page.goto("https://www.saucedemo.com/")
    page.get_by_placeholder("Username").fill("standard_user")
    page.get_by_placeholder("Password").fill("secret_sauce")
    page.locator("#login-button").click()
    sort_select = page.locator(".product_sort_container")
    expect(sort_select).to_be_visible(timeout=5000)
    sort_select.select_option("az")
    names = page.locator(".inventory_item_name").all_text_contents()

    assert names == sorted(names), "Товары не отсортированы по имени A-Z"


def test_reversed_sorting_by_name(page):

    page.goto("https://www.saucedemo.com/")
    page.get_by_placeholder("Username").fill("standard_user")
    page.get_by_placeholder("Password").fill("secret_sauce")
    page.locator("#login-button").click()
    sort_select = page.locator(".product_sort_container")
    expect(sort_select).to_be_visible(timeout=5000)
    sort_select.select_option("za")
    names = page.locator(".inventory_item_name").all_text_contents()

    assert names == sorted(names, reverse=True), "Товары не отсортированы по имени Z-A"


def test_sort_by_price(page):

    page.goto("https://www.saucedemo.com/")
    page.get_by_placeholder("Username").fill("standard_user")
    page.get_by_placeholder("Password").fill("secret_sauce")
    page.locator("#login-button").click()
    sort_select = page.locator(".product_sort_container")
    expect(sort_select).to_be_visible(timeout=5000)
    sort_select.select_option("lohi")
    prices_text = page.locator(".inventory_item_price").all_text_contents()
    prices = [float(p.replace("$", "")) for p in prices_text]

    assert prices == sorted(prices), "Товары не отсортированы по цене low → high"

    sort_select.select_option("hilo")
    prices_text = page.locator(".inventory_item_price").all_text_contents()
    prices = [float(p.replace("$", "")) for p in prices_text]

    assert prices == sorted(prices, reverse=True), "Товары не отсортированы по цене high → low"


def test_add_to_cart(page):

    page.goto("https://www.saucedemo.com/")
    page.get_by_placeholder("Username").fill("standard_user")
    page.get_by_placeholder("Password").fill("secret_sauce")
    page.locator("#login-button").click()
    product_card = page.locator(".inventory_item", has_text="Sauce Labs Bike Light")
    add_button = product_card.locator("button")
    add_button.click()

    expect(add_button).to_have_text("Remove")
    expect(page.locator(".shopping_cart_badge")).to_have_text("1")


def test_add_sauce_labs_onesie_to_cart(page):

    page.goto("https://www.saucedemo.com/")
    page.get_by_placeholder("Username").fill("standard_user")
    page.get_by_placeholder("Password").fill("secret_sauce")
    page.locator("#login-button").click()

    product_card = page.locator(".inventory_item", has_text="Sauce Labs Onesie")
    add_button = product_card.locator("button")

    add_button.click()
    expect(add_button).to_have_text("Remove")

    cart_badge = page.locator(".shopping_cart_badge")
    expect(cart_badge).to_have_text("1")

    add_button.click()

    expect(add_button).to_have_text("Add to cart")
    expect(cart_badge).not_to_be_visible()


def test_product_details_onesie(page):

    page.goto("https://www.saucedemo.com/")
    page.get_by_placeholder("Username").fill("standard_user")
    page.get_by_placeholder("Password").fill("secret_sauce")
    page.locator("#login-button").click()
    product_card = page.locator(".inventory_item", has_text="Sauce Labs Onesie")
    product_name = product_card.locator('[data-test="inventory-item-name"]').inner_text()
    product_price = product_card.locator('[data-test="inventory-item-price"]').inner_text()
    product_card.locator('[data-test="inventory-item-name"]').click()
    detail_name = page.locator('[data-test="inventory-item-name"]').inner_text()
    detail_price = page.locator('[data-test="inventory-item-price"]').inner_text()

    assert detail_name == product_name, "Название товара не совпадает"
    assert detail_price == product_price, "Цена товара не совпадает"


def test_product_fleece_jacket(page):
    page.goto("https://www.saucedemo.com/")
    page.get_by_placeholder("Username").fill("standard_user")
    page.get_by_placeholder("Password").fill("secret_sauce")
    page.locator("#login-button").click()
    product_card = page.locator(".inventory_item", has_text="Fleece Jacket")
    product_name = product_card.locator('[data-test="inventory-item-name"]').inner_text()
    product_price = product_card.locator('[data-test="inventory-item-price"]').inner_text()
    product_card.locator('[data-test="inventory-item-name"]').click()
    detail_name = page.locator('[data-test="inventory-item-name"]').inner_text()
    detail_price = page.locator('[data-test="inventory-item-price"]').inner_text()

    assert detail_name == product_name, "Название товара не совпадает"
    assert detail_price == product_price, "Цена товара не совпадает"


def test_delete_product_onesie(page):

    page.goto("https://www.saucedemo.com/")
    page.get_by_placeholder("Username").fill("standard_user")
    page.get_by_placeholder("Password").fill("secret_sauce")
    page.locator("#login-button").click()
    product_card = page.locator(".inventory_item", has_text="Sauce Labs Onesie")
    product_button = product_card.locator('[data-test="add-to-cart-sauce-labs-onesie"]')
    product_button.click()
    remove_button = product_card.locator('[data-test="remove-sauce-labs-onesie"]')

    assert remove_button.is_visible(), "Кнопка Remove не появилась"

    remove_button.click()
    add_button = product_card.locator('[data-test="add-to-cart-sauce-labs-onesie"]')

    assert add_button.is_visible(), "Кнопка Add to cart не вернулась после удаления"
