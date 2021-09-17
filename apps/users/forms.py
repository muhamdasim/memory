from django import forms
from allauth.account.forms import SignupForm
from django.contrib.auth.forms import UserChangeForm
from .models import CustomUser


class TherapistSignUpForm(SignupForm):
    is_subscribe = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    is_accept = forms.BooleanField(widget=forms.CheckboxInput())

    def custom_signup(self, request, user):
        user.is_subscribe = self.cleaned_data['is_subscribe']
        user.save()
        return user


class CustomUserChangeForm(UserChangeForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name')


class UploadAvatarForm(forms.Form):
    avatar = forms.FileField()
