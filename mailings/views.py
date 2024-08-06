from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView

from mailings.forms import MessageForm, ClientForm, MailingSettingsForm, MailingSettingsManagerForm
from mailings.models import Client, MailingSettings, Log, Message


class ClientCreateView(LoginRequiredMixin, CreateView):
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


class ClientDeleteView(LoginRequiredMixin,DeleteView):
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
