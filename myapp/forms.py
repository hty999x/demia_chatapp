from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import CustomUser, Data
from django.contrib.auth.forms import AuthenticationForm 

# User = get_user_model()

class SignUpForm(UserCreationForm):
    # Username = forms.CharField(
    #     max_length=30,
    #     # help_text='オプション',
    #     label='Username:'
    # )
    # Email = forms.EmailField(
    #     max_length=254,
    #     help_text='必須 有効なメールアドレスを入力してください。',
    #     label='Email address:'
    # )
    # Password1 = forms.CharField(
    #     max_length=10,
    #     label='Password:'
    # )
    # icon = forms.FileField()
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'icon')
        # パスワードは書かなくていい

class LoginForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'password')
    # """ログインフォーム"""
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
