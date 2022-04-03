import pytest as pytest


def test_home(client):
    response = client.get('/')
    assert response.status_code == 200

@pytest.mark.django_db
def test_sign_up(client, user):
    response_get = client.get('/sign-up')
    response_post = client.post('/sign-up', {'username': user.username, 'password': user.password, 'email': user.email})
    assert response_get.status_code == 200
    assert response_post.status_code == 200

    # url = reverse('homepage-url')
   # response = client.get(url)
   # assert response.status_code == 200



def test_log(client):
    response = client.get('/log')
    assert response.status_code == 200

def test_logout(client):
    response = client.get('/logout')
    assert response.status_code == 302 #redirect na home
