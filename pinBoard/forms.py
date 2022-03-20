import crispy_forms.bootstrap
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.forms import TextInput, NumberInput, PasswordInput, Textarea, DateTimeInput, TimeInput

from pinBoard.models import ShopItem, Task, Note, Meeting


class ShopItemForm(forms.ModelForm):
    class Meta:
        model = ShopItem
        fields = ("name", "quantity")

        widgets = {
            'name': TextInput(attrs={'placeholder': "Nazwa przedmiotu do kupienia"}),
            'quantity': NumberInput(attrs={'placeholder': "Ilość"})
        }


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ("content", "priority")

        widgets = {
            'content': TextInput(attrs={'placeholder': "treść zadania"})

        }


class UserForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'password', 'email', 'families')

        error_messages = {
            'username': {
                'unique': ("Podany login jest zajęty!")
            }
        }

        widgets = {
            'username': TextInput(attrs={'placeholder': 'Nazwa użytkownika'}),
            'password': PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'twoje hasło'
            }),
            'email': TextInput(attrs={'placeholder': "Adres e-mail"}),
            'families': TextInput(attrs={'placeholder': "Your family"}),
        }

    def save(self, commit=True, *args):
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data.get('password'))
        user.username = self.cleaned_data.get('username')

        if commit:
            user.save()
        return user


class UserLogInForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'password')

        widgets = {
            'username': TextInput(attrs={'placeholder': 'Nazwa użytkownika'}),
            'password': PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'twoje hasło'
            })

        }


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ('content',)

        widgets = {
            'content': Textarea(attrs={'placeholder': 'treść notatki'})
        }


class MeetingForm(forms.ModelForm):
    class Meta:
        model = Meeting
        fields = ("date", "hour", "location", "name")

        widgets = {
            "date": DateTimeInput(attrs={'placeholder': "rrrr-mm-dd"}),
            "hour": TimeInput(attrs={'placeholder': 'hh:mm:ss'})
        }
