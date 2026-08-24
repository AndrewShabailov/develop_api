import allure
from src.main.ui.pages.basket_page import BasketPage
from playwright.sync_api import Page


class BasketSteps:
    def __init__(self, page: Page):
        self.page = page
        self.basket = BasketPage(page)

    @allure.step("Открываем корзину")
    def open_cart(self):
        self.basket.open_cart()
        return self

    @allure.step("Проверяем, что товар {product_name} есть в корзине")
    def expect_item_in_cart(self, product_name: str):
        self.basket.expect_item_in_cart(product_name)
        return self

    @allure.step("Проверяем, что товара {product_name} нет в корзине")
    def expect_item_not_in_cart(self, product_name: str):
        self.basket.expect_item_not_in_cart(product_name)
        return self

    @allure.step("Удаляем товар из корзины: {product_name}")
    def remove_item(self, product_name: str):
        self.basket.remove_item(product_name)
        return self

    @allure.step("Переходим к Checkout")
    def checkout(self):
        self.basket.checkout()
        return self

    @allure.step("Получаем список названий товаров в корзине")
    def get_item_names(self) -> list[str]:
        return self.basket.get_item_names()

    @allure.step("Получаем общую сумму товаров в корзине")
    def get_items_total_price(self) -> float:
        return self.basket.get_items_total_price()
