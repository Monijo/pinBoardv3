from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect

from pinBoard.forms import UserForm, UserLogInForm


def home(request):
    return render(request, 'pinBoard/landing_page.html')


def sign_up(request):
    if request.method == "POST":
        form = UserForm(request.POST)

        if form.is_valid():
            user_log = form.save()
            login(request, user_log)
            return redirect('pinBoard:sign_in')

    else:
        form = UserForm()
    return render(request, 'pinBoard/sign_up.html', {'form': form})


def sign_in(request):
    if request.method == "POST":
        user_log = authenticate(username=request.POST.get("username"), password=request.POST.get("password"))
        if user_log is not None:
            login(request, user_log)
            return redirect("pinBoard:dashboard")

    else:
        form = UserLogInForm()
    return render(request, "pinBoard/log_in.html", {"form": form})


def log_out(request):
    logout(request)
    return redirect("pinBoard:home")


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
