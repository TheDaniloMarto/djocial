import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from pytest_django.asserts import assertRedirects, assertTemplateUsed

pytestmark = pytest.mark.django_db


def test_status_code_when_user_first_access_login_page(client) -> None:
    request = client.get(reverse("accounts:login"))
    assert request.status_code == 200


def test_the_template_used_by_login_view(client) -> None:
    request = client.get(reverse("accounts:login"))
    assertTemplateUsed(request, "registration/login.html")


def test_status_code_when_failure_login(client) -> None:
    datas = {"username": "user pass", "password": "pass test"}
    request = client.post(reverse("accounts:login"), **datas)
    assert request.status_code == 200


def test_status_code_when_successfully_login(client) -> None:
    datas = {"username": "user pass", "password": "pass test"}
    User.objects.create_user(**datas)
    request = client.post(reverse("accounts:login"), **datas)
    assert request.status_code == 200


def test_the_status_code_when_user_is_logged_out(client) -> None:
    datas = {"username": "user pass", "password": "pass test"}
    User.objects.create_user(**datas)
    client.login(**datas)
    request = client.get(reverse("accounts:logout"))
    assert request.status_code == 302


def test_redirect_URL_when_user_is_logged_out(client) -> None:
    datas = {"username": "user pass", "password": "pass test"}
    User.objects.create_user(**datas)
    client.login(**datas)
    request = client.get(reverse("accounts:logout"))
    assertRedirects(request, reverse("accounts:login"))
