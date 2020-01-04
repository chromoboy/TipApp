from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from Tip.models import Team
from Tip.models import TEST_CHOICES


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    # champion = forms.CharField(label='Dein Weltmeister?'
    #                            , widget=forms.Select(choices=TEST_CHOICES))

    # user defined fields
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        #, 'champion']


#   Update email username
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        # champion = forms.CharField(label='Dein Weltmeister?'
        #                                , widget=forms.Select(choices=TEST_CHOICES))
        fields = ['image', 'champion']
