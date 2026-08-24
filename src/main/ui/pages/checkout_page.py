from playwright.sync_api import Page, expect


class CheckoutPage:
    URL = "https://www.saucedemo.com/checkout-step-one.html"

    def __init__(self, page: Page):
        self.page = page
        self.first_name_input = page.locator('[data-test="firstName"]')
        self.last_name_input = page.locator('[data-test="lastName"]')
        self.postal_code_input = page.locator('[data-test="postalCode"]')
        self.continue_button = page.locator('[data-test="continue"]')
        self.finish_button = page.locator('[data-test="finish"]')
        self.error_message = page.locator('[data-test="error"]')
        self.success_message = page.locator(".complete-header")
        self.item_total = page.locator(".summary_subtotal_label")

    def start_checkout(self, first_name: str, last_name: str, postal_code: str):
        self.first_name_input.fill(first_name)
        self.last_name_input.fill(last_name)
        self.postal_code_input.fill(postal_code)
        self.continue_button.click()

    def finish_checkout(self):
        self.finish_button.click()

    def get_error_text(self) -> str:
        return self.error_message.inner_text()

    def get_success_text(self) -> str:
        return self.success_message.inner_text()

    def get_item_total(self) -> float:
        total_text = self.item_total.inner_text()
        return float(total_text.replace("Item total: $", ""))

    def get_item_total_after_continue(self) -> float:
        expect(self.item_total).to_be_visible()
        total_text = self.item_total.inner_text()
        return float(total_text.replace("Item total: $", ""))
