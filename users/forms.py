from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, UserChangeForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields


class CustomUserEditForm(UserChangeForm):
    password = None
    status = forms.CharField(widget=forms.TextInput(attrs={'size': '40'}), required=False)

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'status', 'gender')


class CustomPasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = CustomUser
        fields = ('old_password', 'new_password1', 'new_password2')
        