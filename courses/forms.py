# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import GameProfile


class ProfileEditForm(forms.Form):
    first_name = forms.CharField(max_length=150, required=False, label='Ім\'я')
    last_name = forms.CharField(max_length=150, required=False, label='Прізвище')
    email = forms.EmailField(required=False, label='Email')
    avatar = forms.ImageField(required=False, label='Фото профілю')

    def __init__(self, *args, user=None, profile=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.profile = profile
        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['email'].initial = user.email
        for f in self.fields:
            self.fields[f].widget.attrs.setdefault('class', 'form-input')

    def save(self):
        if self.user:
            self.user.first_name = self.cleaned_data.get('first_name', '')
            self.user.last_name = self.cleaned_data.get('last_name', '')
            self.user.email = self.cleaned_data.get('email', '')
            self.user.save()
        if self.profile and self.cleaned_data.get('avatar'):
            self.profile.avatar = self.cleaned_data['avatar']
            self.profile.save()


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=False, label='Email')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Логін'
        self.fields['password1'].label = 'Пароль'
        self.fields['password2'].label = 'Підтвердіть пароль'
        for f in self.fields:
            self.fields[f].widget.attrs.setdefault('class', 'form-input')
            self.fields[f].widget.attrs.setdefault('placeholder', self.fields[f].label)
