from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .forms import(
    SignUpForm, 
    LoginForm, 
    Talk_roomForm, 
    UsernameChangeForm, 
    MailaddressChangeForm, 
    IconChangeForm, 
    PasswordChangeForm
    )
from django.contrib.auth.forms import (
    UserCreationForm, 
)
from .models import CustomUser, Data
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeDoneView, PasswordChangeView
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.db.models import Q
import operator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView

def index(request):
    return render(request, "myapp/index.html")

# def signup_view(request):
#     if request.method == 'POST':
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             form=SignUpForm(request.POST,request.FILES)
#             form.save()
#             return redirect('index')
#     else:
#         form = SignUpForm()
#     return render(request, 'myapp/signup.html', {'form': form})

# class Login(LoginView):
#     form_class = LoginForm
#     template_name = 'myapp/login.html'

# def login_view(request):
#     form = LoginForm
#     return render(request, 'myapp/login.html', {'form': form})


class Friends(ListView):
    model = CustomUser
    template_name = "myapp/friends.html"
    context_object_name = "message_list"

    def get_queryset(self):
        query = self.request.GET.get('query')
        customuser = self.request.user

        if query:
            friend_list = CustomUser.objects.filter(username__icontains=query)
        else:
            friend_list = CustomUser.objects.all()

        friends = friend_list.exclude(id=customuser.id)
        message_list = []
        message_y_list = []
        message_n_list = []
    
        for friend in friends:
            message = Data.objects.filter(
                Q(talk_from=customuser, talk_to=friend) | Q(talk_to=customuser, talk_from=friend)
            ).order_by('time').last()

            if message:
                message_y_list.append([friend, message.talk, message.time])
            else:
                message_n_list.append([friend, None, None])
    
        message_y_list = sorted(message_y_list, key=operator.itemgetter(2), reverse=True)

        message_list.extend(message_y_list)
        message_list.extend(message_n_list)
        return message_list

@login_required
def talk_room(request, user_id):
    user = request.user
    friend = CustomUser.objects.filter(id=user_id).first()
    # friend = get_object_or_404(CustomUser, id=user_id)
    # friend_name = friend.username
    message = Data.objects.filter(
            Q(talk_from=user, talk_to=friend) | Q(talk_to=user, talk_from=friend)
            ).order_by('time')
    form = Talk_roomForm
    context = {
        "form":form,
        "friend":friend,
        "message_list":message
    }
    if request.method == "POST":
        new_talk = Data(talk_from=user, talk_to=friend)
        form = Talk_roomForm(request.POST, instance=new_talk)
        if form.is_valid():
            form.save()
            return redirect("talk_room", user_id)
        else:
            print(form.errors)
    return render(request, "myapp/talk_room.html", context)

@login_required
def setting(request):
    return render(request, "myapp/setting.html")



@login_required
def username_change(request):
    user = request.user
    if request.method == "GET":
        form = UsernameChangeForm(instance=user)
    elif request.method == "POST":
        form = UsernameChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("username_change_done")
    context = {
        "form":form
    }
    return render(request, "myapp/settings/username_change.html", context)
    """"""

@login_required
def mailaddress_change(request):
    user = request.user
    if request.method == "GET":
        form = MailaddressChangeForm(instance=user)

    elif request.method == "POST":
        form = MailaddressChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("mailaddress_change_done")
        else:
            print(form.errors)

    context = {
        "form": form,
    }
    return render(request, "myapp/settings/mailaddress_change.html", context)

@login_required
def icon_change(request):
    user = request.user
    if request.method == "GET":
        form = IconChangeForm(instance=user)

    elif request.method == "POST":
        form = IconChangeForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect("icon_change_done")
        else:
            print(form.errors)

    context = {
        "form": form,
    }
    return render(request, "myapp/settings/icon_change.html", context)

class PasswordChange(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy("password_change_done")
    template_name = 'myapp/settings/password_change.html'

class Logout(LoginRequiredMixin, LogoutView):
    """"""

@login_required
def username_change_done(request):
    return render(request, "myapp/settings/username_change_done.html")

@login_required
def mailaddress_change_done(request):
    return render(request, "myapp/settings/mailaddress_change_done.html")

@login_required
def icon_change_done(request):
    return render(request, "myapp/settings/icon_change_done.html")
    
@login_required
def password_change_done(request):
    return render(request, "myapp/settings/password_change_done.html")