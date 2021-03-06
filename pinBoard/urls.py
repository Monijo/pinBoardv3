from django.urls import path

from . import views

app_name = 'pinBoard'

urlpatterns = [
    path('', views.home, name='home'),
    path('sign-up', views.sign_up, name='sign_up'),
    path('log', views.sign_in, name='sign_in'),
    path('logout', views.log_out, name='log_out'),

    path('families', views.family_list, name="family_list"),
    path('create_familie', views.create_family, name="create_family"),

    path('dashboard/<int:f_id>', views.dashboard, name='dashboard'),
    path('dashboard/<int:f_id>/send_mail_view/', views.send_mail_view, name='send_mail_view'),
    path('dashboard/<int:f_id>/send_mail_view/<uuid>', views.confirm_invitation, name='invitation_link'),
    path('dashboard/<int:f_id>/shop_list_form', views.add_shop_item, name='shop_list_form'),
    path('dashboard/<int:f_id>/task-form', views.add_task, name='task_form'),

    path('dashboard/sensors', views.sensors, name='sensors'),

    path('users/<int:id>', views.user_view, name='user_view'),
    path('users/<int:id>/task_form', views.user_add_task_self, name='user_add_task_self'),
    path('users/<int:id>/note_form', views.note_form, name='note_form'),
    path('users/<int:id>/all_notes', views.all_notes, name='all_notes'),
    path('users/<int:id>/meeting_form', views.meeting_form, name='meeting_form'),
    path('users/<int:id>/all_meetings', views.all_meetings, name='all_meetings'),
    path('users/<int:id>/archive', views.archive, name='archive'),

]
