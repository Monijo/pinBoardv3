import pytest


@pytest.fixture(scope='function')
def user(db, django_user_model):
    user_ = django_user_model.objects.create_user(
        username="TestUser",
        email='test@te.pl',
        password='TestPass123'
    )
    yield user_
