from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import UserCreateView, user_verify, restore_password, UserListView, ProfileView, toggle_activity

app_name = UsersConfig.name

urlpatterns = [path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
               path('logout/', LogoutView.as_view(), name='logout'),
               path('register/', UserCreateView.as_view(), name='register'),
               path('email-confirm/<str:token>/', user_verify, name='email-confirm'),
               path('password_restore/', restore_password, name='password_restore'),
               path('user_list/', UserListView.as_view(), name='user_list'),
               path('profile/', ProfileView.as_view(), name='profile'),
               path('toggle_activity/<int:pk>/', toggle_activity, name='toggle_activity'),
               ]
