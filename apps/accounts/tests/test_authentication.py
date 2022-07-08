from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class TestLoginView(TestCase):
    def setUp(self) -> None:
        self.request = self.client.get(reverse("accounts:login"))

    def test_the_status_code(self) -> None:
        assert self.request.status_code == 200

    def test_the_template_used(self) -> None:
        self.assertTemplateUsed(self.request, "registration/login.html")


class TestLogoutView(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:

        cls.datas = {"username": "user test", "password": "pass test"}

        User.objects.create_user(**cls.datas)

    def setUp(self) -> None:
        self.client.login(
            username=self.datas.get("username"), password=self.datas.get("password")
        )
        self.request = self.client.get(reverse("accounts:logout"))

    def test_the_status_code(self) -> None:
        assert self.request.status_code == 302

    def test_the_redirect_URL(self) -> None:
        self.assertRedirects(self.request, "/accounts/login/")
