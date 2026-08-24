import allure
from src.main.ui.pages.checkout_page import CheckoutPage
from playwright.sync_api import Page


class CheckoutSteps:
    def __init__(self, page: Page):
        self.page = page
        self.checkout = CheckoutPage(page)

    @allure.step("Начинаем Checkout: {first_name} {last_name}, {postal_code}")
    def start_checkout(self, first_name: str, last_name: str, postal_code: str):
        self.checkout.start_checkout(first_name, last_name, postal_code)
        return self

    @allure.step("Завершаем Checkout")
    def finish_checkout(self):
        self.checkout.finish_checkout()
        return self

    @allure.step("Получаем текст ошибки на Checkout")
    def get_error_text(self) -> str:
        return self.checkout.get_error_text()

    @allure.step("Получаем сумму товаров после continue")
    def get_item_total_after_continue(self) -> float:
        return self.checkout.get_item_total_after_continue()
