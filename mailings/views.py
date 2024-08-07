from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView, TemplateView

from blog.models import Blog
from blog.services import get_blogs_from_cache
from mailings.forms import MessageForm, ClientForm, MailingSettingsForm, MailingSettingsManagerForm
from mailings.models import Client, MailingSettings, Log, Message


class HomePageView(TemplateView):
    template_name = 'mailings/home_page.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        mailings = MailingSettings.objects.all()
        clients = Client.objects.all()
        context_data['all_mailings'] = mailings.count()
        context_data['active_mailings'] = mailings.filter(status='STATED').count()
        context_data['active_clients'] = clients.values('email').distinct().count()

        context_data['random_blogs'] = get_blogs_from_cache().order_by('?')[:3]

        return context_data


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailings:client_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailings:client_list')


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('mailings:client_list')


class ClientListView(ListView):
    model = Client


class ClientDetailView(DetailView):
    model = Client


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailings:message_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MessageListView(ListView):
    model = Message


class MessageDetailView(DetailView):
    model = Message


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailings:message_list')

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return MessageForm
        raise PermissionDenied


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('mailings:message_list')


class MailingSettingsCreateView(LoginRequiredMixin, CreateView):
    model = MailingSettings
    form_class = MailingSettingsForm
    success_url = reverse_lazy('mailings:mailingsettings_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MailingSettingsUpdateView(LoginRequiredMixin, UpdateView):
    model = MailingSettings
    form_class = MailingSettingsForm
    success_url = reverse_lazy('mailings:mailingsettings_list')

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return MailingSettingsForm
        if user.has_perm('mailings.change_status'):
            return MailingSettingsManagerForm

        raise PermissionDenied


class MailingSettingsDeleteView(LoginRequiredMixin, DeleteView):
    model = MailingSettings
    success_url = reverse_lazy('mailings:mailingsettings_list')


class MailingSettingsListView(ListView):
    model = MailingSettings


class MailingSettingsDetailView(DetailView):
    model = MailingSettings


class LogListView(ListView):
    model = Log
