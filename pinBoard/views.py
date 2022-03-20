import random
from multiprocessing.connection import families

from django.contrib.auth import login, authenticate, logout
from django.forms import inlineformset_factory
from django.http import HttpResponse
from django.shortcuts import render, redirect

from pinBoard.forms import UserForm, UserLogInForm, ShopItemForm, TaskForm
from pinBoard.models import Sentence, Task, ShopItem, User, Family


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
    if request.method == "GET":
        sentences = Sentence.objects.all()
        random_sentence = random.choice(sentences)
        # familyFormset = inlineformset_factory(User, Family)
        # formset = familyFormset(isinstance=families)

        # tasks = farequest.user.families.family.tasks
        # items_to_buy = ShopItem.objects.filter(family=request.user)

        context = {'random_sentence': random_sentence,
                   # "formset": formset,
                   #  "instance": families,

                   }

        return render(request, 'pinBoard/dashboard.html', context)
    else:

        if request.POST.get("tasks_members"):
            member_id = request.POST.get("tasks_members")
            member = User.objects.get(id=member_id)
            task_id = request.POST.get("tasks")

            selected_task = Task.objects.get(id=task_id)
            selected_task.member = member
            selected_task.save()

        id_task_to_delete = request.POST.get("delete")
        if id_task_to_delete:
            task_to_delete = Task.objects.get(id=id_task_to_delete)
            task_to_delete.delete()

        return redirect("pinBoard:dashboard")


def add_shop_item(request):
    if request.method == "POST":
        form = ShopItemForm(request.POST)

        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            item.save()
            return redirect("pinBoard:dashboard")

    else:
        form = ShopItemForm()

    return render(request, "pinBoard/shop_list_form.html", {'form': form})


def add_task(request):
    if request.method == "POST":
        form = TaskForm(request.POST)

        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect("pinBoard:dashboard")

    else:
        form = TaskForm()

    return render(request, "pinBoard/user_task_form.html", {'form': form})


def archive(request):
    return HttpResponse("Działa!")


def sensors(request):
    pass

#user
def user_view(request, id):
    if request.method == "GET":
        user = User.objects.get(id=id)
        user_notes = list(user.notes.all().order_by("-id"))
        user_meetings = user.meetinges.all().order_by("date")
        return render(request, "pinBoard/user_view.html", {"user": user,
                                                             "user_meetings": user_meetings,
                                                             "user_notes": user_notes,
                                                             })
    else:

        if request.POST.get("delete"):
            id_task_to_delete = request.POST.get("delete")

            task_to_delete = Task.objects.get(id=id_task_to_delete)
            task_to_delete.delete()

            return redirect('pinBoard:user_view', id=id)



def note_form(request):
    pass


def all_notes(request):
    pass


def meeting_form(request):
    pass


def all_meetings(request):
    pass
