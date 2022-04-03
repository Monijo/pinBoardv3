import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class Family(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class User(AbstractUser):

    families = models.ManyToManyField(Family, through="FamilyUser")

    def __str__(self):
        return self.username


class FamilyUser(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    family = models.ForeignKey(Family, on_delete=models.CASCADE)
    is_owner = models.BooleanField(default=False)

    class Meta:
        unique_together = [['user', 'family']]


class Invitation(models.Model):
    number = models.UUIDField(default=uuid.uuid4)
    family = models.ForeignKey(Family, on_delete=models.CASCADE, related_name="invitations")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_invitations")
    target_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name="target_user_invitations", verbose_name="Imie osoby którą chcesz zaprosić")
    email = models.EmailField(blank=True)
    expired = models.BooleanField()
    created_date = models.DateTimeField(auto_now_add=True)


class Task(models.Model):
    content = models.CharField(max_length=255, verbose_name="Treść zadania")
    is_done = models.BooleanField(default=False)
    priority = models.BooleanField(default=False, verbose_name="Priorytet")
    family = models.ForeignKey(Family, on_delete=models.CASCADE, null=True, related_name="tasks")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="tasks")

    def __str__(self):
        return self.content


class ShopItem(models.Model):
    name = models.CharField(max_length=255, verbose_name="Przedmiot")
    quantity = models.IntegerField(verbose_name="Ilość sztuk")
    family = models.ForeignKey(Family, on_delete=models.CASCADE, null=True, related_name="shop_items")

    def __str__(self):
        return self.name


class Sentence(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(verbose_name="Treść")

    def __str__(self):
        return self.title


class Note(models.Model):
    content = models.TextField(verbose_name="Treść notatki")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, related_name="notes")

    def __str__(self):
        return self.content


class Meeting(models.Model):
    date = models.DateField(verbose_name="Data")
    hour = models.TimeField(verbose_name="Godzina")
    location = models.CharField(max_length=255, verbose_name="Miejsce")
    name = models.CharField(max_length=255, verbose_name="Nazwa spotkania")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, related_name="meetinges")

    def __str__(self):
        return self.name


class ArchiweTasks(models.Model):
    content = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="archive_tasks")

