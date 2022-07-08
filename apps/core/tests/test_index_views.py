from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class TestIndexViewWhenUserIsNotAuthenticate(TestCase):
    def setUp(self) -> None:
        self.request = self.client.get(reverse("core:index"))

    def test_the_status_code(self) -> None:
        assert self.request.status_code == 302

    def test_the_redirect_URL(self) -> None:
        self.assertRedirects(self.request, "/accounts/login/?next=/")


class TestIndexViewWhenUserIsAuthenticate(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:

        cls.datas = {"username": "user test", "password": "pass test"}

        User.objects.create_user(**cls.datas)

    def setUp(self) -> None:
        self.client.login(
            username=self.datas.get("username"), password=self.datas.get("password")
        )
        self.request = self.client.get(reverse("core:index"))

    def test_the_status_code(self) -> None:
        assert self.request.status_code == 200

    def test_the_template_used_by_index_view(self) -> None:
        self.assertTemplateUsed(self.request, "pages/index.html")
