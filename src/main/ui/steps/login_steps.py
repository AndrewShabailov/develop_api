import allure
from src.main.ui.pages.login_page import LoginPage
from playwright.sync_api import Page


class LoginSteps:
    LOGIN_URL = "https://www.saucedemo.com/"

    def __init__(self, page: Page):
        self.page = page
        self.login_page = LoginPage(page)

    @allure.step("Открываем страницу логина")
    def open_login_page(self):
        self.login_page.open()
        return self

    @allure.step("Логинимся пользователем {username}")
    def login(self, username: str, password: str):
        self.login_page.login(username, password)
        return self

    @allure.step("Получаем текст ошибки при логине")
    def get_error_text(self) -> str:
        return self.login_page.get_error_text()

