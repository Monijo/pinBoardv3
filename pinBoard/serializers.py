from .models import ArchiweTasks, Meeting, Note, Sentence, ShopItem, Task, Invitation, FamilyUser, User, Family

from rest_framework import serializers


class ArchiveTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArchiweTasks
        fields = ("content", "user")


class MeetingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meeting
        fields = ("date", "hour", "location", "name", "user")


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ("content", "user")


class SentenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sentence
        fields = ("title", "content")


class ShopItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopItem
        fields = ("name", "quantity", "family")


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ("content", "is_done", "priority", "family", "user")


class InvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitation
        fields = ("number", "family", "user", "target_user", "email", "expired", "created_date")


class FamilyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = FamilyUser
        fields = ("user", "family", "is_owner")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("families",)


class FamilySerializer(serializers.ModelSerializer):
    class Meta:
        model = Family
        fields = ("name",)
