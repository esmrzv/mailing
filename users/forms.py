from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


from mailings.forms import StyleFormMixin
from users.models import User


class UserRegistrationForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2',)


class UserProfileForm(StyleFormMixin, UserChangeForm):
    class Meta:
        model = User
        fields = ('fullname', 'email', 'phone',)

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            self.fields['password'].widget = forms.HiddenInput()
