import pytest
from django.contrib.auth import get_user_model

from pinBoard.models import Note


def test_create_user(django_user_model, user):
    users = django_user_model.objects.all()
    assert len(users) == 1


def test_should_check_password(user):
    user.set_password('secret')
    assert user.check_password('secret') is True




