from dataclasses import fields
from django import forms

from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.models import User

from .models import *

class RegisterForm(UserCreationForm):
    firstname = forms.CharField(required=True,widget=forms.TextInput(attrs={'class':'form-control'}))
    lastname = forms.CharField(required=True,widget=forms.TextInput(attrs={'class':'form-control'}))
    email  =    forms.EmailField(required=True,widget=forms.EmailInput(attrs={'class':'form-control'}))
    class Meta:
        model = User
        fields = ['username','firstname','lastname','email','password1','password2']
        
    def __init__(self,*args, **kwargs):
        super(RegisterForm, self).__init__(*args,**kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        
class LoginForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','password1']
    
    def __init__(self,*args, **kwargs):
        super(LoginForm, self).__init__(*args,**kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio','user']
        
class ProfileUpdateForm(forms.ModelForm):
    bio = forms.CharField(required=True,widget=forms.TextInput(attrs={'class':'form-control'}))
    
    class Meta:
        model = Profile
        fields = ['bio','contact','user_profile']
        
class PostProjectForm(forms.ModelForm):
    description = forms.CharField(required=True,widget=forms.TextInput(attrs={'class':'form-control'}))
    class Meta:
        model = Post
        fields = ['image','title','description','url','technologies']
        
class RatingProjectForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['design_rate','usability_rate','content_rate']