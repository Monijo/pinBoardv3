from django.urls import path

from . import views

app_name = 'pinBoard'

urlpatterns = [
    path('', views.home, name='home'),
    path('sign-up', views.sign_up, name='sign_up'),
    path('log', views.sign_in, name='sign_in'),
    path('logout', views.log_out, name='log_out'),

    path('users/', views.dashboard, name='dashboard'),
    path('users/shop_list_form', views.add_shop_item, name='shop_list_form'),
    path('users/task-form', views.add_task, name='task_form'),
    path('users/archive', views.archive, name='archive'),
    path('users/sensors', views.sensors, name='sensors'),

    path('users/<int:id>', views.user_view, name='user_view'),
    path('users/<int:id>/task_form', views.user_add_task_self, name='user_add_task_self'),
    path('users/<int:id>/note_form', views.note_form, name='note_form'),
    path('users/<int:id>/all_notes', views.all_notes, name='all_notes'),
    path('users/<int:id>/meeting_form', views.meeting_form, name='meeting_form'),
    path('users/<int:id>/all_meetings', views.all_meetings, name='all_meetings'),

]
