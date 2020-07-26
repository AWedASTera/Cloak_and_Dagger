from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Agent, Location, Route

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

class AgentKillForm(forms.Form):
    victim = forms.ModelChoiceField(queryset = Agent.objects.all())

class AgentTravelForm(forms.Form):
    route = forms.ModelChoiceField(queryset = Route.objects.all())



     