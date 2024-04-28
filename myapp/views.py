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
from django.db.models import Q, Prefetch, F, Subquery, OuterRef, Exists
from django.db.models.functions import Coalesce
import operator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views import View
from django.views.generic.edit import FormView

def index(request):
    return render(request, "myapp/index.html")

class Friends(ListView, LoginRequiredMixin):
    model = CustomUser
    template_name = "myapp/friends.html"
    context_object_name = "message_list"

    def get_queryset(self):
        query = self.request.GET.get('query')
        customuser = self.request.user
        # friend_list = super().get_queryset()
        data_subquery = Data.objects.filter(
            Q(talk_to=customuser, talk_from=OuterRef("pk")) |
            Q(talk_from=customuser, talk_to=OuterRef("pk"))
        ).order_by("-time")
        friend_list = super().get_queryset().annotate(
            latest_message_talk=Subquery(data_subquery.values("talk")[:1]),
            latest_message_time=Subquery(data_subquery.values("time")[:1]),
        )

        if query:
            friend_list = friend_list.filter(Q(username__icontains=query) | Q(email__icontains=query))

        friends = friend_list.exclude(id=customuser.id)
        message_list = []
        message_y_list = []
        message_n_list = []
    
        for friend in friends:
            # message = friend.   Data.objects.filter(
            #     Q(talk_from=customuser, talk_to=friend) | Q(talk_to=customuser, talk_from=friend)
            # ).order_by('time').last()

            # if friend.latest_send_data == None:

            # elif friend.latest_received_data == None:

            # if (friend.latest_send_data.time | friend.latest_received_data.time) == None:
            #     if (friend.latest_send_data.time & friend.latest_send_data.time) == null:
            #         message.talk=None
            #         message.time=None
            #     elif friend.latest_send_data.time == null:
            #         message.
            # latest_message = friend.latest_message

            if friend.latest_message_talk:
                message_y_list.append([friend, friend.latest_message_talk, friend.latest_message_time])
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
            ).order_by('time').select_related("talk_from")
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

class UsernameChangeView(View, LoginRequiredMixin):
    template_name = "myapp/settings/username_change.html"
    def get(self, request):
        user = request.user
        form = UsernameChangeForm(instance=user) 
        context = {"form": form}
        return render(request, self.template_name, context)
    def post(self, request):
        user=request.user
        form = UsernameChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("username_change_done")
        context = {"form": form}
        return render(request, self.template_name, context)

class MailaddressChangeView(View, LoginRequiredMixin):
    template_name = "myapp/settings/mailaddress_change.html"
    def get(self, request):
        user = request.user
        form = MailaddressChangeForm(instance=user) 
        context = {"form": form}
        return render(request, self.template_name, context)
    def post(self, request):
        user=request.user
        form = MailaddressChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("mailaddress_change_done")
        context = {"form": form}
        return render(request, self.template_name, context)

class IconChangeView(View, LoginRequiredMixin):
    template_name = "myapp/settings/icon_change.html"
    def get(self, request):
        user = request.user
        form = IconChangeForm(instance=user) 
        context = {"form": form}
        return render(request, self.template_name, context)
    def post(self, request):
        user=request.user
        form = IconChangeForm(request.POST, request.FILES , instance=user)
        if form.is_valid():
            form.save()
            return redirect("icon_change_done")
        context = {"form": form}
        return render(request, self.template_name, context)

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