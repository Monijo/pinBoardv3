import pytest as pytest
from django.urls import reverse
from django.core import mail

def test_home(client):
    response = client.get('/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_sign_up(client, user):
    url = reverse("pinBoard:sign_up")
    response_get = client.get(url)
    response_post = client.post(url, {'username': user.username, 'password': user.password, 'email': user.email})
    assert response_get.status_code == 200
    assert response_post.status_code == 200


def test_log(client):
    url = reverse("pinBoard:sign_in")
    response = client.get(url)
    assert response.status_code == 200

def test_logout(client):
    url = reverse("pinBoard:log_out")
    response = client.get(url)
    assert response.status_code == 302 #redirect na home


# def test_dashboard(client, family):
#     url = reverse("pinBoard:dashboard", args=[family.id])
#     response_get = client.get(url)
#     assert response_get.status_code == 200
#
# def test_archive(client, user):
#     url = reverse("pinBoard:archive", args=[user.id])
#     response_get = client.get(url)
#     assert response_get.status_code == 200
#
# def test_user_view(client, user):
#     url = reverse("pinBoard:user_view", args=[user.id])
#     response_get = client.get(url)
#     assert response_get.status_code == 200
#


def test_mail(mailoutbox):
    mail.send_mail('subject', 'body', 'from@example.com', ['to@example.com'])
    assert len(mailoutbox) == 1
    m = mailoutbox[0]
    assert m.subject == 'subject'
    assert m.body == 'body'
    assert m.from_email == 'from@example.com'
    assert list(m.to) == ['to@example.com']