from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *
from django.shortcuts import get_object_or_404

class NeighbourhoodForm(forms.ModelForm):    
    class Meta:
        model = Neighbourhood
        fields = ('neighbourhood',) 
        
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user', 'hood']