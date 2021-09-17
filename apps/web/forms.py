from django import forms
from django.conf import settings

from apps.web.models import Patients


class PasswordChangeForm(forms.Form):
    cur_pass_notmatch = False
    cur_pass = forms.CharField(min_length=4, widget=forms.PasswordInput())
    new_pass = forms.CharField(min_length=4, widget=forms.PasswordInput())
    repeat_pass = forms.CharField(min_length=4, widget=forms.PasswordInput())

    def set_cur_pass_notmatch(self):
        self.cur_pass_notmatch = True
        return 0

    def clean_cur_pass(self):
        if self.cur_pass_notmatch:
            raise forms.ValidationError("The current password is not matched")
        return self.cleaned_data.get('cur_pass')

    def clean_repeat_pass(self):
        new_pass = self.cleaned_data.get('new_pass')
        repeat_pass = self.cleaned_data.get('repeat_pass')

        if new_pass and new_pass != repeat_pass:
            raise forms.ValidationError("New password and Repeat password does not match")
        # if new_pass == cur_pass:
        #     raise forms.ValidationError("New password is the same as current one")
        return repeat_pass


class ProfileChangeForm(forms.Form):
    email = forms.CharField(max_length=255)
    username = forms.CharField(max_length=255)
    language = forms.ChoiceField(choices=settings.LANGUAGES, widget=forms.Select())
    is_subscribe = forms.BooleanField(widget=forms.CheckboxInput())
