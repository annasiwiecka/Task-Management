from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    password1 = forms.CharField(widget=forms.PasswordInput, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

        def save(self, commit=True):
            user = super(NewUserForm, self).save(commit=False)
            user.email = self.cleaned_data['email']
            
            user.set_password(self.cleaned_data['password1'])
            
            if commit:
                user.save()
            return user