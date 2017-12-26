from django import forms

class Shorten(forms.Form):
    url = forms.CharField(max_length=1000)

class Login(forms.Form):
    email = forms.CharField(max_length=250)
    password = forms.CharField(max_length=150)

class Signup(forms.Form):
    fname = forms.CharField(max_length=250)
    lname = forms.CharField(max_length=250)
    email = forms.CharField(max_length=250)
    password = forms.CharField(max_length=150)
    repassword = forms.CharField(max_length=150)
