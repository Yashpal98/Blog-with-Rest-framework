from django import forms

class UserProfileForm(forms.Form):
    profile = forms.FileField()