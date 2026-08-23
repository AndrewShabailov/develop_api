from playwright.sync_api import expect


def test_add_item_and_check_in_cart(auth_page):

    auth_page.locator('[data-test="add-to-cart-sauce-labs-backpack"]').click()
    auth_page.locator(".shopping_cart_link").click()
    item_name = auth_page.locator('[data-test="inventory-item-name"]')

    assert item_name.inner_text() == "Sauce Labs Backpack"


def test_add_items_and_check_in_cart(auth_page):

    auth_page.locator('[data-test="add-to-cart-sauce-labs-fleece-jacket"]').click()
    auth_page.locator('[data-test="add-to-cart-sauce-labs-bolt-t-shirt"]').click()
    auth_page.locator(".shopping_cart_link").click()
    name_jacket = auth_page.locator('.inventory_item_name', has_text='Sauce Labs Fleece Jacket')
    name_t_shirt = auth_page.locator('.inventory_item_name', has_text='Sauce Labs Bolt T-Shirt')

    assert name_jacket.inner_text() == "Sauce Labs Fleece Jacket"
    assert name_t_shirt.inner_text() == "Sauce Labs Bolt T-Shirt"


def test_remove_item_from_cart(auth_page):

    auth_page.locator('[data-test="add-to-cart-sauce-labs-fleece-jacket"]').click()
    auth_page.locator('[data-test="shopping-cart-link"]').click()
    jacket = auth_page.locator('.inventory_item_name', has_text='Sauce Labs Fleece Jacket')

    expect(jacket).to_be_visible()
    auth_page.locator('[data-test="remove-sauce-labs-fleece-jacket"]').click()

    expect(jacket).not_to_be_visible()


def test_remove_items_from_cart(auth_page):

    auth_page.locator('[data-test="add-to-cart-sauce-labs-backpack"]').click()
    auth_page.locator('[data-test="add-to-cart-test.allthethings()-t-shirt-(red)"]').click()
    auth_page.locator('[data-test="shopping-cart-link"]').click()
    backpack = auth_page.locator('.inventory_item_name', has_text='Sauce Labs Backpack')
    t_shirt = auth_page.locator('.inventory_item_name', has_text='Test.allTheThings() T-Shirt (Red)')

    expect(backpack).to_be_visible()
    expect(t_shirt).to_be_visible()

    auth_page.locator('[data-test="remove-sauce-labs-backpack"]').click()
    auth_page.locator('[data-test="remove-test.allthethings()-t-shirt-(red)"]').click()

    expect(backpack).not_to_be_visible()
    expect(t_shirt).not_to_be_visible()


def test_checkout_multiple_items(auth_page):

    jacket_card = auth_page.locator(".inventory_item", has_text="Sauce Labs Fleece Jacket")
    t_shirt_card = auth_page.locator(".inventory_item", has_text="Sauce Labs Bolt T-Shirt")

    jacket_card.locator("button").click()
    t_shirt_card.locator("button").click()

    auth_page.locator('[data-test="shopping-cart-link"]').click()

    jacket_name = auth_page.locator('.inventory_item_name', has_text='Sauce Labs Fleece Jacket')
    t_shirt_name = auth_page.locator('.inventory_item_name', has_text='Sauce Labs Bolt T-Shirt')
    expect(jacket_name).to_be_visible()
    expect(t_shirt_name).to_be_visible()

    prices_text = auth_page.locator(".inventory_item_price").all_text_contents()
    prices = [float(p.replace("$","")) for p in prices_text]
    expected_total = sum(prices)

    auth_page.locator('[data-test="checkout"]').click()
    auth_page.locator('[data-test="firstName"]').fill("A")
    auth_page.locator('[data-test="lastName"]').fill("K")
    auth_page.locator('[data-test="postalCode"]').fill("000")
    auth_page.locator('[data-test="continue"]').click()

    item_total_text = auth_page.locator(".summary_subtotal_label").inner_text()
    item_total_value = float(item_total_text.split("$")[1])

    assert item_total_value == expected_total,\
        f"Item total {item_total_value} не совпадает с суммой товаров {expected_total}"


    tax_text = auth_page.locator(".summary_tax_label").inner_text()
    tax_value = float(tax_text.split("$")[1])
    total_text = auth_page.locator(".summary_total_label").inner_text()
    total_value = float(total_text.split("$")[1])
    assert total_value == round(item_total_value + tax_value, 2),\
        "Total не совпадает с суммой Item total + Tax"

    auth_page.locator('[data-test="finish"]').click()

    success_message = auth_page.locator(".complete-header")
    expect(success_message).to_have_text("Thank you for your order!")


def test_checkout_without_items(auth_page):

    auth_page.locator('[data-test="add-to-cart-sauce-labs-fleece-jacket"]').click()
    auth_page.locator('[data-test="shopping-cart-link"]').click()
    jacket = auth_page.locator('.inventory_item_name', has_text='Sauce Labs Fleece Jacket')

    expect(jacket).to_be_visible()

    auth_page.locator('[data-test="checkout"]').click()
    auth_page.get_by_placeholder("First Name").fill("NewUser")
    auth_page.get_by_placeholder("Last Name").fill("Nrk")
    auth_page.locator('[data-test="continue"]').click()

    error_message = auth_page.locator('[data-test="error"]')
    expect(error_message).to_have_text('Error: Postal Code is required')
