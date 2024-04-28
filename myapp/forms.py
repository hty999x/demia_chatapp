from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import CustomUser, Data
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from allauth.account.forms import ( 
    LoginForm, 
    SignupForm, 
    ResetPasswordKeyForm, 
    ResetPasswordForm
)


class SignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'icon')
        labels = {"icon":"アイコン"}

class NewSignUpForm(SignupForm):
    icon = forms.ImageField()
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['icon'].label = "アイコン"
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'icon')
    def signup(self, request, user):
        user.icon = self.cleaned_data['icon']
        user.save()
        return user

class LoginForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'password')
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     for field in self.fields.values():
    #         field.widget.attrs['class'] = 'form-control'
    #         field.widget.attrs['placeholder'] = field.label   
        
class Talk_roomForm(forms.ModelForm):
    class Meta:
        model = Data
        fields = ("talk",)
        widgets = {"talk": forms.TextInput(attrs={"autocomplete": "off"})}

class UsernameChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ("username",)
        labels = {"username":"新しいユーザー名"}
    
class MailaddressChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ("email",)
        labels = {"email":"新しいメールアドレス"}
        # labelじゃなくてlabels

class IconChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ("icon",)
        labels = {"icon":"アイコン"}


class PasswordChangeForm(PasswordChangeForm):
    """"""