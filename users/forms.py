from django.contrib.auth.forms import UserCreationForm
from .models import CostumUser, Profile
from django.forms import ModelForm


class CostumUserCreationForm(UserCreationForm):
    class Meta:
        model = CostumUser
        fields = ['username']


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = "__all__"
