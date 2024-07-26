from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView

from mailings.forms import MessageForm
from mailings.models import Client, MailingSettings, Log, Message


class ClientCreateView(CreateView):
    model = Client
    fields = ('email', 'full_name', 'comment')
    success_url = reverse_lazy('mailings:client_list')


class ClientUpdateView(UpdateView):
    model = Client
    fields = ('email', 'full_name', 'comment')
    success_url = reverse_lazy('mailings:client_list')


class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy('mailings:client_list')


class ClientListView(ListView):
    model = Client


class ClientDetailView(DetailView):
    model = Client


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailings:message_list')


class MessageListView(ListView):
    model = Message


class MessageDetailView(DetailView):
    model = Message


class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailings:message_list')


class MessageDeleteView(DeleteView):
    model = Message
    success_url = reverse_lazy('mailings:message_list')



class MailingSettingsCreateView(CreateView):
    model = MailingSettings
    fields = ('client', 'start_time', 'end_time', 'periodicity', 'status', 'title', 'text')
    success_url = reverse_lazy('mailings:mailing_settings_list')


class MailingSettingsUpdateView(UpdateView):
    model = MailingSettings
    fields = ('client', 'start_time', 'end_time', 'periodicity', 'status', 'title', 'text')
    success_url = reverse_lazy('mailings:mailingsettings_list')


class MailingSettingsDeleteView(DeleteView):
    model = MailingSettings
    success_url = 'mailings:mailing_settings_list'


class MailingSettingsListView(ListView):
    model = MailingSettings


class MailingSettingsDetailView(DetailView):
    model = MailingSettings


class LogListView(ListView):
    model = Log
