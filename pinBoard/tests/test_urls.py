from django.urls import reverse, resolve

class TestUrl:
    def test_detail_url(self):
        path = reverse('home')
        assert resolve(path).view_name == 'home'

    # def test__url(self):
    #     path = reverse('dashboard', kwargs={'f_id': 9})
    #     assert resolve(path).view_name == 'dashboard'