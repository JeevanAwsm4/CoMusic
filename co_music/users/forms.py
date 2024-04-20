from django.forms import ModelForm,widgets
from django.contrib.auth.models import User




class SignupForm(ModelForm):
    class Meta:
        model = User
        fields = ["first_name","username", "password"]
        widgets = {
            "first_name" : widgets.TextInput(attrs={"placeholder":"name"}),
            "username" : widgets.TextInput(attrs={"placeholder":"email"}),
            "password" : widgets.PasswordInput(attrs={"placeholder":"password"})
        }