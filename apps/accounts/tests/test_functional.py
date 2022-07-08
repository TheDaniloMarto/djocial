import time

from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.support.ui import WebDriverWait
from seleniumlogin import force_login
from webdriver_manager.firefox import GeckoDriverManager


class TestFunctionalBase(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        options = FirefoxOptions()
        options.add_argument("--headless")
        cls.driver = webdriver.Firefox(
            service=FirefoxService(GeckoDriverManager().install()), options=options
        )

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()


class TestLoginFunctionality(TestFunctionalBase):
    def test_the_title_of_page(self) -> None:
        self.driver.get(f"{self.live_server_url}/accounts/login/")
        assert self.driver.title == "Djocial | Login"

    def test_if_error_messages_appear_when_login_is_denied(self) -> None:
        self.driver.get(f"{self.live_server_url}/accounts/login/")

        input_username = self.driver.find_element(
            By.CLASS_NAME, "qa-form-login__username"
        )
        input_username.send_keys("user test")

        input_password = self.driver.find_element(
            By.CLASS_NAME, "qa-form-login__password"
        )
        input_password.send_keys("user pass")

        button_butmit = self.driver.find_element(By.CLASS_NAME, "qa-form-login__submit")
        button_butmit.click()

        error_messages = WebDriverWait(self.driver, timeout=1).until(
            lambda d: d.find_element(By.CLASS_NAME, "qa-form-errors")
        )

        assert error_messages

    def test_login_successful(self) -> None:
        datas = {
            "username": "user test",
            "password": "pass test",
        }

        User.objects.create_user(**datas)

        self.driver.get(f"{self.live_server_url}/accounts/login/")

        input_username = self.driver.find_element(
            By.CLASS_NAME, "qa-form-login__username"
        )
        input_username.send_keys(datas.get("username"))

        input_password = self.driver.find_element(
            By.CLASS_NAME, "qa-form-login__password"
        )
        input_password.send_keys(datas.get("password"))

        button_butmit = self.driver.find_element(By.CLASS_NAME, "qa-form-login__submit")
        button_butmit.click()

        title = WebDriverWait(self.driver, timeout=1).until(lambda d: d.title)

        assert title == "Djocial | Home"


class TestLogoutFunctionality(TestFunctionalBase):
    def test_if_logout_button_works(self) -> None:

        user = User.objects.create_user(username="myuser", password="password")
        force_login(user, self.driver, self.live_server_url)
        self.driver.get(f"{self.live_server_url}/")

        button_logout = self.driver.find_element(By.CLASS_NAME, "qa-button-logout")

        time.sleep(2)

        button_logout.click()

        time.sleep(2)

        assert self.driver.title == "Djocial | Login"
