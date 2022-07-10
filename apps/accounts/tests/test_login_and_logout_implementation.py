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


class TestBase(StaticLiveServerTestCase):
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


class TestLogin(TestBase):
    def setUp(self) -> None:
        self.driver.get(f"{self.live_server_url}/accounts/login/")

        self.datas = {
            "username": "user test",
            "password": "pass test",
        }

    def __login(self) -> None:
        username = self.driver.find_element(By.CLASS_NAME, "qa-form-login__username")
        username.clear()
        username.send_keys(self.datas.get("username"))

        password = self.driver.find_element(By.CLASS_NAME, "qa-form-login__password")
        password.clear()
        password.send_keys(self.datas.get("password"))

        button_butmit = self.driver.find_element(By.CLASS_NAME, "qa-form-login__submit")
        button_butmit.click()

    def test_failure_login(self) -> None:
        self.__login()
        error_messages = WebDriverWait(self.driver, timeout=1).until(
            lambda d: d.find_element(By.CLASS_NAME, "qa-form-errors")
        )
        assert error_messages

    def test_successfull_login(self) -> None:
        User.objects.create_user(**self.datas)
        self.__login()
        title = WebDriverWait(self.driver, timeout=1).until(lambda d: d.title)
        assert title == "Djocial | Home"


class TestLogout(TestBase):
    def setUp(self) -> None:
        user = User.objects.create_user(username="myuser", password="password")
        force_login(user, self.driver, self.live_server_url)
        self.driver.get(f"{self.live_server_url}/")

    def test_if_logout_button_works(self) -> None:
        button_logout = self.driver.find_element(By.CLASS_NAME, "qa-button-logout")
        button_logout.click()
        time.sleep(2)
        assert self.driver.title == "Djocial | Login"
