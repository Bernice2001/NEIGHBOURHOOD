from . models import Profile,Neighbour,Businesses,Feeds
from django import forms


'''
forms here
'''

class ProfileForm(forms.ModelForm):
    class Meta:

        model=Profile
        exclude=['user']
        widgets={
            "neigbor":forms.Select(),
        }

class BusinessForm(forms.ModelForm):
    class Meta:
        model=Businesses
        exclude=['user',]
        widgets={
            'businessesName': forms.TextInput(attrs={'placeholder':'Add a business Name'}),
            'email': forms.TextInput(attrs={'placeholder':'Add a business email'}),
            
        }

class PostForm(forms.ModelForm):
    class Meta:
        model=Feeds
        exclude=['user','neigbor']
        widgets={
            'post': forms.TextInput(attrs={'placeholder':'Tell us whats goin on'}),
        }

class UpdateForm(forms.ModelForm):
    class Meta:
        model=Profile
        exclude=['user']
        widgets={
            "neigbor":forms.Select(),
        }

class ChangeHood(forms.ModelForm):
    class Meta:
        model=Profile
        exclude=['user','image','fullname','location','secondaryEmail']
        widgets={
            "neigbor":forms.Select(),
        }
