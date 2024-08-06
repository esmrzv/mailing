import random

from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse

from django.views.generic import CreateView, ListView, UpdateView
import secrets

from config.settings import EMAIL_HOST_USER
from users.forms import UserRegistrationForm, UserProfileForm
from users.models import User
from django.contrib.auth.decorators import permission_required


class UserCreateView(CreateView):
    model = User
    form_class = UserRegistrationForm
    success_url = reverse_lazy('users:login')

    def __str__(self):
        return f'{self.fullname}'

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f'http://{host}/users/email-confirm/{token}/'
        send_mail(
            subject='Потверждение почты',
            message=f'Подтвердите почту перейдя по ссылке {url}',
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email]
        )
        return super().form_valid(form)


def user_verify(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse('users:login'))


def restore_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.get(email=email)
        new_password = ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890',
                                              k=12))
        user.password = make_password(new_password)
        user.save()
        send_mail(
            subject='Восстановление пароля',
            message=f'Вот ваш новый пароль {new_password}',
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email])
        return redirect(reverse('users:login'))
    return render(request, 'users/password_restore.html')


class UserListView(PermissionRequiredMixin, ListView):
    model = User
    permission_required = 'users.view_all_users'


@permission_required('users.deactivate_user')
def toggle_activity(request, pk):
    user = User.objects.get(pk=pk)
    if user.is_active:
        user.is_active = False
    else:
        user.is_active = True
    user.save()
    return redirect(reverse('users:user_list'))


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user
