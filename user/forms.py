from typing import Any
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

class SignupForm(UserCreationForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={'id':'required'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'id':'required'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'id':'required'}))
    class Meta:
        model = User
        fields = ['username','email','first_name','last_name']
    
    def save(self, commit=True):
        our_user = super().save(commit=False)
        if commit == True:
            our_user.is_active = False
            our_user.save()
        return our_user