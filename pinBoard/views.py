from django.shortcuts import render


def home(request):
    return render(request, 'pinBoard/landing_page.html')

def sign_up(request):
    pass


def sign_in(request):
    pass


def log_out(request):
    pass


def dashboard(request):
    return render(request, 'pinBoard/dashboard.html')


def shop_list_form(request):
    pass


def task_form(request):
    pass


def archive(request):
    pass


def sensors(request):
    pass


def member_view(request):
    pass


def note_form(request):
    pass


def all_notes(request):
    pass


def meeting_form(request):
    pass


def all_meetings(request):
    pass
