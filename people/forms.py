#coding: utf-8
from django import forms
from django.forms import ModelForm, CheckboxSelectMultiple, RadioSelect, Select
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, ReadOnlyPasswordHashField
from django.utils.translation import ugettext, ugettext_lazy as _
from .models import Person



class CustomUserCreationForm(ModelForm):
    password1 = forms.CharField(label=_("Password"),
        widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"),
        widget=forms.PasswordInput)
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
        'duplicate_username': _("Ja existe uma pessoa com este email."),
    }

    class Meta:
        model = Person
        fields = ('email',)

    def clean_password2(self):
        #Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Senhas não conferem")
        return password2

    def clean_email(self):
        email = self.cleaned_data["email"]
        if Person.objects.filter(email=email).count():
            raise forms.ValidationError(self.error_messages['duplicate_username'])
        else:
            return email

    def save(self, commit=True):
        #Save the provided password in hashed format
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class CustomUserChangeForm(ModelForm):

    class Meta:
        model = Person
        fields = ('email','name')

class UpdatePassword(forms.Form):

    password1 = forms.CharField(label="Senha",widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirme sua senha",widget=forms.PasswordInput)

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError('Senhas nao conferem')
        return password2


def validation_email(self):
    email = self.cleaned_data["email"]
    confirmation = self.cleaned_data['confirm_email']

    if email != confirmation:
        raise forms.ValidationError("Informe emails iguais")