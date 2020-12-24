from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

#A class that uses the base sign up form with added fields
class SignUpForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("username", "password1", "password2")

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)

        #Save other fields here
        
        if commit:
            user.save()
        return user

class SignUpManager():

    def SignUp(self, request):

        
        if request.method != 'POST':
            return {"outcome": 0 }

        form = SignUpForm(data=request.POST)
    
        username = None

        if form.is_valid():

            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            print("New user: " + username)
            user = authenticate(request, username=username, password=password)
            return {"form": form, "outcome": 1 }
        else:
            return {"form": form, "outcome": 2 }