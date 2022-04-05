import pytest
from django.urls import resolve, reverse

from pinBoard.models import Family
from pinBoard.views import home, sign_up, sign_in, family_list, create_family, dashboard, send_mail_view, add_shop_item, \
    add_task, sensors, user_view, user_add_task_self, note_form, all_notes, meeting_form, all_meetings, archive, log_out


def test_url_home():
    found = resolve(reverse('pinBoard:home'))
    assert found.func == home


def test_url_sign_up():
    found = resolve(reverse('pinBoard:sign_up'))
    assert found.func == sign_up


def test_url_sign_in():
    found = resolve(reverse('pinBoard:sign_in'))
    assert found.func == sign_in


def test_url_log_out():
    found = resolve(reverse('pinBoard:log_out'))
    assert found.func == log_out


def test_url_family_list():
    found = resolve(reverse('pinBoard:family_list'))
    assert found.func == family_list


def test_url_create_family():
    found = resolve(reverse('pinBoard:create_family'))
    assert found.func == create_family


@pytest.mark.django_db
def test_url_dashboard(family):
    found = resolve(reverse('pinBoard:dashboard', args=[family.id]))
    assert found.func == dashboard


@pytest.mark.django_db
def test_url_send_mail_view(family):
    found = resolve(reverse('pinBoard:send_mail_view', args=[family.id]))
    assert found.func == send_mail_view


@pytest.mark.django_db
def test_url_shop_list_form(family):
    found = resolve(reverse('pinBoard:shop_list_form', args=[family.id]))
    assert found.func == add_shop_item


@pytest.mark.django_db
def test_url_task_form(family):
    found = resolve(reverse('pinBoard:task_form', args=[family.id]))
    assert found.func == add_task


def test_url_sensors():
    found = resolve(reverse('pinBoard:sensors'))
    assert found.func == sensors


@pytest.mark.django_db
def test_url_user_view(user):
    found = resolve(reverse('pinBoard:user_view', args=[user.id]))
    assert found.func == user_view


@pytest.mark.django_db
def test_url_user_add_task_self(user):
    found = resolve(reverse('pinBoard:user_add_task_self', args=[user.id]))
    assert found.func == user_add_task_self

@pytest.mark.django_db
def test_url_note_form(user):
    found = resolve(reverse('pinBoard:note_form', args=[user.id]))
    assert found.func == note_form


@pytest.mark.django_db
def test_url_all_notes(user):
    found = resolve(reverse('pinBoard:all_notes', args=[user.id]))
    assert found.func == all_notes


@pytest.mark.django_db
def test_url_meeting_form(user):
    found = resolve(reverse('pinBoard:meeting_form', args=[user.id]))
    assert found.func == meeting_form


@pytest.mark.django_db
def test_url_all_meetings(user):
    found = resolve(reverse('pinBoard:all_meetings', args=[user.id]))
    assert found.func == all_meetings


@pytest.mark.django_db
def test_url_archive(user):
    found = resolve(reverse('pinBoard:archive', args=[user.id]))
    assert found.func == archive



