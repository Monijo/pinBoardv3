import random

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.urls import reverse

from pinBoard.forms import UserForm, UserLogInForm, ShopItemForm, TaskForm, NoteForm, MeetingForm, FamilyForm, \
    InvitationForm
from pinBoard.models import Sentence, Task, ShopItem, User, Family, Note, Meeting, ArchiweTasks, Invitation, FamilyUser


def home(request):

    """
    Function rendering landing page view of the application
    """

    return render(request, 'pinBoard/landing_page.html')


def sign_up(request):

    """
    The function rendering the registration view to the application.
    """

    if request.method == "POST":
        form = UserForm(request.POST)

        if form.is_valid():
            user_log = form.save(commit=False)
            user_log.save()
            login(request, user_log)
            return redirect('pinBoard:sign_in')

    else:
        form = UserForm()
    return render(request, 'pinBoard/sign_up.html', {'form': form})


def sign_in(request):

    """
    A function that renders the application login view.
    """

    if request.method == "POST":
        user_log = authenticate(username=request.POST.get("username"), password=request.POST.get("password"))
        if user_log is not None:
            login(request, user_log)
            return redirect(f"users/{request.user.id}")

    else:
        form = UserLogInForm()
    return render(request, "pinBoard/log_in.html", {"form": form})


def log_out(request):

    """
    Function that logs out of the application.
    """

    logout(request)
    return redirect("pinBoard:home")


@login_required
def family_list(request):

    """
    Function displaying the list of families the user belongs to.
    """

    if request.method == "GET":
        families = request.user.families.all()
        return render(request, "pinBoard/family_list.html", {"families": families})
    else:
        family_id = request.POST.get("family_id")
        return redirect(f"dashboard/{family_id}")


@login_required
def create_family(request):

    """
    Function that displays the form for adding a family to the user.
    """

    if request.method == "POST":
        form = FamilyForm(request.POST)

        if form.is_valid():
            family = form.save(commit=False)

            family.save()
            family.user_set.add(request.user)
            family.save()

            return redirect("pinBoard:family_list")

    else:
        form = FamilyForm()
    return render(request, "pinBoard/createFamily.html", {"form": form})


@login_required
def dashboard(request, f_id):

    """
    Function that displays a view belonging to a family with a specific f_id.
    """

    if request.method == "GET":
        sentences = Sentence.objects.all()
        random_sentence = random.choice(sentences)
        family = Family.objects.get(id=f_id)
        family_tasks = family.tasks.filter(user__isnull=True)
        family_shop_list = family.shop_items

        context = {'random_sentence': random_sentence, 'tasks': family_tasks, 'family': family,
                   "shop_items": family_shop_list}

        return render(request, 'pinBoard/dashboard.html', context)
    else:

        if request.POST.get("add_to_user"):
            task_to_transfer = Task.objects.get(id=request.POST.get("add_to_user"))
            task_to_transfer.user = request.user
            task_to_transfer.save()

        if request.POST.get("delete"):
            id_task_to_delete = request.POST.get("delete")
            task_to_delete = Task.objects.get(id=id_task_to_delete)
            task_to_delete.delete()

        return redirect(f"/dashboard/{f_id}")


@login_required
def add_shop_item(request, f_id):

    """
    Function rendering form - add item to shopping list.
    """

    if request.method == "POST":
        form = ShopItemForm(request.POST)
        family = Family.objects.get(id=f_id)

        if form.is_valid():
            item = form.save(commit=False)
            item.family = family
            item.save()
            return redirect(f"/dashboard/{f_id}")

    else:
        form = ShopItemForm()
        family = Family.objects.get(id=f_id)

    return render(request, "pinBoard/shop_list_form.html", {'form': form, 'family': family})


@login_required
def add_task(request, f_id):

    """
    A function that renders a form for adding a task to a family.
    """

    if request.method == "POST":
        form = TaskForm(request.POST)
        family = Family.objects.get(id=f_id)

        if form.is_valid():
            task = form.save(commit=False)
            task.family = family
            task.save()
            return redirect(f"/dashboard/{f_id}")

    else:
        form = TaskForm()
        family = Family.objects.get(id=f_id)
    return render(request, "pinBoard/user_task_form.html", {'form': form, 'family': family})


@login_required
def send_mail_view(request, f_id):

    """
    A function that renders a form for inviting a new family member.
    """

    if request.method == "POST":
        form = InvitationForm(request.user, request.POST)

        if form.is_valid():
            invitation = form.save(commit=False)
            invitation.user = request.user
            invitation.expired = False
            invitation.save()

            invitation_link = reverse("pinBoard:invitation_link",
                                      kwargs={"f_id": invitation.family.pk, "uuid": invitation.number})
            if invitation.target_user or invitation.email:
                email = invitation.email or invitation.target_user.email
                result = send_mail(
                    "Hello",
                    f'''
                            Do you want to join our family {invitation.family.name}?
                            Click link: {invitation_link}

                             ''',
                    'another@example.com',
                    [email],
                    fail_silently=False,

                )
                if result == 0:
                    invitation.delete()
                    return HttpResponse("Nie uda??o si?? wys??a?? maila! Spr??buj ponownie!")

            return redirect("pinBoard:family_list")

    else:
        form = InvitationForm(request.user)
    return render(request, "pinBoard/invitation_form.html", {"form": form})


def confirm_invitation(request, f_id, uuid):

    """
    A function that renders a confirmation page for wanting to belong to family.
    """


    invitation = Invitation.objects.get(number=uuid)

    if invitation:
        if request.method == "GET":
            return render(request, "pinBoard/confirm_invitation.html")
        else:
            if invitation.target_user:

                family = FamilyUser.objects.filter(family__name=invitation.family)[0]
                family.user.name = invitation.target_user

                return redirect("pinBoard:user_view", id=invitation.target_user_id)
            if invitation.email:
                if request.user:
                    family = FamilyUser.objects.filter(family__name=invitation.family)[0]
                    family.user.add(request.user)
                else:
                    return HttpResponse("Zaloguj si?? lub za??u?? konto ??eby wy??wietli?? zawarto??c strony")
    return HttpResponse("Cos posz??o nie tak!")


@login_required
def archive(request, id):

    """
    A function that renders a list of completed tasks by the user.
    """

    archived_tasks = request.user.archive_tasks.all()
    return render(request, "pinBoard/archive.html", {"archive_tasks": archived_tasks})


@login_required
def sensors(request):

    """
    Function rendering the result of the reading from temperature, humidity and air pollution sensors.
    """

    return render(request, "pinBoard/sensors.html")


# user
@login_required
def user_view(request, id):

    """
    A function that renders a user view.
    """

    if request.method == "GET":
        user = User.objects.get(id=id)
        user_notes = list(user.notes.all().order_by("-id"))
        user_meetings = user.meetinges.all().order_by("date")
        return render(request, "pinBoard/user_view.html", {"user": user, "user_meetings": user_meetings,
                                                           "user_notes": user_notes})
    else:

        if request.POST.get("delete"):
            id_task_to_delete = request.POST.get("delete")

            task_to_delete = Task.objects.get(id=id_task_to_delete)
            task_to_delete.delete()

            return redirect('pinBoard:user_view', id=id)
        if request.POST.get("done"):
            task_id = request.POST.get("done")
            task = Task.objects.get(id=task_id)
            archive_task = ArchiweTasks.objects.create(content=task.content, user=request.user)
            archive_task.save()
            task.delete()
            return redirect('pinBoard:user_view', id=id)


@login_required
def user_add_task_self(request, id):

    """
    A function that renders a form for adding a task to the user's task list.
    """

    if request.method == "POST":
        form = TaskForm(request.POST)

        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect("pinBoard:user_view", id=id)

    else:
        form = TaskForm()

    return render(request, "pinBoard/user_self_task_form.html", {'form': form})


@login_required
def note_form(request, id):

    """
    A function that renders a form for adding a note to the user's notes list.
    """

    if request.method == "GET":
        form = NoteForm()
        return render(request, "pinBoard/note_form.html", {"form": form})

    else:
        form = NoteForm(request.POST)

        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            return redirect("pinBoard:user_view", id=id)


@login_required
def all_notes(request, id):

    """
    A function that renders a list of all user notes.
    """

    if request.method == "GET":
        user = User.objects.get(id=id)
        all_notes_of_member = user.notes.all()

        context = {
            "all_notes": all_notes_of_member,
            'user': user
        }

        return render(request, "pinBoard/all_notes.html", context)

    else:
        note_id = request.POST.get("delete_note")
        note_to_delete = Note.objects.get(id=note_id)
        note_to_delete.delete()

        return redirect("pinBoard:all_notes", id=id)


@login_required
def meeting_form(request, id):

    """
    A function that renders the appointment creation form.
    """

    if request.method == "GET":
        form = MeetingForm()
        return render(request, "pinBoard/meetings_form.html", {"form": form})

    else:
        form = MeetingForm(request.POST)
        if form.is_valid():
            meeting = form.save(commit=False)
            meeting.user = request.user
            meeting.save()

            return redirect("pinBoard:all_meetings", id=id)


@login_required
def all_meetings(request, id):

    """
    A function that renders a list of all of the user's appointments.
    """

    if request.method == "GET":
        all_user_meetings = Meeting.objects.filter(user__id=id).order_by("date")
        user = User.objects.get(id=id)

        context = {
            "all__user_meetings": all_user_meetings,
            "user": user
        }
        return render(request, "pinBoard/all_meetings.html", context)
