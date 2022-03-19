from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from pinBoard.models import User
from . import models

admin.site.register(User, UserAdmin)
admin.site.register(models.Family)
admin.site.register(models.FamilyUser)
admin.site.register(models.Invitation)
admin.site.register(models.Task)
admin.site.register(models.ShopItem)
admin.site.register(models.Sentence)
admin.site.register(models.Note)
admin.site.register(models.Meeting)
