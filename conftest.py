import pytest
from django.test import Client

from pinBoard.models import Task, Family, Note


@pytest.fixture(scope='function')
def user(db, django_user_model):
    user_ = django_user_model.objects.create_user(
        username="TestUser",
        email='test@te.pl',
        password='TestPass123'
    )
    yield user_

@pytest.fixture
def client():
    client = Client()
    return client


@pytest.fixture
def note(db, user):
    note_ = Note.objects.create(
        content="To jest tresc",
        user=user.id)

    yield note_

@pytest.fixture
def family(db):
    family_ = Family.objects.create(name="Kowalscy", id=1000)
    yield family_
