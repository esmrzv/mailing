from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView


from mailings.models import Client, MailingSettings, Log


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
