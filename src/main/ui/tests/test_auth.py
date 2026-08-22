from playwright.sync_api import expect


def test_auth(page):
    page.goto("https://www.saucedemo.com/")

    page.get_by_placeholder("Username").fill("standard_user")
    page.get_by_placeholder("Password").fill("secret_sauce")

    page.locator("#login-button").click()

    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")


def test_login_locked_out_user(page):
    page.goto("https://www.saucedemo.com/")

    page.get_by_placeholder("Username").fill("locked_out_user")
    page.get_by_placeholder("Password").fill("secret_sauce")

    page.locator("#login-button").click()
    error = page.locator("h3[data-test='error']")

    expect(page).to_have_url("https://www.saucedemo.com/")
    expect(error).to_be_visible()
    expect(error).to_have_text("Epic sadface: Sorry, this user has been locked out.")


def test_logout(page):
    page.goto("https://www.saucedemo.com/")

    page.get_by_placeholder("Username").fill("standard_user")
    page.get_by_placeholder("Password").fill("secret_sauce")

    page.locator("#login-button").click()

    page.locator("#react-burger-menu-btn").click()
    page.locator("#logout_sidebar_link").click()

    expect(page).to_have_url("https://www.saucedemo.com/")
    expect(page.locator("#login-button")).to_be_visible()


def test_logout_visual_user(page):
    page.goto("https://www.saucedemo.com/")

    page.get_by_placeholder("Username").fill("visual_user")
    page.get_by_placeholder("Password").fill("secret_sauce")

    page.locator("#login-button").click()

    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")

    page.locator("#react-burger-menu-btn").click()
    page.locator("#logout_sidebar_link").click()

    expect(page).to_have_url("https://www.saucedemo.com/")
    expect(page.locator("#login-button")).to_be_visible()


