from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

#A class that uses the base sign up form with added fields
class SignUpForm(UserCreationForm):
    first_name_field = forms.CharField(required=True)
    last_name_field = forms.CharField(required=True)
    email_field = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ("username", "first_name_field", "last_name_field", "email_field", "password1", "password2")

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)

        #Save other fields here
        user.first_name_field = self.cleaned_data["first_name_field"]
        user.last_name_field = self.cleaned_data["last_name_field"]
        user.email_field = self.cleaned_data["email_field"]
        
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