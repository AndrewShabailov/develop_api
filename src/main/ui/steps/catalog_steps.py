import allure
from src.main.ui.pages.catalog_page import CatalogPage
from playwright.sync_api import Page, expect


class CatalogSteps:
    def __init__(self, page: Page):
        self.page = page
        self.catalog = CatalogPage(page)

    @allure.step("Логинимся пользователем {username}")
    def login(self, username: str, password: str):
        self.catalog.login(username, password)
        return self

    @allure.step("Добавляем товар в корзину: {product_name}")
    def add_to_cart(self, product_name: str):
        button = self.catalog.add_to_cart(product_name)
        expect(button).to_have_text("Remove")
        return self

    @allure.step("Удаляем товар из корзины: {product_name}")
    def remove_from_cart(self, product_name: str):
        button = self.catalog.remove_from_cart(product_name)
        expect(button).to_have_text("Add to cart")
        return self

    @allure.step("Сортируем товары: {option}")
    def sort_items(self, option: str):
        self.catalog.sort_items(option)
        return self

    @allure.step("Получаем количество товаров в каталоге")
    def get_products_count(self) -> int:
        return self.catalog.get_products_count()

    @allure.step("Получаем список названий товаров")
    def get_product_names(self) -> list[str]:
        return self.catalog.get_product_names()

    @allure.step("Получаем список цен товаров")
    def get_product_prices(self) -> list[float]:
        return self.catalog.get_product_prices()

    @allure.step("Получаем количество товаров в корзине")
    def get_cart_count(self) -> int:
        return self.catalog.get_cart_count()

    @allure.step("Открываем страницу деталей товара: {product_name}")
    def open_product_details(self, product_name: str):
        return self.catalog.open_product_details(product_name)

    @allure.step("Выполняем логаут")
    def logout(self):
        self.catalog.logout()
        return self
