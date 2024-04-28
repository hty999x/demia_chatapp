from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # path('signup', views.signup_view, name='signup'),
    # path('login', views.Login.as_view(), name='login'),
    # path('friends', views.friends, name='friends'),
    # path('friends_n', views.friends_n, name='friends_n'),
    # path('friends_y', views.Friends.as_view(), name='friends_y'),
    path('friends', views.Friends.as_view(), name='friends'),
    path('talk_room/<int:user_id>/', views.talk_room, name='talk_room'),
    path('setting', views.setting, name='setting'),
    path('username_change', views.UsernameChangeView.as_view(), name='username_change'),
    path('mailaddress_change', views.MailaddressChangeView.as_view(), name='mailaddress_change'),
    path('icon_change', views.IconChangeView.as_view(), name='icon_change'),
    path('password_change', views.PasswordChange.as_view(), name='password_change'),
    path("logout/", views.Logout.as_view(), name="logout"),
    path('username_change_done', views.username_change_done, name='username_change_done'),
    path('mailaddress_change_done', views.mailaddress_change_done, name='mailaddress_change_done'),
    path('icon_change_done', views.icon_change_done, name='icon_change_done'),
    path('password_change_done', views.password_change_done, name='password_change_done'),
    path('accounts/', include('allauth.urls'))
]