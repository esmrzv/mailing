from django.contrib import admin
from mailings.models import Client, Log, MailingSettings


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'comment',)
    list_filter = ('full_name',)


@admin.register(MailingSettings)
class MailingSettingsAdmin(admin.ModelAdmin):
    list_display = ('title', 'periodicity', 'status',)
    list_filter = ('client', 'title',)


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ('time', 'status', 'server_response', 'mailing_list', 'client',)
    list_filter = ('status', 'server_response', 'client',)