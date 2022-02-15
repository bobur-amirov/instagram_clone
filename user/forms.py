from django import forms
from django.contrib.auth.forms import UserChangeForm

from .models import Profile


class ProfileForm(forms.ModelForm):
    phone = forms.CharField(label='Enter Phone', max_length=15, min_length=9)
    username = forms.CharField(label='Enter Username', max_length=20)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat Password', widget=forms.PasswordInput)

    class Meta:
        model = Profile
        fields = ['username', 'phone']

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        user = Profile.objects.filter(username=username)
        if user.count():
            raise forms.ValidationError("Username already exists")
        return username

    def clean_password2(self):
        pas = self.cleaned_data
        if pas['password'] != pas['password2']:
            raise forms.ValidationError("Password do not match! ")
        return pas['password2']

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if Profile.objects.filter(phone=phone).exists():
            raise forms.ValidationError('Please use another Phone, that is already token')
        return phone


class ProfileEditForm(UserChangeForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'username', 'image', 'phone', 'bio', 'location', 'birth_date']