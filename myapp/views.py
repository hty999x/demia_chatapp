from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, LoginForm, Talk_roomForm
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Data
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.db.models import Q
import operator

def index(request):
    return render(request, "myapp/index.html")

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form=SignUpForm(request.POST,request.FILES)
            form.save()
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'myapp/signup.html', {'form': form})

class Login(LoginView):
    form_class = LoginForm
    template_name = 'myapp/login.html'

# def login_view(request):
#     form = LoginForm
#     return render(request, 'myapp/login.html', {'form': form})

@login_required
def friends(request):
    customuser = request.user
    friends = CustomUser.objects.exclude(id=customuser.id) # フィルタリング条件 です。id フィールドが customuser.id と一致しないすべての CustomUser オブジェクトを取得します。つまり、ログイン中のユーザー自身を除外して、他のユーザーを取得するためのクエリ
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
    
    context = {
        "message_list": message_list,
    }
    return render(request, "myapp/friends.html", context)

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

def setting(request):
    return render(request, "myapp/setting.html")
