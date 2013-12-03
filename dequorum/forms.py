from django import forms
from .models import Thread, Post, Profile


class CreateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['nickname', 'avatar']


class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Profile
        fields = ['nickname']

class CreateThreadForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = ['subject']


class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']