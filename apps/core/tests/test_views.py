import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from pytest_django.asserts import assertRedirects, assertTemplateUsed

pytestmark = pytest.mark.django_db


def test_the_status_of_the_dashboard_view_when_user_is_not_ath(client) -> None:
    request = client.get(reverse("core:dashboard"))
    assert request.status_code == 302


def test_the_redirect_URL_when_user_is_not_auth(client) -> None:
    request = client.get(reverse("core:dashboard"))
    assertRedirects(request, "/accounts/login/?next=/")


def test_the_status_of_the_dashboard_view_when_user_is_ath(client) -> None:
    datas = {"username": "user test", "password": "pass test"}
    User.objects.create_user(**datas)
    client.login(**datas)
    request = client.get(reverse("core:dashboard"))
    assert request.status_code == 200


def test_the_template_used_by_dashboard_view(client) -> None:
    datas = {"username": "user test", "password": "pass test"}
    User.objects.create_user(**datas)
    client.login(**datas)
    request = client.get(reverse("core:dashboard"))
    assertTemplateUsed(request, "core/dashboard.html")
